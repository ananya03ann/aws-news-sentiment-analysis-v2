
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="News Sentiment Dashboard",
    page_icon="📰",
    layout="wide"
)

# ==============================
# CUSTOM CSS
# ==============================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="metric-container"] {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #333;
}

</style>
""", unsafe_allow_html=True)