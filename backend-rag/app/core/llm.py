import os
import requests
from typing import Dict, Any
from app.settings import OPENROUTER_BASE_URL, LLM_MODEL, MAX_TOKEN_OUTPUT

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def _call_openrouter(messages: list, reasoning: bool = True, temperature: float = 0.0) -> Dict[str, Any]:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set in environment.")
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://qonfido-backend-rag.up.railway.app",
    "X-Title": "Qonfido AI Project",
    }
    payload = {
    "model": LLM_MODEL,
    "messages": messages,
    "max_tokens": MAX_TOKEN_OUTPUT,
    "extra_body": {"reasoning": {"enabled": True}} if reasoning else {},
    "temperature": temperature,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    try:
        resp.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"OpenRouter API error: {e} - {resp.text}")
    return resp.json()


def generate_answer(system_prompt: str, user_query: str, context: str, reasoning: bool = True, temperature: float = 0.0):
    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Context: {context} Question: {user_query}"},
    ]
    resp = _call_openrouter(messages=messages, reasoning=reasoning, temperature=temperature)
    choice = resp.get("choices", [None])[0]
    if not choice:
        raise RuntimeError(f"No choices returned from OpenRouter: {resp}")
    message = choice.get("message", {})
    assistant_text = message.get("content")
    reasoning_details = message.get("reasoning_details")

    print("\nmessage: ", message)
    print("\nassistant_text: ", assistant_text)
    print("\nreasoning_details: ", reasoning_details)
    return {"answer": assistant_text, "reasoning_details": reasoning_details[0] if isinstance(reasoning_details, list) else reasoning_details}