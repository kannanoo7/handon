class HttpResponse:
    def __init__(self, body="", status=200, headers=None):
        self.body = body if isinstance(body, bytes) else body.encode()
        self.status = status
        self.headers = headers or {}

    def _status_line(self):
        status_messages = {
            200: "OK",
            404: "Not Found",
            500: "Internal Server Error"
        }
        return f"HTTP/1.1 {self.status} {status_messages.get(self.status, '')}\r\n"

    def build(self):
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "text/html"

        self.headers["Content-Length"] = str(len(self.body))

        header_lines = ""
        for key, value in self.headers.items():
            header_lines += f"{key}: {value}\r\n"

        return (
            self._status_line() +
            header_lines +
            "\r\n"
        ).encode() + self.body