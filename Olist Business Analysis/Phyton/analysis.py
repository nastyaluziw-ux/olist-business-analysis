# ============================================
# OLIST BUSINESS ANALYSIS
# ============================================

# Libraries

import pandas as pd
import matplotlib.pyplot as plt
import os
import kagglehub
import numpy as np



# ============================================
# LOAD DATA
# ============================================
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

# Load required datasets
customers = pd.read_csv(
    os.path.join(path, "olist_customers_dataset.csv")
)

orders = pd.read_csv(
    os.path.join(path, "olist_orders_dataset.csv")
)

payments = pd.read_csv(
    os.path.join(path, "olist_order_payments_dataset.csv")
)

print("Datasets loaded successfully")
# Check dataset dimensions

datasets = {
    "Customers": customers,
    "Orders": orders,
    "Payments": payments
}

for name, df in datasets.items():
    print(f"\n{name}")
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")

print("Path to dataset files:", path)
print(os.listdir(path))
orders = pd.read_csv(os.path.join(path, "olist_orders_dataset.csv"))
# ============================================
# DATA CLEANING
# ============================================
print(orders.head())
print(orders.info())
# Convert datatime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

print(orders[date_columns].dtypes)
# Duplicates

duplicate_rows = pd.DataFrame({
    "dataset": ["customers", "orders", "payments"],
    "duplicate_rows": [
        customers.duplicated().sum(),
        orders.duplicated().sum(),
        payments.duplicated().sum()
    ]
})


print(duplicate_rows)

key_validation = pd.DataFrame({
    "validation": [
        "Duplicated customer_id in customers",
        "Duplicated order_id in orders",
        "Duplicated payment identifier"
    ],
    "duplicates": [
        customers["customer_id"].duplicated().sum(),
        orders["order_id"].duplicated().sum(),
        payments.duplicated(
            subset=["order_id", "payment_sequential"]
        ).sum()
    ]
})

print(key_validation)



def missing_values_summary(dataframe):
    summary = (
        dataframe
        .isna()
        .sum()
        .rename("missing_values")
        .reset_index()
        .rename(columns={"index": "column"})
    )

    summary["missing_percentage"] = (
        summary["missing_values"]
        .div(len(dataframe))
        .mul(100)
        .round(2)
    )

    return (
        summary[
            summary["missing_values"] > 0
        ]
        .sort_values(
            "missing_percentage",
            ascending=False
        )
        .reset_index(drop=True)
    )
from IPython.display import display
print("Missing values — Customers")
display(missing_values_summary(customers))

print("Missing values — Orders")
display(missing_values_summary(orders))

print("Missing values — Payments")
display(missing_values_summary(payments))

#### Initial Missing Values Findings

# Missing values were identified only in three order timestamp columns:

# order_delivered_customer_date`: 2.98%
# order_delivered_carrier_date`: 1.79%
# order_approved_at`: 0.16%

#The missing values were not removed automatically. Their relationship with `order_status` was examined to determine whether they represent incomplete order lifecycle stages or potential data quality issues.

orders_missing_analysis = orders.assign(
    missing_approved_date=orders["order_approved_at"].isna(),
    missing_carrier_date=orders["order_delivered_carrier_date"].isna(),
    missing_customer_date=orders["order_delivered_customer_date"].isna()
)

missing_by_status = (
    orders_missing_analysis
    .groupby("order_status", as_index=False)
    .agg(
        total_orders=("order_id", "size"),
        missing_approved_date=("missing_approved_date", "sum"),
        missing_carrier_date=("missing_carrier_date", "sum"),
        missing_customer_date=("missing_customer_date", "sum")
    )
    .sort_values("total_orders", ascending=False)
)


missing_by_status["missing_approved_percentage"] = (
    missing_by_status["missing_approved_date"]
    .div(missing_by_status["total_orders"])
    .mul(100)
    .round(2)
)

missing_by_status["missing_carrier_percentage"] = (
    missing_by_status["missing_carrier_date"]
    .div(missing_by_status["total_orders"])
    .mul(100)
    .round(2)
)

missing_by_status["missing_customer_percentage"] = (
    missing_by_status["missing_customer_date"]
    .div(missing_by_status["total_orders"])
    .mul(100)
    .round(2)
)

print(missing_by_status)

### Findings
#- Three columns contain missing values.
#- The highest percentage of missing values is found in `order_delivered_customer_date` (2.98%).
#- These missing values are expected because canceled, unavailable, or in-progress orders have not been delivered yet.
#-Most missing values are related to orders that did not complete the delivery process.
#- The percentage of missing data is low, so it is unlikely to have a significant impact on the analysis.
# New column "delays_days"



# ============================================
# BUSINESS ANALYSIS
# ============================================
# EDA 1 Status of orders
orders["delivery_time"] = (
    orders["order_delivered_customer_date"]
    -
    orders["order_purchase_timestamp"]
).dt.days

