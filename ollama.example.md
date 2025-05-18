<!-- toc -->

## Table of Contents
- [Ollama Example – Bitcoin Price Forecasting](#ollama-example--bitcoin-price-forecasting)
  * [Project Overview](#project-overview)
  * [Describe the Implementation](#describe-the-implementation)
    + [1. Real-Time Data Ingestion](#1-real-time-data-ingestion)
    + [2. Time-Series Processing](#2-time-series-processing)
    + [3. LLM Integration with Ollama-Python](#3-llm-integration-with-ollama-python)
    + [4. Streamlit Dashboard](#4-streamlit-dashboard)
    + [5. Optional: Streaming Pipeline](#5-optional-streaming-pipeline)
  * [Challenges Faced](#challenges-faced)
  * [Useful Resources](#useful-resources)
  * [Python Libraries Used](#python-libraries-used)
  * [General Guidelines for Reuse](#general-guidelines-for-reuse)
  * [References](#references)

<!-- tocstop -->

# Ollama Example – Bitcoin Price Forecasting

This example markdown explains how the **"Ollama Python #2"** project was implemented using Python, Ollama, and real-time data processing techniques. It demonstrates how to turn the high-level project description into code and functional components using:

- Real-time BTC/USDT price feeds from Binance
- Trend summarization and forecasting using a locally running LLM via Ollama
- Streamlit dashboard for interaction and visualization

# Ollama Example Usage

> **Note:**
> In the dashboard, prompts are always sent with a context constraint: the LLM is instructed to only answer questions about Bitcoin price analytics, and to politely refuse off-topic questions. The dashboard also limits LLM output to 400 characters for clarity.

## Example Prompt (Dashboard Style)

```
You are a crypto market analyst. Only answer questions about Bitcoin price, trends, or analytics. If the question is off-topic, politely refuse and say: 'Sorry, I can only answer questions about Bitcoin price analytics.'

What is the weather today?
```

## Example Output

```
Sorry, I can only answer questions about Bitcoin price analytics.
```

---

## Project Overview

This project delivers a **real-time Bitcoin price analysis dashboard** that:

- Ingests BTC/USDT prices from Binance
- Computes moving averages and volatility
- Uses an LLM (via `ollama-python`) to generate **natural language summaries**
- Forecasts the next value using a **naïve baseline**
- Visualizes everything inside an interactive **Streamlit** app

---

## Describe the Implementation

### 1. Real-Time Data Ingestion

- We used the Binance REST API to fetch recent 1-minute candle data.
- Implemented using `requests.get()` in a function inside `binance.py`.
- Cached results in memory to reduce redundant calls.

### 2. Time-Series Processing

- Parsed JSON data into a `pandas.DataFrame`
- Calculated the following:
  - **Simple Moving Averages** (user-defined windows)
  - **Rolling Volatility** (standard deviation of % returns)
  - **Hourly Returns**
- Used these metrics to construct LLM prompts.

### 3. LLM Integration with Ollama-Python

- Used `ollama_API.py` to wrap calls to Ollama's `/generate` endpoint.
- Default model: `mistral:latest`
- Summarization prompts included:
  > "Here are the last 60 Bitcoin prices: [...]. Summarize the trend in two sentences."

- Forecast prompts used:
  > "Here are the last 12 prices: [...]. Predict the next price in USD. Return only the number."

### 4. Streamlit Dashboard

- Sidebar controls: MA windows, data interval, custom prompt
- Main layout:
  - Latest price metric card
  - Candlestick chart with overlays
  - Rolling volatility chart
  - Hourly returns bar chart
  - Button to generate LLM summary
- Code lives in `streamlit_app.py`

### 5. Optional: Streaming Pipeline

- We used periodic polling for simplicity.
- For real stream ingestion, we explored options like `faust` or `websockets`.
- This was not fully implemented due to scope and compute limitations.

---

## Challenges Faced

- Ollama's LLM inference is **compute-heavy** without GPU acceleration.
- Prompt design matters: unstructured prompts caused hallucinations or over-verbosity.
- Streaming real-time data and inference simultaneously adds load on the system.
- Handling time-zone alignment and proper API rate-limiting was important.

---

## Useful Resources

- [Ollama-Python Documentation](https://github.com/ollama/ollama-python)
- [Binance API Docs](https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data)
- [Time Series Forecasting with Machine Learning – Ch.11](https://www.oreilly.com/library/view/time-series-forecasting/9781098105830/)

---

## Python Libraries Used

- `ollama-python`: interface with the Ollama LLM backend
- `pandas`, `numpy`: time series analysis
- `requests`: Binance API calls
- `streamlit`: user interface
- `plotly`: dynamic candlestick + line charts
- `dotenv`, `os`: managing model/environment configuration

---

## General Guidelines for Reuse

- Start with `ollama.example.py` for minimal working usage
- Use `ollama.example.ipynb` to prototype metrics, plots, and LLM interactions
- Run Ollama locally with quantized weights (e.g., mistral:latest)
- Do not overload LLM prompts—keep short and instruction-focused
- Test inference latency on your machine before running continuous loops
- Reuse `ollama_API.py` as a standalone module in any project needing summarization

---

## References

- [Project Spec – Ollama Python #2](https://ollama.com)  
- [Streamlit Docs](https://docs.streamlit.io/)  
- [Faust Streaming Guide](https://faust.readthedocs.io/)  
- [OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)

---
