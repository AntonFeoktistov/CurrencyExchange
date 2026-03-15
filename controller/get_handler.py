from http.server import BaseHTTPRequestHandler
import json
from view.view import View
from service.service import Service
from errors import errors
from .json_mixin import JSONMixin


class GetHandler(JSONMixin):
    def __init__(self, handler, view: View, service: Service):
        self.handler = handler
        self.view = view
        self.service = service

    def send_index(self):
        self.send_json(self.view.get_index_json(), 200)

    def send_error_page(self):
        self.send_json(self.view.get_error_json("нет такой страницы"), 404)

    def send_currencies(self):
        try:
            currency_list = self.service.get_currencies()
            self.send_json(self.view.get_json_from_list(currency_list), 200)
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)

    def send_currency(self, path: str):
        try:
            currency = self.service.get_currency(path)
            self.send_json(self.view.get_json_from_dict(currency), 200)
        except errors.NoCodeInPathError:
            self.send_json(
                self.view.get_error_json("Код валюты отсутсвует в адресе"), 400
            )
        except errors.NoSuchCurrencyError:
            self.send_json(self.view.get_error_json("Валюта не найдена"), 404)
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)

    def send_exchange_rates(self):
        try:
            exchange_rates = self.service.get_exchange_rates()
            self.send_json(self.view.get_json_from_list(exchange_rates), 200)
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)

    def send_exchange_rate(self, path: str):
        try:
            exchange_rate = self.service.get_exchange_rate(path)
            self.send_json(self.view.get_json_from_dict(exchange_rate), 200)
        except errors.NoExchangeRatesInPathError:
            self.send_json(
                self.view.get_error_json("Коды валют пары отсутствуют в адресе"), 400
            )
        except errors.NoSuchExchangeRateError:
            self.send_json(
                self.view.get_error_json("Обменный курс для пары не найден"), 404
            )
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)
