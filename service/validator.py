class Validator:
    def validate_currency_code(path: str):
        # /currency/USD
        return len(path) == 13

    def validate_currency_form(name: list, code: list, sign: list):
        if not name or not code or not sign:
            return False
        if (
            Validator.validate_code(code[0])
            and Validator.validate_name(name[0])
            and Validator.validate_sign(sign[0])
        ):
            return True
        return False

    def validate_exchange_form(base_code: list, target_code: list, rate: list):
        if not base_code or not target_code or not rate:
            return False
        print(base_code, target_code, rate)
        if (
            Validator.validate_code(base_code[0])
            and Validator.validate_code(target_code[0])
            and Validator.validate_rate(rate[0])
        ):
            return True
        return False

    def validate_exchange_rate(path):
        # /exchangeRate/USDEUR
        return len(path) == 20

    def validate_code(code: str):
        return len(code) == 3 if code else False

    def validate_name(name: str):
        return len(name) <= 30 if name else False

    def validate_sign(sign: str):
        return len(sign) == 1 if sign else False

    def validate_rate(rate: float):
        try:
            rate_value = float(rate)
            return rate_value > 0
        except (ValueError, TypeError):
            return False
