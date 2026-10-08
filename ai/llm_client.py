"""One small wrapper so every AI helper can use either a cloud or a private LLM.

Set LLM_PROVIDER in your .env file:
  gemini  -> Google Gemini API (needs GEMINI_API_KEY)
  ollama  -> a private model running locally with Ollama (no data leaves your machine)
"""
import json
import os
import time
import urllib.request

from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")


def _ask_gemini(prompt: str, temperature: float) -> str:
    from google import genai
    from google.genai import errors, types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    for attempt in range(1, 5):
        try:
            res = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                ),
            )
            return res.text
        except errors.ServerError:  # 503 busy / 500: retry with backoff
            time.sleep(5 * attempt)
    raise RuntimeError("Gemini is unavailable after 4 attempts; try again later.")


def _ask_ollama(prompt: str, temperature: float) -> str:
    payload = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
                          "options": {"temperature": temperature}}).encode()
    req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as res:
        return json.loads(res.read())["response"]


def ask_llm(prompt: str, temperature: float = 0.2) -> str:
    """Send a prompt to the configured LLM and return its text answer."""
    if PROVIDER == "ollama":
        return _ask_ollama(prompt, temperature)
    if PROVIDER == "gemini":
        return _ask_gemini(prompt, temperature)
    raise ValueError(f"Unknown LLM_PROVIDER '{PROVIDER}'. Use 'gemini' or 'ollama'.")


def load_prompt(name: str, **values) -> str:
    """Load ai/prompts/<name>.md and fill {placeholders}."""
    path = os.path.join(os.path.dirname(__file__), "prompts", f"{name}.md")
    with open(path, encoding="utf-8") as f:
        template = f.read()
    return template.format(**values)
