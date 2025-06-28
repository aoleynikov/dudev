#!/usr/bin/env python3
"""
Test script that simulates a developer answering questions and evaluates the result
"""
import os
from prompt_builder.core import interactive_interview, generate_prompt
from prompt_builder.schema import Profile, MIN_FIELDS
from prompt_builder.planner import choose_field_llm
from prompt_builder.llm import chat
from prompt_builder.prompts import render_fallback_question
from prompt_builder.vendors import write_vendor_output, get_available_vendors

class DeveloperSimulator:
    def __init__(self, developer_profile):
        self.profile_data = developer_profile
        
    def answer_question(self, field, question):
        """Simulate answering a question based on the developer profile"""
        return self.profile_data.get(field, f"I'm not sure about {field}")

def automated_interview(developer_profile):
    """Run the interview process automatically using simulated answers"""
    simulator = DeveloperSimulator(developer_profile)
    profile = Profile()
    
    print("🤖 Starting automated interview simulation...")
    print(f"Simulating developer: {developer_profile.get('role', 'Unknown')}")
    print("-" * 50)
    
    while True:
        missing = [f for f in MIN_FIELDS if getattr(profile, f) is None]
        if not missing:
            break

        try:
            field, question = choose_field_llm(profile.dict(), missing)
            print(f"🤔 LLM asks: {question}")
        except Exception as e:
            field = missing[0]
            question = render_fallback_question(field)
            print(f"🤔 Fallback question: {question}")
        
        answer = simulator.answer_question(field, question)
        print(f"👨‍💻 Developer answers: {answer}")
        print()
        
        setattr(profile, field, answer)

    return profile

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

# Test developer profiles
TEST_DEVELOPERS = {
    "senior_fullstack": {
        "intended_use": "Daily coding workflow, code reviews, and architectural decisions",
        "primary_languages": "TypeScript, Python, Go",
        "coding_style": "Standard conventions, prefer functional patterns, strict TypeScript config",
        "testing_approach": "Jest for TS, pytest for Python, 90% coverage minimum, TDD preferred",
        "tooling_preferences": "VS Code, Docker for dev, GitHub Actions for CI",
        "workflow_process": "Feature branch → Tests first → Implementation → PR review → Merge",
        "current_project": "Building a microservices architecture for e-commerce platform", 
        "experience_level": "Senior (8+ years)"
    },
    
    "junior_frontend": {
        "intended_use": "Learning new concepts and debugging help while coding",
        "primary_languages": "JavaScript, HTML, CSS, React",
        "coding_style": "Following Prettier/ESLint, learning component patterns",
        "testing_approach": "Just started with basic unit tests, no TDD yet",
        "current_project": "Learning React and building portfolio website",
        "experience_level": "Junior (1-2 years)",
        "common_tasks": "Component development, styling, debugging, learning new frameworks"
    },
    
    "data_scientist": {
        "intended_use": "Data analysis, model prototyping, and statistical exploration",
        "role": "Data Scientist",
        "experience_level": "Mid-level (4 years)",
        "primary_languages": "Python, R, SQL",
        "current_project": "Machine learning model for customer churn prediction", 
        "preferred_style": "Mathematical explanations with practical implementation",
        "common_tasks": "Data analysis, model training, visualization, statistical testing"
    },
    
    "computer_science_student": {
        "intended_use": "Homework help, learning programming concepts, and project guidance",
        "role": "Computer Science Student",
        "experience_level": "Beginner (6 months)",
        "primary_languages": "Java, Python, C++",
        "current_project": "Final semester project building a web-based student management system",
        "preferred_style": "Patient explanations with learning resources and practice exercises",
        "common_tasks": "Learning algorithms, homework assignments, debugging code, understanding concepts"
    },
    
    "hobbyist_parent": {
        "intended_use": "Weekend hobby projects and learning web development in spare time",
        "role": "Parent/Homemaker with Programming Hobby",
        "experience_level": "Self-taught beginner (2 years on and off)",
        "primary_languages": "Python, HTML/CSS, JavaScript",
        "current_project": "Building a family expense tracker app in spare time",
        "preferred_style": "Simple explanations that fit into busy schedule, bite-sized learning",
        "common_tasks": "Weekend coding projects, following tutorials, automating household tasks, learning web development"
    },
    
    "devops_engineer": {
        "intended_use": "Infrastructure automation, CI/CD pipeline management, and incident response",
        "primary_languages": "Python, Bash, YAML, Go",
        "coding_style": "Infrastructure as Code, declarative configs, immutable deployments",
        "testing_approach": "Infrastructure testing with Terratest, pipeline validation, smoke tests",
        "current_project": "Migrating legacy applications to Kubernetes and implementing GitOps workflows",
        "experience_level": "Mid-level (5 years)",
        "common_tasks": "Infrastructure as code, deployment automation, monitoring setup, troubleshooting production issues"
    },
    
    "mobile_developer": {
        "intended_use": "Cross-platform mobile app development and performance optimization",
        "role": "Mobile Developer",
        "experience_level": "Senior (6 years)",
        "primary_languages": "Swift, Kotlin, Flutter/Dart, React Native",
        "current_project": "Building a fitness tracking app with real-time analytics and offline sync",
        "preferred_style": "Code examples with performance considerations and best practices",
        "common_tasks": "UI/UX implementation, API integration, performance optimization, app store deployment"
    },
    
    "freelance_consultant": {
        "intended_use": "Client project delivery, rapid prototyping, and technical consultation",
        "role": "Freelance Technical Consultant",
        "experience_level": "Expert (12+ years)",
        "primary_languages": "JavaScript, Python, PHP, Java",
        "current_project": "Architecting e-commerce platform for mid-size retail client",
        "preferred_style": "Efficient solutions that balance quality with time constraints",
        "common_tasks": "Requirements gathering, system architecture, client communication, rapid development"
    },
    
    "security_engineer": {
        "intended_use": "Security analysis, vulnerability assessment, and secure code review",
        "primary_languages": "Python, C++, JavaScript, SQL",
        "coding_style": "Secure coding practices, OWASP guidelines, defensive programming",
        "testing_approach": "Security-focused testing: SAST, DAST, penetration testing, fuzzing",
        "current_project": "Implementing zero-trust security architecture for fintech company",
        "experience_level": "Senior (7 years)",
        "common_tasks": "Threat modeling, penetration testing, security audits, incident response"
    },
    
    "startup_cto": {
        "intended_use": "Technical leadership, architectural decisions, and team mentoring",
        "primary_languages": "TypeScript, Python, Go, Rust",
        "coding_style": "Pragmatic architecture, microservices, event-driven design",
        "testing_approach": "Balanced approach: critical path TDD, integration tests, minimal viable testing",
        "current_project": "Building MVP for AI-powered SaaS platform while scaling engineering team",
        "experience_level": "Expert (10+ years)",
        "common_tasks": "Technology strategy, team building, investor presentations, hands-on coding when needed"
    }
}

