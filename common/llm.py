"""Tiny provider-agnostic LLM client shared by all three projects.

Default provider is a local Ollama container (docker). Set LLM_PROVIDER=openai
and OPENAI_API_KEY in the root .env to use a GPT model instead. No Azure.
"""
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OPENAI_BASE = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-minilm")
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")


def chat(messages, model="qwen2.5:0.5b", temperature=0.7, max_tokens=300, json_mode=False):
    """Return (text, seconds). `messages` is an OpenAI-style list of dicts."""
    t0 = time.time()
    if PROVIDER == "openai":
        body = {"model": OPENAI_MODEL, "messages": messages,
                "temperature": temperature, "max_tokens": max_tokens}
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        r = requests.post(f"{OPENAI_BASE}/chat/completions", json=body, timeout=120,
                          headers={"Authorization": f"Bearer {OPENAI_KEY}"})
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"]
    else:
        body = {"model": model, "messages": messages, "stream": False,
                "options": {"temperature": temperature, "num_predict": max_tokens}}
        if json_mode:
            body["format"] = "json"
        r = requests.post(f"{OLLAMA_URL}/api/chat", json=body, timeout=600)
        r.raise_for_status()
        text = r.json()["message"]["content"]
    return text.strip(), time.time() - t0


def embed(texts):
    """Return a list of embedding vectors for `texts`."""
    if PROVIDER == "openai":
        r = requests.post(f"{OPENAI_BASE}/embeddings", timeout=120,
                          headers={"Authorization": f"Bearer {OPENAI_KEY}"},
                          json={"model": OPENAI_EMBED_MODEL, "input": texts})
        r.raise_for_status()
        return [d["embedding"] for d in r.json()["data"]]
    r = requests.post(f"{OLLAMA_URL}/api/embed", timeout=600,
                      json={"model": EMBED_MODEL, "input": texts})
    r.raise_for_status()
    return r.json()["embeddings"]


def available_models():
    if PROVIDER == "openai":
        return [OPENAI_MODEL]
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return [m["name"] for m in r.json()["models"] if "minilm" not in m["name"] and "embed" not in m["name"]]
    except Exception:
        return []
