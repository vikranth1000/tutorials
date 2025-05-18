"""
dash_app.py: Main dashboard application for real-time Bitcoin price analytics and LLM-powered insights.

- Provides a live dashboard for BTC/USDT using Dash and Plotly.
- Features: real-time price chart, moving averages, rolling volatility, hourly returns, anomaly detection, LLM summary, LLM forecasting, and a custom prompt box (with context constraints).
- Integrates with Binance API for data and Ollama LLM for natural language analytics.
"""
import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from binance import fetch_klines
from ollama_API import call_ollama
import datetime
import pytz
import io
import base64

# ---- App Setup ----
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "BTC Real-Time Analytics & LLM"

LOCAL_TZ = "America/New_York"
SIDEBAR_WIDTH = 370

# ---- Utility Functions ----
def get_live_data(interval="1m", limit=300):
    df = fetch_klines(symbol="BTCUSDT", interval=interval, limit=limit)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
    # Convert to local timezone
    df["Time"] = pd.to_datetime(df["Time"]).dt.tz_convert(LOCAL_TZ)
    return df

def get_historical_data(start_date, end_date, interval="1d"):
    # Fetch historical klines for the given date range and interval
    # Assumes fetch_klines can accept start and end time (if not, you may need to extend it)
    df = fetch_klines(symbol="BTCUSDT", interval=interval, start_str=start_date, end_str=end_date)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
    df["Time"] = pd.to_datetime(df["Time"]).dt.tz_convert(LOCAL_TZ)
    return df

def compute_metrics(df, ma_window=45, ma5=False, ma15=False, ma30=False):
    df = df.copy()
    df["MA"] = df["close"].rolling(ma_window, min_periods=1).mean()
    if ma5:
        df["MA_5"] = df["close"].rolling(5, min_periods=1).mean()
    if ma15:
        df["MA_15"] = df["close"].rolling(15, min_periods=1).mean()
    if ma30:
        df["MA_30"] = df["close"].rolling(30, min_periods=1).mean()
    df["returns"] = df["close"].pct_change()
    df["volatility"] = df["returns"].rolling(30).std() * 100
    df_hr = df.set_index("Time").resample("1h").last().ffill()
    df_hr["hr_return"] = df_hr["close"].pct_change() * 100
    return df, df_hr

def detect_anomaly(df, threshold=2.0):
    pct = df["close"].pct_change() * 100
    if abs(pct.iloc[-1]) > threshold:
        return True, pct.iloc[-1]
    return False, pct.iloc[-1]

