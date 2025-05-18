<!-- toc -->

- [Ollama API Tutorial](#ollama-api-tutorial)
  * [Overview](#overview)
  * [How It Works](#how-it-works)
    + [Function Signature](#function-signature)
    + [Behavior](#behavior)
  * [Example Usage](#example-usage)
  * [Error Handling](#error-handling)
  * [General Guidelines](#general-guidelines)
  * [References](#references)

<!-- tocstop -->

# Ollama API Tutorial

> **Note:**
> In the dashboard, `call_ollama` is always used with a context constraint: the LLM is instructed to only answer questions about Bitcoin price analytics, and to politely refuse off-topic questions. The dashboard also limits LLM output to 400 characters for clarity.

This document describes how the **`ollama_API.py`** module works and how to use it in the context of real-time LLM-based forecasting and summarization tasks.

It serves as a native API interface to interact with a **locally running LLM using Ollama**, and is tightly integrated into the project's data-to-summary/forecasting pipeline.

---


---

## Overview

The `ollama_API.py` module exposes a simple API to interact with a running Ollama model on your local system. It uses the `ollama` Python client to send prompt requests to the `/generate` endpoint exposed by the Ollama daemon.

It wraps the client call in a function called `call_ollama()` that abstracts:

- Base URL configuration
- Model name override
- Prompt formatting
- Error handling and logging

This is used in both **Streamlit app** and **notebooks/scripts** where LLMs are needed for:
- Trend summarization (e.g., "BTC gained 2.5% in the last hour")
- Next-value prediction (e.g., "Forecast = $30,512.00")

---

## How It Works

The API consists of one public function:

### `call_ollama(prompt: str, model: Optional[str] = None) -> str`

| Argument | Type | Description |
|----------|------|-------------|
| `prompt` | `str` | The text input to send to the model |
| `model`  | `str or None` | Optional override of the default model (e.g., "mistral") |

**Returns**:  
The model's raw output as a string (stripped of whitespace).

**Environment variables used**:
- `OLLAMA_URL`: default = `"http://localhost:11434"`
- `OLLAMA_MODEL`: default = `"mistral:latest"`

---

### Behavior

Internally:
1. Loads the Ollama client with the specified URL
2. Sends a prompt using the `client.generate()` method
3. Returns only the `response["response"]` string from the output
4. Raises `RuntimeError` on failure

We use a global client (`_OLLAMA_CLIENT`) to avoid reinitialization on every call.

---

## Example Usage

```python
from ollama_API import call_ollama

prompt = (
    "Bitcoin has risen from $30,100 to $30,600 over the past 60 minutes. "
    "Summarize the short-term trend in two sentences."
)

try:
    summary = call_ollama(prompt)
    print("LLM Summary ➜", summary)
except RuntimeError as e:
    print("Failed to get response:", e)
