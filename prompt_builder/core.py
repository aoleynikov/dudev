from .conversation import conduct_conversation, conversation_to_prompt_context
from .schema import Profile, MIN_FIELDS  # Keep for backwards compatibility
from .llm import chat, ensure_json
from .prompts import render_generator_prompts, render_fallback_question
from .project_context import analyze_project_context, get_project_summary, should_enhance_questions
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o-mini")

def interactive_interview():
    """New conversational interview - no rigid fields"""
    conversation = conduct_conversation()
    return conversation

def interactive_interview_legacy():
    """Legacy field-based interview for backwards compatibility"""
    # Analyze project context from current directory
    project_context = analyze_project_context()
    project_summary = get_project_summary(project_context)
    
    # Show project context if detected
    if should_enhance_questions(project_context):
        print(f"📁 Project detected: {project_summary}")
        print("💡 I'll tailor questions based on your project setup.\n")
    
    profile = Profile()
    question_count = 0
    
    while True:
        missing = [f for f in MIN_FIELDS if getattr(profile, f) is None]
        
        # Import here to avoid circular imports
        from .stopping_logic import should_continue_questioning, get_stopping_reason, get_question_priority_for_experience
        
        # Check if we should stop questioning based on experience and responses
        if not missing or not should_continue_questioning(profile.dict(), missing):
            if missing:
                # We're stopping early - show friendly message
                print(f"\n{get_stopping_reason(profile.dict(), missing)}")
            break

        # Prioritize questions based on user experience level
        prioritized_missing = get_question_priority_for_experience(profile.dict(), missing)
        if prioritized_missing:
            missing = prioritized_missing

        try:
            from .planner import choose_field_llm
            field, question = choose_field_llm(profile.dict(), missing, project_context)
        except Exception as e:
            # Fallback to first missing field if planner fails
            field = missing[0]
            question = render_fallback_question(field)
        
        answer = input(f"{question} > ").strip()
        setattr(profile, field, answer)
        question_count += 1
        
        # Safety valves based on user type
        experience_level = profile.experience_level or ""
        intended_use = profile.intended_use or ""
        
        # More aggressive limits for beginners and hobbyists
        max_questions = 8  # Default
        if any(word in experience_level.lower() for word in ['beginner', 'student', 'learning', 'hobby']):
            max_questions = 5
        elif any(word in intended_use.lower() for word in ['homework', 'learning', 'hobby', 'personal', 'spare time']):
            max_questions = 6
            
        if question_count >= max_questions:
            print(f"\n🎯 That gives me a great understanding of your needs!")
            break

    return profile

def generate_prompt(profile_or_conversation) -> str:
    """Generate prompt from either old Profile or new ConversationState"""
    
    # Check if it's the new conversation system
    if hasattr(profile_or_conversation, 'exchanges'):
        # New conversational approach
        context = conversation_to_prompt_context(profile_or_conversation)
        return generate_prompt_from_conversation(context)
    else:
        # Legacy Profile approach
        system, user = render_generator_prompts(profile_or_conversation)
        return chat(system, user)

