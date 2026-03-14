class Validator:
    def validate_currency_code(path: str):
        # /currency/USD
        if len(path) != 13:
            return False
        return True
