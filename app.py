import pandas as pd
import streamlit as st
import requests
from io import StringIO

# --- CONFIG (your IDs) ---
SHEET_ID = "1gMJFoat1UJAEV73AXWTbFLppJeOrMBLuokF9c28fc"   # your Google Sheet ID
GID = "0"                                                # gid for the Model tab
CSV_URL = f"https://docs.google.com/spreadsheets/d/1gMJFoat1UJAEV73AXWTbFLppJeOrMBLuokF9c28fc/export?format=csv&gid=0"
HOME_URL = "https://lineupwire.com"                      # back-to-home link

st.set_page_config(page_title="NFL Daily Model — LineupWire", layout="wide")

# Top bar: Back button + Title
left, right = st.columns([1, 8])
with left:
    # Use link_button if available; otherwise simple markdown link
    try:
        st.link_button("⬅️ Back to Home", HOME_URL, type="primary")
    except Exception:
        st.markdown(f"[⬅️ Back to Home]({HOME_URL})")
with right:
    st.markdown("## 🏈 NFL Daily Model")

st.caption("Source: Google Sheet (Model tab)")

@st.cache_data(ttl=300)
def load_csv(url: str) -> pd.DataFrame:
    r = requests.get(url, timeout=20)
    r.raise_for_status()  # bubble up 403/404
    data = r.content.decode("utf-8", "ignore")
    df = pd.read_csv(StringIO(data))
    return df

# load & show
try:
    df = load_csv(CSV_URL)
except Exception as e:
    st.error(f"Could not load Google Sheet CSV.\n\n**URL:** {CSV_URL}\n\n**Error:** {e}")
    st.stop()

# If you want a specific column order, list them here; otherwise show all
preferred_cols = [
    "Date","Time","Away Team","Home Team","Away Score","Home Score",
    "ML %","Spread","# Model Spread","Total","Model Total","Edge","Spread Edge","Total Edge",
]
cols = [c for c in preferred_cols if c in df.columns]
view = df[cols] if cols else df

st.dataframe(view, use_container_width=True)
