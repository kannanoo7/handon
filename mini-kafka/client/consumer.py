import socket

HOST = '127.0.0.1'
PORT = 9092


def consume(topic, partition, offset=0):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    command = f"CONSUME {topic} {partition} {offset}"
    client.sendall(command.encode())

    response = client.recv(4096).decode()

    print(f"\n--- {topic} | partition {partition} | offset {offset} ---")
    print(response)

    client.close()


if __name__ == "__main__":
    while True:
        topic = input("Topic: ")
        partition = int(input("Partition: "))
        offset = int(input("Offset: "))
        consume(topic, partition, offset)