from view.view import View
from service.service import Service
from errors import errors
from .front_mixin import FrontMixin


class PostHandler(FrontMixin):
    def __init__(self, handler, view: View, service: Service):
        self.handler = handler
        self.view = view
        self.service = service

    def add_currency(self, form: dict):
        try:
            currency = self.service.add_currency(form)
            self.send_json(self.view.get_json(currency), 201)
        except errors.NoFormFieldError:
            self.send_json(
                self.view.get_error_json("Отсутствует нужное поле формы"), 400
            )
        except errors.SuchCurrencyAlreadyExistsError:
            self.send_json(self.view.get_error_json("Такая валюта уже существует"), 409)
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)

    def add_exchange_rate(self, form: dict):
        try:
            exchange_rate = self.service.add_exchange_rate(form)
            self.send_json(self.view.get_json(exchange_rate), 201)
        except errors.NoFormFieldError:
            self.send_json(
                self.view.get_error_json("Отсутствует нужное поле формы"), 400
            )
        except errors.SuchExchangeRateAlreadyExistsError:
            self.send_json(
                self.view.get_error_json("Валютная пара с таким кодом уже существует"),
                409,
            )
        except errors.NoSuchCurrencyError:
            self.send_json(
                self.view.get_error_json("Как минимум одной из валют нет в базе"), 404
            )
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)
