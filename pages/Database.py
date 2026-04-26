import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(layout="wide")

st.title("🗄️ Stored Predictions")

conn = mysql.connector.connect(
    host="localhost",
    user="tricare",
    password="02092002t",
    database="churn_db"
)

df = pd.read_sql("SELECT * FROM predictions ORDER BY id DESC", conn)

st.markdown("### 📊 Customer Records")

st.dataframe(df)