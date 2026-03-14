import os, sys

# Добавляем корневую папку проекта в путь поиска модулей
# Поднимаемся на два уровня вверх: model.py -> model/ -> CurrencyExchange/
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from errors import errors
import sqlite3
from .serializer import Serializer


DB_FILE = "model/currencies.db"


class Model:
    def get_db_connection():
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
        return conn

    def get_all_currency():
        try:
            conn = Model.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Currencies")
            rows = cursor.fetchall()
            currencies = Serializer.make_currency_list(rows)
            return currencies
        except sqlite3.Error as e:
            raise errors.DbError()
        finally:
            if conn:
                conn.close()

    def get_currency(code: str):
        try:
            conn = Model.get_db_connection()
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
        finally:
            if conn:
                conn.close()

    def add_currency(name: str, code: str, sign: str):
        try:
            conn = Model.get_db_connection()
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
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    try:
        currencies = Model.get_all_currency()
        print(currencies)
    except errors.DbError as e:
        print(f"Ошибка: {e}")
