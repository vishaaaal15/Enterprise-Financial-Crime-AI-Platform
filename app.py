import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

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

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    DATA_PATH = os.path.join(
        BASE_DIR,
        "data",
        "transactions_demo.csv"     # Change to transactions_v2.csv for local use
    )

    df = pd.read_csv(DATA_PATH)

    df["transaction_timestamp"] = pd.to_datetime(
        df["transaction_timestamp"]
    )

    return df


df = load_data()

# ---------------------------------------------------
# Load ML Model
# ---------------------------------------------------

@st.cache_resource
def load_model():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    MODEL_PATH = os.path.join(
        BASE_DIR,
        "models",
        "fraud_detection_xgboost.pkl"
    )

    model = joblib.load(MODEL_PATH)

    return model


model = load_model()

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title(
    "🏦 Enterprise Financial Crime Analytics Platform"
)

st.markdown("""
### AI-Powered Fraud Detection & AML Monitoring System

Integrated Platform

- 🐍 Python Data Engineering
- 🗄️ Transaction Database
- 📊 Executive Risk Dashboard
- 🤖 Machine Learning Fraud Detection
- 🧠 AI Investigation Assistant
""")

st.markdown("---")

# ---------------------------------------------------
# Executive KPIs
# ---------------------------------------------------

st.subheader("📊 Executive Dashboard")

total_transactions = len(df)

fraud_transactions = int(
    df["is_fraud"].sum()
)

total_customers = df[
    "sender_customer_id"
].nunique()

total_amount = df[
    "amount"
].sum()

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

fraud_counts[
    "Transaction Type"
] = fraud_counts[
    "Transaction Type"
].replace(
    {
        0: "Non-Fraud",
        1: "Fraud"
    }
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
    "📅 Monthly Fraud Trend"
)

fraud_df = df[
    df["is_fraud"] == 1
].copy()

fraud_df["Month"] = fraud_df[
    "transaction_timestamp"
].dt.to_period("M").astype(str)

fraud_trend = (
    fraud_df
    .groupby("Month")
    .size()
    .reset_index(
        name="Fraud Count"
    )
)

fig2 = px.line(
    fraud_trend,
    x="Month",
    y="Fraud Count",
    markers=True,
    title="Monthly Fraud Trend"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------------------------------------------
# Top Fraud Merchants
# ---------------------------------------------------

st.markdown("---")

st.subheader(
    "🏪 Top 10 High Risk Merchants"
)

merchant_fraud = (
    df[df["is_fraud"] == 1]
    .groupby("merchant_name")
    .size()
    .reset_index(name="Fraud Count")
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
    df.groupby(
        "customer_risk"
    )["sender_customer_id"]
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
    title="Customer Risk"
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
    "⚠️ Transaction Risk Score Distribution"
)

fig5 = px.histogram(
    df,
    x="transaction_risk_score",
    nbins=40,
    title="Transaction Risk Score"
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
    "Enterprise Financial Crime Analytics Platform | ML + AI + Analytics"
)
