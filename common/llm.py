"""Tiny LLM client shared by all three projects.

Chat goes to the Azure OpenAI deployment configured in the root .env.
Calls are deliberately cheap: small max_tokens, call counter, hard cap.
Embeddings are computed locally (hashing vectors) because the .env only has a chat deployment.
"""
import os
import time
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv
from sklearn.feature_extraction.text import HashingVectorizer

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-04-01-preview")
MAX_CALLS = int(os.getenv("MAX_LLM_CALLS", "150"))  # safety cap per process

calls = 0


class ContentFiltered(Exception):
    """Azure's content filter rejected the prompt (common for jailbreak-style input)."""


def chat(messages, model=None, temperature=0.7, max_tokens=80, json_mode=False):
    """Return (text, seconds). `model` is ignored: there is one deployment."""
    global calls
    if calls >= MAX_CALLS:
        raise RuntimeError(f"LLM call cap reached ({MAX_CALLS}); raise MAX_LLM_CALLS in .env")
    calls += 1
    body = {"messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    t0 = time.time()
    r = requests.post(f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}/chat/completions",
                      params={"api-version": API_VERSION}, headers={"api-key": KEY}, json=body, timeout=60)
    if r.status_code == 400 and "content_filter" in r.text:
        raise ContentFiltered(r.text[:200])
    r.raise_for_status()
    return (r.json()["choices"][0]["message"]["content"] or "").strip(), time.time() - t0


_hasher = HashingVectorizer(n_features=1024, analyzer="char_wb", ngram_range=(3, 5), alternate_sign=False, norm="l2")


def embed(texts):
    """Local, free, stateless text vectors (character n-grams). No API call."""
    return _hasher.transform(texts).toarray().tolist()


def available_models():
    return [DEPLOYMENT]
