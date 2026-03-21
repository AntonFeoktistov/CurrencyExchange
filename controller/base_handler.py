from functools import cached_property
from http.server import BaseHTTPRequestHandler
import urllib
from .front_mixin import FrontMixin
from view.view import View
from service.service import Service
from .get_handler import GetHandler
from .post_handler import PostHandler
from .patch_handler import PatchHandler


class BaseHandler(BaseHTTPRequestHandler, FrontMixin):

    def do_GET(self):
        if self.path == "/currencies":
            self.get_handler.send_currencies()

        elif self.path.startswith("/currency/"):
            self.get_handler.send_currency(self.path)

        elif self.path == "/exchangeRates":
            self.get_handler.send_exchange_rates()

        elif self.path.startswith("/exchangeRate/"):
            self.get_handler.send_exchange_rate(self.path)

        elif self.path.startswith("/exchange"):

            self.get_handler.convert_amount(self.get_query(self.path))
        else:
            self.send_static(self.path)

    def do_POST(self):
        form = self.get_form()
        if self.path == "/currencies":
            self.post_handler.add_currency(form)

        if self.path == "/exchangeRates":
            self.post_handler.add_exchange_rate(form)

    def do_PATCH(self):
        form = self.get_form()
        if self.path.startswith("/exchangeRate/"):
            self.patch_handler.update_exchange_rate(form, self.path)

    def get_query(self, path: str):
        try:
            parsed_path = urllib.parse.urlparse(path)
            return urllib.parse.parse_qs(parsed_path.query)
        except Exception:
            return {}

    def get_form(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            return urllib.parse.parse_qs(post_data.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {}

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

    @cached_property
    def patch_handler(self):
        return PatchHandler(self, self.view, self.service)
