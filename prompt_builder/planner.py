from .schema import MIN_FIELDS
from .llm import chat, ensure_json
from .prompts import render_planner_prompts

def choose_field_llm(profile_dict: dict, missing: list[str]) -> tuple[str, str]:
    system, user = render_planner_prompts(profile_dict, missing)
    raw = chat(system, user)
    data = ensure_json(raw)
    return data["field"], data["question"]