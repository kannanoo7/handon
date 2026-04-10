import socket
import os
import threading

from http.request import HttpRequest
from http.response import HttpResponse
from handlers.router import Router

HOST = '127.0.0.1'
PORT = 8080
STATIC_DIR = "static"

# -----------------------------
# 🧠 Router Setup
# -----------------------------
router = Router()

import json
from http.response import HttpResponse

def create_user_handler(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed", status=405)

    data = request.json or {}

    name = data.get("name", "unknown")
    age = data.get("age", "unknown")

    response_data = {
        "message": "User created",
        "name": name,
        "age": age
    }

    return HttpResponse(
        body=json.dumps(response_data),
        status=200,
        headers={"Content-Type": "application/json"}
    )


def form_handler(request):
    name = request.form_data.get("name", "guest")
    age = request.form_data.get("age", "unknown")

    return HttpResponse(
        f"<h1>Form Submitted: {name}, Age: {age}</h1>",
        status=200
    )


router.add_route("/api/user", create_user_handler)
router.add_route("/submit", form_handler)
def home_handler(request):
    return HttpResponse("<h1>Home Page</h1>", status=200)


def about_handler(request):
    return HttpResponse("<h1>About Page</h1>", status=200)

def user_handler(request):
    user_id = request.query_params.get("id", "unknown")
    name = request.query_params.get("name", "guest")

    return HttpResponse(
        f"<h1>User ID: {user_id}, Name: {name}</h1>",
        status=200
    )
def user_detail_handler(request):
    user_id = request.path_params.get("id")

    return HttpResponse(
        f"<h1>User ID: {user_id}</h1>",
        status=200
    )


router.add_route("/user/{id}", user_detail_handler)


router.add_route("/user", user_handler)
router.add_route("/", home_handler)
router.add_route("/about", about_handler)


# -----------------------------
# 📁 Static File Handling
# -----------------------------
def serve_static_file(path):
    if path == "/":
        path = "/index.html"

    file_path = os.path.join(STATIC_DIR, path.lstrip("/"))

    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "rb") as f:
            return f.read()
    except Exception as e:
        print("File read error:", e)
        return None


def get_content_type(path):
    if path.endswith(".html"):
        return "text/html"
    elif path.endswith(".css"):
        return "text/css"
    elif path.endswith(".js"):
        return "application/javascript"
    elif path.endswith(".png"):
        return "image/png"
    elif path.endswith(".jpg") or path.endswith(".jpeg"):
        return "image/jpeg"
    elif path.endswith(".gif"):
        return "image/gif"
    else:
        return "text/plain"


# -----------------------------
# 🔁 Client Handler (Thread)
# -----------------------------
def handle_client(client_socket, address):
    print(f"\n[NEW CONNECTION] {address}")

    try:
        data = client_socket.recv(1024)

        if not data:
            return

        request_text = data.decode(errors='ignore')
        request = HttpRequest(request_text)

        print(f"{request.method} {request.path}")

        # -----------------------------
        # 📁 Static file check
        # -----------------------------
        file_content = serve_static_file(request.path)

        if file_content is not None:
            actual_path = request.path if request.path != "/" else "/index.html"
            content_type = get_content_type(actual_path)

            response = HttpResponse(
                body=file_content,   # bytes
                status=200,
                headers={"Content-Type": content_type}
            )
        else:
            # -----------------------------
            # 🔀 Router fallback
            # -----------------------------
            handler = router.resolve(request)
            response = handler(request)

        # -----------------------------
        # 📤 Send response
        # -----------------------------
        client_socket.sendall(response.build())

    except Exception as e:
        print("Error:", e)

        error_response = HttpResponse(
            "<h1>500 Internal Server Error</h1>",
            status=500
        )
        client_socket.sendall(error_response.build())

    finally:
        client_socket.close()


# -----------------------------
# 🚀 Server Setup
# -----------------------------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

print(f"🚀 Server running on http://{HOST}:{PORT}")


# -----------------------------
# 🔁 Main Loop (Threaded)
# -----------------------------
while True:
    client_socket, address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, address)
    )

    thread.start()