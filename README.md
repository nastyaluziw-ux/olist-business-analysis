# Olist E-commerce Business Analysis

## Overview

This project analyzes the **Olist Brazilian E-commerce dataset** to evaluate business performance, customer behavior, revenue concentration, geographic differences, and delivery performance.

The goal was not only to calculate KPIs, but to investigate business questions, test hypotheses, and translate the results into actionable recommendations.


## Business Objectives

The analysis focuses on the following questions:


* How has revenue changed over time?
* Which Brazilian states generate the most revenue?
* How concentrated is revenue geographically?
* How does delivery performance vary across states?
* Is delivery performance associated with regional sales?
* How many customers purchase more than once?
* Are repeat customers more valuable?
* Which customer segments contribute the most revenue?
* How concentrated is revenue across the customer base?

---

# Dataset

The analysis uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains approximately:

* **99K orders**
* **96K unique customers**
* Order and delivery information
* Payment transactions
* Customer locations
* Product and seller information

Main tables used:

* `olist_orders_dataset`
* `olist_customers_dataset`
* `olist_order_payments_dataset`
* `olist_order_items_dataset`
* `olist_products_dataset`
* `olist_sellers_dataset`

Multiple tables were joined using `order_id` and `customer_id`.

For customer-level analysis, `customer_unique_id` was used to identify the same customer across multiple purchases and correctly calculate repeat purchasing behavior.

---

# Tools

### SQL — SQLite

Used for:

* KPI calculation
* JOINs
* Aggregations
* CTEs
* CASE WHEN
* Window functions
* `LAG()`
* Date calculations
* Regional analysis
* Repeat customer analysis

### Python

Libraries:

* pandas
* NumPy
* Matplotlib

Used for:

* Data inspection
* Data cleaning
* Missing-value analysis
* Datetime transformation
* Exploratory data analysis
* Dataset merging
* Revenue analysis
* Delivery analysis
* Customer-level aggregation
* Customer segmentation
* Pareto analysis
* Tableau dataset preparation

### Tableau

Used to create two interactive dashboards:

1. **Executive Business Dashboard**
2. **Customer Segmentation & Revenue Concentration Dashboard**

---

# Data Quality & Preparation

Before performing the analysis, the data was inspected for missing values, duplicates, inconsistent records, and data types.

Important missing values identified in the orders table included:

* `order_delivered_customer_date`: **2,965 missing**
* `order_delivered_carrier_date`: **1,783 missing**
* `order_approved_at`: **160 missing**

Most missing delivery dates were associated with canceled, unavailable, shipped, or still-processing orders rather than being random missing data.

Datetime columns were converted to proper datetime format, and new variables were created for:

* Purchase month
* Delivery duration
* Delivery performance
* Customer-level revenue
* Number of orders per customer
* Customer segment
* Customer type

Special attention was given to **data grain and JOIN duplication**.

For example, an order may have more than one payment record. Therefore, order-level metrics such as delivery time were calculated separately from payment-level aggregations to avoid duplicating orders.

---

# Business KPIs

The following KPIs were calculated using SQL:

* **Total Revenue:** approximately **BRL 16.0M**
* **Total Orders:** approximately **99K**
* **Active Customers:** **96,096**
**Average Order Value:** approximately **BRL 161**
* **Cancellation Rate:** approximately **0.63%**
* **Average Delivery Time:** approximately **12 days**

---

# Analysis & Findings

## 1. Revenue Trend

Monthly revenue increased substantially throughout 2017.

Revenue reached approximately:

**BRL 1.19M in November 2017**

and remained around **BRL 1M per month** during much of 2018.

However, the beginning and end of the dataset contain unusually low transaction volumes.

November 2016 is also missing from the monthly sequence.

Because of this, extreme Month-over-Month growth rates at the beginning and end of the dataset were not considered representative of normal business performance.

### Finding

Olist experienced strong revenue growth during the main observation period before reaching a relatively stable monthly revenue level.

---

## 2. Geographic Revenue Concentration

São Paulo is by far the largest market.

Top states by revenue include:

| State             |    Revenue |
| ----------------- |-----------:|
| São Paulo         | BRL 5.998M |
| Rio de Janeiro    | BRL 2.144M |
| Minas Gerais      | BRL 1.872M |
| Rio Grande do Sul | BRL 890.9K |
| Paraná            | BRL 811.2K |

São Paulo, Rio de Janeiro, and Minas Gerais together generate approximately **62.6% of total observed revenue**.

At first, this could suggest that these markets simply perform better.

However, additional analysis showed that these states also have much larger customer bases and order volumes.

For example:

| State          | Orders | Customers |
| -------------- | -----: | --------: |
| São Paulo      | 43,622 |    40,301 |
| Rio de Janeiro | 13,527 |    12,384 |
| Minas Gerais   | 12,102 |    11,259 |
| Roraima        |     46 |        45 |
| Amapá          |     70 |        67 |

