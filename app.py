import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Customer Churn Comprehensive Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for polished dashboard appearance
st.markdown("""
    <style>
        .main { background-color: #0e1117; }
        .metric-card {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        .stMetric label { color: #94a3b8 !important; font-size: 0.9rem !important; }
        .stMetric .metric-value { font-weight: 700 !important; font-size: 1.8rem !important; }
        .insight-box {
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366f1;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- DYNAMIC DATA LOADING ---
st.sidebar.header("📂 Dataset Source")
uploaded_file = st.sidebar.file_uploader("Upload Custom CSV File", type=["csv"], help="Upload any telecom churn CSV to analyze instantly.")

@st.cache_data
def process_data(file_source):
    df = pd.read_csv(file_source)
    
    # Numeric conversions
    if 'MonthlyCharges' in df.columns:
        df['MonthlyCharges'] = pd.to_numeric(df['MonthlyCharges'], errors='coerce').fillna(0)
    else:
        df['MonthlyCharges'] = 0

    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    else:
        df['TotalCharges'] = 0

    if 'tenure' in df.columns:
        df['tenure'] = pd.to_numeric(df['tenure'], errors='coerce').fillna(0)
    else:
        df['tenure'] = 0

    # Categorical safeguards
    for col in ['gender', 'Contract', 'InternetService', 'PaymentMethod', 'Churn', 'Partner', 'Dependents']:
        if col not in df.columns:
            df[col] = "Unknown"

    if 'SeniorCitizen' in df.columns:
        df['SeniorCitizenLabel'] = df['SeniorCitizen'].apply(lambda x: 'Senior (65+)' if x == 1 else 'Non-Senior')
    else:
        df['SeniorCitizenLabel'] = 'Non-Senior'
    
    # Feature Engineering for Tenure Group
    def tenure_group(tenure):
        if tenure <= 12:
            return '0-1 Year'
        elif tenure <= 36:
            return '1-3 Years'
        else:
            return '3+ Years'
            
    df['TenureGroup'] = df['tenure'].apply(tenure_group)
    return df

if uploaded_file is not None:
    try:
        df = process_data(uploaded_file)
        st.sidebar.success(f"Loaded: `{uploaded_file.name}` ({len(df):,} rows)")
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")
        df = process_data("dataset/churn_data.csv")
else:
    df = process_data("dataset/churn_data.csv")
    st.sidebar.info("Using default dataset (`churn_data.csv`)")

# --- TITLE & HEADER ---
st.title("📊 Customer Churn Analytics Platform")
st.markdown("Developed by **Rohit** | End-to-End Data Analytics & Dynamic Web Application Platform")


# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filter Dashboard")

gender_options = ["All"] + list(df["gender"].unique())
selected_gender = st.sidebar.selectbox("Gender", gender_options)

contract_options = ["All"] + list(df["Contract"].unique())
selected_contract = st.sidebar.selectbox("Contract Type", contract_options)

internet_options = ["All"] + list(df["InternetService"].unique())
selected_internet = st.sidebar.selectbox("Internet Service", internet_options)

payment_options = ["All"] + list(df["PaymentMethod"].unique())
selected_payment = st.sidebar.selectbox("Payment Method", payment_options)

senior_options = ["All", "Senior (65+)", "Non-Senior"]
selected_senior = st.sidebar.selectbox("Senior Citizen", senior_options)

min_tenure, max_tenure = int(df["tenure"].min()), int(df["tenure"].max())
selected_tenure = st.sidebar.slider("Tenure Range (Months)", min_tenure, max_tenure, (min_tenure, max_tenure))

# Apply Filters
filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]
if selected_contract != "All":
    filtered_df = filtered_df[filtered_df["Contract"] == selected_contract]
if selected_internet != "All":
    filtered_df = filtered_df[filtered_df["InternetService"] == selected_internet]
if selected_payment != "All":
    filtered_df = filtered_df[filtered_df["PaymentMethod"] == selected_payment]
if selected_senior != "All":
    filtered_df = filtered_df[filtered_df["SeniorCitizenLabel"] == selected_senior]

filtered_df = filtered_df[
    (filtered_df["tenure"] >= selected_tenure[0]) & 
    (filtered_df["tenure"] <= selected_tenure[1])
]

# --- KEY METRICS SUMMARY ---
total_cust = len(filtered_df)
churned_cust = len(filtered_df[filtered_df["Churn"] == "Yes"])
churn_rate = (churned_cust / total_cust * 100) if total_cust > 0 else 0
avg_monthly = filtered_df["MonthlyCharges"].mean() if total_cust > 0 else 0
revenue_lost = filtered_df[filtered_df["Churn"] == "Yes"]["MonthlyCharges"].sum()

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Customers", f"{total_cust:,}")
m2.metric("Churned Customers", f"{churned_cust:,}")
m3.metric("Overall Churn Rate", f"{churn_rate:.2f}%")
m4.metric("Avg Monthly Charges", f"${avg_monthly:.2f}")
m5.metric("Monthly Revenue Lost", f"${revenue_lost:,.2f}")

st.markdown("---")

# --- TABBED ANALYTICS DASHBOARD ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview & Churn Drivers", 
    "💵 Financial & Revenue Impact", 
    "👥 Demographics & Services", 
    "💡 Business Recommendations", 
    "📋 Data & SQL Queries"
])

# --- TAB 1: OVERVIEW & CHURN DRIVERS (Power BI Match) ---
with tab1:
    st.subheader("Key Churn Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    # 1. Churn Distribution (Donut Chart)
    with col1:
        st.markdown("#### Customer Churn Distribution")
        churn_counts = filtered_df["Churn"].value_counts().reset_index()
        churn_counts.columns = ["Churn", "Count"]
        fig_churn = px.pie(
            churn_counts, 
            names="Churn", 
            values="Count", 
            hole=0.5,
            color="Churn",
            color_discrete_map={"No": "#3b82f6", "Yes": "#ef4444"}
        )
        fig_churn.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_churn, use_container_width=True)

    # 2. Churn by Gender
    with col2:
        st.markdown("#### Customer Churn by Gender")
        gender_churn = filtered_df[filtered_df["Churn"] == "Yes"]["gender"].value_counts().reset_index()
        gender_churn.columns = ["Gender", "Count"]
        fig_gender = px.pie(
            gender_churn, 
            names="Gender", 
            values="Count", 
            color="Gender",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gender, use_container_width=True)

    # 3. Churn Rate by Contract Type
    with col3:
        st.markdown("#### Churn Rate by Contract Type (%)")
        contract_rate = filtered_df.groupby("Contract")["Churn"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
        contract_rate.columns = ["Contract", "ChurnRate"]
        fig_contract_rate = px.bar(
            contract_rate, 
            x="Contract", 
            y="ChurnRate", 
            color="Contract",
            text=contract_rate["ChurnRate"].apply(lambda x: f"{x:.1f}%"),
            color_discrete_sequence=["#f43f5e", "#f59e0b", "#10b981"]
        )
        fig_contract_rate.update_layout(yaxis_title="Churn Rate (%)", showlegend=False)
        st.plotly_chart(fig_contract_rate, use_container_width=True)

    st.markdown("---")
    
    col4, col5, col6 = st.columns(3)

    # 4. Churn by Contract Type (Absolute Count)
    with col4:
        st.markdown("#### Churn by Contract Type (Count)")
        contract_cnt = filtered_df[filtered_df["Churn"] == "Yes"]["Contract"].value_counts().reset_index()
        contract_cnt.columns = ["Contract", "Churned"]
        fig_contract_cnt = px.bar(
            contract_cnt, 
            y="Contract", 
            x="Churned", 
            orientation='h',
            color="Contract",
            color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc"]
        )
        fig_contract_cnt.update_layout(showlegend=False)
        st.plotly_chart(fig_contract_cnt, use_container_width=True)

    # 5. Churn by Internet Service
    with col5:
        st.markdown("#### Churn by Internet Service")
        internet_cnt = filtered_df[filtered_df["Churn"] == "Yes"]["InternetService"].value_counts().reset_index()
        internet_cnt.columns = ["InternetService", "Churned"]
        fig_internet = px.bar(
            internet_cnt, 
            y="InternetService", 
            x="Churned", 
            orientation='h',
            color="InternetService",
            color_discrete_sequence=["#fb7185", "#38bdf8", "#4ade80"]
        )
        fig_internet.update_layout(showlegend=False)
        st.plotly_chart(fig_internet, use_container_width=True)

    # 6. Churn by Payment Method
    with col6:
        st.markdown("#### Churn by Payment Method")
        payment_cnt = filtered_df[filtered_df["Churn"] == "Yes"]["PaymentMethod"].value_counts().reset_index()
        payment_cnt.columns = ["PaymentMethod", "Churned"]
        fig_payment = px.bar(
            payment_cnt, 
            y="PaymentMethod", 
            x="Churned", 
            orientation='h',
            color="PaymentMethod",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_payment.update_layout(showlegend=False)
        st.plotly_chart(fig_payment, use_container_width=True)

    # 7. Tenure Group Churn
    st.markdown("#### Churn by Tenure Group")
    tenure_cnt = filtered_df[filtered_df["Churn"] == "Yes"]["TenureGroup"].value_counts().reindex(["0-1 Year", "1-3 Years", "3+ Years"]).reset_index()
    tenure_cnt.columns = ["TenureGroup", "Churned"]
    fig_tenure_grp = px.bar(
        tenure_cnt, 
        x="TenureGroup", 
        y="Churned", 
        color="TenureGroup",
        text="Churned",
        color_discrete_sequence=["#ef4444", "#f59e0b", "#10b981"]
    )
    fig_tenure_grp.update_layout(showlegend=False)
    st.plotly_chart(fig_tenure_grp, use_container_width=True)

# --- TAB 2: FINANCIAL & REVENUE IMPACT ---
with tab2:
    st.subheader("Financial & Charges Analysis")
    
    fcol1, fcol2 = st.columns(2)
    
    with fcol1:
        st.markdown("#### Tenure vs. Monthly Charges (SVG Render)")
        fig_scatter = px.scatter(
            filtered_df, 
            x="tenure", 
            y="MonthlyCharges", 
            color="Churn", 
            opacity=0.65,
            render_mode="svg",
            color_discrete_map={"No": "#3b82f6", "Yes": "#ef4444"},
            labels={"tenure": "Tenure (Months)", "MonthlyCharges": "Monthly Charges ($)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with fcol2:
        st.markdown("#### Monthly Charges Distribution by Churn")
        fig_box = px.box(
            filtered_df, 
            x="Churn", 
            y="MonthlyCharges", 
            color="Churn",
            color_discrete_map={"No": "#3b82f6", "Yes": "#ef4444"},
            points="outliers"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("#### Revenue Impact by Payment Method ($ Lost)")
    rev_payment = filtered_df[filtered_df["Churn"] == "Yes"].groupby("PaymentMethod")["MonthlyCharges"].sum().reset_index()
    fig_rev = px.bar(
        rev_payment, 
        x="PaymentMethod", 
        y="MonthlyCharges", 
        color="PaymentMethod",
        text=rev_payment["MonthlyCharges"].apply(lambda x: f"${x:,.0f}"),
        color_discrete_sequence=px.colors.qualitative.Dark2
    )
    fig_rev.update_layout(yaxis_title="Monthly Revenue Lost ($)", showlegend=False)
    st.plotly_chart(fig_rev, use_container_width=True)

# --- TAB 3: DEMOGRAPHICS & SERVICES ---
with tab3:
    st.subheader("Customer Demographics & Add-on Services Analysis")
    
    dcol1, dcol2 = st.columns(2)
    
    with dcol1:
        st.markdown("#### Senior Citizen Churn Rate")
        senior_churn = filtered_df.groupby("SeniorCitizenLabel")["Churn"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
        senior_churn.columns = ["SeniorCitizen", "ChurnRate"]
        fig_senior = px.bar(
            senior_churn, 
            x="SeniorCitizen", 
            y="ChurnRate", 
            color="SeniorCitizen",
            text=senior_churn["ChurnRate"].apply(lambda x: f"{x:.1f}%"),
            color_discrete_sequence=["#38bdf8", "#f43f5e"]
        )
        fig_senior.update_layout(yaxis_title="Churn Rate (%)", showlegend=False)
        st.plotly_chart(fig_senior, use_container_width=True)
        
    with dcol2:
        st.markdown("#### Partner & Dependents Impact on Churn")
        family_df = filtered_df.groupby(["Partner", "Dependents"])["Churn"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
        family_df.columns = ["Partner", "Dependents", "ChurnRate"]
        fig_family = px.bar(
            family_df, 
            x="Partner", 
            y="ChurnRate", 
            color="Dependents", 
            barmode="group",
            text=family_df["ChurnRate"].apply(lambda x: f"{x:.1f}%")
        )
        fig_family.update_layout(yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig_family, use_container_width=True)

    st.markdown("#### Add-on Services Impact on Churn Rate")
    services = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
    service_rates = []
    for s in services:
        if s in filtered_df.columns:
            rate = (filtered_df[(filtered_df[s] == "No") & (filtered_df["Churn"] == "Yes")].shape[0] / 
                    filtered_df[filtered_df[s] == "No"].shape[0] * 100) if filtered_df[filtered_df[s] == "No"].shape[0] > 0 else 0
            service_rates.append({"Service": s, "ChurnRateWithoutService": rate})
            
    srv_df = pd.DataFrame(service_rates)
    fig_srv = px.bar(
        srv_df, 
        x="Service", 
        y="ChurnRateWithoutService", 
        color="Service",
        text=srv_df["ChurnRateWithoutService"].apply(lambda x: f"{x:.1f}%"),
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_srv.update_layout(yaxis_title="Churn Rate Without Service (%)", showlegend=False)
    st.plotly_chart(fig_srv, use_container_width=True)

# --- TAB 4: BUSINESS RECOMMENDATIONS ---
with tab4:
    st.subheader("💡 Strategic Recommendations & Action Plan")
    
    st.markdown("""
    <div class="insight-box">
        <h4>1. Convert Month-to-Month Contracts to Long-Term Plans</h4>
        <p><b>Insight:</b> Customers on Month-to-Month contracts have a <b>42.7% churn rate</b>, compared to less than 3% for two-year contract holders.<br>
        <b>Action:</b> Launch targeted discount campaigns offering 10-15% incentives or free streaming add-ons for switching to annual commitments.</p>
    </div>
    <div class="insight-box">
        <h4>2. Address Fiber Optic Service Satisfaction</h4>
        <p><b>Insight:</b> Fiber Optic users experience significantly higher churn (<b>41.9%</b>) than DSL users (<b>19.0%</b>), despite paying higher monthly rates.<br>
        <b>Action:</b> Conduct quality-of-service audits and improve tech support resolution times specifically for Fiber Optic lines.</p>
    </div>
    <div class="insight-box">
        <h4>3. Promote Auto-Pay Payment Methods</h4>
        <p><b>Insight:</b> Electronic Check users account for over <b>57% of all churned customers</b>.<br>
        <b>Action:</b> Encourage automatic bank transfers or credit card payments by offering a $5 monthly bill credit for auto-pay enrollment.</p>
    </div>
    <div class="insight-box">
        <h4>4. Early Tenure Onboarding (0-1 Year Risk)</h4>
        <p><b>Insight:</b> Over <b>55% of all churn occurs within the first 12 months</b> of customer tenure.<br>
        <b>Action:</b> Implement proactive check-ins at months 1, 3, and 6 with complimentary tech support and service walkthroughs.</p>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 5: DATA EXPLORER & SQL QUERIES ---
with tab5:
    st.subheader("📋 Filtered Dataset & SQL Analysis")
    
    st.markdown("#### Filtered Customer Data (`" + str(len(filtered_df)) + "` rows)")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download Button
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data as CSV", data=csv_data, file_name="filtered_churn_data.csv", mime="text/csv")
    
    st.markdown("---")
    st.markdown("#### SQL Queries Used in Analysis")
    
    with st.expander("View 10 Key Analytical SQL Queries"):
        st.code("""
-- 1. Total Customers & Churn Distribution
SELECT Churn, COUNT(*) AS total_customers 
FROM customers 
GROUP BY Churn;

-- 2. Churn Rate Percentage
SELECT ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent 
FROM customers;

-- 3. Churn by Contract Type
SELECT Contract, COUNT(*) AS total_customers, SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned_customers 
FROM customers 
GROUP BY Contract;

-- 4. Churn by Internet Service
SELECT InternetService, COUNT(*) AS total_customers, SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned 
FROM customers 
GROUP BY InternetService;

-- 5. Total Revenue Lost Due to Churn
SELECT SUM(MonthlyCharges) AS monthly_revenue_lost 
FROM customers 
WHERE Churn='Yes';
        """, language="sql")
