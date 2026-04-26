import streamlit as st
import pickle
import pandas as pd
import mysql.connector

st.set_page_config(layout="wide")

st.markdown("""
<style>
.stApp {background-color:#f8fafc;}

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

model = pickle.load(open("churn_model.pkl", "rb"))
scaler = pickle.load(open("churn_scaler.pkl", "rb"))
columns = pickle.load(open("model_columns.pkl", "rb"))

conn = mysql.connector.connect(
    host=st.secrets["DB_HOST"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASS"],
    database=st.secrets["DB_NAME"],
    port=3306
)
cursor = conn.cursor()

st.title("🤖 Customer Churn Prediction")
st.markdown("### 🧾 Customer Details")

col1, col2 = st.columns(2)

with col1:
    tenure = st.number_input("Tenure (Months)", 0, 100)
    monthly = st.number_input("Monthly Charges")
    total = st.number_input("Total Charges")

    senior_option = st.selectbox("Senior Citizen", ["Select", "No", "Yes"])
    partner = st.selectbox("Partner", ["Select", "No", "Yes"])
    dependents = st.selectbox("Dependents", ["Select", "No", "Yes"])

with col2:
    phone = st.selectbox("Phone Service", ["Select", "No", "Yes"])
    internet = st.selectbox("Internet Service", ["Select", "DSL", "Fiber optic", "No"])
    contract = st.selectbox("Contract Type", ["Select", "Month-to-month", "One year", "Two year"])
    paperless = st.selectbox("Paperless Billing", ["Select", "No", "Yes"])

if st.button("🚀 Predict Churn"):

    if "Select" in [senior_option, partner, dependents, phone, internet, contract, paperless]:
        st.warning("⚠ Please fill all fields")

    else:
        senior = 1 if senior_option == "Yes" else 0

        sample = pd.DataFrame({
            "SeniorCitizen": [senior],
            "tenure": [tenure],
            "MonthlyCharges": [monthly],
            "TotalCharges": [total],
            "Partner": [partner],
            "Dependents": [dependents],
            "PhoneService": [phone],
            "InternetService": [internet],
            "Contract": [contract],
            "PaperlessBilling": [paperless]
        })

        sample = pd.get_dummies(sample)
        sample = sample.reindex(columns=columns, fill_value=0)
        sample_scaled = scaler.transform(sample)

        pred = model.predict(sample_scaled)[0]
        prob = model.predict_proba(sample_scaled)[0][1]

        st.markdown("### 📊 Prediction Result")

        if pred == 1:
            st.markdown(f"<div class='result-red'>⚠ Customer Likely to Churn ({prob*100:.2f}%)</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-green'>✅ Customer Will Stay ({(1-prob)*100:.2f}%)</div>", unsafe_allow_html=True)

        cursor.execute("""
            INSERT INTO predictions (tenure, monthly, total, contract, prediction, probability)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (tenure, monthly, total, contract, int(pred), float(prob)))

        conn.commit()

        if pred == 1:
            st.markdown("### 🔍 Why Customer May Churn")

            reasons = []

            if tenure < 12:
                reasons.append("Customer is new (low tenure)")
            if monthly > 80:
                reasons.append("High monthly charges")
            if "month" in contract.lower():
                reasons.append("No long-term contract")
            if "fiber" in internet.lower():
                reasons.append("Expensive internet service")

            for r in reasons:
                st.write("•", r)

            st.markdown("### 🔬 AI Insights")

            insights = []

            if monthly > 80:
                insights.append(("🔺", "High charges increase churn risk"))
            else:
                insights.append(("🔻", "Affordable charges reduce churn risk"))

            if tenure < 12:
                insights.append(("🔺", "Short tenure increases churn"))
            else:
                insights.append(("🔻", "Long-term customers are stable"))

            if "month" in contract.lower():
                insights.append(("🔺", "Month-to-month contract is risky"))
            else:
                insights.append(("🔻", "Long-term contract reduces churn"))

            if "fiber" in internet.lower():
                insights.append(("🔺", "Fiber users tend to churn more"))

            for icon, msg in insights:
                st.write(icon, msg)

            st.markdown("### 💡 Suggested Actions")

            if monthly > 80:
                st.info("Offer discount or cheaper plan")

            if "month" in contract.lower():
                st.info("Encourage long-term contract")

            if tenure < 12:
                st.info("Provide onboarding support")