def generate_prompt_from_conversation(context: dict) -> str:
    """Generate prompt from conversational context using strategy-aware approach"""
    
    strategy_used = context.get('strategy_used', 'generic')
    conversation_text = context.get('full_conversation_text', '')
    insights = context.get('insights', {})
    developer_type = context.get('developer_type', 'general_developer')
    project_context = context.get('project_context', {})
    
    # Adapt system prompt based on strategy used
    if strategy_used == "educational":
        system_prompt = """You are an expert at creating personalized coding assistant prompts for LEARNING-FOCUSED developers. These are people genuinely interested in growing their programming skills. Create a supportive, educational prompt that helps them learn and improve.

Your task is to:
1. Create guidance that builds understanding and knowledge
2. Focus on foundational practices and concepts
3. Include educational explanations for WHY practices matter
4. Provide learning resources and growth paths
5. Use encouraging, supportive language
6. Build confidence while introducing best practices gradually

Create a prompt that supports their learning journey and skill development."""
        
        user_prompt = f"""Based on this conversation with a developer who wants to learn and improve their coding skills, create a supportive coding assistant prompt:

**Conversation:**
{conversation_text}

**Developer Profile:** {developer_type} (learning-focused)
**Learning Goals:** {insights}
**Project Context:** {project_context}

Generate a learning-focused prompt that includes:
- Foundational coding practices with explanations
- Educational context for WHY practices matter
- Learning resources and next steps for growth
- Supportive, encouraging language
- Gradual introduction of best practices
- Confidence-building guidance

Make it educational and supportive. Focus on building understanding and good habits over time."""
        
    elif strategy_used == "emergency":
        system_prompt = """You are an expert at creating MINIMAL, CRISIS-RESOLUTION coding assistant prompts for non-programmers facing technical emergencies. These users have zero programming experience and just need to fix something broken.

CRITICAL REQUIREMENTS:
1. NO testing frameworks or coverage requirements
2. NO complex tooling setups (no ESLint, Prettier, etc.)
3. NO git workflows, branching, or pull requests
4. NO "best practices" - focus on "works quickly"
5. NO educational explanations - just direct instructions
6. NO industry standards - use whatever is simplest
7. Step-by-step instructions for non-programmers
8. Focus on immediate crisis resolution

Your goal: Create the FASTEST path to fixing the broken system."""
        
        user_prompt = f"""Based on this conversation with a non-programmer facing a technical emergency, create an extremely practical, crisis-resolution prompt:

**Conversation:**
{conversation_text}

**User Profile:** {developer_type} (emergency crisis situation)
**Crisis Details:** {insights}
**System Context:** {project_context}

Generate a CRISIS-RESOLUTION prompt that includes ONLY:
- Step-by-step instructions for non-programmers
- The absolute minimum needed to fix the problem
- Direct commands they can copy and paste
- Simple troubleshooting steps
- Skip ALL non-essential activities
- Focus on getting the system working again

AVOID completely:
- Testing frameworks or coverage
- Code formatting tools  
- Git workflows and conventions
- "Best practices" or "industry standards"
- Complex explanations
- Anything not directly related to fixing the crisis

Make it emergency-focused. They need it working NOW."""
        
    elif strategy_used == "advanced":
        system_prompt = """You are an expert at creating personalized coding assistant prompts for EXPERIENCED developers. Based on a conversation with a senior developer, create a sophisticated prompt that respects their expertise.

Your task is to:
1. Generate advanced, nuanced guidance
2. Focus on architectural decisions and trade-offs
3. Address team leadership and mentoring aspects
4. Include professional workflow optimizations
5. Respect their experience and judgment
6. Cover scaling and enterprise considerations

Create a prompt that enhances their professional effectiveness."""
        
        user_prompt = f"""Based on this conversation with an experienced developer, create a professional coding assistant prompt:

**Conversation:**
{conversation_text}

**Developer Profile:** {developer_type} (advanced level)
**Professional Context:** {insights}
**Project Context:** {project_context}

Generate a sophisticated prompt that includes:
- Advanced architectural and design patterns
- Team leadership and code review practices
- Professional workflow and tool optimizations
- Scaling and performance considerations
- Mentoring and knowledge sharing approaches
- Enterprise-level best practices

Make it professionally focused and respect their expertise. Address complex scenarios and trade-offs."""
        
    else:
        # Generic/fallback approach - let LLM determine experience level from conversation
        # Determine experience level from conversation context
        experience_detection_prompt = f"""Based on this conversation, what is the developer's experience level?

Conversation:
{conversation_text}

Respond with just one word: "beginner", "intermediate", or "advanced"
- beginner: New to coding, learning basics, less than 2 years experience
- intermediate: Some experience, 2-5 years, comfortable with basics
- advanced: Senior level, 5+ years, leads projects/teams"""

        try:
            experience_level = chat("You determine developer experience levels.", experience_detection_prompt).strip().lower()
            if experience_level not in ['beginner', 'intermediate', 'advanced']:
                experience_level = 'intermediate'  # default fallback
        except:
            experience_level = 'intermediate'  # fallback on error
        
        if experience_level == 'beginner':
            system_prompt = """You are an expert at creating personalized coding assistant prompts for BEGINNER developers. Based on a conversation with a new developer, create a supportive, learning-focused prompt that won't overwhelm them.

Your task is to:
1. Focus on foundational practices and learning
2. Prioritize essential tools and workflows
3. Include educational resources and explanations
4. Keep recommendations simple and actionable
5. Encourage growth and experimentation

Create a prompt that supports their learning journey without overwhelming them."""
            
            user_prompt = f"""Based on this conversation with a beginner developer, create a supportive coding assistant prompt:

**Conversation:**
{conversation_text}

**Developer Profile:** {developer_type} (beginner level)
**Learning Focus:** {insights}
**Project Context:** {project_context}

Generate a beginner-friendly prompt that includes ONLY:
- Essential coding practices for their current project
- Simple, beginner-appropriate tools
- Learning resources and explanations
- Encouragement for experimentation
- Basic workflow suggestions

Keep it supportive and avoid overwhelming them with too many tools or complex concepts."""
            
        elif experience_level == 'advanced':
            system_prompt = """You are an expert at creating personalized coding assistant prompts for EXPERIENCED developers. Based on a conversation with a senior developer, create a sophisticated prompt that respects their expertise.

Your task is to:
1. Generate advanced, nuanced guidance
2. Focus on architectural decisions and trade-offs
3. Address professional workflow optimizations
4. Include scaling and enterprise considerations
5. Respect their experience and judgment

Create a prompt that enhances their professional effectiveness."""
            
            user_prompt = f"""Based on this conversation with an experienced developer, create a professional coding assistant prompt:

**Conversation:**
{conversation_text}

**Developer Profile:** {developer_type} (advanced level)
**Professional Context:** {insights}
**Project Context:** {project_context}

Generate a sophisticated prompt that includes:
- Advanced architectural and design patterns
- Professional workflow and tool optimizations
- Scaling and performance considerations
- Team leadership and code review practices
- Enterprise-level best practices

Make it professionally focused and respect their expertise."""
            
        else:
            # Intermediate or unknown experience level
            system_prompt = """You are an expert at creating personalized coding assistant prompts. Based on a natural conversation with a developer, create a balanced, practical prompt that will make their coding assistant more helpful.

Your task is to:
1. Synthesize insights from the conversation 
2. Consider their project context and experience level
3. Generate practical, actionable instructions
4. Focus on essential practices and tools
5. Make assumptions about industry standards they likely follow

Create a prompt that feels personalized but not overwhelming."""
            
            user_prompt = f"""Based on this conversation with a developer, create a balanced coding assistant prompt:

**Conversation:**
{conversation_text}

**Developer Profile:** {developer_type}
**Key Insights:** {insights}
**Project Context:** {project_context}

Generate a practical prompt that includes:
- Essential coding practices for their project
- Appropriate testing approach and tools
- Code formatting preferences (assume industry standards)
- Basic workflow suggestions
- Language-specific guidance for their stack

Make it actionable and specific to their context, but avoid overwhelming them with too many recommendations."""

    return chat(system_prompt, user_prompt)