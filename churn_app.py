import base64
import streamlit as st

st.set_page_config(layout="wide")

# ---------- BACKGROUND (HERO) ----------
def set_bg(image_path="bg.png"):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    /* Main app background */
    .stApp {{
        background: #0f172a;
    }}

    /* HERO SECTION */
    .hero {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        border-radius: 18px;
        padding: 60px 40px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }}

    /* Dark overlay on image */
    .hero::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: rgba(15, 23, 42, 0.75);
    }}

    .hero-content {{
        position: relative;
        z-index: 2;
        color: white;
    }}

    /* Navbar */
    .navbar {{
        background:#0f172a;
        padding:15px;
        border-radius:10px;
        margin-bottom:20px;
    }}

    .navbar h1 {{
        color:white;
        margin:0;
    }}

    .navbar p {{
        color:#cbd5f5;
        margin:0;
        font-size:14px;
    }}

    /* Cards */
    .card {{
        background:white;
        padding:20px;
        border-radius:12px;
        box-shadow:0px 4px 15px rgba(0,0,0,0.1);
        text-align:center;
    }}

    .card h3 {{
        margin-bottom:10px;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background:#1e293b;
    }}

    [data-testid="stSidebar"] * {{
        color:white;
    }}

    </style>
    """, unsafe_allow_html=True)

set_bg()

# ---------- NAVBAR ----------
st.markdown("""
<div class="navbar">
    <h1>📊 Customer Churn Intelligence System</h1>
    <p>Predict • Explain • Retain Customers</p>
</div>
""", unsafe_allow_html=True)

# ---------- HERO SECTION ----------
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>Customer Churn Prediction System</h1>
        <p style="font-size:18px;">
        Leverage machine learning to predict churn, analyze customer behavior,
        and take proactive actions to improve retention.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- STATS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card"><h3>👥 1000+</h3><p>Customers Analyzed</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h3>🎯 95%</h3><p>Prediction Accuracy</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card"><h3>⚡ 24/7</h3><p>Real-time Insights</p></div>', unsafe_allow_html=True)

# ---------- FEATURES ----------
st.markdown("### 🚀 Features")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="card"><h3>🤖 AI Prediction</h3><p>Accurate churn prediction using ML</p></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card"><h3>📊 Data Insights</h3><p>Visual analytics & trends</p></div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card"><h3>⚡ Smart Actions</h3><p>Retention strategies</p></div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card"><h3>🗄️ Data Management</h3><p>Store & manage predictions</p></div>', unsafe_allow_html=True)

st.info("👈 Use sidebar to navigate")