from model.model import Model
from errors import errors
from .validator import Validator


class Service:

    def get_currencies(self):
        try:
            return Model.get_all_currency()
        except errors.DbError:
            raise

    def get_currency(self, path: str):
        try:
            is_currency_valid = Validator.validate_currency_code(path)
            if not is_currency_valid:
                raise errors.NoCodeInPathError()
            code = path[-3:].upper()
            currency = Model.get_currency(code)
            if currency:
                return currency
            else:
                raise errors.NoSuchCurrencyError()
        except errors.DbError:
            raise

    def add_currency(self, form: dict):
        try:
            if not form:
                raise errors.NoFormFieldError()
            name = form.get("name", None)  # извлекает массив а не строку
            code = form.get("code", None)
            sign = form.get("sign", None)
            if not Validator.validate_currency_form(name, code, sign):
                raise errors.NoFormFieldError()
            name, code, sign = name[0], code[0].upper(), sign[0]
            if Model.get_currency(code):
                raise errors.SuchCurrencyAlreadyExistsError()
            currency = Model.add_currency(name, code, sign)
            return currency
        except errors.DbError:
            raise
