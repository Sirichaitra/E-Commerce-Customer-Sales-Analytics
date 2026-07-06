import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------------
# Plot Settings
# -------------------------------------------------
sns.set_theme(style="whitegrid")

# -------------------------------------------------
# Load Datasets
# -------------------------------------------------
customers = pd.read_csv("../cleaned_data/customers.csv")
orders = pd.read_csv("../cleaned_data/orders.csv")
payments = pd.read_csv("../cleaned_data/payments.csv")
products = pd.read_csv("../cleaned_data/products.csv")
order_items = pd.read_csv("../cleaned_data/order_items.csv")
reviews = pd.read_csv("../cleaned_data/reviews.csv")

print("Datasets Loaded Successfully")

# -------------------------------------------------
# Convert Date Columns
# -------------------------------------------------
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# =================================================
# 1. Monthly Orders
# =================================================

monthly_orders = (
    orders.groupby(["order_year", "order_month"])["order_id"]
    .count()
    .reset_index()
)

monthly_orders["Month"] = (
    monthly_orders["order_year"].astype(str)
    + "-"
    + monthly_orders["order_month"].astype(str).str.zfill(2)
)

plt.figure(figsize=(12,5))
plt.plot(
    monthly_orders["Month"],
    monthly_orders["order_id"],
    marker="o"
)

plt.xticks(rotation=45)
plt.title("Monthly Orders")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("../images/monthly_orders.png")
plt.show()

# =================================================
# 2. Monthly Revenue
# =================================================

revenue_df = orders.merge(payments, on="order_id")

monthly_revenue = (
    revenue_df.groupby(
        revenue_df["order_purchase_timestamp"].dt.to_period("M")
    )["payment_value"]
    .sum()
)

plt.figure(figsize=(12,5))
monthly_revenue.plot(marker="o")

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("../images/monthly_revenue.png")
plt.show()

# =================================================
# 3. Top 10 Product Categories
# =================================================

category_sales = (
    order_items.merge(products, on="product_id")
    .groupby("product_category_name_english")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))
category_sales.sort_values().plot(kind="barh")

plt.title("Top 10 Product Categories")
plt.xlabel("Revenue")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig("../images/top_categories.png")
plt.show()

# =================================================
# 4. Top 10 Sellers
# =================================================

seller_sales = (
    order_items.groupby("seller_id")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))
seller_sales.sort_values().plot(kind="barh")

plt.title("Top 10 Sellers")
plt.xlabel("Revenue")
plt.ylabel("Seller")
plt.tight_layout()
plt.savefig("../images/top_sellers.png")
plt.show()

# =================================================
# 5. Payment Method Distribution
# =================================================

plt.figure(figsize=(7,7))

payments["payment_type"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")
plt.title("Payment Method Distribution")
plt.tight_layout()
plt.savefig("../images/payment_methods.png")
plt.show()

# =================================================
# 6. Review Score Distribution
# =================================================

plt.figure(figsize=(8,5))

sns.countplot(
    data=reviews,
    x="review_score",
    order=[1,2,3,4,5]
)

plt.title("Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("../images/review_scores.png")
plt.show()

# =================================================
# 7. Top 10 States by Orders
# =================================================

state_orders = (
    customers.merge(orders, on="customer_id")
    .groupby("customer_state")["order_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,5))
state_orders.plot(kind="bar")

plt.title("Top States by Orders")
plt.xlabel("State")
plt.ylabel("Orders")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../images/top_states.png")
plt.show()

# =================================================
# 8. Order Status Distribution
# =================================================

plt.figure(figsize=(8,5))

sns.countplot(
    data=orders,
    x="order_status",
    order=orders["order_status"].value_counts().index
)

plt.xticks(rotation=45)

plt.title("Order Status Distribution")
plt.tight_layout()
plt.savefig("../images/order_status.png")
plt.show()

# =================================================
# 9. Payment Value Distribution
# =================================================

plt.figure(figsize=(10,5))

plt.hist(
    payments["payment_value"],
    bins=50
)

plt.title("Payment Value Distribution")
plt.xlabel("Payment Value")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("../images/payment_distribution.png")
plt.show()

# =================================================
# 10. Delivery Days Distribution
# =================================================

plt.figure(figsize=(10,5))

sns.histplot(
    orders["delivery_days"].dropna(),
    bins=30
)

plt.title("Delivery Days Distribution")
plt.xlabel("Delivery Days")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("../images/delivery_days.png")
plt.show()

print("\nEDA Completed Successfully!")
print("All charts are saved inside the images folder.")