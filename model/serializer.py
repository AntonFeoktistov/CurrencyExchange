class Serializer:

    def make_currency(self, row):
        currency = {}
        if row:
            currency = {
                "id": row["ID"],
                "name": row["FullName"],
                "code": row["Code"],
                "sign": row["Sign"],
            }
        return currency

    def make_currency_list(self, rows: list):
        currencies = []
        for row in rows:
            currency = self.make_currency(row)
            currencies.append(currency)
        return currencies

    def make_exchange_rate(self, model, row):
        exchange_rate = {}
        if row:
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

    def make_exchange_rate_list(self, rows: list):
        exchange_rates = []
        for row in rows:
            exchange_rate = self.make_exchange_rate(row)
            exchange_rates.append(exchange_rate)
        return exchange_rates
