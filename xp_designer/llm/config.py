"""API key configuration for the LLM client.

Reads from OPENAI_API_KEY env, or xp_designer/llm/.api_key if unset.
"""

from __future__ import annotations

import os
from pathlib import Path

_API_KEY_FILE = Path(__file__).resolve().parent / ".api_key"


def get_api_key() -> str | None:
    """Return the OpenAI API key, or None if not configured."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key.strip()
    if _API_KEY_FILE.exists():
        return _API_KEY_FILE.read_text().strip()
    return None
