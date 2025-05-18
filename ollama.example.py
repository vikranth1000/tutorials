import json
from pathlib import Path
import pandas as pd

# ── CONFIG ──────────────────────────────────────────────────────────────────────
INPUT_CSV = Path("historical_analysis/data/historical_btc_data.csv")
OUTPUT_JSONL = Path("finetune_data.jsonl")
WINDOW = 60  # use last 60 closes as prompt
# ────────────────────────────────────────────────────────────────────────────────

def make_example(prices):
    """
    Given a list of floats, builds a prompt string listing them and a completion
    asking for the next price.
    """
    lines = [f"{i+1:02d}. {p:.2f}" for i,p in enumerate(prices)]
    prompt = (
        "Here are the last 60 BTC/USDT closing prices (most recent last):\n"
        + "\n".join(lines)
        + "\n\nPlease forecast the next closing price (just the number)."
    )
    return prompt

def main():
    df = pd.read_csv(INPUT_CSV)
    # assume df has 'start' (ms) and 'close'
    df["Time"] = pd.to_datetime(df["start"], unit="ms", utc=True)
    series = df.set_index("Time")["close"].astype(float).dropna()

    with open(OUTPUT_JSONL, "w") as out:
        for i in range(len(series) - WINDOW):
            hist = series.iloc[i : i + WINDOW].tolist()
            target = series.iloc[i + WINDOW]
            prompt = make_example(hist)
            completion = f" {target:.2f}"  # leading space is important
            out.write(json.dumps({
                "prompt": prompt,
                "completion": completion
            }) + "\n")
    print(f"Wrote {OUTPUT_JSONL}")

if __name__=="__main__":
    main()
