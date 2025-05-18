# Real-Time Bitcoin Price Analysis and Forecasting using Ollama-python

**Course**: DATA605 – Spring 2025  
**Student**: Vikranth Reddimasu  
**Instructor**: Prof. Giacinto Paolo Saggese  

---

## Table of Contents

- [Overview](#overview)  
- [Architecture](#architecture)  
- [Key Features](#key-features)  
- [System Workflow](#system-workflow)  
- [Setup and Installation](#setup-and-installation)  
- [How to Use](#how-to-use)  
- [Dashboard Insights](#dashboard-insights)
  - [1. Price Chart Overview](#1-price-chart-overview)
  - [2. LLM Trend Summary](#2-llm-trend-summary)
  - [3. Rolling Volatility](#3-rolling-volatility)
  - [4. Hourly Returns (Full Range)](#4-hourly-returns-full-range)
  - [5. Hourly Returns (Intraday)](#5-hourly-returns-intraday)
  - [6. Intraday Price Chart](#6-intraday-price-chart)
  - [7. Controls and Forecasting](#7-controls-and-forecasting)
- [Technologies Used](#technologies-used)  
- [Limitations](#limitations)  
- [Future Work](#future-work)  

---

## Overview

This project is a real-time Bitcoin analytics dashboard that combines live crypto price data, technical analysis, and large language model (LLM) insights. It uses the Binance API, pandas, and a local Ollama LLM to provide:
- Real-time price charts with moving averages
- Rolling volatility and hourly returns
- LLM-generated natural language summaries
- LLM-based forecasting with context and reasoning
- A custom prompt box for user questions (with constraints)

---

## Architecture

```
Binance Price API ➔ Pandas DataFrame ➔ Technical Metrics (MA, Volatility, Returns) ➔
Streamlit UI
         └──➔ LLM Prompt ➔ Ollama Python API ➔ Text Summary
```

### Description of Components:

- **Data Source**: Binance public REST API for BTC/USDT kline data.
- **Analysis Layer**: Python (pandas, numpy) for real-time metric calculations.
- **LLM Integration**: Ollama-Python connects to a local Mistral-7B model to summarize price trends.
- **UI Layer**: Streamlit frontend using Plotly for interactive charts and dynamic controls.

---

## Key Features

- **Live price ingestion** from Binance (1m, 1h intervals)
- **Moving average plots** (custom window, MA5, MA15, MA30)
- **Rolling volatility chart** (30-period std dev)
- **Hourly return bar chart** (last ~16 hours, due to Binance API limit)
- **LLM-generated summaries** (trend, percent change, highs/lows)
- **LLM forecasting** (uses past 3 days of hourly closes, gives forecast + reasoning)
- **Custom LLM prompt** (user can ask questions, but LLM is constrained to only answer about Bitcoin price analytics)
- **Download data** as CSV
- **Modern, responsive UI** (Dash + Bootstrap)

---

## System Workflow

1. User selects number of data points, interval, and MA parameters.
2. The app fetches and caches price data (via Binance API).
3. Metrics are calculated using `pandas` and plotted with `plotly`.
4. On-demand LLM summaries are generated using `ollama`.
5. Visuals and text summaries are updated live in the dashboard.

---

## Setup and Installation

> ### Quick Start (Docker)
>
> If you have Docker installed, just run:
>
> ```bash
> docker-compose up --build
> ```
>
> This launches the dashboard on `http://localhost:8050`.

### 1. Clone the repository
```bash
git clone https://github.com/vikranth1000/tutorials.git
cd tutorials/DATA605/Spring2025/projects/TutorTask184_Spring2025_Real-Time_Bitcoin_Price_Analysis_and_Forecasting_with_Ollama-Python
```

### 2. Install Python dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Ollama
- [Download Ollama](https://ollama.com) for your OS
- Or pull via Docker:
```bash
ollama pull mistral:latest
```
- Start the server (default at `http://localhost:11434`)

### 4. Launch the App
```bash
python dash_app.py
```

Or using Docker:
```bash
docker-compose up --build
```

---

## How to Use

- Use the **sidebar** to select:
  - Moving average window
  - Refresh interval
- Click **"Generate LLM Summary"** to trigger trend analysis.
- Click **"Forecast Next Price (LLM)"** for an LLM-based prediction.
- View live price, volatility, and returns charts.
- Anomaly alerts highlight large price moves.

---

## Technologies Used

- **Python 3.12+**  
- **Dash** – Web-based UI framework  
- **Pandas / Numpy** – Time-series and numeric computation  
- **Plotly** – Interactive charts  
- **Binance API** – Market data source  
- **Ollama-Python** – LLM query client  
- **Docker / Compose** – Cross-platform containerization

---

## Limitations

- Forecasting model is naïve (last price projection only)
- LLM summaries may vary in quality depending on model and prompt
- App supports only BTC/USDT pair currently
- UI is minimal (no authentication or persistent storage)
- Local inference may be slow on lower-spec machines

---

## Future Work

- Integrate **ARIMA / LSTM / Prophet** models for actual forecasting
- Fine-tune LLM with historical crypto market data
- Support more symbols (ETH, BNB, etc.) via dropdowns
- Deploy online (e.g. Streamlit Cloud, GCP)
- Add **alerts**, **trading signals**, and **mobile compatibility**
- Enhance UX with tooltips, glossary, and dark/light themes

---

## Custom LLM Prompt (with Constraints)

- The dashboard includes a prompt box where you can ask the LLM questions.
- **Constraint:** The LLM will only answer questions about Bitcoin price, trends, or analytics. Off-topic questions are politely refused.
- **Output length:** LLM responses are limited to 400 characters for clarity.
- **Forecasting:** When forecasting, the LLM is given 3 days of hourly closes and asked for a two-sentence answer: the forecast and a brief explanation.

---


## File Structure

- `dash_app.py` – Main dashboard app
- `binance.py` – Binance API interface (1000-row limit for 1m data)
- `ollama_API.py` – LLM API interface (with context/output constraints)
- `data/fresh_btc_data.csv` – Fallback BTC price data
- `requirements.txt`, `Dockerfile`, `docker-compose.yml` – Setup files

---

## Notes
- The dashboard only supports BTC/USDT (can be extended).
- No historical mode or fine-tuning included in this version.
- All code is documented and ready for submission.

---

**Contact:**  
Vikranth Reddimasu  
vikranthreddimasu@gmail.com
