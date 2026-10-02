USE `retail_events_db`;


/*
Q1. Basic Filtering – High-Value Products
Find all event records where the base_price is greater than 1,000.

Display:
- event_id
- store_id
- product_code
- base_price
- promo_type

Concepts:
SELECT, WHERE, comparison operators.
*/

SELECT f.event_id, f.store_id, f.product_code,f.base_price, f.promo_type FROM fact_events f
WHERE f.base_price>1000;

/*
Q2. Sorting Promotional Events
Display all events where quantity sold after the promotion was greater than 100.

Display:
- event_id
- product_code
- promo_type
- quantity_sold(before_promo)
- quantity_sold(after_promo)

Sort by quantity_sold(after_promo) in descending order.

Concepts:
WHERE, ORDER BY, DESC.
*/

SELECT f.event_id, f.product_code,f.promo_type,f.`quantity_sold(before_promo)`,f.`quantity_sold(after_promo)` FROM fact_events f
WHERE f.`quantity_sold(after_promo)`>100
ORDER BY f.`quantity_sold(after_promo)` DESC;

/*
Q3. DISTINCT Promotion Types
Find all unique promotion types used in the dataset.

Display only the unique promo_type values.

Concepts:
DISTINCT.
*/
SELECT DISTINCT promo_type from fact_events;

/*
Q4. Basic Aggregation
Calculate the following for the complete fact_events table:

- Total number of events
- Total quantity sold before promotion
- Total quantity sold after promotion
- Average base price
- Maximum base price
- Minimum base price

Return all metrics in one row.

Concepts:
COUNT, SUM, AVG, MAX, MIN.
*/

SELECT COUNT(f.event_id),
SUM(f.`quantity_sold(before_promo)`),
SUM(f.`quantity_sold(after_promo)`),
AVG(f.base_price),
MAX(f.base_price),
MIN(f.base_price)
FROM fact_events f;

/*
Q5. Sales Volume by Promotion Type
For each promo_type, calculate:

- Number of events
- Total quantity sold before promotion
- Total quantity sold after promotion

Sort by total quantity sold after promotion in descending order.

Concepts:
GROUP BY, COUNT, SUM, ORDER BY.
*/

SELECT f.promo_type, COUNT(f.event_id), SUM(f.`quantity_sold(before_promo)`), SUM(f.`quantity_sold(after_promo)`) from fact_events f
GROUP BY f.promo_type
ORDER BY SUM(f.`quantity_sold(after_promo)`) DESC;

/*
Q6. Promotion Uplift
For every promotion type, calculate:

- Total quantity before promotion
- Total quantity after promotion
- Quantity increase/decrease

Use:

Quantity Change = After Promo Quantity - Before Promo Quantity

Display:
- promo_type
- total_before
- total_after
- quantity_change

Sort by quantity_change descending.

Concepts:
GROUP BY, SUM, arithmetic calculations, aliases.
*/

SELECT f.promo_type, SUM(f.`quantity_sold(before_promo)`) as total_before,
SUM(f.`quantity_sold(after_promo)`) as total_after,
SUM(f.`quantity_sold(after_promo)`) - SUM(f.`quantity_sold(before_promo)`) as quantity_change
FROM fact_events f
GROUP BY f.promo_type
ORDER BY quantity_change DESC;


/*
Q7. Product Performance
Using fact_events and dim_products, calculate total quantity sold after promotion for every product.

Display:
- product_code
- product_name
- category
- total quantity after promotion

Sort by total quantity after promotion descending.

Concepts:
INNER JOIN, GROUP BY, SUM, ORDER BY.
*/

SELECT p.product_code, p.product_name, p.category,
SUM(f.`quantity_sold(after_promo)`) as `total quantity after promotion`
FROM fact_events f
INNER JOIN dim_products p 
ON f.product_code = p.product_code
GROUP BY p.product_code, p.product_name, p.category
ORDER BY `total quantity after promotion` DESC;


