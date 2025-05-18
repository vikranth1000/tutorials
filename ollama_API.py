# ollama_API.py
"""
ollama_API.py: Ollama LLM API interface for the real-time Bitcoin dashboard.

- call_ollama: Sends a prompt to the local LLM (Ollama) and returns the response.
  In the dashboard, prompts include context to restrict answers to Bitcoin analytics, and output is truncated to 400 characters for clarity.
"""

import os
import logging
from ollama import Client
from ollama import chat

LOG = logging.getLogger("ollama_api")

# Read from environment or fallback to model tag actually installed
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:latest")  # ← this is the key fix

_client = None

def _get_client() -> Client:
    global _client
    if _client is None:
        LOG.info(f"Connecting to Ollama at {OLLAMA_URL}")
        _client = Client(host=OLLAMA_URL)
    return _client

def _safe_call(*args, **kwargs) -> str:
    try:
        resp = _client.generate(*args, **kwargs).get("response", "")
        return resp.strip()
    except Exception as e:
        LOG.exception("Ollama call failed")
        raise RuntimeError(f"Ollama inference error: {e}") from e

def call_ollama(prompt: str, model: str = None) -> str:
    """
    Send a prompt to the local Ollama LLM and return the response.
    Args:
        prompt: The prompt string to send (should include context if needed)
        model: Optional model override (default from env)
    Returns:
        The LLM's response as a string (stripped of whitespace)
    """
    client = _get_client()
    model = model or OLLAMA_MODEL
    return _safe_call(model=model, prompt=prompt)

def generate_forecast(prompt: str) -> str:
    return call_ollama(prompt)

