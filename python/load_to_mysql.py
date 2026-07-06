import pandas as pd
from sqlalchemy import create_engine, text

# -----------------------------
# MySQL Connection
# -----------------------------
username = "root"
password = "root123"
host = "localhost"
port = "3306"
database = "customer_sales_analytics"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# -----------------------------
# Dataset Path
# -----------------------------
path = "../cleaned_data/"

# -----------------------------
# Tables and Files
# -----------------------------
files = [
    ("customers", "customers.csv"),
    ("orders", "orders.csv"),
    ("products", "products.csv"),
    ("sellers", "sellers.csv"),
    ("order_items", "order_items.csv"),
    ("payments", "payments.csv"),
    ("reviews", "reviews.csv")
]

# -----------------------------
# Clear all tables before importing
# -----------------------------
with engine.begin() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

    conn.execute(text("TRUNCATE TABLE reviews"))
    conn.execute(text("TRUNCATE TABLE payments"))
    conn.execute(text("TRUNCATE TABLE order_items"))
    conn.execute(text("TRUNCATE TABLE orders"))
    conn.execute(text("TRUNCATE TABLE sellers"))
    conn.execute(text("TRUNCATE TABLE products"))
    conn.execute(text("TRUNCATE TABLE customers"))

    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

# -----------------------------
# Load Data
# -----------------------------
for table, file in files:

    print(f"\nLoading {table}...")

    # Read CSV
    df = pd.read_csv(path + file)

    # Convert NaN to None (NULL in MySQL)
    df = df.where(pd.notnull(df), None)

    # Convert datetime columns for Orders table
    if table == "orders":
        date_cols = [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]

        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors="coerce")

        # Convert NaT to None
        df = df.where(pd.notnull(df), None)

    # Convert datetime columns for Order Items table
    elif table == "order_items":
        df["shipping_limit_date"] = pd.to_datetime(
            df["shipping_limit_date"],
            errors="coerce"
        )
        df = df.where(pd.notnull(df), None)

    # Convert datetime columns for Reviews table
    elif table == "reviews":
        review_dates = [
            "review_creation_date",
            "review_answer_timestamp"
        ]

        for col in review_dates:
            df[col] = pd.to_datetime(df[col], errors="coerce")

        df = df.where(pd.notnull(df), None)

    # Load into MySQL
    df.to_sql(
        name=table,
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"{len(df)} rows inserted into {table}")

print("\nAll tables imported successfully!")