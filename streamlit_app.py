#streamlit_app.py

from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import sys

# allow imports from project root
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from ollama_API import call_ollama
from binance import fetch_klines

# Mapping for pandas frequency aliases
FREQ_MAP = {"minutes": "T", "hours": "H"}

# ── Page setup ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="BTC/USDT Live Dashboard", layout="wide")
st.markdown("""
    <style>
      .main .block-container {background: #212121;}
      header, .css-1d391kg {background: #181818;}
      .stPlotlyChart > div {background: #171717;}
      .css-1avcm0n, .css-k008qs {color: #E0E0E0;}
      footer, #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ── Data loader with cache ─────────────────────────────────────────────────
@st.cache_data(ttl=15, show_spinner=False)
def load_live(candles: int, interval: str) -> pd.DataFrame:
    """
    Fetch the last `candles` kline data at `interval` from Binance.
    """
    return fetch_klines(symbol="BTCUSDT", interval=interval, limit=candles)

# ── Sidebar controls ───────────────────────────────────────────────────────
st.sidebar.header("Controls")

# Data points to load
candles = st.sidebar.number_input(
    label="Data points to load",
    min_value=1,
    max_value=1000,
    value=300,
    help=(
        "How many historical data points to load (max 1000).\n"
        "Each point is one “candle” at your chosen interval (e.g. "
        "300 at 1h covers the last 300 hours)."
    )
)

# Interval selector
interval = st.sidebar.selectbox(
    "Interval",
    ["1m", "5m", "15m", "1h"],
    index=3,
    help="Time interval for each candle."
)

if st.sidebar.button("Refresh candles"):
    load_live.clear()

## Forecast inputs
horizon = st.sidebar.number_input(
    label="Prediction window",
    min_value=1,
    max_value=120,
    value=30,
    help=(
        "How many future data points to predict.\n"
        "If you’re forecasting hourly, 30 here means “next 30 hours.”"
    )
)
freq = st.sidebar.selectbox(
    label="Time unit for prediction",
    options=["minutes", "hours"],
    index=1,
    help="Pick the time unit that “Prediction window” uses."
)

# Moving averages
st.sidebar.markdown("---")
st.sidebar.markdown("**Moving Averages**")
primary_ma = st.sidebar.slider(
    "Primary MA window",
    min_value=5, max_value=120, value=45,
    help="Window length for the primary moving average."
)
show_ma15 = st.sidebar.checkbox("MA 15")
show_ma30 = st.sidebar.checkbox("MA 30")
show_ma60 = st.sidebar.checkbox("MA 60")

# Custom LLM prompt
st.sidebar.markdown("---")
use_custom = st.sidebar.checkbox("Use custom LLM prompt")
if use_custom:
    st.sidebar.markdown("#### Prompt suggestions")
    st.sidebar.markdown(
        "- Summarize percentage change with values\n"
        "- Identify any recent highs or lows\n"
        "- Highlight volatility patterns\n"
    )
    custom_prompt = st.sidebar.text_area(
        "Enter your custom prompt",
        height=120,
        max_chars=500,
        help="Ask anything about the BTC/USDT data."
    )
else:
    custom_prompt = ""

# Raw data toggle
show_raw = st.sidebar.checkbox(
    "Show raw data",
    help="Display the last 200 rows of raw OHLCV data."
)

# ── Load & validate data ────────────────────────────────────────────────────
df = load_live(candles, interval)
if df.empty:
    st.error("No data returned from Binance.")
    st.stop()

# Ensure numeric types
for col in ["open", "high", "low", "close", "volume"]:
    df[col] = df[col].astype(float)

# ── Latest price metric ────────────────────────────────────────────────────
latest_price = df["close"].iat[-1]
latest_time = df["Time"].iat[-1].strftime("%Y-%m-%d %H:%M UTC")
st.metric(
    label="Latest BTC/USDT price",
    value=f"${latest_price:,.2f}",
    help=f"as of {latest_time}"
)

# ── Price chart + MAs ──────────────────────────────────────────────────────
df["MA_primary"] = df["close"].rolling(primary_ma, min_periods=1).mean()
if show_ma15:
    df["MA_15"] = df["close"].rolling(15, min_periods=1).mean()
if show_ma30:
    df["MA_30"] = df["close"].rolling(30, min_periods=1).mean()
if show_ma60:
    df["MA_60"] = df["close"].rolling(60, min_periods=1).mean()

fig = go.Figure()
# candlesticks
fig.add_trace(go.Candlestick(
    x=df["Time"], open=df["open"], high=df["high"],
    low=df["low"], close=df["close"],
    increasing_line_color="#00E676",
    decreasing_line_color="#FF3D00",
    name="Price"
))
# primary MA
fig.add_trace(go.Scatter(
    x=df["Time"], y=df["MA_primary"],
    line=dict(width=2), name=f"MA {primary_ma}"
))
# additional MAs
if show_ma15:
    fig.add_trace(go.Scatter(x=df["Time"], y=df["MA_15"], name="MA 15"))
if show_ma30:
    fig.add_trace(go.Scatter(x=df["Time"], y=df["MA_30"], name="MA 30"))
if show_ma60:
    fig.add_trace(go.Scatter(x=df["Time"], y=df["MA_60"], name="MA 60"))

fig.update_layout(
    title="Price Chart",
    paper_bgcolor="#171717",
    plot_bgcolor="#171717",
    font_color="#E0E0E0",
    xaxis=dict(gridcolor="#212121"),
    yaxis=dict(gridcolor="#212121"),
    margin=dict(l=40, r=40, t=40, b=40),
    legend=dict(bgcolor="#171717")
)
st.plotly_chart(fig, use_container_width=True)

# ── LLM Summary ─────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("LLM Trend Summary")

if st.button("Generate LLM Summary"):
    with st.spinner("Querying LLM…"):
        # build our 60-point snippet
        recent = df.tail(60)[["Time", "close"]]
        snippet = "\n".join(
            f"{t.strftime('%H:%M')} → {c:.2f}"
            for t, c in recent.values
        )

        base = (
        "You are a crypto market analyst.\n"
        "Ignore any external information—use *only* the data below.\n\n"
        "Here are the last 60 BTC/USDT closing prices (time → price):\n"
        f"{snippet}\n\n"
        "Return **only** the result (no methodology), in plain English:\n"
        )

        if use_custom and custom_prompt.strip():
            prompt = base + custom_prompt.strip()
        else:
            prompt = (
            base +
            "Summarize the percent change (with numbers), the most recent high and low, "
            "and the short‐term trend in no more than 3 sentences."
            )   
        summary = call_ollama(prompt)
    st.write(summary)

# ── Rolling volatility ──────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Rolling Volatility (%)")
vol_window = 30
df["returns"] = df["close"].pct_change()
df["volatility"] = df["returns"].rolling(vol_window).std() * 100
latest_vol = df["volatility"].iat[-1]
st.write(f"{vol_window}-period vol: {latest_vol:.2f}%")

fig_vol = go.Figure()
fig_vol.add_trace(go.Scatter(
    x=df["Time"], y=df["volatility"], name="Volatility",
    line=dict(width=2)
))
fig_vol.update_layout(
    paper_bgcolor="#171717",
    plot_bgcolor="#171717",
    font_color="#E0E0E0",
    xaxis=dict(gridcolor="#212121"),
    yaxis=dict(gridcolor="#212121"),
    margin=dict(l=40, r=40, t=40, b=40)
)
st.plotly_chart(fig_vol, use_container_width=True)

# ── Hourly returns ──────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Hourly Returns (%)")
df_hr = df.set_index("Time").resample("1h").last().ffill()
df_hr["hr_return"] = df_hr["close"].pct_change() * 100

colors = ["#00E676" if r >= 0 else "#FF3D00" for r in df_hr["hr_return"]]
fig_ret = go.Figure()
fig_ret.add_trace(go.Bar(
    x=df_hr.index, y=df_hr["hr_return"],
    marker_color=colors, name="Return"
))
fig_ret.update_layout(
    paper_bgcolor="#171717",
    plot_bgcolor="#171717",
    font_color="#E0E0E0",
    xaxis=dict(gridcolor="#212121"),
    yaxis=dict(gridcolor="#212121"),
    margin=dict(l=40, r=40, t=40, b=40)
)
st.plotly_chart(fig_ret, use_container_width=True)

# ── Quick naïve forecast ────────────────────────────────────────────────────
st.markdown("---")
if st.button("Quick naïve forecast"):
    last = df["close"].iat[-1]
    st.info(
        f"Naïve model predicts BTC will hover near **${last:,.2f}** "
        f"for the next {horizon} {freq}."
    )

# ── Raw data ────────────────────────────────────────────────────────────────
if show_raw:
    st.markdown("---")
    st.dataframe(df.set_index("Time").tail(200))
