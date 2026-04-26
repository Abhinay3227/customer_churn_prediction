import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Business Dashboard")

data = pd.read_csv("customer_churn.csv")
data['Churn'] = data['Churn'].map({"Yes":1,"No":0})

# KPI CARDS
c1,c2,c3 = st.columns(3)

with c1:
    st.markdown(f"<div class='card'>👥 Total Customers<br><h2>{len(data)}</h2></div>", unsafe_allow_html=True)

with c2:
    st.markdown(f"<div class='card'>📉 Churn Rate<br><h2>{data['Churn'].mean()*100:.2f}%</h2></div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<div class='card'>💰 Avg Charges<br><h2>{data['MonthlyCharges'].mean():.2f}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# CHARTS
col1,col2 = st.columns(2)

with col1:
    fig = px.histogram(data, x="Churn", title="Churn Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.box(data, x="Churn", y="MonthlyCharges", title="Charges vs Churn")
    st.plotly_chart(fig, use_container_width=True)

col3,col4 = st.columns(2)

with col3:
    fig = px.histogram(data, x="Contract", color="Churn", title="Contract Impact")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.box(data, x="Churn", y="tenure", title="Tenure vs Churn")
    st.plotly_chart(fig, use_container_width=True)

# INSIGHTS
st.markdown("### 💡 Key Insights")
st.write("⚡ Month-to-month customers churn more")
st.write("📉 High charges increase churn")
st.write("📊 Low tenure customers are risky")