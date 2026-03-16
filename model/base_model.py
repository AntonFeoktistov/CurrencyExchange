import sqlite3


DB_FILE = "currencies.db"


class BaseModel:
    def get_db_connection(self):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
