from view.view import View
from service.service import Service
from errors import errors
from .front_mixin import FrontMixin


class PatchHandler(FrontMixin):
    def __init__(self, handler, view: View, service: Service):
        self.handler = handler
        self.view = view
        self.service = service

    def update_exchange_rate(self, form: dict, path: str):
        try:
            exchange_rate = self.service.update_exchange_rate(form, path)
            self.send_json(self.view.get_json(exchange_rate), 200)
        except errors.NoFormFieldError:
            self.send_json(
                self.view.get_error_json("Отсутствует нужное поле формы"), 400
            )
        except errors.NoSuchExchangeRateError:
            self.send_json(
                self.view.get_error_json("Валютная пара отсутствует в базе данных"),
                404,
            )
        except errors.NoExchangeRatesInPathError:
            self.send_json(
                self.view.get_error_json("Коды валют пары отсутствуют в адресе"), 400
            )
        except errors.DbError:
            self.send_json(self.view.get_error_json("Ошибка базы данных"), 500)
