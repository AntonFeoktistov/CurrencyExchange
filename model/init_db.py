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
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
            CREATE TABLE Currencies (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Code VARCHAR(3) NOT NULL UNIQUE,
                FullName VARCHAR(30) NOT NULL,
                Sign VARCHAR(3) NOT NULL
            )
        """
        )
        print("Таблица Currencies создана.")

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
        print(f"Добавлено {len(currencies)} валют.")

        cursor.execute("SELECT ID, Code FROM Currencies")
        currency_ids = {code: id_ for id_, code in cursor.fetchall()}

        cursor.execute(
            """
            CREATE TABLE ExchangeRates (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                BaseCurrencyId INTEGER NOT NULL,
                TargetCurrencyId INTEGER NOT NULL,
                Rate DECIMAL(12,6) NOT NULL,
                
                FOREIGN KEY (BaseCurrencyId) REFERENCES Currencies(ID),
                FOREIGN KEY (TargetCurrencyId) REFERENCES Currencies(ID),
                UNIQUE (BaseCurrencyId, TargetCurrencyId)
            )
        """
        )
        print("Таблица ExchangeRates создана.")

        exchange_rates = [
            (currency_ids["USD"], currency_ids["EUR"], 0.92),
            (currency_ids["USD"], currency_ids["RUB"], 92.50),
            (currency_ids["EUR"], currency_ids["USD"], 1.09),
            (currency_ids["GBP"], currency_ids["RUB"], 118.50),
            (currency_ids["JPY"], currency_ids["USD"], 0.0067),
            (currency_ids["RUB"], currency_ids["EUR"], 0.0099),
            (currency_ids["RUB"], currency_ids["GBP"], 0.0084),
            (currency_ids["RUB"], currency_ids["JPY"], 1.61),
        ]

        cursor.executemany(
            """
            INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate)
            VALUES (?, ?, ?)
        """,
            exchange_rates,
        )
        print(f"Добавлено {len(exchange_rates)} обменных курсов.")

        conn.commit()
        print("✅ База данных успешно инициализирована.")

    except sqlite3.Error as e:
        print(f"❌ Ошибка при работе с БД: {e}")
        conn.rollback()
    finally:
        conn.close()
        print(f"\n🔒 Соединение с {db_file} закрыто.")


if __name__ == "__main__":
    create_database()
