import os
import requests
import pandas as pd

BASE_URL = os.getenv("BINANCE_API_URL", "https://api.binance.com/api/v3")

def fetch_klines(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 300):
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
