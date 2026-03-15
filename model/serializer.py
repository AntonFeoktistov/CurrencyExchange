class Serializer:

    def make_currency(row: dict):
        currency = {}
        if row:
            currency = {
                "id": row["ID"],
                "name": row["FullName"],
                "code": row["Code"],
                "sign": row["Sign"],
            }
        return currency

    def make_currency_list(rows: dict):
        currencies = []
        for row in rows:
            currency = Serializer.make_currency(row)
            currencies.append(currency)
        return currencies

    @staticmethod
    def make_exchange_rate_by_row(model, row):
        exchange_rate = {
            "id": row["ID"],
            "baseCurrency": model.currency_model.get_currency_by_id(
                row["BaseCurrencyId"]
            ),
            "targetCurrency": model.currency_model.get_currency_by_id(
                row["TargetCurrencyId"]
            ),
            "rate": row["Rate"],
        }
        return exchange_rate
