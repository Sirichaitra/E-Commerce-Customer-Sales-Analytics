SELECT COUNT(*) AS total_customers
FROM customers;

SELECT COUNT(*) AS total_orders
FROM orders;

SELECT COUNT(*) AS total_products
FROM products;

SELECT COUNT(*) AS total_sellers
FROM sellers;

SELECT
ROUND(SUM(payment_value),2) AS total_revenue
FROM payments;

SELECT
ROUND(AVG(payment_value),2) AS average_order_value
FROM payments;

SELECT
ROUND(AVG(review_score),2) AS average_review_score
FROM reviews;

SELECT COUNT(*) AS delivered_orders
FROM orders
WHERE order_status='delivered';

SELECT
ROUND(
SUM(order_status='delivered')*100/COUNT(*),
2
) AS delivery_success_rate
FROM orders;

SELECT COUNT(*) AS late_deliveries
FROM orders
WHERE delivery_delay=1;

-- =====================================================
-- MODULE 2 : SALES ANALYSIS
-- =====================================================

-- 11. Monthly Revenue
SELECT
    o.order_year,
    o.order_month_name,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM orders o
JOIN payments p
ON o.order_id = p.order_id
GROUP BY o.order_year, o.order_month, o.order_month_name
ORDER BY o.order_year, o.order_month;


-- 12. Monthly Orders
SELECT
    order_year,
    order_month_name,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_year, order_month, order_month_name
ORDER BY order_year, order_month;


-- 13. Top 10 States by Revenue
SELECT
    c.customer_state,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN payments p
ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY revenue DESC
LIMIT 10;


-- 14. Top 10 Cities by Orders
SELECT
    c.customer_city,
    COUNT(*) AS total_orders
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_city
ORDER BY total_orders DESC
LIMIT 10;


-- 15. Top 10 Product Categories by Revenue
SELECT
    p.product_category_name_english,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_category_name_english
ORDER BY revenue DESC
LIMIT 10;


-- 16. Top 10 Sellers by Revenue
SELECT
    seller_id,
    ROUND(SUM(price), 2) AS revenue
FROM order_items
GROUP BY seller_id
ORDER BY revenue DESC
LIMIT 10;


-- 17. Payment Method Distribution
SELECT
    payment_type,
    COUNT(*) AS total_transactions
FROM payments
GROUP BY payment_type
ORDER BY total_transactions DESC;


-- 18. Review Score Distribution
SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM reviews
GROUP BY review_score
ORDER BY review_score;


-- 19. Average Delivery Time
SELECT
    ROUND(AVG(delivery_days), 2) AS average_delivery_days
FROM orders;


-- 20. Orders by Status
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;