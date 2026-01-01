import streamlit as st

# Try to get from Streamlit secrets first
try:
    api_key = st.secrets["TAVILY_API_KEY"]
except Exception:
    # Fallback to env var (for local dev)
    api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY not found in secrets or environment variables")
