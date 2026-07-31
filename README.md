## 📊 Customer Churn Analysis
---
⭐ End-to-End Data Analysis Project
Tools Used: Python | SQL | Power BI
Focus: Business Insights & Decision Making
---
## Overview

This project analyzes customer churn in a telecom dataset to identify key factors influencing customer attrition.
The goal is to help businesses reduce churn and improve customer retention using data-driven insights.

---
---
 ## 🎯 Problem Statement
---
Customer churn is a major challenge for telecom companies.
This project aims to:

 - Identify customers likely to churn
 - Understand factors driving churn
 - Provide actionable strategies to improve retention
---
## Dashboard Preview

![Dashboard](churn_dashboard.png)

---

## Dataset

The dataset contains telecom customer information with **7043 records** and several attributes related to services and customer behavior.

Key columns include:

* Gender
* Tenure
* Contract Type
* Internet Service
* Payment Method
* Monthly Charges
* Churn Status

---

## Key Metrics

* **Total Customers:** 7043
* **Churned Customers:** 1869
* **Average Monthly Charges:** 64.76
* **Churn Rate:** 26.54%

---

## Key Insights

* Customers with **month-to-month contracts have the highest churn rate**.
* **Fiber optic internet users churn more frequently than DSL users**.
* Customers using **electronic check payment method show higher churn**.
* Customers with **tenure < 1 year are more likely to churn**.

---
 ## 🚀 Actionable Insights
 ---
- High-risk customers contribute significantly to overall churn
- Short-term contract users are more likely to leave
- High monthly charges increase churn probability 

  ---
  
  
  ## 💡 Business Recommendations
  ---
  
- Offer discounts or incentives for long-term contracts
- Target high-risk customers with retention campaigns
- Improve service quality for fiber optic users
- Provide better pricing strategies for high-charge customers

  ---
  
 ## 🧠 Why This Project Matters

This project demonstrates a real-world data analysis workflow:

- Data cleaning
- SQL querying
- Data visualization
- Insight generation
- Business decision-making
  
## Tools & Technologies

* **Python** – Data cleaning and exploratory analysis
* **SQL** – Querying and data analysis
* **Power BI** – Interactive dashboard and visualization

---

## Project Structure

```
Customer-Churn-Analysis
│
├── dataset       # raw dataset
├── python        # data analysis scripts
├── sql           # SQL queries
├── powerbi       # Power BI dashboard (.pbix)
├── churn_dashboard.png # dashboard preview
└── README.md
---

## 🔄 Dynamic CSV Analysis & Power BI Usage

### 1. Online Dynamic CSV Analysis (Streamlit App)
- Open the live web app.
- In the sidebar under **📂 Dataset Source**, use the file uploader to drag & drop any customer churn CSV dataset.
- The entire dashboard (KPIs, charts, distributions, and data table) will automatically update and re-analyze your new dataset!

### 2. Local Power BI Dataset Refresh
To analyze a new CSV locally in Power BI Desktop (`powerbi/@dashboard.pbix`):
1. Replace `dataset/churn_data.csv` with your new CSV dataset (keep column names consistent).
2. Open `powerbi/@dashboard.pbix` in Power BI Desktop.
3. Click **Refresh** on the Home tab to automatically update all visuals with your new data!

---

## Author

**Rohit**  
[GitHub Profile](https://github.com/rohit661199)


