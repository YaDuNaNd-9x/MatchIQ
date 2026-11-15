import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = PROJECT_ROOT / "analytics" / "sql"

load_dotenv(PROJECT_ROOT / ".env", override=True)


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )


def run_queries():
    sql_files = sorted(SQL_DIR.glob("*.sql"))

    if not sql_files:
        print("No SQL files found.")
        return

    print(f"Found {len(sql_files)} SQL queries.")

    with get_connection() as connection:
        for sql_file in sql_files:
            print("\n" + "=" * 90)
            print(f"QUERY: {sql_file.name}")
            print("=" * 90)

            query = sql_file.read_text(encoding="utf-8")

            with connection.cursor() as cursor:
                cursor.execute(query)

                columns = [column.name for column in cursor.description]
                rows = cursor.fetchall()

            print(" | ".join(columns))
            print("-" * 90)

            for row in rows[:15]:
                print(" | ".join(str(value) for value in row))

            print(f"\nRows returned: {len(rows)}")

    print("\nALL SQL ANALYTICS QUERIES EXECUTED SUCCESSFULLY.")


if __name__ == "__main__":
    run_queries()