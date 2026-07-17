# ============================================================
# Page 4: AML Monitoring System
# Enterprise Financial Crime Platform
# ============================================================


import streamlit as st
import pandas as pd
import plotly.express as px



# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------


st.set_page_config(

    page_title="AML Monitoring",

    page_icon="🕵️",

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
    "🕵️ AI-Powered AML Monitoring System"
)


st.markdown(
"""
Anti-Money Laundering transaction monitoring platform.

Detects:

- Suspicious transactions
- Unusual customer behavior
- High-risk activity
- Potential financial crime cases
"""
)


st.markdown("---")



# ------------------------------------------------------------
# AML Rule Engine
# ------------------------------------------------------------


st.subheader(
    "⚙️ AML Rule Engine"
)



def aml_rule_engine(row):


    rules = []



    # Rule 1: High value transaction

    if row["amount"] > 500000:

        rules.append(
            "Large Transaction"
        )



    # Rule 2: High risk customer

    if row["customer_risk"] == "High":

        rules.append(
            "High Risk Customer"
        )



    # Rule 3: Cross border transaction

    if row["cross_border"] == 1:

        rules.append(
            "Cross Border Activity"
        )



    # Rule 4: High merchant risk

    if row["merchant_risk_score"] > 80:

        rules.append(
            "High Risk Merchant"
        )



    return ", ".join(rules)



df["AML_Rules_Triggered"] = df.apply(

    aml_rule_engine,

    axis=1

)



# ------------------------------------------------------------
# Suspicious Activity Detection
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "🚨 Suspicious Activity Detection"
)



aml_alerts = (

    df[

        df["AML_Rules_Triggered"] != ""

    ]

)



st.success(

    f"Detected {len(aml_alerts):,} suspicious activities"

)



# ------------------------------------------------------------
# AML KPIs
# ------------------------------------------------------------


col1,col2,col3,col4 = st.columns(4)



col1.metric(

    "Total Alerts",

    f"{len(aml_alerts):,}"

)



col2.metric(

    "High Value Cases",

    f"{(df['amount']>500000).sum():,}"

)



col3.metric(

    "Cross Border Alerts",

    f"{(df['cross_border']==1).sum():,}"

)



col4.metric(

    "Merchant Risk Alerts",

    f"{(df['merchant_risk_score']>80).sum():,}"

)





# ------------------------------------------------------------
# SAR Investigation Queue
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "📋 SAR Investigation Queue"
)



sar_columns = [

    "transaction_id",

    "sender_customer_id",

    "amount",

    "customer_city",

    "merchant_name",

    "AML_Rules_Triggered",

    "transaction_risk_score"

]



sar_queue = (

    aml_alerts[sar_columns]

    .sort_values(

        "transaction_risk_score",

        ascending=False

    )

)



st.dataframe(

    sar_queue.head(100),

    use_container_width=True

)





# ------------------------------------------------------------
# AML Rule Distribution
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "📊 AML Alert Pattern Analysis"
)



rule_counts = (

    aml_alerts["AML_Rules_Triggered"]

    .value_counts()

    .reset_index()

)



rule_counts.columns = [

    "AML Rule",

    "Alert Count"

]



fig1 = px.bar(

    rule_counts,

    x="AML Rule",

    y="Alert Count",

    text="Alert Count",

    title="Most Common AML Triggers"

)



st.plotly_chart(

    fig1,

    use_container_width=True

)





# ------------------------------------------------------------
# Customer Suspicious Activity
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "👤 Customer Suspicious Activity Ranking"
)



customer_alerts = (

    aml_alerts

    .groupby(
        "sender_customer_id"
    )

    .size()

    .reset_index(

        name="Alert Count"

    )

    .sort_values(

        "Alert Count",

        ascending=False

    )

)



fig2 = px.bar(

    customer_alerts.head(10),

    x="sender_customer_id",

    y="Alert Count",

    text="Alert Count",

    title="Customers With Highest AML Alerts"

)



st.plotly_chart(

    fig2,

    use_container_width=True

)





# ------------------------------------------------------------
# Download SAR Report
# ------------------------------------------------------------


st.markdown("---")


st.subheader(
    "📥 Export SAR Report"
)



csv = sar_queue.to_csv(

    index=False

)



st.download_button(

    label="Download SAR Investigation File",

    data=csv,

    file_name="AML_SAR_Report.csv",

    mime="text/csv"

)





st.markdown("---")


st.success(
"""
✅ AML Monitoring System Active

Financial Crime Rules + Suspicious Activity Detection + SAR Workflow
"""
)