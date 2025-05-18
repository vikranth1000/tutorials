import os
import requests
import pandas as pd
from datetime import datetime, timedelta

BASE_URL = os.getenv("BINANCE_API_URL", "https://api.binance.com/api/v3")

"""
binance.py: Binance API interface for the real-time Bitcoin dashboard.

- fetch_klines: Fetches recent kline/candlestick data for a given symbol and interval (used in dashboard).
  Note: Binance API limits to 1000 rows per request for 1m data, so the dashboard's hourly returns bar chart covers the last ~16 hours.
- get_historical_klines: (Not used in dashboard) Fetches historical klines over a date range, with fallback to local CSV if needed.
"""

def fetch_klines(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 300):
    """
    Fetch recent kline/candlestick data from Binance API.
    Args:
        symbol: Trading pair symbol (default BTCUSDT)
        interval: Kline interval (e.g., '1m', '1h')
        limit: Number of rows to fetch (max 1000 for 1m interval)
    Returns:
        DataFrame with columns: Time, open, high, low, close, volume
    """
    url = f"{BASE_URL}/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code == 451:
        us_url = "https://api.binance.us/api/v3/klines"
        resp = requests.get(us_url, params=params, timeout=10)

    resp.raise_for_status()
    data = resp.json()

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df.rename(columns={"open_time": "Time"})
    return df[["Time", "open", "high", "low", "close", "volume"]]

def get_historical_klines(symbol, interval, start, end, api_key=None, api_secret=None):
    """
    Fetch historical klines from Binance API for a given symbol, interval, start, and end date.
    If API fails or is rate-limited, fallback to loading from a default CSV file.
    Returns a DataFrame with columns: Time, open, high, low, close, volume
    """
    # Convert start/end to milliseconds
    def to_ms(dt):
        if isinstance(dt, str):
            dt = pd.to_datetime(dt)
        return int(dt.timestamp() * 1000)

    start_ms = to_ms(start)
    end_ms = to_ms(end)
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_ms,
        "endTime": end_ms,
        "limit": 1000
    }
    headers = {}
    if not api_key:
        api_key = os.environ.get("BINANCE_API_KEY")
    if not api_secret:
        api_secret = os.environ.get("BINANCE_API_SECRET")
    if api_key:
        headers["X-MBX-APIKEY"] = api_key
    try:
        all_data = []
        while True:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if not data:
                break
            all_data.extend(data)
            if len(data) < 1000:
                break
            params["startTime"] = data[-1][0] + 1
            if params["startTime"] > end_ms:
                break
        if not all_data:
            raise Exception("No data returned from Binance API.")
        df = pd.DataFrame(all_data, columns=[
            "Time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "num_trades", "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df = df[["Time", "open", "high", "low", "close", "volume"]]
        df["Time"] = pd.to_datetime(df["Time"], unit="ms", utc=True)
        return df
    except Exception as e:
        print(f"Binance API failed: {e}. Falling back to CSV.")
        # Fallback: load from default CSV
        try:
            df = pd.read_csv("data/fresh_btc_data.csv")
            df["Time"] = pd.to_datetime(df["timestamp"], utc=True)
            df = df[(df["Time"] >= pd.to_datetime(start)) & (df["Time"] <= pd.to_datetime(end))]
            return df[["Time", "open", "high", "low", "close", "volume"]]
        except Exception as e2:
            print(f"CSV fallback also failed: {e2}")
            return pd.DataFrame(columns=["Time", "open", "high", "low", "close", "volume"])
