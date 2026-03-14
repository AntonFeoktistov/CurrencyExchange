class NoCurrenciesError(Exception):
    pass


class DbError(Exception):
    pass


class NoCodeInPathError(Exception):
    pass


class NoSuchCurrencyError(Exception):
    pass


class NoCurrencyInPathError(Exception):
    pass


class NoExchangeRatesInPathError(Exception):
    pass


class NotValidNameError(Exception):
    pass


class NotValidCodeError(Exception):
    pass


class NotValidSignError(Exception):
    pass


class SuchCurrencyAlreadyExistsError(Exception):
    pass


class SuchExchangeRateAlreadyExistsError(Exception):
    pass


class NotValidChangeCodesError(Exception):
    pass


class NotValidChangeRateError(Exception):
    pass


class NoSuchExchangeRateError(Exception):
    pass


class NotValidAmount(Exception):
    pass
