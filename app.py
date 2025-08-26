import streamlit as st, sys, platform

st.set_page_config(page_title="NFL Model — Hello", layout="wide")

st.write("✅ App is alive.")
st.write("Python:", sys.version)
st.write("Platform:", platform.platform())

st.link_button("⬅️ Back to Home", "https://lineupwire.com")
