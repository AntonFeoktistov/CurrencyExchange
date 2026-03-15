from functools import cached_property
from http.server import BaseHTTPRequestHandler
import json
import urllib
import os  # Добавить импорт
from .json_mixin import JSONMixin
from view.view import View
from service.service import Service
from errors import errors
from .get_handler import GetHandler
from .post_handler import PostHandler
from .patch_handler import PatchHandler


class BaseHandler(BaseHTTPRequestHandler, JSONMixin):

    def do_GET(self):
        # Разбираем путь
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API запросы (оставляем как есть)
        if path == "/currencies":
            self.get_handler.send_currencies()
        elif path.startswith("/currency/"):
            self.get_handler.send_currency(path)
        elif path == "/exchangeRates":
            self.get_handler.send_exchange_rates()
        elif path.startswith("/exchangeRate/"):
            self.get_handler.send_exchange_rate(path)
        elif path.startswith("/exchange"):
            self.get_handler.convert_amount(self.get_query(self.path))
        else:
            # Все остальные запросы - пытаемся отдать статику
            self.serve_static(path)

    def serve_static(self, path):
        """Раздача статических файлов фронтенда"""
        try:
            # Путь к папке с фронтендом (создайте её в корне проекта)
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            frontend_dir = os.path.join(base_dir, "frontend")

            # Если запрошен корень - отдаем index.html
            if path == "/" or path == "":
                path = "/index.html"

            # Безопасно формируем путь к файлу
            relative_path = path.lstrip("/")
            file_path = os.path.normpath(os.path.join(frontend_dir, relative_path))

            # Проверяем, что файл действительно внутри frontend (безопасность)
            if not file_path.startswith(os.path.abspath(frontend_dir)):
                self.send_error(403, "Access denied")
                return

            # Проверяем существование файла
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                self.send_error(404, "File not found")
                return

            # Определяем Content-Type
            content_type = self.get_content_type(file_path)

            # Читаем и отдаем файл
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            self.send_error(500, str(e))

    def get_content_type(self, file_path):
        """Определяет Content-Type по расширению файла"""
        ext = os.path.splitext(file_path)[1].lower()
        types = {
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
        return types.get(ext, "application/octet-stream")

    # Остальные методы остаются без изменений
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

    def do_OPTIONS(self):
        """Обработка preflight запросов для CORS"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

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
