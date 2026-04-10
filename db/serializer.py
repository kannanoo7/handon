import struct

USERNAME_SIZE = 32
ROW_SIZE = 4 + USERNAME_SIZE


def serialize_row(row):

    username_bytes = row.username.encode("utf-8")

    username_bytes = username_bytes.ljust(USERNAME_SIZE, b"\x00")

    data = struct.pack("I", row.id) + username_bytes

    return data


def deserialize_row(data):

    id = struct.unpack("I", data[:4])[0]

    username = data[4:4+USERNAME_SIZE].decode().rstrip("\x00")

    return id, username