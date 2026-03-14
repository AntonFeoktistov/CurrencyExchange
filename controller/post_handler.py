import json
from view.view import View
from service.service import Service
from errors import errors


class PostHandler:

    @staticmethod
    def send_json(base_hendler, data: json, status: int):
        """Отправляет JSON с указанным статусом."""
        base_hendler.send_response(status)
        base_hendler.send_header("Content-Type", "application/json; charset=utf-8")
        base_hendler.end_headers()
        base_hendler.wfile.write(data.encode("utf-8"))

    @staticmethod
    def add_currency(base_handler, form: dict):
        try:
            currency = Service.add_currency(form)
            PostHandler.send_json(base_handler, View.get_json_from_dict(currency), 201)
        except errors.NoFormFieldError:
            PostHandler.send_json(
                base_handler, View.get_error_json("Отсутствует нужное поле формы"), 400
            )
        except errors.SuchCurrencyAlreadyExistsError:
            PostHandler.send_json(
                base_handler, View.get_error_json("Такая валюта уже существует"), 409
            )
        except errors.DbError:
            PostHandler.send_json(
                base_handler, View.get_error_json("Ошибка базы данных"), 500
            )
