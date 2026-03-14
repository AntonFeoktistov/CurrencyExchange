from model.model import Model
from errors import errors
from .validator import Validator


class Service:

    def get_currencies():
        try:
            return Model.get_all_currency()
        except errors.DbError:
            raise

    def get_currency(path: str):
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
