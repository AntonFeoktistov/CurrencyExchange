import json
from view.view import View
from service.service import Service
from errors import errors


class GetHandler:

    def send_currency(self):
        pass

    @staticmethod
    def send_json(base_hendler, data: json, status: int):
        """Отправляет JSON с указанным статусом."""
        base_hendler.send_response(status)
        base_hendler.send_header("Content-Type", "application/json; charset=utf-8")
        base_hendler.end_headers()
        base_hendler.wfile.write(data.encode("utf-8"))

    @staticmethod
    def send_index(base_handler):
        GetHandler.send_json(base_handler, View.get_index_json(), 200)

    @staticmethod
    def send_error_page(base_handler):
        GetHandler.send_json(
            base_handler, View.get_error_json("нет такой страницы"), 404
        )

    @staticmethod
    def send_currencies(base_handler):
        try:
            currency_list = Service.get_currencies()
            GetHandler.send_json(
                base_handler, View.get_json_from_list(currency_list), 200
            )
        except errors.DbError:
            GetHandler.send_json(
                base_handler, View.get_error_json("Ошибка базы данных"), 500
            )

    @staticmethod
    def send_currency(base_handler):
        path = base_handler.path
        try:
            currency = Service.get_currency(path)
            GetHandler.send_json(base_handler, View.get_json_from_dict(currency), 200)
        except errors.NoCodeInPathError:
            GetHandler.send_json(
                base_handler, View.get_error_json("Код валюты отсутсвует в адресе"), 400
            )
        except errors.NoSuchCurrencyError:
            GetHandler.send_json(
                base_handler, View.get_error_json("Валюта не найдена"), 404
            )
        except errors.DbError:
            GetHandler.send_json(
                base_handler, View.get_error_json("Ошибка базы данных"), 500
            )
