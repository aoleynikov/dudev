from jinja2 import Template

PLANNER_SYSTEM_TEMPLATE = Template("""You're interviewing a developer to understand their coding practices, assuming they follow industry standards unless they specify otherwise. Focus on deviations from conventions and specific tool choices.

Given a JSON `profile` and a list `missing_fields`, choose ONE field that would give the most actionable insight. Priority order:
1. "intended_use" - what they use their IDE for
2. "primary_languages" - their tech stack  
3. "coding_style" - deviations from language conventions, custom rules
4. "testing_approach" - preferred testing tools within standard practices
5. "tooling_preferences" - specific tools, assuming standard linters/formatters for their languages
6. "workflow_process" - their variation of standard dev workflow
7. "current_project" - technical context
8. "experience_level" - skill level

Assume industry standards (Prettier for JS/TS, Black for Python, gofmt for Go, etc.) and ask about:
- Specific tool choices within standard options
- Deviations from common conventions
- Preferences between established alternatives
- Project-specific requirements

Return valid JSON with:
  field: str   # one of missing_fields  
  question: str  # asking about choices within industry standards
""")

PLANNER_USER_TEMPLATE = Template("""I'm interviewing this developer to create specific coding rules. Here's what I know:
{{ profile | tojson }}

Still need: {{ missing_fields | tojson }}

What should I ask next? Focus on getting concrete, actionable preferences that can become specific coding rules.""")

GENERATOR_SYSTEM_TEMPLATE = Template("""You are a prompt generator creating ACTIONABLE coding rules. Generate a system prompt that assumes industry standard practices for the given languages and only specifies deviations, tool choices, and project-specific rules.

ASSUME industry standards by default:
- Prettier/ESLint for TypeScript/JavaScript
- Black/flake8 for Python  
- gofmt/golangci-lint for Go
- Standard directory structures (src/, test/, etc.)
- Common naming conventions for each language

ONLY specify:
- Chosen tools within standard options
- Deviations from language conventions
- Project-specific requirements
- Workflow variations from standard practices
- Team-specific rules beyond language defaults

Make it practical "house rules" that complement, not replace, industry standards.""")

GENERATOR_USER_TEMPLATE = Template("""Create coding rules assuming industry standards for {{ primary_languages }}:

Intended Use: {{ intended_use }}
Primary Languages: {{ primary_languages }}
Coding Style: {{ coding_style }}
Testing Approach: {{ testing_approach }}
Tooling Preferences: {{ tooling_preferences }}
Workflow Process: {{ workflow_process }}
Current Project: {{ current_project }}
Experience Level: {{ experience_level }}

Generate rules that complement standard practices, focusing on:
- Specific tool choices (e.g., "Use Jest over Mocha", "Use pytest over unittest")
- Project-specific requirements (e.g., coverage thresholds, directory structure)
- Team workflow preferences (e.g., PR process, commit conventions)
- Deviations from defaults only where specified

Assume developers know language conventions - focus on project/team specifics.""")

FALLBACK_QUESTION_TEMPLATE = Template("""Hey, tell me about your {{ field_name }} - I'm curious!""")

def render_planner_prompts(profile_dict: dict, missing_fields: list[str]) -> tuple[str, str]:
    system = PLANNER_SYSTEM_TEMPLATE.render()
    user = PLANNER_USER_TEMPLATE.render(
        profile=profile_dict,
        missing_fields=missing_fields
    )
    return system, user

def render_generator_prompts(profile) -> tuple[str, str]:
    system = GENERATOR_SYSTEM_TEMPLATE.render()
    user = GENERATOR_USER_TEMPLATE.render(
        intended_use=profile.intended_use,
        primary_languages=profile.primary_languages,
        coding_style=profile.coding_style,
        testing_approach=profile.testing_approach,
        tooling_preferences=profile.tooling_preferences,
        workflow_process=profile.workflow_process,
        current_project=profile.current_project,
        experience_level=profile.experience_level
    )
    return system, user

def render_fallback_question(field: str) -> str:
    return FALLBACK_QUESTION_TEMPLATE.render(
        field_name=field.replace('_', ' ')
    )