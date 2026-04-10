from urllib.parse import urlparse, parse_qs
import json


class HttpRequest:
    def __init__(self, raw_data: str):
        self.raw = raw_data

        self.method = None
        self.path = None
        self.version = None
        self.headers = {}

        self.query_params = {}
        self.body = ""
        self.json = None
        self.form_data = {}

        self.parse()

    def parse(self):
        lines = self.raw.split("\r\n")

        # -----------------------------
        # 🧠 Request Line
        # -----------------------------
        request_line = lines[0]
        self.method, full_path, self.version = request_line.split()

        # -----------------------------
        # 🧠 URL parsing
        # -----------------------------
        parsed_url = urlparse(full_path)
        self.path = parsed_url.path
        self.query_params = {
            k: v[0] for k, v in parse_qs(parsed_url.query).items()
        }

        # -----------------------------
        # 🧠 Headers
        # -----------------------------
        i = 1
        while i < len(lines) and lines[i] != "":
            if ": " in lines[i]:
                key, value = lines[i].split(": ", 1)
                self.headers[key.lower()] = value
            i += 1

        # -----------------------------
        # 🧠 Body
        # -----------------------------
        if "\r\n\r\n" in self.raw:
            self.body = self.raw.split("\r\n\r\n", 1)[1]

        content_type = self.headers.get("content-type", "")

        # -----------------------------
        # 🧠 JSON parsing
        # -----------------------------
        if "application/json" in content_type:
            try:
                self.json = json.loads(self.body)
            except:
                self.json = None

        # -----------------------------
        # 🧠 Form parsing
        # -----------------------------
        elif "application/x-www-form-urlencoded" in content_type:
            self.form_data = {
                k: v[0] for k, v in parse_qs(self.body).items()
            }