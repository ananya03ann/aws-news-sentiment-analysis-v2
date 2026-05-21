
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

# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("📰 Dashboard Menu")

menu = st.sidebar.radio(
    "Navigation",
    ["View News", "Analytics"]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
Sentiment score indicates whether
the news article sentiment is positive,
negative, or neutral.

Positive score = Positive news
Negative score = Negative news
"""
)

# ==============================
# POSTGRESQL DATABASE CONNECTION
# ==============================

DB_HOST = "database-1.c3qm2yq0clyo.ap-south-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "newsdb"
DB_USER = "postgres"
DB_PASSWORD = "postgres-123"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)