def show_dialog(developer_name, developer_data):
    """Show the interview as a User-System dialog"""
    print(f"\n{'='*80}")
    print(f"🎯 {developer_name.upper().replace('_', ' ')}")
    print(f"{'='*80}")
    
    simulator = DeveloperSimulator(developer_data)
    profile = Profile()
    
    while True:
        missing = [f for f in MIN_FIELDS if getattr(profile, f) is None]
        if not missing:
            break

        try:
            field, question = choose_field_llm(profile.dict(), missing)
            print(f"\n🤖 System: {question}")
        except Exception as e:
            field = missing[0]
            question = render_fallback_question(field)
            print(f"\n🤖 System: {question}")
        
        answer = simulator.answer_question(field, question)
        print(f"👨‍💻 User: {answer}")
        
        setattr(profile, field, answer)

    # Generate and display the final prompt
    print(f"\n{'='*80}")
    print("📝 GENERATED PROMPT:")
    print(f"{'='*80}")
    
    generated_prompt = generate_prompt(profile)
    print(generated_prompt)
    print(f"{'='*80}")
    
    return profile, generated_prompt

def run_test(developer_name, show_dialog_flag=False, show_prompt_flag=False, output_vendor=None):
    """Run complete test for a specific developer profile"""
    if developer_name not in TEST_DEVELOPERS:
        print(f"❌ Unknown developer: {developer_name}")
        print(f"Available: {list(TEST_DEVELOPERS.keys())}")
        return
        
    developer_data = TEST_DEVELOPERS[developer_name]
    
    if show_dialog_flag:
        # Show dialog
        profile, generated_prompt = show_dialog(developer_name, developer_data)
    else:
        # Generate without showing dialog
        simulator = DeveloperSimulator(developer_data)
        profile = Profile()
        
        while True:
            missing = [f for f in MIN_FIELDS if getattr(profile, f) is None]
            if not missing:
                break

            try:
                field, question = choose_field_llm(profile.dict(), missing)
            except Exception as e:
                field = missing[0]
                question = render_fallback_question(field)
            
            answer = simulator.answer_question(field, question)
            setattr(profile, field, answer)
        
        generated_prompt = generate_prompt(profile)
    
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
    
    # Always show evaluation
    if show_dialog_flag or show_prompt_flag:
        print("🔍 Evaluating prompt quality...")
        evaluation = evaluate_prompt(developer_data, generated_prompt)
        
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
        print("  -o, --output-format <fmt>  Write to vendor-specific file")
        print("  (no flags)                 Show evaluation only")
        print()
        print("Available output formats:")
        for key, name in available_vendors.items():
            print(f"  {key:<10} {name}")
        return
    
    developer_name = args[0]
    run_test(developer_name, show_dialog, show_prompt, output_vendor)

if __name__ == "__main__":
    main()