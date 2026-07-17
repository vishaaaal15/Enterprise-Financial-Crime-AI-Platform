# ============================================================
# Page 2: AI Fraud Prediction Engine
# Enterprise Financial Crime Platform
# ============================================================


import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder



# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(

    page_title="Fraud Prediction Engine",

    page_icon="🚨",

    layout="wide"

)



# ------------------------------------------------------------
# Load ML Model
# ------------------------------------------------------------


@st.cache_resource
def load_model():

    model = joblib.load(
        "models/fraud_detection_xgboost.pkl"
    )

    return model



model = load_model()



# ------------------------------------------------------------
# Header
# ------------------------------------------------------------


st.title(
    "🚨 AI Fraud Detection Prediction Engine"
)


st.markdown(
"""
Machine Learning powered fraud detection system.

Pipeline:

Transaction Data → Feature Processing → XGBoost Model → Fraud Risk Score
"""
)



st.markdown("---")



# ------------------------------------------------------------
# Upload Transaction File
# ------------------------------------------------------------


st.subheader(
    "📂 Upload Transaction Dataset"
)



uploaded_file = st.file_uploader(

    "Upload CSV file",

    type=["csv"]

)



if uploaded_file is not None:



    df = pd.read_csv(
        uploaded_file
    )


    st.success(
        "✅ File uploaded successfully"
    )



    st.subheader(
        "Transaction Preview"
    )


    st.dataframe(
        df.head()
    )



    # --------------------------------------------------------
    # Data Preparation
    # --------------------------------------------------------


    st.markdown("---")


    st.subheader(
        "⚙️ Feature Preparation"
    )



    prediction_df = df.copy()



    # Remove target/leakage columns

    drop_columns = [

        "is_fraud",

        "fraud_type",

        "aml_rule",

        "transaction_risk_score"

    ]



    prediction_df = prediction_df.drop(

        columns=[

            col for col in drop_columns

            if col in prediction_df.columns

        ]

    )



    # Encode categorical columns


    encoder = LabelEncoder()



    categorical_columns = (

        prediction_df

        .select_dtypes(
            include="object"
        )

        .columns

    )



    for col in categorical_columns:


        prediction_df[col] = encoder.fit_transform(

            prediction_df[col]
            .astype(str)

        )



    # Handle missing values


    prediction_df = prediction_df.fillna(0)



    st.success(
        "✅ Data preprocessing completed"
    )





    # --------------------------------------------------------
    # Fraud Prediction
    # --------------------------------------------------------


    st.markdown("---")


    st.subheader(
        "🤖 Model Prediction"
    )



    predictions = model.predict(

        prediction_df

    )



    probabilities = model.predict_proba(

        prediction_df

    )[:,1]





    # --------------------------------------------------------
    # Result Creation
    # --------------------------------------------------------


    result_df = df.copy()



    result_df["Fraud Prediction"] = predictions



    result_df["Fraud Probability (%)"] = (

        probabilities * 100

    ).round(2)



    result_df["Risk Level"] = (

        result_df["Fraud Probability (%)"]

        .apply(

            lambda x:

            "🔴 HIGH RISK"

            if x >= 80

            else

            "🟡 MEDIUM RISK"

            if x >=40

            else

            "🟢 LOW RISK"

        )

    )



    st.success(
        "✅ Fraud detection completed"
    )





    # --------------------------------------------------------
    # Risk KPIs
    # --------------------------------------------------------


    st.markdown("---")


    st.subheader(
        "📊 Prediction Summary"
    )



    total_transactions = len(result_df)



    fraud_cases = (

        result_df["Fraud Prediction"]

        .sum()

    )



    fraud_percentage = (

        fraud_cases /

        total_transactions *

        100

    )



    high_risk_cases = (

        result_df["Risk Level"]

        .value_counts()

        .get(

            "🔴 HIGH RISK",

            0

        )

    )



    col1,col2,col3,col4 = st.columns(4)



    col1.metric(

        "Total Transactions",

        f"{total_transactions:,}"

    )


    col2.metric(

        "Fraud Detected",

        f"{fraud_cases:,}"

    )


    col3.metric(

        "Fraud Rate",

        f"{fraud_percentage:.2f}%"

    )


    col4.metric(

        "High Risk Cases",

        f"{high_risk_cases:,}"

    )





    # --------------------------------------------------------
    # Investigation Queue
    # --------------------------------------------------------


    st.markdown("---")


    st.subheader(
        "🚨 Fraud Investigation Queue"
    )



    fraud_cases_df = (

        result_df[

            result_df["Fraud Prediction"] == 1

        ]

        .sort_values(

            "Fraud Probability (%)",

            ascending=False

        )

    )



    st.dataframe(

        fraud_cases_df.head(100)

    )





    # --------------------------------------------------------
    # Download Report
    # --------------------------------------------------------


    st.markdown("---")


    st.subheader(
        "📥 Export Investigation Report"
    )



    csv = fraud_cases_df.to_csv(

        index=False

    )



    st.download_button(

        label="Download Fraud Report",

        data=csv,

        file_name="fraud_investigation_report.csv",

        mime="text/csv"

    )



else:


    st.info(
        "Upload transaction CSV file to start fraud prediction"
    )