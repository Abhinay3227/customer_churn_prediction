import streamlit as st

st.set_page_config(layout="wide")

# GLOBAL STYLE
st.markdown("""
<style>
.stApp {background-color:#f8fafc;}

.navbar {
    background:#0f172a;
    padding:15px;
    border-radius:10px;
    margin-bottom:20px;
}
.navbar h1 {color:white;margin:0;}
.navbar p {color:#cbd5f5;margin:0;font-size:14px;}

.card {
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
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
.stButton>button:hover {
    background:#2563eb;
}

[data-testid="stSidebar"] {
    background:#1e293b;
}
[data-testid="stSidebar"] * {
    color:white;
}
</style>
""", unsafe_allow_html=True)

# NAVBAR
st.markdown("""
<div class="navbar">
<h1>📊 Customer Churn Intelligence System</h1>
<p>Predict • Explain • Retain Customers</p>
</div>
""", unsafe_allow_html=True)

st.info("👈 Navigate using sidebar")