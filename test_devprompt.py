#!/usr/bin/env python3
"""
Test script that simulates a developer answering questions and evaluates the result
Uses the new conversational system with realistic project environments
"""
import os
from prompt_builder.core import interactive_interview, generate_prompt
from prompt_builder.conversation import conduct_conversation, ConversationState, generate_next_question
from prompt_builder.llm import chat
from prompt_builder.vendors import write_vendor_output, get_available_vendors
from test_environments import get_mock_project_context, get_project_summary_for_persona

class DeveloperSimulator:
    def __init__(self, role_description, persona_name):
        self.role_description = role_description
        self.persona_name = persona_name
        self.conversation_history = []
        
    def answer_question(self, field, question):
        """Simulate answering a question by having LLM roleplay as the developer"""
        
        # Build conversation context
        context = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.conversation_history])
        
        system_prompt = f"""You are roleplaying as: {self.role_description}

Your personality and response goals:
- Answer questions authentically based on your specific background, experience level, and current situation
- Share details about your actual work challenges, preferences, and coding practices
- Be helpful and engaged in the conversation - you genuinely want a better coding assistant
- Reveal information naturally that would be useful for customizing a coding assistant to your needs
- Stay consistent with your persona's experience level, project context, and communication style
- Show your actual motivations, frustrations, and goals related to coding

Response guidelines:
- Give specific, realistic answers that reflect your role
- Share concrete examples from your work when relevant
- Express your actual needs and preferences for coding assistance
- Keep responses conversational and natural (1-2 sentences typically)
- Build on the conversation context - don't repeat information unnecessarily

Remember: This conversation will be used to create a personalized coding assistant prompt for someone like you, so be genuine about what would actually help you in your work."""

        user_prompt = f"""Previous conversation:
{context}

Current question: {question}

Answer as {self.persona_name}:"""

        try:
            answer = chat(system_prompt, user_prompt)
            # Store in conversation history
            self.conversation_history.append((question, answer))
            return answer.strip()
        except Exception as e:
            # Fallback to simple response
            fallback = f"I'm not sure about that specific detail."
            self.conversation_history.append((question, fallback))
            return fallback

def automated_interview(developer_profile, persona_name):
    """Run the conversational interview process automatically using simulated answers"""
    simulator = DeveloperSimulator(developer_profile["description"], developer_profile["name"])
    
    # Get mock project context for this persona
    project_context = get_mock_project_context(persona_name)
    project_summary = get_project_summary_for_persona(persona_name)
    
    print("🤖 Starting automated conversational interview...")
    print(f"Simulating developer: {developer_profile['name']} ({developer_profile.get('description', 'Unknown')[:60]}...)")
    print(f"📁 Project context: {project_summary}")
    print("-" * 50)
    
    # Create conversation state with project context
    conversation = ConversationState(project_context)
    
    # Simulate the conversation
    while conversation.should_continue():
        try:
            question = generate_next_question(conversation)
            print(f"🤔 System: {question}")
        except Exception as e:
            print(f"🤔 Fallback: What brings you to use this coding assistant today?")
            question = "What brings you to use this coding assistant today?"
        
        answer = simulator.answer_question("conversation", question)
        print(f"👨‍💻 {developer_profile['name']}: {answer}")
        print()
        
        conversation.add_exchange(question, answer)

    return conversation

def evaluate_prompt(original_profile, generated_prompt):
    """Use an LLM to evaluate how well the prompt matches the developer"""
    
    evaluation_system = """You are an expert evaluator of AI prompts for coding assistants. 
    You will be given:
    1. A developer profile 
    2. A generated system prompt for a coding assistant
    
    Rate how well the prompt would serve this specific developer on a scale of 1-10, considering:
    - Relevance to their role and experience level
    - Appropriateness for their tech stack
    - Usefulness for their project context
    - Alignment with their communication style
    - Helpfulness for their common tasks
    
    Return your evaluation in this format:
    SCORE: X/10
    STRENGTHS: [list key strengths]
    WEAKNESSES: [list areas for improvement]
    RECOMMENDATION: [brief recommendation]"""
    
    evaluation_user = f"""
    DEVELOPER PROFILE:
    {original_profile}
    
    GENERATED PROMPT:
    {generated_prompt}
    
    Please evaluate how well this prompt would serve this developer."""
    
    return chat(evaluation_system, evaluation_user)

