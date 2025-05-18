# ollama_API.py
import os
import logging
from ollama import Client

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
    client = _get_client()
    model = model or OLLAMA_MODEL
    return _safe_call(model=model, prompt=prompt)
