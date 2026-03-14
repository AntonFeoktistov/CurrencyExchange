from http.server import BaseHTTPRequestHandler
import json
from view.view import View
from service.service import Service
from errors import errors
from .json_mixin import JSONMixin


class PostHandler(JSONMixin):

    def __init__(self, handler, view: View, service: Service):
        self.handler = handler
        self.view = view
        self.service = service

    def add_currency(self, form: dict):
        try:
            currency = self.service.add_currency(form)
            self.send_json(self.view.get_json_from_dict(currency), 201)
        except errors.NoFormFieldError:
            self.send_json(
                self.view.get_error_json("Отсутствует нужное поле формы"), 400
            )
        except errors.SuchCurrencyAlreadyExistsError:
            self.send_json(self.view.get_error_json("Такая валюта уже существует"), 409)
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)
