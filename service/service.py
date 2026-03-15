from functools import cached_property

from model.currency_model import CurrencyModel
from model.exchange_model import ExchangeModel
from errors import errors
from .validator import Validator


class Service:

    def get_currencies(self):
        try:
            return self.currency_model.get_all_currency()
        except errors.DbError:
            raise

    def get_currency(self, path: str):
        try:
            is_currency_valid = Validator.validate_currency_code(path)
            if not is_currency_valid:
                raise errors.NoCodeInPathError()
            code = path[-3:].upper()
            currency = self.currency_model.get_currency_by_code(code)
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
            if self.currency_model.get_currency(code):
                raise errors.SuchCurrencyAlreadyExistsError()
            currency = self.currency_model.add_currency(name, code, sign)
            return currency
        except errors.DbError:
            raise

    def get_exchange_rates(self):
        try:
            return self.exchange_model.get_exchange_rates()
        except errors.DbError:
            raise

    def get_exchange_rate(self, path: str):
        try:
            is_exchange_rate_valid = Validator.validate_exchange_rate(path)
            if not is_exchange_rate_valid:
                raise errors.NoExchangeRatesInPathError()
            code_1 = path[-6:-3].upper()
            code_2 = path[-3:].upper()
            exchange_rate = self.exchange_model.get_exchange_rate(code_1, code_2)
            if exchange_rate:
                return exchange_rate
            else:
                raise errors.NoSuchExchangeRateError()
        except errors.DbError:
            raise

    def add_exchange_rate(self, form: dict):
        try:
            if not form:
                raise errors.NoFormFieldError()
            base_code = form.get(
                "baseCurrencyCode", None
            )  # извлекает массив а не строку
            target_code = form.get("targetCurrencyCode", None)
            rate = form.get("rate", None)
            if not Validator.validate_exchange_form(base_code, target_code, rate):
                raise errors.NoFormFieldError()
            base_code, target_code, rate = (
                base_code[0].upper(),
                target_code[0].upper(),
                rate[0],
            )
            if self.exchange_model.get_exchange_rate(base_code, target_code):
                raise errors.SuchExchangeRateAlreadyExistsError()
            exchange_rate = self.exchange_model.add_exchange_rate(
                base_code, target_code, rate
            )
            if not exchange_rate:
                raise errors.NoSuchCurrencyError()
            return exchange_rate
        except errors.DbError:
            raise

    def update_exchange_rate(self, form: dict, path: str):
        try:
            if not form:
                raise errors.NoFormFieldError()
            rate = form.get("rate", [0])
            if not Validator.validate_rate(rate[0]):
                raise errors.NoFormFieldError()
            is_exchange_rate_valid = Validator.validate_exchange_rate(path)
            if not is_exchange_rate_valid:
                raise errors.NoExchangeRatesInPathError()
            base_code = path[-6:-3].upper()
            target_code = path[-3:].upper()
            if not self.exchange_model.get_exchange_rate(base_code, target_code):
                raise errors.NoSuchExchangeRateError()
            exchange_rate = self.exchange_model.update_exchange_rate(
                base_code, target_code, rate[0]
            )
            return exchange_rate
        except errors.DbError:
            raise

    @cached_property
    def currency_model(self):
        return CurrencyModel()

    @cached_property
    def exchange_model(self):
        return ExchangeModel()
