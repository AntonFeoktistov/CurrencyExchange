class Serializer:

    def make_currency_list(self, rows: dict):
        currencies = []
        for row in rows:
            currencies.append(
                {
                    "ID": row["ID"],
                    "NAME": row["FullName"],
                    "CODE": row["Code"],
                    "SIGN": row["SIGN"],
                }
            )
        return currencies

    def make_currency(self, row: dict):
        currency = {}
        if row:
            currency = {
                "ID": row["ID"],
                "NAME": row["FullName"],
                "CODE": row["Code"],
                "SIGN": row["SIGN"],
            }
        return currency
