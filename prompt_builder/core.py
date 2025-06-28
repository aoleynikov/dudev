from .planner import choose_field_llm
from .schema import Profile, MIN_FIELDS
from .llm import chat, ensure_json
from .prompts import render_generator_prompts, render_fallback_question
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o-mini")

def interactive_interview():
    profile = Profile()
    while True:
        missing = [f for f in MIN_FIELDS if getattr(profile, f) is None]
        if not missing:
            break

        try:
            field, question = choose_field_llm(profile.dict(), missing)
        except Exception as e:
            # Fallback to first missing field if planner fails
            field = missing[0]
            question = render_fallback_question(field)
        
        answer = input(f"{question} > ").strip()
        setattr(profile, field, answer)

    return profile

def generate_prompt(profile: Profile) -> str:
    system, user = render_generator_prompts(profile)
    return chat(system, user)