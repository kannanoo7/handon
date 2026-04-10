class BencodeDecoder:
    def __init__(self, data: bytes):
        self.data = data
        self.index = 0

    def decode(self):
        char = self.data[self.index:self.index+1]

        if char == b'i':
            return self._decode_int()
        elif char == b'l':
            return self._decode_list()
        elif char == b'd':
            return self._decode_dict()
        elif char.isdigit():
            return self._decode_string()
        else:
            raise ValueError("Invalid bencode format")

    def _decode_int(self):
        self.index += 1  # skip 'i'
        end = self.data.index(b'e', self.index)
        number = int(self.data[self.index:end])
        self.index = end + 1
        return number

    def _decode_string(self):
        colon = self.data.index(b':', self.index)
        length = int(self.data[self.index:colon])
        self.index = colon + 1
        string = self.data[self.index:self.index + length]
        self.index += length
        return string

    def _decode_list(self):
        self.index += 1  # skip 'l'
        result = []
        while self.data[self.index:self.index+1] != b'e':
            result.append(self.decode())
        self.index += 1  # skip 'e'
        return result

    def _decode_dict(self):
        self.index += 1  # skip 'd'
        result = {}
        while self.data[self.index:self.index+1] != b'e':
            key = self.decode()
            value = self.decode()
            result[key] = value
        self.index += 1  # skip 'e'
        return result


def bdecode(data: bytes):
    decoder = BencodeDecoder(data)
    return decoder.decode()

def bencode(value):
    if isinstance(value, int):
        return b'i' + str(value).encode() + b'e'

    elif isinstance(value, bytes):
        return str(len(value)).encode() + b':' + value

    elif isinstance(value, str):
        encoded = value.encode()
        return str(len(encoded)).encode() + b':' + encoded

    elif isinstance(value, list):
        return b'l' + b''.join(bencode(v) for v in value) + b'e'

    elif isinstance(value, dict):
        # keys must be sorted
        items = sorted(value.items())
        result = b'd'
        for k, v in items:
            result += bencode(k)
            result += bencode(v)
        result += b'e'
        return result

    else:
        raise TypeError("Unsupported type")