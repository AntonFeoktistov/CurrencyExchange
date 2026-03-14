from http.server import BaseHTTPRequestHandler
import json

import urllib
from view.view import View
from service.service import Service
from errors import errors
from .get_handler import GetHandler
from .post_handler import PostHandler


class BaseHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            GetHandler.send_index(self)
        elif self.path == "/currencies":
            GetHandler.send_currencies(self)
        elif self.path.startswith("/currency/"):
            GetHandler.send_currency(self)
        else:
            GetHandler.send_error_page(self)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        # 2. Декодирование и разбор form-data
        try:
            form = urllib.parse.parse_qs(post_data.decode("utf-8"))
        except UnicodeDecodeError:
            self.send_json(View.get_error_json("Некорректная кодировка данных"), 400)
            return
        if self.path == "/currencies":
            PostHandler.add_currency(self, form)

    def send_json(self, data: json, status: int):
        """Отправляет JSON с указанным статусом."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))
