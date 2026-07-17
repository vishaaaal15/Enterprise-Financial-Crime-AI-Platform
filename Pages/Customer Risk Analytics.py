# ============================================================
# Page 5: Customer Risk Intelligence (Customer 360)
# Enterprise Financial Crime Platform
# ============================================================


import streamlit as st
import pandas as pd
import plotly.express as px



# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

st.set_page_config(

    page_title="Customer Risk Intelligence",

    page_icon="👤",

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
    "👤 Customer Risk Intelligence Platform"
)


st.markdown(
"""
Customer 360 risk analysis system.

Analyze:

- Customer transaction behavior
- Fraud exposure
- Risk profile
- Suspicious activity
"""
)


st.markdown("---")



# ------------------------------------------------------------
# Customer Search
# ------------------------------------------------------------


st.subheader(
    "🔍 Search Customer"
)



customer_list = (

    df["sender_customer_id"]

    .unique()

)



selected_customer = st.selectbox(

    "Select Customer ID",

    customer_list

)



# Filter customer data


customer_df = (

    df[
        df["sender_customer_id"]
        ==
        selected_customer
    ]

)



# ------------------------------------------------------------
# Customer Profile
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "📋 Customer Profile"
)



total_transactions = len(customer_df)



total_amount = (

    customer_df["amount"]

    .sum()

)



fraud_cases = (

    customer_df["is_fraud"]

    .sum()

)



avg_risk = (

    customer_df["transaction_risk_score"]

    .mean()

)



customer_risk = (

    customer_df["customer_risk"]

    .iloc[0]

)



col1,col2,col3,col4,col5 = st.columns(5)



col1.metric(

    "Customer ID",

    selected_customer

)



col2.metric(

    "Transactions",

    f"{total_transactions:,}"

)



col3.metric(

    "Total Exposure",

    f"₹{total_amount:,.0f}"

)



col4.metric(

    "Fraud Cases",

    f"{fraud_cases:,}"

)



col5.metric(

    "Risk Score",

    f"{avg_risk:.2f}"

)





# ------------------------------------------------------------
# Risk Classification
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "⚠️ Customer Risk Status"
)



if avg_risk >= 80:

    st.error(
        "🔴 HIGH RISK CUSTOMER"
    )


elif avg_risk >= 40:

    st.warning(
        "🟡 MEDIUM RISK CUSTOMER"
    )


else:

    st.success(
        "🟢 LOW RISK CUSTOMER"
    )





# ------------------------------------------------------------
# Transaction History
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "💳 Transaction History"
)



st.dataframe(

    customer_df[

        [

        "transaction_id",

        "transaction_timestamp",

        "amount",

        "merchant_name",

        "transaction_risk_score",

        "is_fraud"

        ]

    ]

    .sort_values(

        "transaction_timestamp",

        ascending=False

    )

    .head(100),

    use_container_width=True

)





# ------------------------------------------------------------
# Transaction Amount Trend
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "📈 Customer Transaction Trend"
)



trend = (

    customer_df

    .groupby(

        customer_df["transaction_timestamp"]

        .dt.date

    )

    ["amount"]

    .sum()

    .reset_index()

)



trend.columns = [

    "Date",

    "Amount"

]



fig1 = px.line(

    trend,

    x="Date",

    y="Amount",

    markers=True,

    title="Customer Spending Pattern"

)



st.plotly_chart(

    fig1,

    use_container_width=True

)





# ------------------------------------------------------------
# Merchant Interaction
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "🏪 Merchant Interaction Analysis"
)



merchant = (

    customer_df

    .groupby(

        "merchant_category"

    )

    .size()

    .reset_index(

        name="Transactions"

    )

    .sort_values(

        "Transactions",

        ascending=False

    )

)



fig2 = px.bar(

    merchant,

    x="merchant_category",

    y="Transactions",

    text="Transactions",

    title="Customer Merchant Categories"

)



st.plotly_chart(

    fig2,

    use_container_width=True

)





# ------------------------------------------------------------
# Fraud Analysis
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "🚨 Customer Fraud Analysis"
)



fraud_history = (

    customer_df

    [
        customer_df["is_fraud"]==1
    ]

)



if len(fraud_history) > 0:


    st.warning(

        f"{len(fraud_history)} fraudulent transactions detected"

    )


    st.dataframe(

        fraud_history,

        use_container_width=True

    )


else:


    st.success(

        "No fraudulent transactions detected"

    )





# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------


st.markdown("---")


st.success(
"""
✅ Customer 360 Risk Intelligence Ready

Customer Profiling + Fraud History + Exposure Analysis
"""
)