import pandas as pd
import streamlit as st
from io import StringIO
import requests

# -----------------------
# CONFIG
# -----------------------
SHEET_ID = "1gMgIFoeaTUIJAEV73AXWTbFLppJeOrMBLuoKF9c28fc"
GID = "PASTE_GID_FOR_NFL_TAB"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

st.set_page_config(page_title="NFL Model - LineupWire", layout="wide")

st.title("🏈 NFL Model — LineupWire")

@st.cache_data(ttl=300)
def load_sheet(url: str) -> pd.DataFrame:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.content.decode("utf-8", errors="ignore")
    df = pd.read_csv(StringIO(data))
    return df

def pick_col(df, candidates, default=None):
    for c in candidates:
        if c in df.columns:
            return c
    return default

try:
    df = load_sheet(CSV_URL)
except Exception as e:
    st.error(f"Could not load Google Sheet. Check sharing & URL.\n\n{e}")
    st.stop()

# Try to find common columns (rename if found)
col_time = pick_col(df, ["Time","Kickoff","Game Time"])
col_away = pick_col(df, ["Away Team","Away"])
col_home = pick_col(df, ["Home Team","Home"])
col_away_score = pick_col(df, ["Away Score","AwayScore","Pred Away"])
col_home_score = pick_col(df, ["Home Score","HomeScore","Pred Home"])
col_model_spread = pick_col(df, ["Model Spread","ModelSpread","Spread (Model)","H-A Spread"])
col_book_spread = pick_col(df, ["Book Spread","BookSpread","Spread (Book)"])
col_model_total = pick_col(df, ["Model Total","ModelTotal"])
col_book_total = pick_col(df, ["Book Total","BookTotal"])
col_ml_pretty = pick_col(df, ["ML %","ML%","Winner % (Pretty)"])
col_total_edge = pick_col(df, ["Total Edge","Edge Total","Model-Book Total"])
col_total_bet = pick_col(df, ["Total Bet","OU Bet","O/U Bet"])
col_spread_edge = pick_col(df, ["Spread Edge","Edge Spread","Model-Book Spread"])
col_spread_bet = pick_col(df, ["Spread Bet","ATS Bet"])

# Light cleanup
if col_time and df[col_time].dtype == "object":
    # Keep as is (already human-readable)
    pass

# Order columns nicely if present
ordered = [c for c in [
    col_time, col_away, col_home,
    col_away_score, col_home_score,
    col_model_spread, col_book_spread, col_spread_edge, col_spread_bet,
    col_model_total, col_book_total, col_total_edge, col_total_bet,
    col_ml_pretty
] if c]

view = df[ordered] if ordered else df

# Optional sorting by kickoff if you have the Time column
if col_time and col_time in view.columns:
    try:
        # If time is like "1:00 PM" we can sort by parsing; if not, ignore
        view["_sort"] = pd.to_datetime(view[col_time], errors="coerce")
        view = view.sort_values("_sort", na_position="last").drop(columns=["_sort"])
    except Exception:
        pass

# Styling
def color_bets(val):
    if isinstance(val, str):
        if "BET" in val and "OVER" in val: return "font-weight:600"
        if "BET" in val and "UNDER" in val: return "font-weight:600"
        if "BET" in val and "(" in val: return "font-weight:600"
        if "NO BET" in val: return "opacity:0.6"
    return ""

def color_edges(val):
    try:
        x = float(val)
        if x >= 2: return "background-color: #e8ffe8; font-weight:600"
        if x <= -2: return "background-color: #ffe8e8; font-weight:600"
    except: pass
    return ""

# Render
st.caption("Data source: your Google Sheet • Model columns computed in-sheet")
st.dataframe(
    view.style
        .applymap(color_edges, subset=[c for c in [col_total_edge, col_spread_edge] if c])
        .applymap(color_bets, subset=[c for c in [col_total_bet, col_spread_bet] if c]),
    use_container_width=True
)

# Tiny legend
with st.expander("Legend / Notes"):
    st.markdown("""
- **Model Spread** = Home − Away (your sheet)
- **Spread Edge** = alignment with book & strength (your sheet)
- **Total Edge** = Model Total − Book Total (your sheet)
- **Bets** use your threshold logic (55%+ ML, ±1 spread edge, ±5 total edge, etc.)
- ML% display (e.g., `PHI 77%`) comes from your sheet so abbrevs match Teamnames.
""")
