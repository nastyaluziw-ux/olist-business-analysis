-- =====================================
-- BUSINESS KPIs
-- =====================================
-- 1 KPI
-- Total Revenue
SELECT
	sum(payment_value) as total_revenue
From olist_order_payments_dataset;

-- 2 KPI
-- Active Customers
SELECT
    count(DISTINCT customer_unique_id) as active_customer
From olist_customer_dataset_;

-- KPI 3
-- Total Orders
SELECT
    Count(Distinct order_id) as total_orders
From olist_orders_dataset;

-- KPI 4
-- Average Order Value
SELECT
    ROUND(
        SUM(payment_value) /
        COUNT(DISTINCT order_id),
        2
    ) AS aov
FROM olist_order_payments_dataset;

-- KPI 5
-- Average Revenue by State
 SELECT
     customer_state,
	 ROUND(AVG(payment_value), 2) as  avg_revenue
From olist_customers_dataset as c
JOIN olist_orders_dataset as o
ON  c.customer_id = o.customer_id
JOIN olist_order_payments_dataset as p
ON o.order_id = p. order_id
Group by customer_state
Order by avg_revenue DESC;

-- KPI 6
-- Cancellation Rate
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(
        CASE
            WHEN order_status = 'canceled' THEN 1
            ELSE 0
        END
    ) AS canceled_orders,

    ROUND(
        SUM(
            CASE
                WHEN order_status = 'canceled' THEN 1
                ELSE 0
            END
        ) * 100.0
        / COUNT(DISTINCT order_id),
        2
    ) AS cancellation_rate
FROM olist_orders_dataset;

