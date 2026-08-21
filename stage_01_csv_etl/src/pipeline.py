from xml.parsers.expat import errors

import pandas as pd
import logging

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract(path):
    df = pd.read_csv(path)
    return df

def validate_columns(df):
    
    required_columns = [
        "order_id",
        "customer",
        "quantity",
        "price",
        "order_date",
    ]

    actual_columns = list(df.columns)

    missing_columns = [
        col for col in required_columns
        if col not in actual_columns
    ]

    unexpected_columns = [
        col for col in actual_columns
        if col not in required_columns
    ]

    if missing_columns or unexpected_columns:

        error_message = ""

        if missing_columns:
            error_message += (
                f"Missing column : {missing_columns}."
            )

        if unexpected_columns:
            error_message += (
                f"Unexpected column : {unexpected_columns}."
            )
        raise ValueError(error_message)
    
    return df  

def validate_data(df):

    errors = []

    #1. check null values

    required_field = [
        "order_id",
        "customer",
        "quantity",
        "price",
        "order_date",
    ]

    null_columns = df[required_field].columns[
        df[required_field].isnull().any()
        ].tolist()

    if null_columns:
        errors.append(
            f"Null values found in columns: {null_columns}"
            )

    #2. check duplicated order IDs

    duplicate_orders = df[
        df["order_id"].duplicated(keep=False)
    ]["order_id"].to_list()

    if duplicate_orders:
        errors.append(
            f"Duplicated order IDs found: {duplicate_orders}"
            )

    #3. check quantity and price are numeric

    numeric_columns = ["quantity", "price"]

    for col in numeric_columns:

        converted = pd.to_numeric(
            df[col],
            errors="coerce"
        )
        if converted.isnull().any():

            invalid_values = df.loc[
                converted.isnull(),
                col
            ].to_list()
            errors.append(
                f"Non-numeric values found in column: {col}"
            )
        if (df["price"] < 0).any():
            errors.append("Negative values detected in price.")

        # raise all errors together

        if errors:

            error_message = "\n".join(
                f"- {error}" for error in errors
            )

            raise ValueError(
                f"\nData validation failed: \n{error_message}"
            )

        return df
    
def transform(df):
    df["total_amount"] = df["quantity"] * df["price"]
    return df

def load(df, path):
    df.to_csv(path, index=False)

def main():

    try:
        logging.info("Pipeline started")

        df_orders = extract("data/orders.csv")
        logging.info(f"{len(df_orders)} rows extracted")

        df_orders = validate_columns(df_orders)
        logging.info("Column validation passed")

        df_orders = validate_data(df_orders)
        logging.info("Data validation passed")

        df_orders = transform(df_orders)
        logging.info("Transformation completed")

        load(df_orders, "data/orders_transformed.csv")
        logging.info(f"{len(df_orders)} rows loaded")

        logging.info("Pipeline completed successfully")

        print("Pipeline completed successfully.")

    except Exception as e:

        logging.error(
            f"Pipeline failed: {e}"
        )

        print(
            f"Pipeline failed: {e}"
        )

    

if __name__ == "__main__":
    main()