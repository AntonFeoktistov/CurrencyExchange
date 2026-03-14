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
        form = self.get_form()  # валидация формы дальше
        if self.path == "/currencies":
            self.post_handler.add_currency(form)

    def get_form(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            form = urllib.parse.parse_qs(post_data.decode("utf-8"))
            return form
        except (ValueError, UnicodeDecodeError):
            return None

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
