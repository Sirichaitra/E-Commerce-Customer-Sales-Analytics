import pandas as pd

# Dataset path
path = "../dataset/"

# Load datasets
customers = pd.read_csv(path + "olist_customers_dataset.csv")
orders = pd.read_csv(path + "olist_orders_dataset.csv")
order_items = pd.read_csv(path + "olist_order_items_dataset.csv")
payments = pd.read_csv(path + "olist_order_payments_dataset.csv")
products = pd.read_csv(path + "olist_products_dataset.csv")
reviews = pd.read_csv(path + "olist_order_reviews_dataset.csv")
sellers = pd.read_csv(path + "olist_sellers_dataset.csv")
category = pd.read_csv(path + "product_category_name_translation.csv")

print("Datasets Loaded Successfully")

# --------------------------------------------------
# Check Duplicate Records
# --------------------------------------------------

datasets = {
    "Customers": customers,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Products": products,
    "Reviews": reviews,
    "Sellers": sellers,
    "Category": category
}

print("\nDuplicate Records\n")

for name, df in datasets.items():
    duplicates = df.duplicated().sum()
    print(f"{name}: {duplicates}")

# --------------------------------------------------
# Check Missing Values
# --------------------------------------------------

print("\n" + "=" * 50)
print("Missing Values")
print("=" * 50)

for name, df in datasets.items():
    print(f"\n{name}")
    print(df.isnull().sum())

# --------------------------------------------------
# Convert Date Columns
# --------------------------------------------------

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col])

reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"])
reviews["review_answer_timestamp"] = pd.to_datetime(reviews["review_answer_timestamp"])

order_items["shipping_limit_date"] = pd.to_datetime(order_items["shipping_limit_date"])

print("\nDate columns converted successfully!")

# --------------------------------------------------
# Handle Missing Values - Products
# --------------------------------------------------

# Fill missing product category with 'Unknown'
products["product_category_name"] = products["product_category_name"].fillna("Unknown")

# Fill numeric columns with median
products["product_weight_g"] = products["product_weight_g"].fillna(
    products["product_weight_g"].median()
)

products["product_length_cm"] = products["product_length_cm"].fillna(
    products["product_length_cm"].median()
)

products["product_height_cm"] = products["product_height_cm"].fillna(
    products["product_height_cm"].median()
)

products["product_width_cm"] = products["product_width_cm"].fillna(
    products["product_width_cm"].median()
)

# Fill remaining numeric columns with 0
products["product_name_lenght"] = products["product_name_lenght"].fillna(0)
products["product_description_lenght"] = products["product_description_lenght"].fillna(0)
products["product_photos_qty"] = products["product_photos_qty"].fillna(0)

# --------------------------------------------------
# Handle Missing Values - Reviews
# --------------------------------------------------

reviews["review_comment_title"] = reviews["review_comment_title"].fillna("")
reviews["review_comment_message"] = reviews["review_comment_message"].fillna("")

# --------------------------------------------------
# Check Missing Values After Cleaning
# --------------------------------------------------

print("\n" + "=" * 50)
print("Missing Values After Cleaning")
print("=" * 50)

print("\nProducts")
print(products.isnull().sum())

print("\nReviews")
print(reviews.isnull().sum())




# --------------------------------------------------
# Merge Product Categories with English Translation
# --------------------------------------------------

products = products.merge(
    category,
    on="product_category_name",
    how="left"
)

print("\nProduct categories merged successfully!")

print(products[[
    "product_category_name",
    "product_category_name_english"
]].head())


# --------------------------------------------------
# Create New Features
# --------------------------------------------------

# Order Year
orders["order_year"] = orders["order_purchase_timestamp"].dt.year

# Order Month Number
orders["order_month"] = orders["order_purchase_timestamp"].dt.month

# Order Month Name
orders["order_month_name"] = orders["order_purchase_timestamp"].dt.month_name()

# Order Day Name
orders["order_day_name"] = orders["order_purchase_timestamp"].dt.day_name()

# Delivery Days
orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days

# Delivery Delay (True if delivered after estimated date)
orders["delivery_delay"] = (
    orders["order_delivered_customer_date"]
    > orders["order_estimated_delivery_date"]
)


print("\nNew Features Created:")
print(
    orders[[
        "order_purchase_timestamp",
        "order_year",
        "order_month",
        "order_month_name",
        "order_day_name",
        "delivery_days",
        "delivery_delay"
    ]].head()
)




# --------------------------------------------------
# Save Cleaned Datasets
# --------------------------------------------------

customers.to_csv("../cleaned_data/customers.csv", index=False)
orders.to_csv("../cleaned_data/orders.csv", index=False)
order_items.to_csv("../cleaned_data/order_items.csv", index=False)
payments.to_csv("../cleaned_data/payments.csv", index=False)
products.to_csv("../cleaned_data/products.csv", index=False)
reviews.to_csv("../cleaned_data/reviews.csv", index=False)
sellers.to_csv("../cleaned_data/sellers.csv", index=False)

print("\nCleaned datasets saved successfully!")