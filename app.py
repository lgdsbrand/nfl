import pandas as pd
import streamlit as st
import requests
from io import StringIO

SHEET_ID = "1gMJFoat1UJAEV73AXWTbFLppJeOrMBLuokF9c28fc"   # <- yours
GID = "0"                                                # <- Model tab gid
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

st.set_page_config(page_title="NFL Model – Debug", layout="wide")
st.title("🏈 NFL Model – Debug")

st.write("CSV URL:", CSV_URL)

try:
    r = requests.get(CSV_URL, timeout=20)
    r.raise_for_status()
    data = r.content.decode("utf-8", "ignore")
    df = pd.read_csv(StringIO(data))
except Exception as e:
    st.error(f"CSV load error: {e}")
    st.stop()

st.write("Rows x Columns:", df.shape)
st.write("Columns:", list(df.columns))
st.dataframe(df, use_container_width=True)