# Test developer personas - now defined as role descriptions for LLM roleplay
TEST_DEVELOPERS = {
    "senior_fullstack": {
        "description": "A senior full-stack developer with 8+ years of experience. You work at a tech company building microservices for e-commerce. You're pragmatic, value clean code and testing, prefer TypeScript/Python/Go. You're experienced with code reviews, mentoring junior developers, and making architectural decisions. You care about best practices but are flexible when deadlines matter.",
        "name": "Alex"
    },
    
    "junior_frontend": {
        "description": "A junior frontend developer with 1-2 years of experience. You're still learning React and building your portfolio website. You're enthusiastic but sometimes overwhelmed by all the tools and frameworks. You follow tutorials, ask lots of questions, and are trying to understand best practices. You know HTML/CSS/JavaScript basics and are learning modern development workflows.",
        "name": "Sam"
    },
    
    
    "computer_science_student": {
        "description": "A computer science student in your final semester with about 6 months of programming experience. You're working on a web-based student management system for your capstone project. You know Java, Python, and C++ from classes but are still learning practical development. You want patient explanations, learning resources, and help understanding concepts.",
        "name": "Casey"
    },
    
    "curious_beginner": {
        "description": "A curious but inexperienced developer who genuinely wants to learn and improve. You have about 8 months of coding experience and are excited about understanding how things work. You're working on a personal blog platform to practice and learn. You love asking 'why' and want to understand best practices, not just copy code. You prefer explanations that help you grow as a developer.",
        "name": "Alex"
    },
    
    "emergency_manager": {
        "description": "A project manager whose only developer is on vacation and you need to fix a critical bug in the company's customer portal. You have zero programming experience but the business is losing money every hour this is broken. You just need step-by-step instructions to get it working again - you're not trying to become a programmer, just solve this one crisis.",
        "name": "Sam"
    },
    
    "devops_engineer": {
        "description": "A mid-level DevOps engineer with 5 years of experience. You're migrating legacy applications to Kubernetes and implementing GitOps workflows. You write Python, Bash, YAML, and some Go. You think in terms of infrastructure as code, automation, and reliability. You're always dealing with production issues and care about monitoring and observability.",
        "name": "Morgan"
    },
    
    "mobile_developer": {
        "description": "A senior mobile developer with 6 years of experience. You're building a fitness tracking app with real-time analytics and offline sync. You work with Swift, Kotlin, Flutter, and React Native. You care deeply about performance, user experience, and app store guidelines. You're always thinking about battery life, memory usage, and cross-platform compatibility.",
        "name": "Taylor"
    },
    
    "freelance_consultant": {
        "description": "A freelance technical consultant with 12+ years of experience. You're currently architecting an e-commerce platform for a mid-size retail client. You work with JavaScript, Python, PHP, and Java depending on client needs. You balance quality with time constraints, communicate with non-technical stakeholders, and need to deliver quickly while managing multiple projects.",
        "name": "Avery"
    },
    
    "security_engineer": {
        "description": "A senior security engineer with 7 years of experience. You're implementing zero-trust security architecture for a fintech company. You work with Python, C++, JavaScript, and SQL, always thinking about threats and vulnerabilities. You follow OWASP guidelines, do penetration testing, and review code for security issues. You're paranoid by nature and always thinking about what could go wrong.",
        "name": "Cameron"
    },
    
    "startup_cto": {
        "description": "A startup CTO with 10+ years of experience. You're building an MVP for an AI-powered SaaS platform while scaling your engineering team. You work with TypeScript, Python, Go, and Rust. You make technology strategy decisions, present to investors, mentor your team, but still code when needed. You balance technical debt with speed to market and are always thinking about scalability.",
        "name": "Quinn"
    },
    
    "data_scientist": {
        "description": "A data scientist with 4 years of experience working on customer behavior analysis. You primarily use Python, R, and SQL to build machine learning models and create data visualizations. You work with Jupyter notebooks, pandas, scikit-learn, and TensorFlow. You care about data quality, reproducible research, and translating complex findings into business insights. You collaborate with product teams and present findings to stakeholders.",
        "name": "Taylor"
    },
    
    "reserved_developer": {
        "description": "A mid-level backend developer with 4 years of experience who is naturally reserved and doesn't volunteer much information. You're working on a high-performance trading system with strict latency requirements. You use C++, Python, and some Rust. You're dealing with significant technical debt and legacy code issues that are causing performance bottlenecks. You tend to give brief, professional answers and don't elaborate unless specifically asked. The reality is the codebase is a mess of spaghetti code from multiple previous developers, there are no proper tests, deployment is manual and error-prone, and you're under pressure to maintain microsecond-level latency while fixing these underlying issues. You're naturally hesitant to complain or admit how problematic things are, preferring to focus on technical solutions rather than discussing systemic problems.",
        "name": "Jordan"
    },
    
    "extremely_reserved": {
        "description": "A senior developer with 6 years of experience who is extremely reluctant to share details about problems. You're working on a critical medical device control system using C and embedded systems. On the surface, you'll only mention basic technical work. You NEVER volunteer information about serious issues unless asked very specific follow-up questions. The reality is: you're the only person who understands a life-critical legacy system that controls patient monitoring equipment, the original team left years ago with no documentation, the code is 15+ years old with no version control, a single bug could literally kill patients, you're burning out from the pressure and responsibility, management doesn't understand the technical risks, and you desperately need help but are afraid to admit how precarious everything is. You will only reveal these critical details if pressed with multiple specific questions about challenges, testing, documentation, or team situation.",
        "name": "Sam"
    }
}

