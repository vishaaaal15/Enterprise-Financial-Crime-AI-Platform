import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Merchant Intelligence",
    page_icon="🏪",
    layout="wide"
)


@st.cache_data
def load_data():

    df = pd.read_csv(
        r"C:\Users\vshal\data\processed\transactions_v2.csv"
    )

    return df


df = load_data()



st.title(
    "🏪 Merchant Risk Intelligence Platform"
)


st.markdown(
"""
Analyze merchant fraud exposure and suspicious merchant behavior.
"""
)


st.markdown("---")


# Merchant KPIs

merchant_total = df["merchant_name"].nunique()


fraud_merchants = (

    df[df["is_fraud"]==1]
    ["merchant_name"]
    .nunique()

)


avg_merchant_risk = (

    df["merchant_risk_score"]
    .mean()

)


col1,col2,col3 = st.columns(3)


col1.metric(
    "Total Merchants",
    f"{merchant_total:,}"
)


col2.metric(
    "Fraud Merchants",
    f"{fraud_merchants:,}"
)


col3.metric(
    "Average Merchant Risk",
    f"{avg_merchant_risk:.2f}"
)



# Merchant Ranking

st.markdown("---")

st.subheader(
    "🚨 Highest Fraud Risk Merchants"
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

    .head(20)

)



fig1 = px.bar(

    merchant_risk,

    x="merchant_name",

    y="Fraud Count",

    title="Merchant Fraud Ranking"

)


st.plotly_chart(
    fig1,
    use_container_width=True
)



# Category Risk


st.markdown("---")

st.subheader(
    "📊 Merchant Category Risk"
)



category = (

    df.groupby(
        "merchant_category"
    )
    ["is_fraud"]
    .mean()
    .reset_index()

)


category["Fraud Rate %"] = (

    category["is_fraud"]*100

)



fig2 = px.bar(

    category,

    x="merchant_category",

    y="Fraud Rate %",

    title="Category Fraud Rate"

)


st.plotly_chart(
    fig2,
    use_container_width=True
)



# Merchant Table


st.markdown("---")

st.subheader(
    "📋 Merchant Investigation Queue"
)


st.dataframe(

    merchant_risk,

    use_container_width=True

)


st.success(
"✅ Merchant Intelligence Module Ready"
)