-- OLIST BUSINESS QUESTIONS

-- 1. How has monthly revenue changed over time?
-- Skills: CTE, GROUP BY, strftime(), LAG(), window functions
WITH monthly_revenue  as  (

SELECT
   strftime('%Y-%m', o.order_purchase_timestamp) as month,
   sum(p.payment_value) as revenue
from olist_orders_dataset as o
join olist_order_payments_dataset as p
 on  o.order_id= p.order_id
 GROUP by month

),

revenue_with_lag AS  (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS previous_month_revenue
    FROM monthly_revenue
)

SELECT
     month,
	 revenue,
	 previous_month_revenue,
	 round((revenue- previous_month_revenue) / previous_month_revenue * 100.0, 2) as mom_growth_percentage
from revenue_with_lag
order by month;

--The first months of the dataset contain very low and irregular transaction volumes,
--including a missing month (November 2016). Therefore, early MoM growth rates were not considered representative of the underlying business trend.

-- 2. Which states generate the most revenue?
-- Skills: JOIN, GROUP BY, SUM(), ORDER BY
SELECT
     c.customer_state,
	 sum(p.payment_value) as total_revenue
from olist_customers_dataset as c
join olist_orders_dataset as o
on c.customer_id= o.customer_id
join olist_order_payments_dataset as p
on o.order_id= p.order_id
group by customer_state
order by total_revenue DESC;

---Revenue is geographically concentrated,
--with São Paulo, Rio de Janeiro and Minas Gerais representing the strongest markets. This concentration suggests that Olist is highly dependent on a relatively small number of states for a large share of its revenue.


-- 3. How does delivery performance vary by state?
-- Skills: JOIN, AVG(), julianday(), filtering
with customer_analysis as (
SELECT
           c.customer_state,
		   count(o.order_id) as total_orders,
		   count(DISTINCT(c.customer_unique_id)) as total_customers,
		   sum(p.payment_value) as total_revenue,
		   round(avg(julianday(o.order_delivered_customer_date)- julianday(o.order_purchase_timestamp) ) , 2) AS avg_delivery_days
from olist_orders_dataset as o
join olist_order_payments_dataset as p
on o.order_id=p.order_id
join olist_customers_dataset as c
on o.customer_id= c.customer_id
group by c.customer_state
order by  avg_delivery_days DESC

 )
 SELECT
            customer_state,
			total_orders,
			total_customers,
			total_revenue,
			avg_delivery_days,
            round(total_revenue / total_customers , 2) as revenue_per_customers,
            round(total_orders *1.0/ total_customers as orders_por_customers
 from customer_analysis
 group by customer_state
 order by  avg_delivery_days DESC;

--BUSINESS INSIGHT:
--Regional revenue differences appear to be driven largely by market size
--and order volume rather than low customer value.

--Long delivery times may still represent a potential barrier to growth
--in underserved states, but the current analysis does not prove that
--delivery time causes lower demand.

--RECOMMENDATION:
--Investigate whether logistics improvements in states with high customer
--value but poor delivery performance could be economically viable.


-- 4. What percentage of customers purchase more than once?
-- Skills: CTE, COUNT DISTINCT, CASE WHEN

WITH customer_orders AS (
    SELECT
	           c.customer_unique_id as customers,
			   count(distinct(o.order_id)) as total_orders
    FROM  olist_customers_dataset as c
    JOIN olist_orders_dataset as o
        ON c.customer_id= o.customer_id
    GROUP BY c.customer_unique_id

),
customer_type as (
SELECT
    customers,
	total_orders,
	CASE
        WHEN total_orders > 1 THEN 'Repeat Customer'
        ELSE 'One-time Customer'
    END as customer_type
from customer_orders
)

SELECT
    customer_type,
    COUNT(*) AS customers,
    ROUND( COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
    2
    ) AS customer_percentage
FROM customer_type
GROUP BY customer_type;

--FINDING:
--Only 3.12% of customers made more than one purchase, while 96.88%
--were one-time customers.

--BUSINESS INSIGHT:
--Repeat customers represent a very small share of the customer base.
--Previous customer analysis showed that repeat customers are more valuable
--on average, suggesting that increasing repeat purchases could be a growth
--opportunity.

--LIMITATION:
--The dataset covers a limited observation period, so this result alone
--is not sufficient to conclude that Olist has a customer retention problem.
