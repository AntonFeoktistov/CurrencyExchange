class Validator:
    def validate_currency_code(path: str):
        # /currency/USD
        if len(path) != 13:
            return False
        return True

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

    def validate_code(code: str):
        return len(code) == 3 if code else False

    def validate_name(name: str):
        return len(name) <= 40 if name else False

    def validate_sign(sign: str):
        return len(sign) == 1 if sign else False
