import json
import os


class FrontMixin:
    # содержит методы для взаимодействия с фронтендом

    def send_json(self, data: json, status: int):
        handler = getattr(self, "handler", self)
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json; charset=utf-8")
        handler.end_headers()
        handler.wfile.write(data.encode("utf-8"))

    def send_static(self, path):
        FRONTEND_DIR = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend"
        )
        p = os.path.join(
            FRONTEND_DIR, ("index.html" if path in ("/", "") else path).lstrip("/")
        )
        if os.path.isfile(p):
            with open(p, "rb") as f:
                self.send_response(200)
                self.send_header("Content-Type", self.get_content_type(p))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def get_content_type(self, file_path):
        CONTENT_TYPES = {
            ".html": "text/html",
            ".htm": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".txt": "text/plain",
        }
        return CONTENT_TYPES.get(
            os.path.splitext(file_path)[1].lower(), "application/octet-stream"
        )

    def do_OPTIONS(self):
        """Обработка preflight запросов для CORS"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
