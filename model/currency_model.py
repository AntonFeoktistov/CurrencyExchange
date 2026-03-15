from errors import errors
import sqlite3
from .serializer import Serializer

DB_FILE = "model/currencies.db"


class CurrencyModel:

    def get_db_connection(self):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
        return conn

    def get_all_currency(self):
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Currencies")
                rows = cursor.fetchall()
                currencies = Serializer.make_currency_list(rows)
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
                currency = Serializer.make_currency(row)
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
                currency = Serializer.make_currency(row)
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
                currency = Serializer.make_currency(row) if row else {}
                return currency
        except sqlite3.Error as e:
            raise errors.DbError()