def get_data_range(df):
    start = df["Time"].iloc[0]
    end = df["Time"].iloc[-1]
    delta = end - start
    if delta.days >= 1:
        return f"last {delta.days} days"
    else:
        hours = int(delta.total_seconds() // 3600)
        return f"last {hours} hours"

def get_interval():
    return "1 minute"

# ---- Layout ----
app.layout = html.Div([
    html.Div([
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.Label("Latest BTC/USDT Price", style={
                        "fontSize": "1.1em",
                        "fontWeight": "bold",
                        "color": "#bbb",
                        "textAlign": "center",
                        "display": "block",
                        "marginBottom": "0.2em"
                    }),
                    html.Div([
                        dbc.Button(
                            html.Span("\u21bb", style={"fontSize": "1.5em"}),
                            id="latest-price-refresh-btn",
                            color="secondary",
                            size="sm",
                            style={
                                "width": "2.6em",
                                "height": "2.6em",
                                "borderRadius": "8px 0 0 8px",
                                "marginRight": "0px",
                                "display": "inline-flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "boxShadow": "0 1px 4px rgba(0,0,0,0.10)",
                                "border": "1.5px solid #444",
                                "borderRight": "none",
                                "background": "#23272B"
                            }
                        ),
                        html.Div(id="latest-price-box", style={
                            "fontSize": "0.83em",
                            "fontWeight": "bold",
                            "color": "#00E676",
                            "display": "inline-flex",
                            "alignItems": "center",
                            "background": "#23272B",
                            "borderRadius": "0 8px 8px 0",
                            "padding": "0.5em 2em 0.5em 1em",
                            "boxShadow": "0 2px 8px rgba(0,0,0,0.10)",
                            "minWidth": "180px",
                            "maxWidth": "260px",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "border": "1.5px solid #444",
                            "borderLeft": "none"
                        }),
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "marginBottom": "0.7em",
                        "width": "100%"
                    })
                ]),
            ]),
            html.Hr(style={"margin": "0.8em 0 0.8em 0", "borderColor": "#333"}),
            dbc.CardBody([
                html.Label("Moving Average Window", title="Custom window for main MA line", style={"fontWeight": "bold", "marginBottom": "0.3em"}),
                html.Div(
                    dcc.Slider(id="ma-window", min=5, max=120, step=1, value=45,
                               marks={i: str(i) for i in range(10, 130, 20)},
                               tooltip={"placement": "bottom", "always_visible": False}),
                    style={"marginBottom": "0.5em"}
                ),
                html.Label("Show Additional MAs", title="Show/hide extra moving averages", style={"fontWeight": "bold", "marginBottom": "0.3em"}),
                dbc.Checklist(
                    options=[
                        {"label": "MA 5", "value": "ma5"},
                        {"label": "MA 15", "value": "ma15"},
                        {"label": "MA 30", "value": "ma30"},
                    ],
                    value=["ma5", "ma15", "ma30"],
                    id="ma-checks",
                    inline=True,
                    switch=True,
                    style={"marginBottom": "0.5em"}
                ),
                html.Label("Refresh Interval (sec)", title="How often to auto-refresh data", style={"fontWeight": "bold", "marginBottom": "0.3em"}),
                html.Div(
                    dcc.Slider(id="refresh-interval", min=10, max=120, step=5, value=30,
                               marks={i: str(i) for i in range(10, 130, 20)},
                               tooltip={"placement": "bottom", "always_visible": False}),
                    style={"marginBottom": "0.5em"}
                ),
                dbc.Button("Refresh Now", id="refresh-btn", color="primary", style={"width": "100%", "marginBottom": "0.5em", "borderRadius": "8px", "fontWeight": "bold"}),
                dbc.Button("Generate LLM Summary", id="llm-summary-btn", color="info", style={"width": "100%", "marginBottom": "0.5em", "borderRadius": "8px", "fontWeight": "bold"}),
                dbc.Button("Forecast Next Price (LLM)", id="llm-forecast-btn", color="success", style={"width": "100%", "marginBottom": "0.8em", "borderRadius": "8px", "fontWeight": "bold"}),
                # Custom LLM prompt section
                html.Label("Custom LLM Prompt", style={"fontWeight": "bold"}),
                dcc.Textarea(id="custom-llm-prompt", style={"width": "100%", "height": 45, "marginBottom": "0.5em", "borderRadius": "8px", "border": "1.5px solid #444", "background": "#23272B", "color": "#fff", "padding": "0.5em", "resize": "vertical"}),
                html.Div([
                    dbc.Button("Ask LLM", id="ask-llm-btn", color="warning", style={"width": "48%", "marginRight": "4%", "borderRadius": "8px", "fontWeight": "bold"}),
                    dbc.Button("Clear", id="clear-llm-btn", color="secondary", style={"width": "48%", "borderRadius": "8px", "fontWeight": "bold"}),
                ], style={"display": "flex", "flexDirection": "row", "marginBottom": "0.5em"}),
                html.Div(id="custom-llm-output", style={"whiteSpace": "pre-line", "marginBottom": "1em"}),
                html.Div(id="anomaly-alert", style={"marginBottom": "0.5em"}),
                html.Div(id="llm-summary-output", style={"whiteSpace": "pre-line", "marginBottom": "0.5em"}),
                html.Div(id="llm-forecast-output", style={"whiteSpace": "pre-line", "marginBottom": "0.5em"}),
            ]),
            html.Hr(style={"margin": "0.8em 0 0.8em 0", "borderColor": "#333"}),
            dbc.CardBody([
                html.Div([
                    html.B("Download Data", style={"fontSize": "1.1em", "color": "#bbb"}),
                    html.Div(id="data-summary", style={"fontSize": "0.95em", "marginBottom": "0.3em", "color": "#aaa"}),
                    dbc.Button("Download CSV", id="download-btn", color="secondary", size="sm", style={"width": "100%", "marginBottom": "0.5em", "borderRadius": "8px"}),
                    dcc.Download(id="download-csv")
                ], style={"marginBottom": "0.5em"}),
                html.Div(id="last-updated", style={"fontSize": "0.95em", "color": "#888", "textAlign": "center"}),
            ]),
        ], style={
            "padding": "1.2em 1em",
            "background": "rgba(35, 39, 43, 0.97)",
            "borderRadius": "18px",
            "boxShadow": "0 8px 32px 0 rgba(31, 38, 135, 0.37)",
            "backdropFilter": "blur(4px)",
            "WebkitBackdropFilter": "blur(4px)",
            "border": "1px solid rgba(255,255,255,0.18)",
            "minWidth": f"{SIDEBAR_WIDTH-20}px",
            "maxWidth": f"{SIDEBAR_WIDTH}px",
        })
    ], style={
        "position": "fixed",
        "top": "50%",
        "left": "30px",
        "transform": "translateY(-50%)",
        "zIndex": 1000,
    }),
    # Main content
    html.Div([
        html.H2("Real-Time Bitcoin Analytics & LLM Dashboard", style={"marginBottom": "0.5em", "textAlign": "left", "marginLeft": f"{SIDEBAR_WIDTH+30}px"}),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("BTC/USDT Price Chart"),
                        dbc.CardBody([
                            dcc.Graph(id="price-chart", config={"displayModeBar": True}, style={"height": "520px", "width": "100%"})
                        ])
                    ], style={"marginBottom": "1.2em"}),
                    dbc.Card([
                        dbc.CardHeader("Rolling Volatility (30 periods)"),
                        dbc.CardBody([
                            dcc.Graph(id="vol-chart", config={"displayModeBar": True}, style={"height": "340px", "width": "100%"})
                        ])
                    ], style={"marginBottom": "1.2em"}),
                    dbc.Card([
                        dbc.CardHeader("Hourly Returns (Past 24h)"),
                        dbc.CardBody([
                            dcc.Graph(id="ret-chart", config={"displayModeBar": True}, style={"height": "260px", "width": "100%"})
                        ])
                    ]),
                ], width=12, style={"paddingLeft": "0", "paddingRight": "0", "maxWidth": "100vw"})
            ], style={"height": "80vh", "alignItems": "flex-start"}),
        ], fluid=True, style={"maxWidth": "100vw", "margin": "0 auto", "paddingTop": "1vh", "paddingBottom": "1vh"}),
    ], style={"marginLeft": f"{SIDEBAR_WIDTH+40}px"}),
    dcc.Interval(id="auto-refresh", interval=30*1000, n_intervals=0),
], style={"background": "#181A1B", "minHeight": "100vh"})