### Insight

The regional revenue gap appears to be driven largely by market size and order volume, rather than customers in smaller states necessarily having lower economic value.

Some low-volume states actually show relatively high revenue per customer.

Therefore:

**Low total revenue does not automatically mean low customer value.**

---

# 3. Delivery Performance by State

Delivery performance varies considerably across Brazil.

Examples:

| State          | Average Delivery Time |
| -------------- | --------------------: |
| São Paulo      |         **8.77 days** |
| Minas Gerais   |        **12.00 days** |
| Rio de Janeiro |        **15.38 days** |
| Pará           |        **23.73 days** |
| Alagoas        |        **24.70 days** |
| Amazonas       |        **26.58 days** |
| Amapá          |        **27.10 days** |
| Roraima        |        **29.39 days** |

A clear regional logistics gap is visible.

Several lower-volume states experience delivery times above **20 days**, while São Paulo receives orders in fewer than **9 days on average**.

---

## Initial Hypothesis

The initial hypothesis was:

> Longer delivery times might be one reason why some states generate less revenue.

However, after adding order volume and customer count to the analysis, the relationship became more complex.

High-revenue states also have dramatically larger customer bases.

Therefore, the analysis cannot conclude that faster delivery directly causes higher revenue.

### Insight

Market size appears to explain much of the revenue difference.

However, delivery times approaching one month in some regions may still represent a **potential barrier to growth and customer experience**.

### Recommendation

Before investing heavily in logistics infrastructure, Olist should investigate:

* Seller-to-customer distance
* Freight costs
* Seller availability
* Regional demand
* Customer repeat behavior
* Potential market size

Pilot logistics improvements could be tested in markets where customer value is attractive but delivery performance is poor.

---

# 4. Customer Retention

Customers were classified as:

* **One-time customers**
* **Repeat customers**

Results:

| Customer Type     | Customers |      Share |
| ----------------- | --------: | ---------: |
| One-time Customer |    93,099 | **96.88%** |
| Repeat Customer   |     2,997 |  **3.12%** |

Only **3.12%** of customers purchased more than once during the observation period.

However, repeat customers were substantially more valuable.

### Average Revenue per Customer

* One-time customer: **BRL 161.82**
* Repeat customer: **BRL 314.99**

Repeat customers therefore generate approximately **1.95× more revenue per customer**.

Repeat customers represent only **3.12% of customers** but generate approximately **5.9% of total revenue**.

### Insight

The biggest difference is not simply how many customers Olist has.

It is that **customers who return are much more valuable than customers who purchase only once**.

### Business Opportunity

Increasing repeat purchasing among existing customers could represent an important growth opportunity.

However, the dataset covers a limited observation period, so the analysis alone is not sufficient to conclude that Olist has a structural retention problem.

A cohort analysis over a longer time horizon would be the next step.

---

# 5. Customer Segmentation

Customers were segmented into four groups according to observed customer revenue:

* High Value
* Medium-High
* Medium-Low
* Low Value

Quantile-based segmentation was used, meaning each segment contains approximately **25% of customers by design**.

Therefore, the equal customer distribution itself is **not a business insight**.

The important difference is how much revenue each group generates.

### Average Revenue per Customer

Approximately:

* **High Value:** BRL 397
* **Medium-High:** BRL 141
* **Medium-Low:** BRL 83
* **Low Value:** BRL 43

High Value customers generate approximately **60% of total revenue** despite representing approximately one quarter of the customer base.

### Insight

Customer value is unevenly distributed. The High Value segment, representing approximately 25% of customers by design, generates around 60% of total revenue.

---

# 6. Pareto Analysis

A Pareto analysis was performed to measure customer revenue concentration.

The analysis showed that approximately:

## **48.66% of customers generate 80% of total revenue



**

This confirms that customer value is significantly concentrated.

### Business Interpretation

Olist does not obtain the same economic value from every customer.

Understanding, retaining, and developing high-value customers could therefore have a disproportionately large impact on revenue.

---

# 7. Top Cities

Revenue is also highly concentrated geographically at city level.

Top cities included:

* São Paulo — approximately **BRL 2.20M**
* Rio de Janeiro — approximately **BRL 1.16M**
* Belo Horizonte — approximately **BRL 421.8K**
* Brasília — approximately **BRL 354.2K**
* Curitiba — approximately **BRL 247.4K**

This reinforces the geographic concentration identified at state level.

---

# Main Business Insights

The project produced four main business insights.

### 1. Customer retention represents a potential growth opportunity

Only **3.12%** of customers purchased more than once, but repeat customers generated almost **2× more revenue per customer**.

This suggests that increasing repeat purchasing could create meaningful incremental revenue.

---

### 2. Revenue is highly concentrated among valuable customers

Approximately:

Revenue is unevenly distributed across customers, although the concentration is less extreme than a traditional 80/20 Pareto pattern. 
Approximately 48.66% of customers generate 80% of total revenue.

---

### 3. Regional revenue differences are mainly driven by market size

São Paulo, Rio de Janeiro, and Minas Gerais account for approximately **62.6% of total revenue**, but they also contain far more customers and orders.

Therefore, total revenue alone should not be used to compare regional customer quality.

Metrics such as:

* Revenue per customer
* Orders per customer
* Repeat purchase rate

provide more useful context.

---

### 4. Logistics performance shows a significant regional gap

Delivery ranges from fewer than **9 days in São Paulo** to almost **30 days in Roraima**.

The analysis does not prove that slower delivery causes lower demand.

However, such large differences represent an operational issue worth investigating, especially in markets where customer value remains attractive.

---

# Business Recommendations

Based on the analysis:

### Improve Repeat Purchasing

Investigate strategies that encourage existing customers to purchase again, particularly because repeat customers generate nearly twice the revenue per customer.

Possible strategies could include:

* Personalized offers
* Post-purchase campaigns
* Loyalty incentives
* Product recommendations

---

### Protect High-Value Customers

High-value customers contribute disproportionately to revenue.

Customer experience, service quality, and retention efforts should prioritize these customers.

---

### Investigate Regional Logistics Opportunities

Long delivery times in some states should be investigated before making major infrastructure investments.

The next analysis should incorporate:

* Seller location
* Freight cost
* Customer distance
* Regional demand
* Repeat purchasing

---

### Avoid Using Revenue Alone for Geographic Decisions

Regional revenue should always be considered together with:

* Customer volume
* Order volume
* Revenue per customer
* Market size

Large markets naturally generate more total revenue.

---

# Tableau Dashboards

## Executive Business Dashboard

The first dashboard presents overall business performance and operational KPIs.

It includes:

* Revenue
* Orders
* Customers
* Average Order Value
* Cancellation Rate
* Delivery performance
* Geographic analysis
* Revenue trends
<img width="2046" height="1734" alt="Customer Segmentation   Revenue Concentration (1)" src="https://github.com/user-attachments/assets/263cfcde-b8a9-4898-a6ef-a736a20594c9" />


**View on Tableau Public:**
https://public.tableau.com/views/E-commerceSalesOverviewBrazilianE-commerceDatasetOlist20162018/E-commerceSalesOverview?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link  

---

## Customer Segmentation & Revenue Concentration

The second dashboard focuses on customer value and revenue concentration.

It includes:

* Customer segments
* Revenue contribution by segment  
* Average revenue per customer
* Pareto analysis
* Business insights


**View on Tableau Public:**
https://public.tableau.com/views/CustomersegmentationRevenueconcentrationBrazilianE-commerceDatasetOlist20162018/CustomerSegmentationRevenueConcentration?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

---

# Project Structure


```text
olist-business-analysis/
│
├── README.md
│
├── python/
│   └── analysis.py
│
├── notebooks/
│   └── olist_analysis.ipynb
│
├── sql/
│   ├── kpis.sql
│   └── business_questions.sql
│
├── data/
│   └── brazil_states.csv
│
└── images/
    ├── e_commerce_sales_overview.png
    └── customer_segmentation_revenue_concentration.png


# Limitations

Several limitations should be considered when interpreting the results:

* The dataset covers a limited observation period.
* Early and final months contain unusually low transaction volumes.
* November 2016 is absent from the monthly revenue sequence.
* Customer repeat behavior may be underestimated because customers do not have unlimited time to make another purchase.
* Geographic revenue is influenced by market size.
* Correlation between delivery performance and revenue does not imply causation.
* External factors such as population, income, competition, and infrastructure were not included.
* Quantile customer segments were created for descriptive analysis and do not represent predictive Customer Lifetime Value.

---

# Next Steps

Further analysis could include:

* Customer cohort retention
* Seller-to-customer distance
* Freight cost analysis
* Product category profitability
* Delivery delay versus estimated delivery date
* Regional normalization using population or market size

* Predictive customer value modeling

---

# Skills Demonstrated

**SQL**

JOIN · GROUP BY · CTE · CASE WHEN · COUNT DISTINCT · Window Functions · LAG · Date Functions

**Python**

pandas · NumPy · Data Cleaning · EDA · Aggregation · Merge · Customer Segmentation · Pareto Analysis

**Business Analytics**

KPI Design · Customer Retention · Revenue Analysis · Geographic Analysis · Hypothesis Testing · Business Recommendations

**Visualization**

Tableau · Dashboard Design · Data Storytelling
