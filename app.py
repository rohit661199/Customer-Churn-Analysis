import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📉",
    layout="wide"
)

st.title("📉 Customer Churn Analytics Dashboard")
st.markdown("Developed by **Rohit** | Built with Python, Streamlit, and Plotly")

@st.cache_data
def load_data():
    df = pd.read_csv("dataset/churn_data.csv")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.fillna({'TotalCharges': 0}, inplace=True)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
contract_filter = st.sidebar.multiselect("Contract Type", options=df["Contract"].unique(), default=df["Contract"].unique())
internet_filter = st.sidebar.multiselect("Internet Service", options=df["InternetService"].unique(), default=df["InternetService"].unique())
payment_filter = st.sidebar.multiselect("Payment Method", options=df["PaymentMethod"].unique(), default=df["PaymentMethod"].unique())

filtered_df = df[
    (df["Contract"].isin(contract_filter)) &
    (df["InternetService"].isin(internet_filter)) &
    (df["PaymentMethod"].isin(payment_filter))
]

# KPI Metrics
total_cust = len(filtered_df)
churn_cust = len(filtered_df[filtered_df["Churn"] == "Yes"])
churn_rate = (churn_cust / total_cust * 100) if total_cust > 0 else 0
avg_charges = filtered_df["MonthlyCharges"].mean() if total_cust > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total_cust:,}")
col2.metric("Churned Customers", f"{churn_cust:,}", delta=f"{churn_rate:.1f}% Churn Rate", delta_color="inverse")
col3.metric("Avg Monthly Charge", f"${avg_charges:.2f}")
col4.metric("Active Filters Count", f"{len(filtered_df):,}")

st.markdown("---")

# Charts
ch1, ch2 = st.columns(2)

with ch1:
    st.subheader("Churn Rate by Contract Type")
    contract_df = filtered_df.groupby("Contract")["Churn"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
    fig1 = px.bar(contract_df, x="Contract", y="Churn", labels={"Churn": "Churn Rate (%)"}, color="Contract", color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig1, use_container_width=True)

with ch2:
    st.subheader("Churn by Payment Method")
    fig2 = px.pie(filtered_df[filtered_df["Churn"] == "Yes"], names="PaymentMethod", title="Churn Distribution", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Tenure vs Monthly Charges")
fig3 = px.scatter(filtered_df, x="tenure", y="MonthlyCharges", color="Churn", opacity=0.6, render_mode="svg", labels={"tenure": "Tenure (Months)", "MonthlyCharges": "Monthly Charges ($)"})
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head(100))