# ---- Callbacks ----
@app.callback(
    [Output("price-chart", "figure"),
     Output("vol-chart", "figure"),
     Output("ret-chart", "figure"),
     Output("anomaly-alert", "children"),
     Output("data-summary", "children"),
     Output("last-updated", "children"),
     Output("latest-price-box", "children")],
    [Input("refresh-btn", "n_clicks"),
     Input("auto-refresh", "n_intervals"),
     Input("ma-window", "value"),
     Input("ma-checks", "value"),
     Input("refresh-interval", "value"),
     Input("latest-price-refresh-btn", "n_clicks")],
    prevent_initial_call=False
)
def update_charts(n_clicks, n_intervals, ma_window, ma_checks, refresh_interval, price_refresh):
    df = get_live_data(limit=1440)
    ma5 = "ma5" in ma_checks
    ma15 = "ma15" in ma_checks
    ma30 = "ma30" in ma_checks
    df, df_hr = compute_metrics(df, ma_window, ma5, ma15, ma30)
    anomaly, pct = detect_anomaly(df)
    # Price chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df["Time"], open=df["open"], high=df["high"],
        low=df["low"], close=df["close"], name="Price"
    ))
    fig.add_trace(go.Scatter(
        x=df["Time"], y=df["MA"], line=dict(width=2), name=f"MA {ma_window}",
        line_color="#FF9800"
    ))
    if ma5:
        fig.add_trace(go.Scatter(x=df["Time"], y=df["MA_5"], name="MA 5", line_color="#00E676"))
    if ma15:
        fig.add_trace(go.Scatter(x=df["Time"], y=df["MA_15"], name="MA 15", line_color="#2196F3"))
    if ma30:
        fig.add_trace(go.Scatter(x=df["Time"], y=df["MA_30"], name="MA 30", line_color="#9C27B0"))
    fig.update_layout(title=None, xaxis_title=None, yaxis_title="Price (USD)", margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    # Volatility chart
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(
        x=df["Time"], y=df["volatility"], name="Volatility", line=dict(width=2, color="#42A5F5")
    ))
    fig_vol.update_layout(title=None, xaxis_title=None, yaxis_title="Volatility (%)", margin=dict(l=10, r=10, t=10, b=10))
    # Hourly returns: show last 16 hours (matches Binance 1000-row limit for 1m data)
    now = pd.Timestamp.now(tz=LOCAL_TZ)
    start_nh = now - pd.Timedelta(hours=16)
    df_hr_nh = df_hr.loc[(df_hr.index >= start_nh) & (df_hr.index <= now)]
    all_hours = pd.date_range(start=start_nh, end=now, freq="1h", tz=LOCAL_TZ)
    df_hr_nh = df_hr_nh.reindex(all_hours)
    # Robust fallback: if all hr_return are NaN or empty, fill with zeros
    if df_hr_nh["hr_return"].isna().all() or len(df_hr_nh) == 0:
        df_hr_nh["hr_return"] = 0
    colors = ["#00E676" if (not np.isnan(r) and r >= 0) else "#FF3D00" for r in df_hr_nh["hr_return"]]
    fig_ret = go.Figure()
    fig_ret.add_trace(go.Bar(
        x=df_hr_nh.index, y=df_hr_nh["hr_return"], marker_color=colors, name="Hourly Return"
    ))
    fig_ret.update_layout(title=None, xaxis_title=None, yaxis_title="Return (%)", margin=dict(l=10, r=10, t=10, b=10))
    # Anomaly alert
    alert = None
    if anomaly:
        alert = dbc.Alert(f"Anomaly detected! Last price change: {pct:.2f}%", color="danger", style={"marginTop": "1em"})
    # Data summary
    data_summary = f"Data interval: {get_interval()}. Range: {get_data_range(df)}. Rows: {len(df)}."
    # Last updated
    last_updated = f"Last updated: {df['Time'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S %Z')}"
    # Latest price box
    latest_price = df['close'].iloc[-1] if not df.empty else None
    latest_price_str = f"${latest_price:,.2f}" if latest_price is not None else "N/A"
    return fig, fig_vol, fig_ret, alert, data_summary, last_updated, latest_price_str

