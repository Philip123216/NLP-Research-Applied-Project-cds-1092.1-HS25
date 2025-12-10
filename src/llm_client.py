import json
import requests

import config
from prompts import SYSTEM_PROMPT, build_user_prompt, FORMAT_SCHEMA


def query_ollama(question: str, text_a: str, text_b: str) -> dict:
    """
    Schickt Frage + Kontext1 + Kontext2 an Ollama und gibt ein dict zurück.
    """
    user_prompt = build_user_prompt(question, text_a, text_b)

    body = {
        "model": config.MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "format": FORMAT_SCHEMA,
    }

    resp = requests.post(config.OLLAMA_URL, json=body, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    content = data["message"]["content"]
    parsed = json.loads(content)
    return parsed
