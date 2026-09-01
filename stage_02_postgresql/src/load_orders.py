import csv
import os
from datetime import date
from decimal import Decimal
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Locate project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_FILE = (
    PROJECT_ROOT
    / "stage_01_csv_etl"
    / "data"
    / "orders_transformed.csv"
)


try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    cursor = conn.cursor()

    # Read transformed CSV
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            order_id = int(row["order_id"])
            customer = row["customer"]
            quantity = int(row["quantity"])
            price = Decimal(row["price"])
            order_date = date.fromisoformat(row["order_date"])
            total_amount = Decimal(row["total_amount"])

            cursor.execute(
                """
                INSERT INTO public.orders (
                    order_id,
                    customer,
                    quantity,
                    price,
                    order_date,
                    total_amount
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id)
                DO UPDATE SET
                    customer = EXCLUDED.customer,
                    quantity = EXCLUDED.quantity,
                    price = EXCLUDED.price,
                    order_date = EXCLUDED.order_date,
                    total_amount = EXCLUDED.total_amount;
                """,
                (
                    order_id,
                    customer,
                    quantity,
                    price,
                    order_date,
                    total_amount,
                ),
            )

    conn.commit()

    print("✅ orders_transformed.csv loaded successfully into PostgreSQL!")

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Data load failed:")
    print(e)