def show_dialog(developer_name, developer_data):
    """Show the conversational interview as a User-System dialog"""
    print(f"\n{'='*80}")
    print(f"🎯 {developer_name.upper().replace('_', ' ')} ({developer_data['name']})")
    print(f"{'='*80}")
    
    project_summary = get_project_summary_for_persona(developer_name)
    print(f"📁 Project context: {project_summary}")
    print()
    
    conversation = automated_interview(developer_data, developer_name)

    # Generate and display the final prompt
    print(f"\n{'='*80}")
    print("📝 GENERATED PROMPT:")
    print(f"{'='*80}")
    
    generated_prompt = generate_prompt(conversation)
    print(generated_prompt)
    print(f"{'='*80}")
    
    return conversation, generated_prompt

def run_test(developer_name, show_dialog_flag=False, show_prompt_flag=False, show_review_flag=False, output_vendor=None):
    """Run complete test for a specific developer profile"""
    if developer_name not in TEST_DEVELOPERS:
        print(f"❌ Unknown developer: {developer_name}")
        print(f"Available: {list(TEST_DEVELOPERS.keys())}")
        return
        
    developer_data = TEST_DEVELOPERS[developer_name]
    
    if show_dialog_flag:
        # Show dialog
        conversation, generated_prompt = show_dialog(developer_name, developer_data)
    else:
        # Generate without showing dialog
        conversation = automated_interview(developer_data, developer_name)
        generated_prompt = generate_prompt(conversation)
    
    # Handle vendor output
    if output_vendor:
        try:
            output_path = write_vendor_output(output_vendor, generated_prompt, developer_data)
            vendor_name = get_available_vendors()[output_vendor]
            print(f"✅ Generated {vendor_name} rules: {output_path}")
            return
        except Exception as e:
            print(f"❌ Error writing vendor output: {e}")
            return
    
    if show_prompt_flag and not show_dialog_flag:
        # Show just the prompt
        print(f"\n{'='*80}")
        print(f"📝 GENERATED PROMPT FOR {developer_name.upper().replace('_', ' ')}")
        print(f"{'='*80}")
        print(generated_prompt)
        print(f"{'='*80}")
    
    # Show evaluation
    if show_dialog_flag or show_prompt_flag or show_review_flag:
        if not show_review_flag:  # Don't show this message for review-only mode
            print("🔍 Evaluating prompt quality...")
        evaluation = evaluate_prompt(developer_data, generated_prompt)
        
        if show_review_flag:
            # Review-only mode: just output the evaluation
            print(evaluation)
        else:
            print("📊 Evaluation Results:")
            print("-" * 30)
            print(evaluation)
            print("-" * 30)

def main():
    import sys
    
    # Parse arguments
    args = sys.argv[1:]
    show_dialog = False
    show_prompt = False
    show_review = False
    output_vendor = None
    developer_name = None
    
    # Parse flags
    if "-v" in args or "--verbose" in args:
        show_dialog = True
        show_prompt = True
        args = [arg for arg in args if arg not in ["-v", "--verbose"]]
    
    if "-d" in args or "--dialog" in args:
        show_dialog = True
        args = [arg for arg in args if arg not in ["-d", "--dialog"]]
    
    if "-p" in args or "--prompt" in args:
        show_prompt = True
        args = [arg for arg in args if arg not in ["-p", "--prompt"]]
    
    if "-r" in args or "--review" in args:
        show_review = True
        args = [arg for arg in args if arg not in ["-r", "--review"]]
    
    # Parse vendor output flag
    for i, arg in enumerate(args):
        if arg in ["--output-format", "-o"]:
            if i + 1 < len(args):
                output_vendor = args[i + 1]
                args = args[:i] + args[i+2:]  # Remove both flag and value
                break
    
    if len(args) != 1:
        available_vendors = get_available_vendors()
        print("Usage: python test_devprompt.py [flags] <developer_name>")
        print(f"Available developers: {list(TEST_DEVELOPERS.keys())}")
        print()
        print("Flags:")
        print("  -v, --verbose              Show dialog + prompt (equivalent to -dp)")
        print("  -d, --dialog               Show User-System dialog only")
        print("  -p, --prompt               Show generated prompt only")
        print("  -r, --review               Show evaluation/review only")
        print("  -o, --output-format <fmt>  Write to vendor-specific file")
        print("  (no flags)                 Show evaluation only")
        print()
        print("Available output formats:")
        for key, name in available_vendors.items():
            print(f"  {key:<10} {name}")
        return
    
    developer_name = args[0]
    run_test(developer_name, show_dialog, show_prompt, show_review, output_vendor)

if __name__ == "__main__":
    main()