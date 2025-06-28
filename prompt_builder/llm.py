import openai
import os
import json

_client = openai.OpenAI()

def chat(system: str, user: str, model="gpt-4o-mini") -> str:
    resp = _client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user",   "content": user}],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()

def ensure_json(txt: str) -> dict:
    try:
        # Handle code blocks
        if "```json" in txt:
            txt = txt.split("```json")[1].split("```")[0].strip()
        elif "```" in txt:
            txt = txt.split("```")[1].split("```")[0].strip()
        
        return json.loads(txt)
    except Exception:
        raise ValueError(f"Bad JSON from LLM: {txt}")