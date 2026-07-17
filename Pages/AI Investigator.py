# ============================================================
# AI Investigation Assistant - Gemini Powered
# Financial Crime Analytics Platform
# ============================================================

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai


# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="AI Investigation Assistant",
    page_icon="🤖",
    layout="wide"
)


# ------------------------------------------------------------
# Load Environment
# ------------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_KEY")


if API_KEY is None:

    st.error(
        "Gemini API Key not found. Add GEMINI_API_KEY in .env file."
    )

    st.stop()


client = genai.Client(
    api_key=API_KEY
)


# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

@st.cache_data
def load_data():

    return pd.read_csv(
        r"C:\Users\vshal\data\processed\transactions_v2.csv"
    )


df = load_data()


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.title("🤖 AI Investigation Assistant")

st.markdown(
"""
Generate AI-powered financial crime investigation reports
using transaction intelligence, fraud risk indicators,
and Gemini LLM analysis.
"""
)


st.markdown("---")


# ------------------------------------------------------------
# Transaction Selection
# ------------------------------------------------------------

st.subheader("🔎 Select Transaction")


transaction_id = st.selectbox(
    "Choose Transaction ID",
    df["transaction_id"].astype(str)
)


transaction = df[
    df["transaction_id"].astype(str) == transaction_id
].iloc[0]



# ------------------------------------------------------------
# Transaction Details
# ------------------------------------------------------------

st.markdown("---")

st.subheader("💳 Transaction Details")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Transaction ID",
        transaction["transaction_id"]
    )

    st.metric(
        "Amount",
        f"{transaction['amount']}"
    )

    st.metric(
        "Payment Channel",
        transaction["payment_channel"]
    )


with col2:

    st.metric(
        "Customer Risk",
        transaction["customer_risk"]
    )

    st.metric(
        "Merchant Risk",
        transaction["merchant_risk_score"]
    )

    st.metric(
        "Device Risk",
        transaction["device_risk_score"]
    )


with col3:

    st.metric(
        "Transaction Risk",
        transaction["transaction_risk_score"]
    )

    st.metric(
        "Fraud Status",
        "Fraud" if transaction["is_fraud"] == 1 else "Normal"
    )

    st.metric(
        "Cross Border",
        transaction["cross_border"]
    )


# ------------------------------------------------------------
# Build AI Prompt
# ------------------------------------------------------------


prompt = f"""

You are a Financial Crime Investigation Analyst working for a global bank.

Analyze this suspicious transaction.

Transaction Details:

Transaction ID:
{transaction['transaction_id']}

Amount:
{transaction['amount']}

Merchant:
{transaction['merchant_name']}

Merchant Category:
{transaction['merchant_category']}

Customer Risk:
{transaction['customer_risk']}

Merchant Risk Score:
{transaction['merchant_risk_score']}

Device Risk Score:
{transaction['device_risk_score']}

Transaction Risk Score:
{transaction['transaction_risk_score']}

Payment Channel:
{transaction['payment_channel']}

Transaction Type:
{transaction['transaction_type']}

Cross Border:
{transaction['cross_border']}

Fraud Prediction:
{"Fraud" if transaction['is_fraud']==1 else "Normal"}


Generate a professional banking investigation report.

Include:

1. Executive Summary

2. Key Fraud Risk Factors

3. AML Considerations

4. Investigation Recommendations

5. Business Impact Assessment

6. Final Risk Decision


Use professional financial crime analyst language.
Use bullet points.
"""


# ------------------------------------------------------------
# Generate Report
# ------------------------------------------------------------


st.markdown("---")


if st.button(
    "🚀 Generate Investigation Report"
):

    with st.spinner(
        "Gemini is analyzing transaction..."
    ):


        try:

            response = client.models.generate_content(

                model="gemini-2.0-flash",

                contents=prompt

            )


            report = response.text


            st.subheader(
                "📄 AI Investigation Report"
            )


            st.markdown(
                report
            )


            st.success(
                "✅ Investigation Report Generated"
            )


        except Exception as e:


            st.error(
                "Gemini API Error"
            )

            st.code(
                str(e)
            )



# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.markdown("---")

st.info(
"""
AI Investigation Assistant combines:
    
✓ Transaction Intelligence

✓ Fraud Risk Analytics

✓ AML Monitoring

✓ Generative AI Investigation Support

✓ Analyst Decision Assistance
"""
)