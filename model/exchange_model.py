from functools import cached_property
from errors import errors
import sqlite3
from .serializer import Serializer
from .base_model import BaseModel
from .currency_model import CurrencyModel


class ExchangeModel(BaseModel):

    def get_exchange_rates(self):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ExchangeRates")
                rows = cursor.fetchall()
                exchange_rates = []
                for row in rows:
                    exchange_rate = self.serializer.make_exchange_rate(self, row)
                    exchange_rates.append(exchange_rate)
                return exchange_rates
        except sqlite3.Error as e:
            raise errors.DbError() from e

    def get_exchange_rate(self, base_code: str, target_code: str):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                base_id = self.get_id_by_code(base_code)
                target_id = self.get_id_by_code(target_code)
                if not base_id or not target_id:
                    return
                cursor.execute(
                    """SELECT ID, BaseCurrencyId, TargetCurrencyId, Rate FROM ExchangeRates
                WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?""",
                    (base_id, target_id),
                )
                row = cursor.fetchone()
                exchange_rate = self.serializer.make_exchange_rate(self, row)
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
                print(row)
                print(base_id, target_id)
                print(base_code, target_code)
                return self.serializer.make_exchange_rate(self, row)
        except sqlite3.Error as e:
            raise errors.DbError()

    def update_exchange_rate(self, base_code: str, target_code: str, rate: float | int):
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

    def get_id_by_code(self, code: str):
        currency = self.currency_model.get_currency_by_code(code)
        return currency["id"] if currency else None

    @cached_property
    def currency_model(self):
        return CurrencyModel()

    @cached_property
    def serializer(self):
        return Serializer()
