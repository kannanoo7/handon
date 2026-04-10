#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libavutil/log.h>
#include <libavutil/imgutils.h>
#include <libswscale/swscale.h>
#include <stdio.h>
#include <stdint.h>

/* Save RGB frame as PPM image */
void save_frame_as_ppm(AVFrame *frame, int width, int height, int frame_number)
{
    char filename[64];
    sprintf(filename, "frame_%03d.ppm", frame_number);

    FILE *f = fopen(filename, "wb");

    fprintf(f, "P6\n%d %d\n255\n", width, height);

    fwrite(frame->data[0], 1, width * height * 3, f);

    fclose(f);

    printf("Saved %s\n", filename);
}
void invert_colors(AVFrame *frame, int width, int height)
{
    uint8_t *data = frame->data[0];
    int linesize = frame->linesize[0];

    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width * 3; x++)
        {
            data[y * linesize + x] = 255 - data[y * linesize + x];
        }
    }
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Usage: %s <video file>\n", argv[0]);
        return -1;
    }

    char *filename = argv[1];

    av_log_set_level(AV_LOG_INFO);

    AVFormatContext *fmt_ctx = NULL;

    /* Open input file */
    if (avformat_open_input(&fmt_ctx, filename, NULL, NULL) != 0)
    {
        printf("Could not open file\n");
        return -1;
    }

    /* Read stream info */
    if (avformat_find_stream_info(fmt_ctx, NULL) < 0)
    {
        printf("Could not find stream info\n");
        return -1;
    }

    av_dump_format(fmt_ctx, 0, filename, 0);

    /* Find video stream */
    int video_stream = -1;

    for (unsigned int i = 0; i < fmt_ctx->nb_streams; i++)
    {
        if (fmt_ctx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO)
        {
            video_stream = i;
            break;
        }
    }

    if (video_stream == -1)
    {
        printf("Video stream not found\n");
        return -1;
    }

    printf("Video stream index: %d\n", video_stream);

    /* Get codec parameters */
    AVCodecParameters *codecpar =
        fmt_ctx->streams[video_stream]->codecpar;

    /* Find decoder */
    const AVCodec *decoder =
        avcodec_find_decoder(codecpar->codec_id);

    if (!decoder)
    {
        printf("Decoder not found\n");
        return -1;
    }

    /* Create codec context */
    AVCodecContext *codec_ctx =
        avcodec_alloc_context3(decoder);

    avcodec_parameters_to_context(codec_ctx, codecpar);

    /* Open decoder */
    if (avcodec_open2(codec_ctx, decoder, NULL) < 0)
    {
        printf("Could not open decoder\n");
        return -1;
    }

    /* Allocate frames */
    AVFrame *frame = av_frame_alloc();
    AVFrame *rgb_frame = av_frame_alloc();

    /* Create scaling context (YUV -> RGB) */
    struct SwsContext *sws_ctx =
        sws_getContext(
            codec_ctx->width,
            codec_ctx->height,
            codec_ctx->pix_fmt,
            codec_ctx->width,
            codec_ctx->height,
            AV_PIX_FMT_RGB24,
            SWS_BILINEAR,
            NULL,
            NULL,
            NULL
        );

    /* Allocate RGB buffer */
    int num_bytes =
        av_image_get_buffer_size(
            AV_PIX_FMT_RGB24,
            codec_ctx->width,
            codec_ctx->height,
            1
        );

    uint8_t *buffer = (uint8_t *)av_malloc(num_bytes);

    av_image_fill_arrays(
        rgb_frame->data,
        rgb_frame->linesize,
        buffer,
        AV_PIX_FMT_RGB24,
        codec_ctx->width,
        codec_ctx->height,
        1
    );

    AVPacket packet;

    int frame_count = 0;

    /* Read packets */
    while (av_read_frame(fmt_ctx, &packet) >= 0)
    {
        if (packet.stream_index == video_stream)
        {
            avcodec_send_packet(codec_ctx, &packet);

            while (avcodec_receive_frame(codec_ctx, frame) == 0)
            {
                /* Convert YUV to RGB */
                sws_scale(
                    sws_ctx,
                    (uint8_t const * const *)frame->data,
                    frame->linesize,
                    0,
                    codec_ctx->height,
                    rgb_frame->data,
                    rgb_frame->linesize
                );

            invert_colors(
            rgb_frame,
            codec_ctx->width,
            codec_ctx->height
            );


                /* Save frame */
                save_frame_as_ppm(
                    rgb_frame,
                    codec_ctx->width,
                    codec_ctx->height,
                    frame_count
                );

                frame_count++;

                if (frame_count >= 5)
                    break;
            }
        }

        av_packet_unref(&packet);

        if (frame_count >= 5)
            break;
    }

    /* Cleanup */
    av_free(buffer);
    av_frame_free(&frame);
    av_frame_free(&rgb_frame);
    avcodec_free_context(&codec_ctx);
    avformat_close_input(&fmt_ctx);
    sws_freeContext(sws_ctx);

    printf("Extracted %d frames\n", frame_count);

    return 0;
}