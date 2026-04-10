import socket
import os

HOST = '127.0.0.1'
PORT = 9092
DATA_DIR = 'C:\\Users\\kannan\\Desktop\\mini-kafka\\data'


# Ensure data directory exists
#os.makedirs(os.path.dirname(DATA_DIR), exist_ok=True)
def get_partition_file(topic, partition):
    topic_dir = os.path.join(DATA_DIR, topic)
    os.makedirs(topic_dir, exist_ok=True)

    return os.path.join(topic_dir, f"partition{partition}.log")

def append_to_partition(topic, partition, message):
    file_path = get_partition_file(topic, partition)

    offset = 0
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            offset = len(f.readlines())

    with open(file_path, 'a') as f:
        f.write(f"{offset}:{message}\n")

def read_from_partition(topic, partition, offset):
    file_path = get_partition_file(topic, partition)

    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r') as f:
        lines = f.readlines()

    return lines[offset:]

# def read_all_messages():
#     if not os.path.exists(DATA_FILE):
#         return []

#     with open(DATA_FILE, 'r') as f:
#         return f.readlines()
def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            return

        print(f"[RECEIVED] {data}")
        parts = data.split()

        # PRODUCE <topic> <key> <message>
        if parts[0] == "PRODUCE":
            if len(parts) < 4:
                conn.sendall(b"ERROR: Invalid PRODUCE format\n")
                return

            topic = parts[1]
            key = parts[2]
            message = " ".join(parts[3:]).strip()

            partition = get_partition(key)

            append_to_partition(topic, partition, message)

            conn.sendall(f"ACK (partition {partition})\n".encode())

        # CONSUME <topic> <partition> <offset>
        elif parts[0] == "CONSUME":
            if len(parts) < 3:
                conn.sendall(b"ERROR: Invalid CONSUME format\n")
                return

            topic = parts[1]
            partition = int(parts[2])
            offset = int(parts[3]) if len(parts) > 3 else 0

            messages = read_from_partition(topic, partition, offset)

            if messages is None:
                conn.sendall(b"ERROR: Partition not found\n")
            elif not messages:
                conn.sendall(b"NO NEW MESSAGES\n")
            else:
                response = "".join(messages)
                conn.sendall(response.encode())

        else:
            conn.sendall(b"ERROR: Unknown command\n")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[STARTED] Broker running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)


if __name__ == "__main__":
    start_server() 