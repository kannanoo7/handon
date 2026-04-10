import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8080))
server.listen(5)

print("HTTP Server running on port 8080...")

while True:
    client, addr = server.accept()
    print(f"Connected from {addr}")

    request = client.recv(1024).decode()
    print("----- REQUEST -----")
    print(request)

    # Parse first line
    first_line = request.split("\n")[0]
    method, path, _ = first_line.split()

    # Simple routing
    if path == "/":
        body = "<h1>Home Page</h1>"
    elif path == "/hello":
        body = "<h1>Hello World!</h1>"
    else:
        body = "<h1>404 Not Found</h1>"

    # Build HTTP response
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html\r\n"
    response += "\r\n"
    response += body

    client.send(response.encode())
    client.close()