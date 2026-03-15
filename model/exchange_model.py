from functools import cached_property

from errors import errors
import sqlite3
from .serializer import Serializer
from .currency_model import CurrencyModel

DB_FILE = "model/currencies.db"


class ExchangeModel:

    def get_db_connection(self):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
        return conn

    def get_exchange_rates(self):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ExchangeRates")
                rows = cursor.fetchall()  # id cur1_id cur2_id rate
                exchange_rates = []
                for row in rows:
                    exchange_rate = self.make_exchange_rate_by_row(row)
                    exchange_rates.append(exchange_rate)
                return exchange_rates
        except sqlite3.Error as e:
            raise errors.DbError() from e

    def get_exchange_rate(self, code_1: str, code_2: str):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                id_1 = self.get_id_by_code(code_1)
                id_2 = self.get_id_by_code(code_2)
                if not id_1 or not id_2:
                    return
                cursor.execute(
                    """SELECT ID, BaseCurrencyId, TargetCurrencyId, Rate FROM ExchangeRates
                WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?""",
                    (id_1, id_2),
                )
                row = cursor.fetchone()
                exchange_rate = self.make_exchange_rate_by_row(row) if row else {}
                return exchange_rate
        except sqlite3.Error as e:
            raise errors.DbError() from e

    def add_exchange_rate(self, base_code, target_code, rate):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                base_id = self.get_id_by_code(base_code)
                target_id = self.get_id_by_code(target_code)
                if not base_id or not target_id:
                    return
                cursor.execute(
                    """INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate)
                      VALUES (?, ?, ?)""",
                    (base_id, target_id, rate),
                )
                conn.commit()
                cursor.execute(
                    """SELECT ID, BaseCurrencyId, TargetCurrencyId, Rate 
                    FROM ExchangeRates WHERE BaseCurrencyId = ? AND TargetCurrencyId = ? """,
                    (base_id, target_id),
                )
                row = cursor.fetchone()
                return self.make_exchange_rate_by_row(row)

        except sqlite3.Error as e:
            raise errors.DbError()

    def update_exchange_rate(self, base_code: str, target_code: str, rate: float):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                base_id = self.get_id_by_code(base_code)
                target_id = self.get_id_by_code(target_code)
                cursor.execute(
                    """UPDATE ExchangeRates 
                   SET Rate = ? 
                   WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?""",
                    (rate, base_id, target_id),
                )
                conn.commit()
                exchange_rate = self.get_exchange_rate(base_code, target_code)
                return exchange_rate
        except sqlite3.Error as e:
            raise errors.DbError()

    def make_exchange_rate_by_row(self, row):
        exchange_rate = {
            "ID": row["ID"],
            "BaseCurrency": self.currency_model.get_currency_by_id(
                row["BaseCurrencyId"]
            ),
            "TargetCurrency": self.currency_model.get_currency_by_id(
                row["TargetCurrencyId"]
            ),
            "rate": row["Rate"],
        }
        return exchange_rate

    def get_id_by_code(self, code: str):
        row = self.currency_model.get_currency_by_code(code)
        return row["ID"] if row else None

    @cached_property
    def currency_model(self):
        return CurrencyModel()

    @cached_property
    def serializer(self):
        return Serializer()
