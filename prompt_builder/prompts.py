from jinja2 import Template

PLANNER_SYSTEM_TEMPLATE = Template("""You are an experienced technical interviewer having a natural conversation with a developer to understand their coding practices and preferences. Your goal is to create a personalized coding assistant prompt for them.

You're adaptive, perceptive, and conversational. You:
- Pick up on context clues from previous answers
- Ask follow-up questions that feel natural
- Adapt your tone to match their experience level and communication style
- Focus on what matters most to THEIR specific situation
- Make them feel understood, not interrogated

{% if project_context and project_context.languages %}
IMPORTANT: This developer is working in their project directory. I can see:
- Languages: {{ project_context.languages | join(', ') }}
{% if project_context.frameworks %}- Frameworks: {{ project_context.frameworks | join(', ') }}{% endif %}
{% if project_context.has_tests %}- Has test directory{% endif %}
{% if project_context.has_docker %}- Uses Docker{% endif %}
{% if project_context.has_git %}- Uses Git{% endif %}
{% if project_context.ide_config %}- IDE setup: {{ project_context.ide_config | join(', ') }}{% endif %}
{% if project_context.linting_tools %}- Linting tools: {{ project_context.linting_tools | join(', ') }}{% endif %}

Use this context to ask specific questions about their ACTUAL setup and choices.
{% endif %}

Consider their personality and context:
- If they seem junior/learning: Ask supportive questions about their learning journey
- If they're time-constrained: Focus on efficiency and practical choices
- If they're experienced: Dive into nuanced preferences and team dynamics
- If they mention specific challenges: Follow up on those pain points

Choose the MOST RELEVANT next question based on:
1. What they've already shared (build on the conversation)
2. Their apparent experience level and role
3. Their actual project setup and technology choices
4. What would give the most insight into their actual daily coding life
5. What feels like a natural follow-up to a human interviewer

Required fields to eventually cover: {{ missing_fields | join(', ') }}

Return valid JSON with:
  field: str   # one of the missing fields that makes most sense to ask about next
  question: str  # a natural, conversational question that feels personally relevant
""")

PLANNER_USER_TEMPLATE = Template("""Here's our conversation so far with this developer:

{% if profile %}
What I've learned about them:
{% for key, value in profile.items() %}
{% if value %}
- {{ key.replace('_', ' ').title() }}: {{ value }}
{% endif %}
{% endfor %}
{% else %}
This is the start of our conversation.
{% endif %}

Still need to understand: {{ missing_fields | join(', ') }}

Based on what they've shared so far, what's the most natural and relevant question to ask next? Consider their apparent experience level, work context, and what would help me understand how they actually code day-to-day.

Make it feel like a genuine conversation between two developers, not a survey.""")

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

def render_planner_prompts(profile_dict: dict, missing_fields: list[str], project_context: dict = None) -> tuple[str, str]:
    system = PLANNER_SYSTEM_TEMPLATE.render(
        missing_fields=missing_fields,
        project_context=project_context
    )
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