orders["delays_days"] = (
    orders["order_delivered_customer_date"]
    -
    orders["order_estimated_delivery_date"]
).dt.days
orders[
    [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "delivery_time",
        "delays_days",
    ]
].head()
print(orders)

status_summary= (orders["order_status"]
    .value_counts().rename("total_orders")
    .to_frame()
    .reset_index())

total = status_summary["total_orders"].sum()
status_summary["percentage"] = (status_summary["total_orders"] / total) * 100
status_summary["percentage"] = status_summary["percentage"].round(2)





revenue_payment = (
    payments
    .groupby("payment_type")
    .agg(
    total_revenue = ("payment_value", "sum")

    )
    .reset_index()
)
revenue_payment.sort_values(ascending=False, by="total_revenue", inplace=True)
print(revenue_payment)


##  Monthly Revenue Analysis. This analysis examines monthly revenue and order volume over time to identify seasonal patterns and changes in sales performance. Revenue was calculated using the aggregated payments table to avoid double-counting payment values after merging.
orders["month"] = orders["order_purchase_timestamp"].dt.to_period("M")
payments_summary = (
    payments
    .groupby("order_id")
    .agg(
        total_payment=("payment_value","sum"),
        payment_installments=("payment_installments","max"),
        payment_type=("payment_type","first")
    )
    .reset_index()
)
orders_payments = orders.merge(
    payments_summary,
    on="order_id",
    how="left"
)
orders_payments["month"] = (
    orders_payments["order_purchase_timestamp"]
    .dt.to_period("M")
)


monthly_sales = (
    orders_payments
    .groupby("month")
    .agg(
        total_revenue=("total_payment","sum"),
        number_of_orders=("order_id","count")
    )
    .reset_index()
)
monthly_sales = monthly_sales.sort_values("month")
print(monthly_sales)
# Findings
# 97.02% of all orders were successfully delivered.
# Only 0.63% of orders were canceled, indicating a very low cancellation rate.
# Less than 2% of orders were still in progress (shipped, processing, invoiced, etc.), suggesting that most orders are completed successfully.

# EDA 2 Type of payments
payments = pd.read_csv(os.path.join(path, "olist_order_payments_dataset.csv"))
revenue_payment = (
    payments
    .groupby("payment_type")
    .agg(
    total_revenue = ("payment_value", "sum")

    )
    .reset_index()
)
revenue_payment.sort_values(ascending=False, by="total_revenue", inplace=True)
print(revenue_payment)
#Credit cards generated the highest revenue.
# Boleto was the second most popular payment method.
# Debit cards and vouchers contributed only a small share of total revenue.
# The company should ensure a smooth credit card payment experience because it is the main revenue driver.


# Revenue by state
states = pd.read_csv(
    "../data/brazil_states.csv"
)

orders_customers_payments = orders_payments.merge(
    customers,
    on="customer_id",
    how="left"
)

orders_customers_states = orders_customers_payments.merge(
    states,
    left_on="customer_state",
    right_on="state_code",
    how="left"
)


revenue_by_state = (
    orders_customers_states
    .groupby("state_name")
    .agg(
        revenue=("total_payment","sum"),
        number_of_orders=("order_id","count")
    )
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
)

print(revenue_by_state)
# São Paulo generated the highest revenue, which is expected because it is the most populous and economically active state in Brazil.


# Revenue share (%)
#%%
revenue_by_state["revenue_share"] = (
    revenue_by_state["revenue"] /
    revenue_by_state["revenue"].sum()
    * 100
).round(2)

revenue_by_state["rank"] = range(1, len(revenue_by_state) + 1)

print(revenue_by_state)

#EDA 5 - Top 10 Cities by Revenue
orders_customers_payments["customer_city"]= orders_customers_payments["customer_city"].str.capitalize()
print(orders_customers_payments)

top_cities_revenue = (
    orders_customers_payments
    .groupby("customer_city")
    .agg(
        total_revenue=("total_payment", "sum"),
        number_of_orders=("order_id", "nunique")
    )
    .reset_index()
)
print(top_cities_revenue.sort_values(by="total_revenue", ascending=False).head(10))
print(top_cities_revenue.head(10))

top_cities_revenue["average_order_value"] = (
    top_cities_revenue["total_revenue"] /
    top_cities_revenue["number_of_orders"]
).round(2)
print(top_cities_revenue)

top_10_cities = (
    top_cities_revenue
    .sort_values("total_revenue", ascending=False)
    .head(10)
)

top_10_cities.plot(
    x="customer_city",
    y="total_revenue",
    kind="barh",
    figsize=(10, 6)
)


# São Paulo generated the highest revenue with 2,203,373.09 BRL, making it the company's most important market.
# Rio de Janeiro ranked second with 1,161,927.36 BRL, although its revenue is almost half that of São Paulo.
# Belo Horizonte, Brasília, and Curitiba complete the Top 5 cities by revenue.
# Revenue is concentrated in a small number of large Brazilian cities, suggesting that major urban areas drive most of the company's sales.

