import socket

HOST = '127.0.0.1'
PORT = 9092


def send_message(topic, key, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    command = f"PRODUCE {topic} {key} {message}"
    client.sendall(command.encode())

    response = client.recv(1024).decode()
    print("[BROKER RESPONSE]", response)

    client.close()


if __name__ == "__main__":
    while True:
        topic = input("Topic: ")
        key = input("Key: ")
        msg = input("Message: ")
        send_message(topic, key, msg)