/*
Q8. Category-Level Performance
Using fact_events and dim_products, calculate for every product category:

- Number of events
- Total quantity before promotion
- Total quantity after promotion
- Quantity change

Sort categories by total quantity after promotion descending.

Concepts:
JOIN, GROUP BY, SUM, COUNT, arithmetic calculations.
*/

SELECT p.category, COUNT(f.event_id) as `Number of events`,
SUM(f.`quantity_sold(before_promo)`) as `Total quantity before promotion`,
SUM(f.`quantity_sold(after_promo)`) as `Total quantity after promotion`,
SUM(f.`quantity_sold(after_promo)`) - SUM(f.`quantity_sold(before_promo)`) as `Quantity change`
FROM fact_events f
INNER JOIN dim_products p
ON f.product_code = p.product_code
GROUP BY p.category
ORDER BY `Total quantity after promotion` DESC;


/*
Q9. Store Performance
Using fact_events and dim_stores, calculate for every city:

- Number of promotional events
- Total quantity before promotion
- Total quantity after promotion

Display:
- city
- event_count
- total_before
- total_after

Sort cities by total_after descending.

Concepts:
JOIN, GROUP BY, aggregation, ORDER BY.
*/
SELECT ds.city, COUNT(f.event_id) as event_count,
SUM(f.`quantity_sold(before_promo)`) as total_before,
SUM(f.`quantity_sold(after_promo)`) as total_after
FROM fact_events f
INNER JOIN dim_stores ds
ON f.store_id = ds.store_id
GROUP BY ds.city
ORDER BY total_after DESC;


/*
Q10. Campaign Performance
Using fact_events and dim_campaigns, calculate for each campaign:

- Campaign name
- Start date
- End date
- Number of events
- Total quantity before promotion
- Total quantity after promotion

Sort by total quantity after promotion descending.

Concepts:
JOIN, GROUP BY, date columns, aggregation.
*/

SELECT dc.campaign_name as `Campaign name`,
dc.start_date as `Start date`, dc.end_date as `End date`,
COUNT(fe.event_id) as `Number of events`,
SUM(fe.`quantity_sold(before_promo)`) as `Total quantity before promotion`,
SUM(fe.`quantity_sold(after_promo)`) as `Total quantity after promotion`
FROM dim_campaigns dc
INNER JOIN fact_events fe
ON dc.campaign_id = fe.campaign_id
GROUP BY dc.campaign_name, dc.start_date, dc.end_date
ORDER BY `Total quantity after promotion` DESC;


/*
Q11. Product Category with HAVING
Find product categories where the total quantity sold after promotion is greater than 1,000.

Display:
- category
- total quantity after promotion
- average base price

Sort by total quantity after promotion descending.

Concepts:
JOIN, GROUP BY, HAVING, AVG, SUM.
*/

SELECT dp.category,
SUM(fe.`quantity_sold(after_promo)`) as `total quantity after promotion`,
AVG(fe.base_price) as `average base price`
FROM dim_products dp
INNER JOIN fact_events fe
ON dp.product_code = fe.product_code
GROUP BY dp.category
HAVING `total quantity after promotion` > 1000
ORDER BY `total quantity after promotion` DESC;



/*
Q12. Store + Category Analysis
Using fact_events, dim_stores and dim_products, calculate total quantity sold after promotion for every combination of:

- City
- Product category

Display:
- city
- category
- total quantity after promotion

Sort first by city and then by total quantity descending.

Concepts:
Multiple JOINs, GROUP BY, ORDER BY.
*/

SELECT ds.city,dp.category,
SUM(fe.`quantity_sold(after_promo)`) as `total quantity after promotion`
FROM
dim_stores ds
INNER JOIN  fact_events fe
ON ds.store_id = fe.store_id
INNER JOIN dim_products dp
ON fe.product_code = dp.product_code
GROUP BY ds.city,dp.category
ORDER BY ds.city, `total quantity after promotion` DESC;


