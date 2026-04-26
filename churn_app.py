import base64
import streamlit as st

st.set_page_config(layout="wide")

def set_bg():
    with open("bg.png", "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    .overlay {{
        background: rgba(15, 23, 42, 0.75);
        padding: 40px;
        border-radius: 15px;
    }}

    .navbar {{
        background:#0f172a;
        padding:15px;
        border-radius:10px;
        margin-bottom:20px;
    }}
    .navbar h1 {{color:white;margin:0;}}
    .navbar p {{color:#cbd5f5;margin:0;font-size:14px;}}

    .card {{
        background:white;
        padding:20px;
        border-radius:12px;
        box-shadow:0px 2px 10px rgba(0,0,0,0.08);
        margin-bottom:15px;
    }}

    .stButton>button {{
        background:#3b82f6;
        color:white;
        border-radius:8px;
    }}

    [data-testid="stSidebar"] {{
        background:#1e293b;
    }}
    [data-testid="stSidebar"] * {{
        color:white;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg()