-- Customer Churn Analysis SQL Queries
-- 1. Total Customers
SELECT count(*) as total_customers 
FROM customers;

-- 2. Churn Distribution

select Churn ,count(*) as customers
from customers 
group by Churn;

-- 3. Churn rate
SELECT 
ROUND(
SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),2
) AS churn_rate_percent
FROM customers;

-- 4.Churn by Contract Type 

SELECT 
Contract,
COUNT(*) AS total_customers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned_customers
FROM customers
GROUP BY Contract;

-- 5. Churn by Internet Service 
 
 SELECT 
InternetService,
COUNT(*) AS total_customers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned
FROM customers
GROUP BY InternetService;

-- 6. Average Monthly Charges by Churn

SELECT 
Churn,
AVG(MonthlyCharges) AS avg_monthly_charges
FROM customers
GROUP BY Churn;

-- 7. Tenure vs Churn

SELECT 
CASE
WHEN tenure < 12 THEN '0-1 year'
WHEN tenure < 36 THEN '1-3 years'
ELSE '3+ years'
END AS tenure_group,
COUNT(*) AS customers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned
FROM customers
GROUP BY tenure_group;

-- 8. Payment Method vs Churn

SELECT 
PaymentMethod,
COUNT(*) AS customers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned
FROM customers
GROUP BY PaymentMethod;

-- 9. Total revenue lost due to Churn

SELECT 
SUM(MonthlyCharges) AS monthly_revenue_lost
FROM customers
WHERE Churn='Yes';

-- 10. Senior Citizen vs Churn

SELECT 
SeniorCitizen,
COUNT(*) AS customers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned
FROM customers
GROUP BY SeniorCitizen;