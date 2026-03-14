from http.server import BaseHTTPRequestHandler
import json
from view.view import View
from service.service import Service
from errors import errors


class BaseHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обрабатывает GET‑запросы: отдаёт форму или данные."""
        if self.path == "/":
            self.send_json(View.get_index_json(), 200)
        elif self.path == "/currencies":
            try:
                currency_list = Service.get_currencies()
                self.send_json(View.get_json_from_list(currency_list), 200)
            except errors.DbError:
                self.send_json(View.get_error_json("Ошибка базы данных"), 500)
        elif self.path.startswith("/currency/"):
            try:
                currency = Service.get_currency(self.path)
                self.send_json(View.get_json_from_dict(currency), 200)
            except errors.NoCodeInPathError:
                self.send_json(
                    View.get_error_json("Код валюты отсутсвует в адресе"), 400
                )
            except errors.NoSuchCurrencyError:
                self.send_json(View.get_error_json("Валюта не найдена"), 404)
            except errors.DbError:
                self.send_json(View.get_error_json("Ошибка базы данных"), 500)
        else:
            self.send_json(View.get_error_json("нет такой страницы"), 404)

    def send_json(self, data: json, status: int):
        """Отправляет JSON с указанным статусом."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))
