class Validator:

    def validate_currency_path(pself, path: str):
        return len(path) == 13

    def validate_add_currency_form(self, name: str, code: str, sign: str):
        if (
            self.validate_code(code)
            and self.validate_name(name)
            and self.validate_sign(sign)
        ):
            return True
        return False

    def validate_exchange_form(self, base_code: str, target_code: str, rate: str):
        if (
            self.validate_code(base_code)
            and self.validate_code(target_code)
            and self.validate_rate(rate)
        ):
            return True
        return False

    def validate_exchange_rate_path(self, path):
        return len(path) == 20

    def validate_code(self, code: str):
        return len(code) == 3 if code else False

    def validate_name(self, name: str):
        return (0 < len(name) <= 30) and bool(name and name.strip()) if name else False

    def validate_sign(self, sign: str):
        return (len(sign) == 1 and sign != " ") if sign else False

    def validate_rate(self, rate: float):
        try:
            rate_value = float(rate)
            return rate_value > 0
        except (ValueError, TypeError):
            return False
