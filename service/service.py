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
            if not self.validator.validate_currency_path(path):
                raise errors.NoCodeInPathError()
            code = path[-3:]
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
            name = (form.get("name") or [""])[0]
            code = (form.get("code") or [""])[0]
            sign = (form.get("sign") or [""])[0]
            if not self.validator.validate_add_currency_form(name, code, sign):
                raise errors.NoFormFieldError()
            if self.currency_model.get_currency_by_code(code):
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
            if not self.validator.validate_exchange_rate_path(path):
                raise errors.NoExchangeRatesInPathError()
            base_code = path[-6:-3]
            target_code = path[-3:]
            exchange_rate = self.exchange_model.get_exchange_rate(
                base_code, target_code
            )
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
            base_code = (form.get("baseCurrencyCode") or [""])[0]
            target_code = (form.get("targetCurrencyCode") or [""])[0]
            rate = (form.get("rate") or [""])[0]
            if not self.validator.validate_exchange_form(base_code, target_code, rate):
                raise errors.NoFormFieldError()
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
            rate = (form.get("rate") or [""])[0]
            if not self.validator.validate_rate(rate):
                raise errors.NoFormFieldError()
            if not self.validator.validate_exchange_rate_path(path):
                raise errors.NoExchangeRatesInPathError()
            base_code = path[-6:-3]
            target_code = path[-3:]
            if not self.exchange_model.get_exchange_rate(base_code, target_code):
                raise errors.NoSuchExchangeRateError()
            exchange_rate = self.exchange_model.update_exchange_rate(
                base_code, target_code, rate
            )
            return exchange_rate
        except errors.DbError:
            raise

    def convert_amount(self, query: dict):
        if not query:
            raise errors.NoFormFieldError()
        from_code = (query.get("from") or [""])[0]
        to_code = (query.get("to") or [""])[0]
        amount = (query.get("amount") or [""])[0]
        if not self.validator.validate_exchange_form(from_code, to_code, amount):
            raise errors.NoFormFieldError()
        amount = float(amount)
        AB_variant = self.convert_AB(from_code, to_code, amount)
        if AB_variant:
            return AB_variant
        BA_variant = self.convert_BA(from_code, to_code, amount)
        if BA_variant:
            return BA_variant
        USD_variant = self.convert_USD(from_code, to_code, amount)
        if USD_variant:
            return USD_variant
        return {}

    def convert_AB(self, from_code: str, to_code: str, amount: float | int):
        AB_variant = self.exchange_model.get_exchange_rate(from_code, to_code)
        if AB_variant:
            AB_variant["amount"] = amount
            AB_variant["convertedAmount"] = round(AB_variant["rate"] * amount, 3)
            return AB_variant

    def convert_BA(self, from_code: str, to_code: str, amount: float | int):
        BA_variant = self.exchange_model.get_exchange_rate(to_code, from_code)
        if BA_variant:
            BA_variant["rate"] = round(1 / BA_variant["rate"], 3)
            BA_variant["amount"] = amount
            BA_variant["convertedAmount"] = round(BA_variant["rate"] * amount, 3)
            return BA_variant

    def convert_USD(self, from_code: str, to_code: str, amount: float | int):
        USD_variant_from = self.exchange_model.get_exchange_rate("USD", from_code)
        USD_variant_to = self.exchange_model.get_exchange_rate("USD", to_code)
        if USD_variant_from and USD_variant_to:
            currency_from = self.currency_model.get_currency_by_code(from_code)
            currency_to = self.currency_model.get_currency_by_code(to_code)
            rate = USD_variant_to["rate"] / USD_variant_from["rate"]
            return {
                "baseCurrency": currency_from,
                "targetCurrency": currency_to,
                "rate": rate,
                "amount": amount,
                "convertedAmount": round(rate * amount, 3),
            }

    @cached_property
    def currency_model(self):
        return CurrencyModel()

    @cached_property
    def exchange_model(self):
        return ExchangeModel()

    @cached_property
    def validator(self):
        return Validator()
