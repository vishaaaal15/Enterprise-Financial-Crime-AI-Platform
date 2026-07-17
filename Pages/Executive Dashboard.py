# ============================================================
# Page 1: Executive Fraud Analytics Dashboard
# Enterprise Financial Crime Platform
# ============================================================


import streamlit as st
import pandas as pd
import plotly.express as px



# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="Executive Fraud Dashboard",
    page_icon="🏦",
    layout="wide"
)



# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        r"C:\Users\vshal\data\processed\transactions_v2.csv"
    )


    df["transaction_timestamp"] = pd.to_datetime(
        df["transaction_timestamp"]
    )


    return df



df = load_data()



# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.title(
    "🏦 Enterprise Financial Crime Executive Dashboard"
)


st.markdown(
"""
### AI-Powered Fraud Monitoring & Risk Intelligence Platform

Executive overview of:

- 💳 Transaction Activity
- 🚨 Fraud Exposure
- 👥 Customer Risk
- 🏪 Merchant Risk
- 📈 Fraud Trends
"""
)



st.markdown("---")



# ------------------------------------------------------------
# Executive KPIs
# ------------------------------------------------------------

st.subheader(
    "📊 Executive Risk Overview"
)



total_transactions = len(df)



fraud_transactions = int(
    df["is_fraud"].sum()
)



fraud_rate = (

    fraud_transactions /
    total_transactions *
    100

)



total_customers = (
    df["sender_customer_id"]
    .nunique()
)



transaction_volume = (
    df["amount"]
    .sum()
)



avg_transaction = (
    df["amount"]
    .mean()
)



col1, col2, col3, col4, col5 = st.columns(5)



col1.metric(
    "💳 Total Transactions",
    f"{total_transactions:,}"
)



col2.metric(
    "🚨 Fraud Cases",
    f"{fraud_transactions:,}"
)



col3.metric(
    "⚠️ Fraud Rate",
    f"{fraud_rate:.2f}%"
)



col4.metric(
    "👥 Customers",
    f"{total_customers:,}"
)



col5.metric(
    "💰 Transaction Volume",
    f"₹{transaction_volume/1e9:.2f} B"
)





# ------------------------------------------------------------
# Fraud Distribution
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "🚨 Fraud vs Legitimate Transactions"
)



fraud_distribution = (

    df["is_fraud"]
    .value_counts()
    .reset_index()

)



fraud_distribution.columns = [

    "Fraud Status",
    "Count"

]



fraud_distribution["Fraud Status"] = (

    fraud_distribution["Fraud Status"]
    .replace(
        {
            0:"Legitimate",
            1:"Fraud"
        }
    )

)



fig1 = px.pie(

    fraud_distribution,

    names="Fraud Status",

    values="Count",

    hole=0.45,

    title="Transaction Fraud Distribution"

)



st.plotly_chart(

    fig1,

    use_container_width=True

)





# ------------------------------------------------------------
# Fraud Trend Analysis
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "📈 Monthly Fraud Trend"
)



fraud_trend = (

    df[df["is_fraud"]==1]

    .groupby(

        df["transaction_timestamp"]
        .dt.to_period("M")

    )

    .size()

    .reset_index(

        name="Fraud Count"

    )

)



fraud_trend["transaction_timestamp"] = (

    fraud_trend["transaction_timestamp"]
    .astype(str)

)



fig2 = px.line(

    fraud_trend,

    x="transaction_timestamp",

    y="Fraud Count",

    markers=True,

    title="Fraud Cases Over Time"

)



st.plotly_chart(

    fig2,

    use_container_width=True

)





# ------------------------------------------------------------
# Fraud by Payment Channel
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "💳 Fraud by Payment Channel"
)



payment_risk = (

    df[df["is_fraud"]==1]

    .groupby("payment_channel")

    .size()

    .reset_index(

        name="Fraud Count"

    )

    .sort_values(

        "Fraud Count",

        ascending=False

    )

)



fig3 = px.bar(

    payment_risk,

    x="payment_channel",

    y="Fraud Count",

    text="Fraud Count",

    title="High Risk Payment Channels"

)



st.plotly_chart(

    fig3,

    use_container_width=True

)





# ------------------------------------------------------------
# High Risk Merchants
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "🏪 Top 10 High Risk Merchants"
)



merchant_risk = (

    df[df["is_fraud"]==1]

    .groupby("merchant_name")

    .size()

    .reset_index(

        name="Fraud Count"

    )

    .sort_values(

        "Fraud Count",

        ascending=False

    )

    .head(10)

)



fig4 = px.bar(

    merchant_risk,

    x="merchant_name",

    y="Fraud Count",

    text="Fraud Count",

    title="Merchant Fraud Ranking"

)



st.plotly_chart(

    fig4,

    use_container_width=True

)





# ------------------------------------------------------------
# Customer Risk Segmentation
# ------------------------------------------------------------


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



fig5 = px.bar(

    customer_risk,

    x="Risk Level",

    y="Customer Count",

    text="Customer Count",

    title="Customers by Risk Category"

)



st.plotly_chart(

    fig5,

    use_container_width=True

)





# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------


st.markdown("---")


st.success(
"""
✅ Executive Fraud Analytics Dashboard Ready

Machine Learning + Financial Crime Analytics + Risk Intelligence
"""
)