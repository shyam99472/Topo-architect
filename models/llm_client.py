"""Ollama API wrapper — local server or Ollama Cloud (OLLAMA_API_KEY)."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Optional

import requests


def _find_env_file() -> Path | None:
    candidates = [
        Path(__file__).resolve().parents[1] / ".env",
        Path.cwd() / "topo_architect" / ".env",
        Path.cwd() / ".env",
    ]
    for path in candidates:
        if path.is_file():
            return path
    return None


def _load_dotenv(force_ollama: bool = True) -> None:
    """Load .env; OLLAMA_* keys always refresh from file when force_ollama=True."""
    path = _find_env_file()
    if not path:
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if not key:
            continue
        if force_ollama and key.startswith("OLLAMA_"):
            os.environ[key] = value
        elif key not in os.environ:
            os.environ[key] = value


def get_ollama_config() -> dict[str, Any]:
    """Read fresh Ollama settings from environment + .env file."""
    _load_dotenv(force_ollama=True)
    api_key = os.environ.get("OLLAMA_API_KEY", "").strip()
    base_url = os.environ.get(
        "OLLAMA_BASE_URL",
        "https://ollama.com" if api_key else "http://localhost:11434",
    ).rstrip("/")
    timeout = int(os.environ.get("OLLAMA_TIMEOUT", "30"))
    return {
        "api_key": api_key,
        "base_url": base_url,
        "timeout": timeout,
        "env_file": str(_find_env_file() or ""),
    }


class OllamaClient:
    """Client for Ollama /api/generate and /api/chat with optional Bearer auth."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: int | None = None,
    ):
        cfg = get_ollama_config()
        self.base_url = (base_url or cfg["base_url"]).rstrip("/")
        self.api_key = (api_key if api_key is not None else cfg["api_key"]).strip()
        self.timeout = timeout if timeout is not None else cfg["timeout"]
        self.last_error: str | None = None

    def _headers(self) -> dict[str, str]:
        if self.api_key:
            return {"Authorization": f"Bearer {self.api_key}"}
        return {}

    def status(self) -> dict[str, Any]:
        """Probe Ollama and return diagnostics for the UI."""
        info: dict[str, Any] = {
            "configured": bool(self.api_key),
            "base_url": self.base_url,
            "env_file": get_ollama_config()["env_file"],
            "available": False,
            "models": [],
            "error": None,
        }
        if not self.api_key and "ollama.com" in self.base_url:
            info["error"] = (
                "OLLAMA_API_KEY not set. Create topo_architect/.env or set the variable "
                "in the same terminal as uvicorn, then restart the API."
            )
            return info

        try:
            r = requests.get(
                f"{self.base_url}/api/tags",
                headers=self._headers(),
                timeout=(5, 15),
            )
            if r.status_code == 200:
                info["available"] = True
                info["models"] = [m["name"] for m in r.json().get("models", [])]
                self.last_error = None
            elif r.status_code == 401:
                info["error"] = "Unauthorized — check OLLAMA_API_KEY is valid."
            else:
                info["error"] = f"HTTP {r.status_code}: {r.text[:200]}"
            self.last_error = info["error"]
        except requests.RequestException as exc:
            info["error"] = str(exc)
            self.last_error = info["error"]
        return info

    def is_available(self) -> bool:
        return self.status()["available"]

    def list_models(self) -> list[str]:
        st = self.status()
        return st.get("models") or []

    def generate(
        self,
        prompt: str,
        model: str = "llama3.2",
        system: Optional[str] = None,
        temperature: float = 0.2,
        format_json: bool = False,
    ) -> str:
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system:
            payload["system"] = system
        if format_json:
            payload["format"] = "json"

        r = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            headers=self._headers(),
            timeout=(5, self.timeout),
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str = "llama3.2",
        temperature: float = 0.2,
        format_json: bool = False,
    ) -> str:
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if format_json:
            payload["format"] = "json"

        r = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            headers=self._headers(),
            timeout=(5, self.timeout),
        )
        r.raise_for_status()
        return r.json().get("message", {}).get("content", "").strip()

    def generate_json(
        self,
        prompt: str,
        model: str = "llama3.2",
        system: Optional[str] = None,
        fallback: Optional[dict] = None,
    ) -> dict:
        text = self.generate(
            prompt, model=model, system=system, format_json=True
        )
        parsed = _extract_json(text)
        if parsed is not None:
            return parsed
        if fallback is not None:
            return fallback
        raise ValueError(f"Could not parse JSON from model output: {text[:200]}")


def _extract_json(text: str) -> Optional[dict]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


def get_llm_client() -> OllamaClient:
    """New client each call so .env / env changes apply after API restart."""
    return OllamaClient()


def pick_model(client: OllamaClient, preferred: list[str]) -> str:
    """Choose first available model from preferred list."""
    available = client.list_models()
    if not available:
        return preferred[0]
    for name in preferred:
        if name in available:
            return name
        base = name.split(":")[0]
        for m in available:
            if m == base or m.startswith(base + ":"):
                return m
    return available[0]
