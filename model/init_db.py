import sqlite3
import os


def create_database():
    db_file = "currencies.db"

    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Старый файл {db_file} удалён.")

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # 1. Включаем поддержку внешних ключей
        cursor.execute("PRAGMA foreign_keys = ON")

        # 2. Создаём Currencies
        cursor.execute(
            """
            CREATE TABLE Currencies (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Code VARCHAR(3) NOT NULL UNIQUE,
                FullName VARCHAR(40) NOT NULL,
                Sign VARCHAR(3) NOT NULL
            )
        """
        )
        print("Таблица Currencies создана.")

        # 3. Заполняем Currencies
        currencies = [
            ("USD", "United States Dollar", "$"),
            ("EUR", "Euro", "€"),
            ("GBP", "British Pound Sterling", "£"),
            ("JPY", "Japanese Yen", "¥"),
            ("RUB", "Russian Ruble", "₽"),
        ]
        cursor.executemany(
            """
            INSERT INTO Currencies (Code, FullName, Sign)
            VALUES (?, ?, ?)
        """,
            currencies,
        )

        # 4. Создаём ExchangeRates С ВНЕШНИМИ КЛЮЧАМИ ВНУТРИ CREATE TABLE
        cursor.execute(
            """
            CREATE TABLE ExchangeRates (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                BaseCurrencyId INTEGER NOT NULL,
                TargetCurrencyId INTEGER NOT NULL,
                Rate DECIMAL(12,6) NOT NULL,
                
                -- Внешние ключи прямо в CREATE TABLE
                FOREIGN KEY (BaseCurrencyId) REFERENCES Currencies(ID),
                FOREIGN KEY (TargetCurrencyId) REFERENCES Currencies(ID),
                
                -- Уникальный ключ на пару валют
                UNIQUE (BaseCurrencyId, TargetCurrencyId)
            )
        """
        )
        print("Таблица ExchangeRates создана.")

        conn.commit()
        print("База данных успешно инициализирована.")

    except sqlite3.Error as e:
        print(f"Ошибка при работе с БД: {e}")
        conn.rollback()
    finally:
        conn.close()
        print(f"Соединение с {db_file} закрыто.")


if __name__ == "__main__":
    create_database()
