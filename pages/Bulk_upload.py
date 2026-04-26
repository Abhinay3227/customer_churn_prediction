import streamlit as st
import pandas as pd
import pickle

st.set_page_config(layout="wide")

st.title("📁 Bulk Prediction")

model = pickle.load(open("churn_model.pkl","rb"))
scaler = pickle.load(open("churn_scaler.pkl","rb"))
columns = pickle.load(open("model_columns.pkl","rb"))

file = st.file_uploader("Upload CSV")

if file:
    df = pd.read_csv(file)

    st.markdown("### 👀 Preview")
    st.dataframe(df.head())

    df_proc = pd.get_dummies(df)
    df_proc = df_proc.reindex(columns=columns, fill_value=0)

    df_scaled = scaler.transform(df_proc)
    df["Prediction"] = model.predict(df_scaled)

    st.markdown("### 📊 Results")
    st.dataframe(df)

    st.download_button("⬇ Download Results", df.to_csv(index=False))