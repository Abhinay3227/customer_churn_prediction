import streamlit as st
import pickle
import pandas as pd
import numpy as np
import shap
import mysql.connector

st.set_page_config(layout="wide")

# -----------------------------
# UI STYLE
# -----------------------------
st.markdown("""
<style>
.stApp {background-color:#f8fafc;}

.card {
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom:15px;
}

.result-red {
    background:#fee2e2;
    padding:15px;
    border-radius:10px;
    color:#991b1b;
    font-weight:bold;
}

.result-green {
    background:#dcfce7;
    padding:15px;
    border-radius:10px;
    color:#166534;
    font-weight:bold;
}

.stButton>button {
    background:#3b82f6;
    color:white;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD MODEL + DB
# -----------------------------
model = pickle.load(open("churn_model.pkl","rb"))
scaler = pickle.load(open("churn_scaler.pkl","rb"))
columns = pickle.load(open("model_columns.pkl","rb"))

explainer = shap.TreeExplainer(model)

conn = mysql.connector.connect(
    host=st.secrets["DB_HOST"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASS"],
    database=st.secrets["DB_NAME"],
    port=3306
)

cursor = conn.cursor()

# -----------------------------
# TITLE
# -----------------------------
st.title("🤖 Customer Churn Prediction")

# -----------------------------
# FORM (ALL ORIGINAL INPUTS)
# -----------------------------
st.markdown("### 🧾 Customer Details")

col1, col2 = st.columns(2)

with col1:
    tenure = st.number_input("Tenure (Months)", 0, 100)
    monthly = st.number_input("Monthly Charges")
    total = st.number_input("Total Charges")

    senior_option = st.selectbox("Senior Citizen", ["Select","No","Yes"])
    partner = st.selectbox("Partner",["Select","No","Yes"])
    dependents = st.selectbox("Dependents",["Select","No","Yes"])

with col2:
    phone = st.selectbox("Phone Service",["Select","No","Yes"])
    internet = st.selectbox("Internet Service", ["Select","DSL","Fiber optic","No"])
    contract = st.selectbox("Contract Type", ["Select","Month-to-month","One year","Two year"])
    paperless = st.selectbox("Paperless Billing",["Select","No","Yes"])

predict = st.button("🚀 Predict Churn")

# -----------------------------
# RESULT BELOW FORM
# -----------------------------
if predict:

    # VALIDATION (same as before)
    if "Select" in [senior_option, partner, dependents, phone, internet, contract, paperless]:
        st.warning("⚠ Please fill all fields")

    else:
        senior = 1 if senior_option == "Yes" else 0

        # SAME DATA PROCESSING
        sample = pd.DataFrame({
            "SeniorCitizen":[senior],
            "tenure":[tenure],
            "MonthlyCharges":[monthly],
            "TotalCharges":[total],
            "Partner":[partner],
            "Dependents":[dependents],
            "PhoneService":[phone],
            "InternetService":[internet],
            "Contract":[contract],
            "PaperlessBilling":[paperless]
        })

        sample = pd.get_dummies(sample)
        sample = sample.reindex(columns=columns, fill_value=0)
        sample_scaled = scaler.transform(sample)

        pred = model.predict(sample_scaled)[0]
        prob = model.predict_proba(sample_scaled)[0][1]

        # -----------------------------
        # RESULT
        # -----------------------------
        st.markdown("### 📊 Prediction Result")

        if pred == 1:
            st.markdown(f"<div class='result-red'>⚠ Customer Likely to Churn ({prob*100:.2f}%)</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-green'>✅ Customer Will Stay ({(1-prob)*100:.2f}%)</div>", unsafe_allow_html=True)

        # SAVE TO DB (UNCHANGED)
        cursor.execute("""
        INSERT INTO predictions (tenure, monthly, total, contract, prediction, probability)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (tenure, monthly, total, contract, int(pred), float(prob)))

        conn.commit()

        # -----------------------------
        # ONLY FOR CHURN
        # -----------------------------
        if pred == 1:

            # REASONS
            st.markdown("### 🔍 Why Customer May Churn")

            if tenure < 12:
                st.write("• Low tenure (new customer)")
            if monthly > 80:
                st.write("• High monthly charges")
            if "month" in contract.lower():
                st.write("• No long-term contract")
            if "fiber" in internet.lower():
                st.write("• Expensive internet service")

            # -----------------------------
            # SHAP (FIXED VERSION)
            # -----------------------------
            st.markdown("### 🔬 AI Insights")

            shap_values = explainer.shap_values(sample_scaled)

            # Handle classification output
            if isinstance(shap_values, list):
                shap_values = shap_values[1]

            # Convert to numpy
            shap_values = np.array(shap_values)

            # Ensure 1D
            if shap_values.ndim > 1:
                shap_values = shap_values[0]

            # Convert to 1D explicitly
            shap_values = shap_values.flatten()

            # Match lengths safely
            min_len = min(len(columns), len(shap_values))

            shap_df = pd.DataFrame({
                "Feature": columns[:min_len],
                "Impact": shap_values[:min_len]
            })

            # Sort by importance
            shap_df["AbsImpact"] = shap_df["Impact"].abs()
            shap_df = shap_df.sort_values(by="AbsImpact", ascending=False)

            for _, row in shap_df.head(5).iterrows():
                f = row["Feature"]
                impact = row["Impact"]

                if "MonthlyCharges" in f:
                    msg = "High charges increase churn risk"
                elif "tenure" in f:
                    msg = "Short tenure increases churn"
                elif "Contract_Month-to-month" in f:
                    msg = "Month-to-month contract increases churn"
                elif "InternetService_Fiber optic" in f:
                    msg = "Fiber users tend to churn more"
                else:
                    continue

                if impact > 0:
                    st.write("🔺", msg)
                else:
                    st.write("🔻", msg)

            # ACTIONS
            st.markdown("### 💡 Suggested Actions")

            if monthly > 80:
                st.info("Offer discount plan")

            if "month" in contract.lower():
                st.info("Encourage long-term contract")

            if tenure < 12:
                st.info("Improve onboarding support")