/*
Q13. Promotion Effectiveness by Product
For each product, calculate:

- Product name
- Category
- Total quantity before promotion
- Total quantity after promotion
- Quantity change
- Percentage change

Use:

Percentage Change =
((After Promo - Before Promo) / Before Promo) * 100

Handle division by zero appropriately.

Sort by percentage change descending.

Concepts:
JOIN, GROUP BY, arithmetic calculations, NULLIF, percentage calculations.
*/

SELECT dp.product_name,dp.category,
SUM(fe.`quantity_sold(before_promo)`) as `total quantity before promotion`,
SUM(fe.`quantity_sold(after_promo)`) as `total quantity after promotion`,
SUM(fe.`quantity_sold(after_promo)`) - SUM(fe.`quantity_sold(before_promo)`) as `quantity change`,
(SUM(fe.`quantity_sold(after_promo)`) - SUM(fe.`quantity_sold(before_promo)`))/ NULLIF(SUM(fe.`quantity_sold(before_promo)`),0)*100 as `Percentage change`
FROM dim_products dp
INNER JOIN fact_events fe
ON fe.product_code = dp.product_code
GROUP BY dp.product_name,dp.category
ORDER BY `Percentage change` DESC;


/*
Q14. Campaign and Promotion Type Analysis
For each campaign and promo_type combination, calculate:

- Number of events
- Total quantity before promotion
- Total quantity after promotion
- Quantity change

Display:
- campaign_name
- promo_type
- event_count
- total_before
- total_after
- quantity_change

Sort by campaign_name and quantity_change descending.

Concepts:
Multiple GROUP BY columns, JOIN, aggregation, ORDER BY.
*/
SELECT dc.campaign_name, fe.promo_type, COUNT(fe.event_id) as event_count,
SUM(fe.`quantity_sold(before_promo)`) as total_before,
SUM(fe.`quantity_sold(after_promo)`) as total_after,
SUM(fe.`quantity_sold(after_promo)`) - SUM(fe.`quantity_sold(before_promo)`) as quantity_change
FROM dim_campaigns dc
INNER JOIN fact_events fe
ON dc.campaign_id = fe.campaign_id
GROUP BY dc.campaign_name, fe.promo_type
ORDER BY dc.campaign_name, quantity_change DESC;



/*
Q15. Product Revenue Before and After Promotion
For each product, calculate:

1. Revenue before promotion =
   base_price × quantity_sold(before_promo)

2. Revenue after promotion =
   base_price × quantity_sold(after_promo)

3. Revenue difference =
   Revenue after - Revenue before

Display:
- product_name
- category
- revenue_before
- revenue_after
- revenue_difference

Sort by revenue_difference descending.

Concepts:
JOIN, GROUP BY, SUM, arithmetic calculations, aliases.
*/
SELECT dp.product_name,dp.category,
SUM(fe.`quantity_sold(before_promo)`* fe.base_price)  as revenue_before,
SUM(fe.`quantity_sold(after_promo)`* fe.base_price)  as revenue_after,
SUM(fe.`quantity_sold(after_promo)`* fe.base_price - fe.`quantity_sold(before_promo)`* fe.base_price) as revenue_difference
FROM dim_products dp
INNER JOIN fact_events fe
ON dp.product_code = fe.product_code
GROUP BY dp.product_name,dp.category
ORDER BY revenue_difference DESC;


/*
Q16. Classify Promotion Performance
For every promotion type, calculate total quantity before and after promotion.

Then classify the promotion using CASE:

- Percentage change >= 50% → "High Impact"
- Percentage change >= 20% → "Medium Impact"
- Percentage change < 20% → "Low Impact"

Display:
- promo_type
- total_before
- total_after
- percentage_change
- performance_category

Sort by percentage_change descending.

Concepts:
GROUP BY, CASE, arithmetic calculations, NULLIF, aliases.
*/

