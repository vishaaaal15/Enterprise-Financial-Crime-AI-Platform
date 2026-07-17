# ============================================================
# Page 3: Risk Analytics Dashboard
# Enterprise Financial Crime Platform
# ============================================================


import streamlit as st
import pandas as pd
import plotly.express as px



# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

st.set_page_config(

    page_title="Risk Analytics",

    page_icon="📊",

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
    "📊 Enterprise Risk Analytics Dashboard"
)


st.markdown(
"""
Advanced transaction risk intelligence system.

Analyze:

- Transaction Risk
- Customer Risk
- Device Risk
- Merchant Risk
- Geographic Risk
"""
)



st.markdown("---")



# ------------------------------------------------------------
# Risk KPI Section
# ------------------------------------------------------------


st.subheader(
    "⚠️ Risk Overview"
)



total_transactions = len(df)



high_risk_transactions = (

    df[df["transaction_risk_score"] >= 80]

    .shape[0]

)



avg_risk_score = (

    df["transaction_risk_score"]

    .mean()

)



fraud_transactions = (

    df["is_fraud"]

    .sum()

)



col1,col2,col3,col4 = st.columns(4)



col1.metric(

    "Total Transactions",

    f"{total_transactions:,}"

)



col2.metric(

    "High Risk Transactions",

    f"{high_risk_transactions:,}"

)



col3.metric(

    "Average Risk Score",

    f"{avg_risk_score:.2f}"

)



col4.metric(

    "Fraud Cases",

    f"{fraud_transactions:,}"

)





# ------------------------------------------------------------
# Transaction Risk Distribution
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "📈 Transaction Risk Score Distribution"
)



fig1 = px.histogram(

    df,

    x="transaction_risk_score",

    nbins=50,

    title="Risk Score Distribution"

)



st.plotly_chart(

    fig1,

    use_container_width=True

)





# ------------------------------------------------------------
# Risk by Payment Channel
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "💳 Payment Channel Risk Analysis"
)



payment_risk = (

    df.groupby(
        "payment_channel"
    )

    ["transaction_risk_score"]

    .mean()

    .reset_index()

)



fig2 = px.bar(

    payment_risk,

    x="payment_channel",

    y="transaction_risk_score",

    text="transaction_risk_score",

    title="Average Risk by Payment Channel"

)



st.plotly_chart(

    fig2,

    use_container_width=True

)





# ------------------------------------------------------------
# Device Risk Analysis
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "📱 Device Risk Intelligence"
)



device_risk = (

    df.groupby(
        "device_type"
    )

    ["device_risk_score"]

    .mean()

    .reset_index()

)



fig3 = px.bar(

    device_risk,

    x="device_type",

    y="device_risk_score",

    text="device_risk_score",

    title="Device Risk Score"

)



st.plotly_chart(

    fig3,

    use_container_width=True

)





# ------------------------------------------------------------
# Geography Risk
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "🌎 Geographic Fraud Analysis"
)



geo = (

    df[df["is_fraud"]==1]

    .groupby(
        "customer_state"
    )

    .size()

    .reset_index(

        name="Fraud Count"

    )

    .sort_values(

        "Fraud Count",

        ascending=False

    )

)



fig4 = px.bar(

    geo,

    x="customer_state",

    y="Fraud Count",

    text="Fraud Count",

    title="Fraud by State"

)



st.plotly_chart(

    fig4,

    use_container_width=True

)





# ------------------------------------------------------------
# Cross Border Risk
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "🌐 Cross Border Transaction Risk"
)



cross_border = (

    df.groupby(
        "cross_border"
    )

    ["is_fraud"]

    .mean()

    .reset_index()

)



cross_border["Fraud Rate %"] = (

    cross_border["is_fraud"]

    *100

)



fig5 = px.bar(

    cross_border,

    x="cross_border",

    y="Fraud Rate %",

    text="Fraud Rate %",

    title="Cross Border Fraud Rate"

)



st.plotly_chart(

    fig5,

    use_container_width=True

)





# ------------------------------------------------------------
# Merchant Category Risk
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "🏪 Merchant Category Risk"
)



merchant_category = (

    df.groupby(
        "merchant_category"
    )

    ["is_fraud"]

    .mean()

    .reset_index()

)



merchant_category["Fraud Rate %"] = (

    merchant_category["is_fraud"]

    *100

)



merchant_category = (

    merchant_category

    .sort_values(

        "Fraud Rate %",

        ascending=False

    )

)



fig6 = px.bar(

    merchant_category.head(10),

    x="merchant_category",

    y="Fraud Rate %",

    text="Fraud Rate %",

    title="Highest Risk Merchant Categories"

)



st.plotly_chart(

    fig6,

    use_container_width=True

)





# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------


st.markdown("---")


st.success(
"""
✅ Risk Analytics Dashboard Ready

Transaction Risk + Device Intelligence + Geographic Risk + Merchant Analytics
"""
)