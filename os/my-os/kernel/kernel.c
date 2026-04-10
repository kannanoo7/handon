#define VIDEO_MEMORY 0xb8000
#define WIDTH 80
#define HEIGHT 25

// -------------------------
// PUT CHAR AT POSITION
// -------------------------
void put_char(char c, int x, int y) {
    char* video = (char*) VIDEO_MEMORY;

    int pos = (y * WIDTH + x) * 2;
    video[pos] = c;
    video[pos + 1] = 0x0F;
}

// -------------------------
// PRINT STRING
// -------------------------
void print_at(char* str, int x, int y) {
    int i = 0;
    while (str[i]) {
        put_char(str[i], x + i, y);
        i++;
    }
}

// -------------------------
// CLEAR SCREEN
// -------------------------
void clear_screen() {
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            put_char(' ', x, y);
        }
    }
}

// -------------------------
// DRAW BOX (UI ELEMENT)
// -------------------------
void draw_box(int x, int y, int w, int h) {

    // top & bottom
    for (int i = 0; i < w; i++) {
        put_char('-', x + i, y);
        put_char('-', x + i, y + h - 1);
    }

    // sides
    for (int i = 0; i < h; i++) {
        put_char('|', x, y + i);
        put_char('|', x + w - 1, y + i);
    }

    // corners
    put_char('+', x, y);
    put_char('+', x + w - 1, y);
    put_char('+', x, y + h - 1);
    put_char('+', x + w - 1, y + h - 1);
}

// -------------------------
// KERNEL MAIN
// -------------------------
void kernel_main() {

    clear_screen();

    // title
    print_at("MY OS UI", 30, 1);

    // draw window
    draw_box(20, 5, 40, 10);

    // inside text
    print_at("Welcome to your OS!", 25, 8);
    print_at("Level 8: UI System", 25, 10);

    while (1);
}