WITH promo_performance AS(
SELECT
        fe.promo_type,
        SUM(fe.`quantity_sold(before_promo)`) AS total_before,
        SUM(fe.`quantity_sold(after_promo)`) AS total_after,
        ((SUM(fe.`quantity_sold(after_promo)`) - SUM(fe.`quantity_sold(before_promo)`)) /
         NULLIF(SUM(fe.`quantity_sold(before_promo)`), 0)) * 100 AS percentage_change
    FROM fact_events fe
    GROUP BY fe.promo_type

)

SELECT promo_type, total_before, total_after, percentage_change,

CASE
    WHEN percentage_change >= 50 THEN 'High Impact'
    WHEN percentage_change >= 20 THEN 'Medium Impact'
    ELSE 'Low Impact'
END as performance_category

FROM promo_performance
ORDER BY percentage_change DESC;



/*
Q17. Top Products Within Each Category
Using a CTE:

1. Calculate total quantity sold after promotion for every product.
2. Rank products within each category based on total quantity sold after promotion.
3. Return only the top 2 products from every category.

Display:
- category
- product_name
- total_quantity_after
- category_rank

Concepts:
CTE, JOIN, GROUP BY, DENSE_RANK/ROW_NUMBER,
PARTITION BY, window functions.
*/

With product_sales AS (
    SELECT dp.category, dp.product_name,
           SUM(fe.`quantity_sold(after_promo)`) AS total_quantity_after
    FROM fact_events fe
    INNER JOIN dim_products dp
    ON fe.product_code = dp.product_code
    GROUP BY dp.category, dp.product_code, dp.product_name
),
ranked_products AS (
    SELECT category, product_name, total_quantity_after,
           DENSE_RANK() OVER (PARTITION BY category ORDER BY total_quantity_after DESC) AS category_rank
    FROM product_sales
)

SELECT category, product_name, total_quantity_after, category_rank
FROM ranked_products
WHERE category_rank <= 2
ORDER BY category, category_rank;






/*

Q18. Best-Performing Stores Within Each City
Calculate total quantity sold after promotion for each store.

Join dim_stores to obtain the city.

Then rank stores within each city based on total quantity sold after promotion.

Return the top 2 stores from each city.

Display:
- city
- store_id
- total_quantity_after
- city_rank

Concepts:
JOIN, CTE, GROUP BY, window functions,
PARTITION BY, RANK/DENSE_RANK.
*/

With store_sales AS (
    SELECT ds.store_id, ds.city,
           SUM(fe.`quantity_sold(after_promo)`) AS total_quantity_after
    FROM fact_events fe
    INNER JOIN dim_stores ds
    ON fe.store_id = ds.store_id
    GROUP BY ds.store_id,ds.city
),
ranked_stores AS (
    SELECT store_id, city, total_quantity_after,
           DENSE_RANK() OVER (PARTITION BY city ORDER BY total_quantity_after DESC) AS city_rank
    FROM store_sales
)

SELECT city, store_id, total_quantity_after, city_rank
FROM ranked_stores
WHERE city_rank <= 2
ORDER BY city, city_rank;



/*
Q19. Campaign-Level Product Performance
For every campaign and product:

Calculate:
- Total quantity before promotion
- Total quantity after promotion
- Quantity change
- Percentage change

Then rank products within each campaign based on percentage change.

Return the top 3 products for every campaign.

Display:
- campaign_name
- product_name
- total_before
- total_after
- quantity_change
- percentage_change
- campaign_rank

Concepts:
Multiple JOINs, CTE, GROUP BY, arithmetic calculations,
NULLIF, window functions, PARTITION BY, ranking.
*/

