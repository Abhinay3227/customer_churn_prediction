import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(layout="wide")

st.title("🗄️ Stored Predictions")

conn = mysql.connector.connect(
    host=st.secrets["DB_HOST"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASS"],
    database=st.secrets["DB_NAME"],
    port=st.secrets["DB_PORT"]
)

cursor = conn.cursor()

df = pd.read_sql("SELECT * FROM predictions ORDER BY id DESC", conn)
st.dataframe(df)

st.markdown("### 📊 Customer Records")

st.dataframe(df)