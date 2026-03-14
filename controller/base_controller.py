from functools import cached_property
from http.server import BaseHTTPRequestHandler
import json

import urllib
from .json_mixin import JSONMixin
from view.view import View
from service.service import Service
from errors import errors
from .get_handler import GetHandler
from .post_handler import PostHandler


class BaseHandler(BaseHTTPRequestHandler, JSONMixin):

    def do_GET(self):
        if self.path == "/":
            self.get_handler.send_index()
        elif self.path == "/currencies":
            self.get_handler.send_currencies()
        elif self.path.startswith("/currency/"):
            self.get_handler.send_currency(self.path)
        else:
            self.get_handler.send_error_page()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        # 2. Декодирование и разбор form-data
        try:
            form = urllib.parse.parse_qs(post_data.decode("utf-8"))
        except UnicodeDecodeError:
            self.send_json(
                self.view.get_error_json("Некорректная кодировка данных"), 400
            )
            return
        if self.path == "/currencies":
            self.post_handler.add_currency(form)

    @cached_property
    def view(self):
        return View()

    @cached_property
    def service(self):
        return Service()

    @cached_property
    def get_handler(self):
        return GetHandler(self, self.view, self.service)

    @cached_property
    def post_handler(self):
        return PostHandler(self, self.view, self.service)
