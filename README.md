# Enterprise Financial Crime Analytics Platform

**Author:** Vishal Singh | [LinkedIn](https://linkedin.com/in/vishal-singhdataanalyst) | [GitHub](https://github.com/vishaaaal15)
**Stack:** Python · SQL · XGBoost · SHAP · Streamlit · Plotly · Google Gemini API
**Dataset:** 200,000+ simulated financial transactions
**Domain:** Fraud Detection · Explainable AI · Risk Analytics

---

## Project Overview

An AI-powered financial crime analytics platform for detecting suspicious transactions, monitoring AML risk, and supporting investigator decision-making through machine learning and interactive dashboards. Built as an interactive Streamlit application combining fraud prediction, customer intelligence, AML monitoring, and explainable AI in one tool.

---

## How It Works

1. **Data pipeline** — processes 200,000+ synthetic banking transactions, including data cleaning, feature engineering, and risk scoring to surface high-risk activity. Generate a synthetic demo dataset with `create_demo_dataset.py`, or upload your own transaction file via the Streamlit UI.
2. **Fraud scoring** — an XGBoost classifier scores each transaction for fraud probability.
3. **Explainability** — SHAP values show which features drove each prediction, giving compliance teams interpretable, transparent risk predictions rather than a black-box score.
4. **Dashboards** — Python, SQL, and Plotly visualizations covering fraud trends, customer risk profiles, transaction patterns, and operational KPIs for business users.
5. **AI-generated summary** — the Google Gemini API converts model output into a readable risk summary for a non-technical reader.
6. **Multi-page app** — results are organized across Streamlit pages (risk overview, flagged transactions, customer intelligence, explainability view).

*A FastAPI REST layer for these predictions is in development locally and will be added to this repo once pushed.*

---

## Repository Structure

```
Enterprise-Financial-Crime-AI-Platform/
│
├── Data/                     # Sample / generated transaction data
├── Pages/                    # Additional Streamlit pages (multi-page app)
├── app.py                    # Main Streamlit entry point
├── create_demo_dataset.py    # Generates a synthetic demo dataset to run the app without real data
├── check_gemini_models.py    # Utility script to list available Gemini models for the account in use
├── test_gemini.py            # Basic connectivity test for the Gemini API integration
├── requirements.txt          # Python dependencies
└── .gitignore
```

---

## How to Run

```bash
git clone https://github.com/vishaaaal15/Enterprise-Financial-Crime-AI-Platform
cd Enterprise-Financial-Crime-AI-Platform
pip install -r requirements.txt

# optional: generate a demo dataset if you don't have your own transaction data
python create_demo_dataset.py

# set your Gemini API key (required for the AI summary feature)
export GEMINI_API_KEY="your-key-here"

streamlit run app.py
```

The app will open in your browser. Upload a transaction CSV (or use the generated demo dataset) to see fraud predictions, SHAP explanations, and an AI-generated risk summary.

---

## Model Performance

XGBoost fraud classifier evaluated on a held-out test split of the 200,000+ transaction dataset, reaching approximately 85% accuracy in flagging high-risk transactions. *(Note: replace with your exact test-set metrics — precision/recall/F1 — once you've re-run and confirmed them, so this matches what you report on your resume.)*

---

## Notes

- The Gemini API key is required for the AI-summary feature; the core fraud-detection and SHAP explainability features work without it.
- `check_gemini_models.py` and `test_gemini.py` are development/debugging utilities used while building the Gemini integration, not part of the main app flow.