@app.callback(
    Output("llm-summary-output", "children"),
    Input("llm-summary-btn", "n_clicks"),
    State("ma-window", "value"),
    State("ma-checks", "value"),
    prevent_initial_call=True
)
def generate_llm_summary(n_clicks, ma_window, ma_checks):
    df = get_live_data()
    ma5 = "ma5" in ma_checks
    ma15 = "ma15" in ma_checks
    ma30 = "ma30" in ma_checks
    df, _ = compute_metrics(df, ma_window, ma5, ma15, ma30)
    recent = df.tail(60)[["Time", "close"]]
    snippet = "\n".join(f"{t.strftime('%H:%M')} → {c:.2f}" for t, c in recent.values)
    prompt = (
        "You are a crypto market analyst.\n"
        "Ignore any external information—use *only* the data below.\n\n"
        "Here are the last 60 BTC/USDT closing prices (time → price):\n"
        f"{snippet}\n\n"
        "Return **only** the result (no methodology), in plain English:\n"
        "Summarize the percent change (with numbers), the most recent high and low, "
        "and the short‐term trend in no more than 3 sentences."
    )
    try:
        summary = call_ollama(prompt)
    except Exception as e:
        summary = f"LLM call failed: {e}"
    return summary

@app.callback(
    Output("llm-forecast-output", "children"),
    Input("llm-forecast-btn", "n_clicks"),
    State("ma-window", "value"),
    State("ma-checks", "value"),
    prevent_initial_call=True
)
def generate_llm_forecast(n_clicks, ma_window, ma_checks):
    # Use past 3 days of hourly closes for LLM forecast
    df = get_live_data(interval="1h", limit=72)  # 72 hours = 3 days
    closes = df["close"].tolist()
    times = df["Time"].dt.strftime('%Y-%m-%d %H:%M').tolist()
    snippet = "\n".join(f"{t}: {c:.2f}" for t, c in zip(times, closes))
    prompt = (
        "You are a crypto market analyst.\n"
        "Here are the last 3 days of BTC/USDT hourly closing prices:\n"
        f"{snippet}\n\n"
        "In two sentences: Forecast the next hour's price, and briefly explain your reasoning based on the data above."
    )
    try:
        forecast = call_ollama(prompt)
    except Exception as e:
        forecast = f"LLM call failed: {e}"
    return f"Forecast: {forecast}"

@app.callback(
    Output("download-csv", "data"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    df = get_live_data()
    csv_string = df.to_csv(index=False)
    b64 = base64.b64encode(csv_string.encode()).decode()
    return dict(content=csv_string, filename="btc_dashboard_data.csv")

@app.callback(
    Output("custom-llm-output", "children"),
    Input("ask-llm-btn", "n_clicks"),
    State("custom-llm-prompt", "value"),
    prevent_initial_call=True
)
def ask_llm(n_clicks, prompt):
    context = (
        "You are a crypto market analyst. Only answer questions about Bitcoin price, trends, or analytics. "
        "If the question is off-topic, politely refuse and say: 'Sorry, I can only answer questions about Bitcoin price analytics.'\n"
    )
    MAX_LLM_OUTPUT_LEN = 400
    if not prompt or not prompt.strip():
        return "Please enter a prompt."
    full_prompt = context + "\n" + prompt.strip()
    try:
        response = call_ollama(full_prompt)
    except Exception as e:
        response = f"LLM call failed: {e}"
    if len(response) > MAX_LLM_OUTPUT_LEN:
        response = response[:MAX_LLM_OUTPUT_LEN] + '... [truncated]'
    return response

@app.callback(
    Output("custom-llm-prompt", "value"),
    Input("clear-llm-btn", "n_clicks"),
    prevent_initial_call=True
)
def clear_llm_prompt(n_clicks):
    return ""

# ---- Run App ----
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0") 