WITH sales_campaign AS (
 SELECT dc.campaign_id,
 dc.campaign_name,
 dp.product_name,
 SUM(fe.`quantity_sold(before_promo)`) AS total_before,
 SUM(fe.`quantity_sold(after_promo)`) AS total_after,
 SUM(fe.`quantity_sold(after_promo)`) - SUM(fe.`quantity_sold(before_promo)`)  AS quantity_change,
 ((SUM(fe.`quantity_sold(after_promo)`) -
     SUM(fe.`quantity_sold(before_promo)`))
    / NULLIF(SUM(fe.`quantity_sold(before_promo)`), 0)) * 100 AS percentage_change
 FROM dim_campaigns dc
 INNER JOIN fact_events fe
 ON dc.campaign_id = fe.campaign_id
 INNER JOIN dim_products dp
 ON fe.product_code = dp.product_code
 GROUP BY dc.campaign_id, dc.campaign_name, dp.product_name

),
camp_rank AS (
SELECT *,
 DENSE_RANK() OVER (PARTITION BY campaign_name ORDER BY percentage_change DESC) AS campaign_rank
FROM sales_campaign
)
SELECT campaign_name, product_name, total_before, total_after,
 quantity_change, percentage_change, campaign_rank
FROM camp_rank
WHERE campaign_rank <=3
ORDER BY campaign_name, campaign_rank;



/*
Q20. Complete Promotional Performance Analysis
Create a complete analytical report at the product-category level.

For every product, calculate:

- Product name
- Category
- Number of promotional events
- Total quantity before promotion
- Total quantity after promotion
- Quantity change
- Percentage change
- Revenue before promotion
- Revenue after promotion
- Revenue change
- Average base price
- Product rank within its category

Use:

Quantity Change =
Total After - Total Before

Percentage Change =
((Total After - Total Before) / Total Before) * 100

Revenue Before =
SUM(base_price × quantity_before)

Revenue After =
SUM(base_price × quantity_after)

Revenue Change =
Revenue After - Revenue Before

Then:

1. Rank products within each category by Revenue Change.
2. Return only the top 2 products from each category.
3. Use appropriate handling for division by zero.
*/


WITH product_performance AS (
    SELECT
        dp.product_code,
        dp.product_name,
        dp.category,

        COUNT(DISTINCT fe.event_id) AS promotional_events,

        SUM(fe.`quantity_sold(before_promo)`) AS total_before,
        SUM(fe.`quantity_sold(after_promo)`) AS total_after,

        SUM(
            fe.base_price * fe.`quantity_sold(before_promo)`
        ) AS revenue_before,

        SUM(
            fe.base_price * fe.`quantity_sold(after_promo)`
        ) AS revenue_after,

        AVG(fe.base_price) AS average_base_price

    FROM fact_events fe
    INNER JOIN dim_products dp
        ON fe.product_code = dp.product_code

    GROUP BY
        dp.product_code,
        dp.product_name,
        dp.category
),

product_changes AS (
    SELECT
        product_code, product_name, category, promotional_events, total_before, total_after,
        total_after - total_before AS quantity_change,
        (
            (total_after - total_before)
            / NULLIF(total_before, 0)
        ) * 100 AS percentage_change,

        revenue_before,
        revenue_after,

        revenue_after - revenue_before AS revenue_change,

        average_base_price

    FROM product_performance
),
ranked_products AS (
    SELECT
        product_name,
        category,
        promotional_events,
        total_before,
        total_after,
        quantity_change,
        percentage_change,
        revenue_before,
        revenue_after,
        revenue_change,
        average_base_price,

        DENSE_RANK() OVER (
            PARTITION BY category
            ORDER BY revenue_change DESC
        ) AS product_rank

    FROM product_changes
)
SELECT
    product_name,
    category,
    promotional_events,
    total_before,
    total_after,
    quantity_change,
    percentage_change,
    revenue_before,
    revenue_after,
    revenue_change,
    average_base_price,
    product_rank

FROM ranked_products
WHERE product_rank <= 2
ORDER BY category, product_rank;











