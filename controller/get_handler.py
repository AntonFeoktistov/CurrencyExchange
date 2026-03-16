from view.view import View
from service.service import Service
from errors import errors
from .front_mixin import FrontMixin


class GetHandler(FrontMixin):
    def __init__(self, handler, view: View, service: Service):
        self.handler = handler
        self.view = view
        self.service = service

    def send_currencies(self):
        try:
            currency_list = self.service.get_currencies()
            self.send_json(self.view.get_json(currency_list), 200)
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)

    def send_currency(self, path: str):
        try:
            currency = self.service.get_currency(path)
            self.send_json(self.view.get_json(currency), 200)
        except errors.NoCodeInPathError:
            self.send_json(
                self.view.get_error_json("Код валюты отсутствует в адресе"), 400
            )
        except errors.NoSuchCurrencyError:
            self.send_json(self.view.get_error_json("Валюта не найдена"), 404)
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)

    def send_exchange_rates(self):
        try:
            exchange_rates = self.service.get_exchange_rates()
            self.send_json(self.view.get_json(exchange_rates), 200)
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)

    def send_exchange_rate(self, path: str):
        try:
            exchange_rate = self.service.get_exchange_rate(path)
            self.send_json(self.view.get_json(exchange_rate), 200)
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

    def convert_amount(self, query: dict):
        try:
            amounts = self.service.convert_amount(query)
            if not amounts:
                self.send_json(
                    self.view.get_error_json("Невозможно обменять валюты"), 404
                )
                return
            self.send_json(self.view.get_json(amounts), 200)
        except errors.NoFormFieldError:
            self.send_json(self.view.get_error_json("Некорректные данные формы"), 400)
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)
