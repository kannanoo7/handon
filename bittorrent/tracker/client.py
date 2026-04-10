import socket
import urllib.parse
from torrent.bencode import bdecode


class TrackerClient:
    def __init__(self, torrent):
        self.torrent = torrent

    def _generate_peer_id(self):
        return b'-PC0001-' + b'123456789012'  # 20 bytes total

    def _url_encode(self, data: bytes):
        return urllib.parse.quote_from_bytes(data)

    def get_peers(self):
        url = self.torrent.announce

        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        port = parsed.port or 80

        peer_id = self._generate_peer_id()

        params = {
            'info_hash': self._url_encode(self.torrent.info_hash),
            'peer_id': self._url_encode(peer_id),
            'port': 6881,
            'uploaded': 0,
            'downloaded': 0,
            'left': self.torrent.length,
            'compact': 1
        }

        query = urllib.parse.urlencode(params)

        request = (
            f"GET {parsed.path}?{query} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Connection: close\r\n\r\n"
        )

        # 🔥 RAW SOCKET (like your HTTP server project)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(request.encode())

        response = b''
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data

        sock.close()

        # Split headers and body
        header_end = response.index(b'\r\n\r\n') + 4
        body = response[header_end:]

        decoded = bdecode(body)
        return decoded