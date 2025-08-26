import streamlit as st, sys, platform
st.set_page_config(page_title="NFL Hello", layout="wide")
st.title("🏈 NFL Test App")
st.write("✅ App is alive.")
st.write("Python:", sys.version)
st.write("Platform:", platform.platform())
st.link_button("⬅️ Back to Home", "https://lineupwire.com")
