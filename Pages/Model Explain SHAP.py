# ============================================================
# AI Model Explainability Dashboard (SHAP)
# ============================================================

import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder

# ------------------------------------------------------------
# Page Config
# ------------------------------------------------------------

st.set_page_config(
    page_title="AI Model Explainability",
    page_icon="🧠",
    layout="wide"
)

# ------------------------------------------------------------
# Load Model
# ------------------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("models/fraud_detection_xgboost.pkl")

model = load_model()

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
# Create Date Features (if missing)
# ------------------------------------------------------------

if "transaction_timestamp" in df.columns:

    df["transaction_timestamp"] = pd.to_datetime(
        df["transaction_timestamp"]
    )

    if "year" not in df.columns:
        df["year"] = df["transaction_timestamp"].dt.year

    if "month" not in df.columns:
        df["month"] = df["transaction_timestamp"].dt.month

    if "day" not in df.columns:
        df["day"] = df["transaction_timestamp"].dt.day

    if "hour" not in df.columns:
        df["hour"] = df["transaction_timestamp"].dt.hour

    if "day_of_week" not in df.columns:
        df["day_of_week"] = df["transaction_timestamp"].dt.dayofweek

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.title("🧠 AI Model Explainability Dashboard")
st.write("Explain how the XGBoost model detects fraudulent transactions.")

st.markdown("---")

# ------------------------------------------------------------
# Prepare Features
# ------------------------------------------------------------

X = df.drop(
    columns=[
        "is_fraud",
        "fraud_type",
        "aml_rule",
        "transaction_risk_score",
        "transaction_timestamp"      # Remove timestamp after extracting features
    ],
    errors="ignore"
)

# ------------------------------------------------------------
# Encode Categorical Features
# ------------------------------------------------------------

categorical_cols = X.select_dtypes(include="object").columns

for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

# Convert bool → int

for col in X.select_dtypes(include="bool").columns:
    X[col] = X[col].astype(int)

# Fill missing values

X = X.fillna(0)

# ------------------------------------------------------------
# Match Model Features
# ------------------------------------------------------------

try:

    expected_features = model.get_booster().feature_names

    if expected_features:

        # Add any missing columns
        for col in expected_features:
            if col not in X.columns:
                X[col] = 0

        # Keep only expected columns in the same order
        X = X[expected_features]

except Exception:
    pass

# ------------------------------------------------------------
# Debug Information
# ------------------------------------------------------------

st.subheader("📋 Model Information")

st.write("Dataset Features:", X.shape[1])

try:
    st.write("Model Features:", model.n_features_in_)
except:
    pass

# ------------------------------------------------------------
# Sample Data
# ------------------------------------------------------------

X_sample = X.sample(
    min(500, len(X)),
    random_state=42
)

# ------------------------------------------------------------
# SHAP Explainability
# ------------------------------------------------------------

st.markdown("---")
st.subheader("🔍 Global Feature Importance")

try:

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_sample)

    fig = plt.figure(figsize=(12,7))

    shap.summary_plot(
        shap_values,
        X_sample,
        show=False
    )

    st.pyplot(fig)

    plt.close()

    st.markdown("---")

    st.subheader("📊 Top Fraud Drivers")

    fig = plt.figure(figsize=(12,7))

    shap.summary_plot(
        shap_values,
        X_sample,
        plot_type="bar",
        show=False
    )

    st.pyplot(fig)

    plt.close()

    importance = np.abs(shap_values).mean(axis=0)

    importance_df = pd.DataFrame({

        "Feature": X_sample.columns,
        "SHAP Importance": importance

    }).sort_values(
        "SHAP Importance",
        ascending=False
    )

    st.markdown("---")

    st.subheader("🏦 Top 10 Important Features")

    st.dataframe(
        importance_df.head(10),
        use_container_width=True
    )

    st.success("✅ SHAP Explainability Completed Successfully")

except Exception as e:

    st.error("SHAP Error")

    st.code(str(e))