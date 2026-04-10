import hashlib
from torrent.bencode import bdecode, bencode


class Torrent:
    def __init__(self, filepath):
        with open(filepath, 'rb') as f:
            data = f.read()

        self.raw_data = data
        self.meta = bdecode(data)

        self.announce = self.meta.get(b'announce', b'').decode()

        info = self.meta[b'info']
        self.info = info

        self.name = info.get(b'name', b'').decode()
        self.piece_length = info[b'piece length']
        self.length = info.get(b'length', 0)

        pieces = info[b'pieces']
        self.pieces = [
            pieces[i:i+20]
            for i in range(0, len(pieces), 20)
        ]

        # 🔥 IMPORTANT PART
        self.info_hash = self._compute_info_hash()

    def _compute_info_hash(self):
        encoded_info = bencode(self.info)
        return hashlib.sha1(encoded_info).digest()

    def get_info_hash_hex(self):
        return self.info_hash.hex()

    def print_info(self):
        print("Tracker:", self.announce)
        print("File Name:", self.name)
        print("File Size:", self.length)
        print("Piece Length:", self.piece_length)
        print("Number of Pieces:", len(self.pieces))
        print("Info Hash (hex):", self.get_info_hash_hex())