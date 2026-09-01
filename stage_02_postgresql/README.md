# Stage 02 — PostgreSQL Data Ingestion

## Objective

Load the transformed CSV generated in Stage 01 into PostgreSQL using Python.

## Pipeline

orders_transformed.csv
→ Python
→ psycopg2
→ PostgreSQL
→ public.orders

## Technologies

- Python
- PostgreSQL
- psycopg2
- python-dotenv
- Git / GitHub

## Features

- PostgreSQL connection using environment variables
- Secure credential management with `.env`
- CSV ingestion using Python
- Data type conversion
- UPSERT using `ON CONFLICT`
- Idempotent pipeline execution

## Source

Input file:

`stage_01_csv_etl/data/orders_transformed.csv`

## Target Table

`public.orders`

Columns:

- order_id
- customer
- quantity
- price
- order_date
- total_amount
