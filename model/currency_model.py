from functools import cached_property

from errors import errors
import sqlite3
from .serializer import Serializer
from .base_model import BaseModel


class CurrencyModel(BaseModel):

    def get_all_currency(self):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Currencies")
                rows = cursor.fetchall()
                currencies = self.serializer.make_currency_list(rows)
            return currencies
        except sqlite3.Error as e:
            raise errors.DbError() from e

    def get_currency_by_code(self, code: str):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, FullName, Code, Sign FROM Currencies WHERE CODE = ?",
                    (code,),
                )
                row = cursor.fetchone()
                currency = self.serializer.make_currency(row)
                return currency
        except sqlite3.Error as e:
            raise errors.DbError()

    def add_currency(self, name: str, code: str, sign: str):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Currencies (FullName, Code, Sign) VALUES (?, ?, ?)",
                    (name, code, sign),
                )
                conn.commit()
                cursor.execute("SELECT * FROM Currencies WHERE Code = ?", (code,))
                row = cursor.fetchone()
                currency = self.serializer.make_currency(row)
                return currency
        except sqlite3.Error as e:
            raise errors.DbError()

    def get_currency_by_id(self, id: int):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT ID, FullName, Code, Sign FROM Currencies WHERE ID = ?",
                    (id,),
                )
                row = cursor.fetchone()
                currency = self.serializer.make_currency(row)
                return currency
        except sqlite3.Error as e:
            raise errors.DbError()

    @cached_property
    def serializer(self):
        return Serializer()
