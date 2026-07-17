# ============================================================
# AI Investigation Assistant - Gemini Powered
# Enterprise Financial Crime Analytics Platform
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
# Load API Key
# ------------------------------------------------------------

try:
    API_KEY = st.secrets["GEMINI_KEY"]
except Exception:
    load_dotenv()
    API_KEY = os.getenv("GEMINI_KEY")

if not API_KEY:
    st.error("❌ Gemini API Key not found.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

@st.cache_data
def load_data():

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    DATA_PATH = os.path.join(
        BASE_DIR,
        "data",
        "transactions_v2.csv"
    )

    return pd.read_csv(DATA_PATH)

df = load_data()

# ------------------------------------------------------------
# Clean Missing Values
# ------------------------------------------------------------

df["device_risk_score"] = df["device_risk_score"].fillna(0)
df["transaction_risk_score"] = df["transaction_risk_score"].fillna(0)
df["merchant_risk_score"] = df["merchant_risk_score"].fillna(0)
df["customer_risk"] = df["customer_risk"].fillna("Unknown")

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.title("🤖 AI Investigation Assistant")

st.write(
    "Generate AI-powered Financial Crime Investigation Reports "
    "using Gemini AI."
)

st.markdown("---")

# ------------------------------------------------------------
# Select Transaction
# ------------------------------------------------------------

transaction_id = st.selectbox(
    "Select Transaction ID",
    df["transaction_id"].astype(str)
)

transaction = df[
    df["transaction_id"].astype(str) == transaction_id
].iloc[0]

# ------------------------------------------------------------
# Transaction Details
# ------------------------------------------------------------

st.subheader("💳 Transaction Details")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Transaction ID",
        transaction["transaction_id"]
    )

    st.metric(
        "Amount",
        f"₹{transaction['amount']:,.2f}"
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

st.markdown("---")

# ------------------------------------------------------------
# Prompt
# ------------------------------------------------------------

prompt = f"""
You are a Senior Financial Crime Investigation Analyst.

Analyze the following banking transaction.

Transaction ID: {transaction['transaction_id']}

Amount: {transaction['amount']}

Merchant: {transaction['merchant_name']}

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
{"Fraud" if transaction["is_fraud"]==1 else "Normal"}

Generate a professional investigation report.

Include:

1. Executive Summary

2. Fraud Risk Factors

3. AML Considerations

4. Recommended Investigation Actions

5. Business Impact

6. Final Risk Decision

Use professional banking language.
Return markdown bullet points.
"""

# ------------------------------------------------------------
# Generate Report
# ------------------------------------------------------------

if st.button("🚀 Generate Investigation Report"):

    with st.spinner("Analyzing transaction..."):

        try:

            response = client.models.generate_content(

                model="gemini-2.5-flash",

                contents=prompt

            )

            st.subheader("📄 AI Investigation Report")

            st.markdown(response.text)

            st.success(
                "✅ Investigation Report Generated Successfully"
            )

        except Exception as e:

            st.error("Gemini API Error")

            st.code(str(e))

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.markdown("---")

st.info("""
### Enterprise AI Investigation Assistant

✔ Transaction Intelligence

✔ Fraud Risk Analytics

✔ AML Monitoring

✔ Explainable Investigation Support

✔ Generative AI

✔ Banking Decision Assistance
""")