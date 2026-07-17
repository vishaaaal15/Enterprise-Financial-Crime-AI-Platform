import streamlit as st
import pandas as pd
import plotly.express as px
import joblib


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Enterprise Financial Crime Analytics Platform",
    page_icon="🏦",
    layout="wide"
)


# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

@st.cache_data
def load_data():

    import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "transactions_v2.csv"
)

df = pd.read_csv(DATA_PATH)


df = load_data()


# ---------------------------------------------------
# Load ML Model
# ---------------------------------------------------

@st.cache_resource
def load_model():

    model = joblib.load(
        "models/fraud_detection_xgboost.pkl"
    )

    return model


model = load_model()


# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title(
    "🏦 Enterprise Financial Crime Analytics Platform"
)

st.markdown(
"""
### AI-Powered Fraud Detection & AML Monitoring System

Integrated Platform:

- 🐍 Python Data Engineering
- 🗄️ MySQL Transaction Database
- 📊 Risk Analytics Dashboard
- 🤖 Machine Learning Fraud Detection
- 🧠 AI Investigation Assistant (Coming Soon)
"""
)


st.markdown("---")


# ---------------------------------------------------
# Executive KPIs
# ---------------------------------------------------

st.subheader("📊 Executive Dashboard")


total_transactions = len(df)

fraud_transactions = int(
    df["is_fraud"].sum()
)

total_customers = (
    df["sender_customer_id"]
    .nunique()
)

total_amount = (
    df["amount"]
    .sum()
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "💳 Total Transactions",
    f"{total_transactions:,}"
)


col2.metric(
    "🚨 Fraud Transactions",
    f"{fraud_transactions:,}"
)


col3.metric(
    "👥 Customers",
    f"{total_customers:,}"
)


col4.metric(
    "💰 Total Amount",
    f"₹{total_amount/1e9:.2f} B"
)



# ---------------------------------------------------
# Fraud Distribution
# ---------------------------------------------------

st.markdown("---")

st.subheader(
    "📈 Fraud vs Non-Fraud Distribution"
)


fraud_counts = (
    df["is_fraud"]
    .value_counts()
    .reset_index()
)


fraud_counts.columns = [
    "Transaction Type",
    "Count"
]


fraud_counts["Transaction Type"] = (
    fraud_counts["Transaction Type"]
    .replace(
        {
            0:"Non-Fraud",
            1:"Fraud"
        }
    )
)


fig1 = px.pie(
    fraud_counts,
    names="Transaction Type",
    values="Count",
    hole=0.45,
    title="Fraud Distribution"
)


st.plotly_chart(
    fig1,
    use_container_width=True
)



# ---------------------------------------------------
# Fraud Trend
# ---------------------------------------------------

st.markdown("---")

st.subheader(
    "📅 Fraud Trend Analysis"
)


fraud_trend = (
    df[df["is_fraud"] == 1]
    .groupby(
        df["transaction_timestamp"]
        .dt.to_period("M")
    )
    .size()
    .reset_index(
        name="Fraud Count"
    )
)


fraud_trend[
    "transaction_timestamp"
] = (
    fraud_trend[
        "transaction_timestamp"
    ]
    .astype(str)
)



fig2 = px.line(
    fraud_trend,
    x="transaction_timestamp",
    y="Fraud Count",
    markers=True,
    title="Monthly Fraud Transactions"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)



# ---------------------------------------------------
# Merchant Risk
# ---------------------------------------------------

st.markdown("---")

st.subheader(
    "🏪 Top 10 High-Risk Merchants"
)


merchant_fraud = (
    df[df["is_fraud"] == 1]
    .groupby("merchant_name")
    .size()
    .reset_index(
        name="Fraud Count"
    )
)


merchant_fraud = (
    merchant_fraud
    .sort_values(
        "Fraud Count",
        ascending=False
    )
    .head(10)
)



fig3 = px.bar(
    merchant_fraud,
    x="merchant_name",
    y="Fraud Count",
    text="Fraud Count",
    title="Merchant Fraud Ranking"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)



# ---------------------------------------------------
# Customer Risk
# ---------------------------------------------------

st.markdown("---")

st.subheader(
    "👥 Customer Risk Segmentation"
)


customer_risk = (
    df.groupby("customer_risk")
    ["sender_customer_id"]
    .nunique()
    .reset_index()
)


customer_risk.columns = [
    "Risk Level",
    "Customer Count"
]


fig4 = px.bar(
    customer_risk,
    x="Risk Level",
    y="Customer Count",
    text="Customer Count",
    title="Customers by Risk Category"
)


st.plotly_chart(
    fig4,
    use_container_width=True
)



# ---------------------------------------------------
# Transaction Risk Score
# ---------------------------------------------------

st.markdown("---")

st.subheader(
    "⚠️ Transaction Risk Score Analysis"
)


fig5 = px.histogram(
    df,
    x="transaction_risk_score",
    nbins=50,
    title="Transaction Risk Score Distribution"
)


st.plotly_chart(
    fig5,
    use_container_width=True
)



# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.markdown("---")

st.success(
    "Enterprise Financial Crime Analytics Platform | ML + Analytics + AI Ready"
)