# EDA 6  Pareto Analysis
# # Calculate the total revenue generated by each customer during their lifetime
# # Customers are ranked from highest to lowest revenue to identify the most valuable customers
#
# # Calculate cumulative revenue to understand how much total revenue is generated
# # as we move through customers ranked by their spending
#
# # Calculate the percentage of total revenue accumulated by customers
# # This helps identify the concentration of revenue and perform a Pareto analysis
total_lifetime_revenue = (
    orders_customers_payments
    .groupby("customer_unique_id")
    .agg(
        total_revenue=("total_payment", "sum")
    )
    .reset_index()
    .sort_values("total_revenue", ascending=False)
    .reset_index(drop=True)
)

total_lifetime_revenue["cumulative_revenue"] = (
    total_lifetime_revenue["total_revenue"]
    .cumsum()
)

total_lifetime_revenue["cumulative_percentage"] = (
    total_lifetime_revenue["cumulative_revenue"]
    / total_lifetime_revenue["total_revenue"].sum()
    * 100
)
total_lifetime_revenue["rank"] = (
    total_lifetime_revenue.index + 1
)
print(total_lifetime_revenue.head(10))
pareto_80 = total_lifetime_revenue[
    total_lifetime_revenue["cumulative_percentage"] >= 80
].iloc[0]

customer_percentage_80 = (
    pareto_80["rank"]
    / len(total_lifetime_revenue)
    * 100
)

print(
    f"{customer_percentage_80:.2f}% of customers generate 80% of total revenue."
)




# The top customers were ranked according to their lifetime revenue.
# 46,766 customers account for 80% of total revenue.
# These customers represent approximately 48.6% of the customer base.
#  Identify the number of customers responsible for 80% of total revenue
# #This helps evaluate whether revenue is concentrated among a small group of customers

#  Customer segment
customer_segments = total_lifetime_revenue.copy()

customer_segments["segment"] = pd.qcut(
    customer_segments["total_revenue"],
    q=4,
    labels=[
        "Low Value",
        "Medium-Low Value",
        "Medium-High Value",
        "High Value"
    ])
customer_segments["segment"].value_counts()
print(customer_segments)

segment_analysis = (
    customer_segments
    .groupby("segment",observed=True, as_index=False)
    .agg(
        customers=("customer_unique_id","count"),
        revenue=("total_revenue","sum")
    )

)

print(segment_analysis)

segment_analysis["revenue_percentage"] = (
    segment_analysis["revenue"] /
    segment_analysis["revenue"].sum()
    * 100
).round(2)


segment_analysis["average_customer_value"] = (
    segment_analysis["revenue"] /
    segment_analysis["customers"]
).round(2)

print(segment_analysis)

# customer type
customer_summary = (
    orders_customers_payments
    .groupby("customer_unique_id")
    .agg(
        total_revenue=("total_payment", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

customer_summary["average_order_value"] = (
    customer_summary["total_revenue"]
    / customer_summary["total_orders"]
)

customer_summary["customer_type"] = np.where(
    customer_summary["total_orders"] > 1,
    "Repeat Customer",
    "One-time Customer"
)
customer_summary_type=(
    customer_summary
    .groupby("customer_type")
    .agg(
        total_revenue=("total_revenue", "sum"),
        avg_revenue=("total_revenue", "mean"),
        customers = ("customer_unique_id", "count")
    )
    .reset_index()
    )

print(customer_summary_type)


customer_summary_type["customer_percentage"] = (
    customer_summary_type["customers"]
    / customer_summary_type["customers"].sum()
    * 100
)

customer_summary_type["customer_revenue_percentage"] = (
     customer_summary_type["total_revenue"]
     / customer_summary_type["total_revenue"].sum()
     *100
).round(2)
print(customer_summary_type)




# ============================================

# VISUALIZATIONS
# ============================================
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))

customer_percentage = (
    np.arange(len(total_lifetime_revenue))
    /
    len(total_lifetime_revenue)
    * 100
)

plt.plot(
    customer_percentage,
    total_lifetime_revenue["cumulative_percentage"]
)

plt.axhline(
    80,
    linestyle="--"
)

plt.xlabel("Customers (%)")
plt.ylabel("Cumulative Revenue (%)")
plt.title("Customer Revenue Concentration")

plt.show()

output_folder = os.path.join(
    os.path.dirname(__file__),
    "../data/processed"
)

os.makedirs(output_folder, exist_ok=True)

customer_summary.to_csv(
    os.path.join(output_folder, "customer_summary.csv"),
    index=False
)

orders_customers_payments.to_csv(
    os.path.join(output_folder, "fact_orders.csv"),
    index=False
)
