"""
Conversational interview system - no rigid fields, just natural dialogue
Uses simple questioning approach without strategy pattern complexity
"""
from typing import Dict, Any, List, Optional
from .llm import chat
from .project_context import analyze_project_context, get_project_summary
import json

class ConversationState:
    """Tracks the state of our conversation with the developer"""
    
    def __init__(self, project_context: Dict[str, Any] = None):
        self.exchanges: List[Dict[str, str]] = []
        self.insights: Dict[str, Any] = {}
        self.project_context = project_context or {}
        self.context_summary = ""
        self.developer_type = None
        self.conversation_depth = 0
        
    def add_exchange(self, question: str, answer: str):
        """Add a question-answer exchange"""
        self.exchanges.append({
            "question": question,
            "answer": answer
        })
        self.conversation_depth += 1
        
        # Only extract insights when we have enough conversation content
        if self.conversation_depth >= 2:
            self._extract_insights_from_full_conversation()
        self._detect_developer_type()
    
    def _extract_insights_from_full_conversation(self):
        """Extract insights using LLM analysis of the full conversation"""
        # Build full conversation text
        conversation_text = ""
        for exchange in self.exchanges:
            conversation_text += f"Q: {exchange['question']}\nA: {exchange['answer']}\n"
        
        insight_prompt = f"""Analyze this conversation and extract key insights about the developer. Return ONLY a JSON object with these fields:

{{
    "languages": ["list of programming languages mentioned"],
    "testing_interest": true/false,
    "learning_focused": true/false,
    "experience_indicators": ["any words/phrases indicating experience level"],
    "project_focus": "brief description of what they're working on",
    "preferences": ["any coding preferences or interests mentioned"]
}}

Conversation:
{conversation_text}

Return only the JSON, no other text."""

        try:
            insights_json = chat("You extract developer insights from conversations.", insight_prompt)
            # Parse the JSON response and clean it
            cleaned_json = insights_json.strip()
            # Remove any markdown code blocks if present
            if cleaned_json.startswith('```'):
                cleaned_json = cleaned_json.split('\n', 1)[1]
            if cleaned_json.endswith('```'):
                cleaned_json = cleaned_json.rsplit('\n', 1)[0]
            
            extracted = json.loads(cleaned_json)
            
            # Update insights with LLM-extracted data
            if extracted.get('languages'):
                self.insights['languages'] = extracted['languages']
            if extracted.get('testing_interest'):
                self.insights['testing_interest'] = extracted['testing_interest']
            if extracted.get('learning_focused'):
                self.insights['learning_focused'] = extracted['learning_focused']
            if extracted.get('experience_indicators'):
                self.insights['experience_indicators'] = extracted['experience_indicators']
            if extracted.get('project_focus'):
                self.insights['project_focus'] = extracted['project_focus']
            if extracted.get('preferences'):
                self.insights['preferences'] = extracted['preferences']
                
        except Exception as e:
            # Fallback: don't extract insights if LLM fails
            # The system will work fine without detailed insights
            pass
    
    def _detect_developer_type(self):
        """Detect what type of developer this is based on conversation"""
        # Simplified detection based on project context and conversation
        if self.insights.get('learning_focused'):
            self.developer_type = 'learning_developer'
        elif self.project_context.get('project_type') == 'portfolio':
            self.developer_type = 'portfolio_developer'
        elif self.project_context.get('has_tests') and self.project_context.get('ci_cd'):
            self.developer_type = 'professional_developer'
        else:
            self.developer_type = 'general_developer'
    
    def should_continue(self) -> bool:
        """Decide if we should ask another question using intelligent assessment"""
        # Always continue for at least 2 questions to establish context
        if self.conversation_depth < 2:
            return True
        
        # Hard limit: never go beyond 6 questions to avoid fatigue
        if self.conversation_depth >= 6:
            return False
        
        # Use LLM to assess if we have enough information
        conversation_text = ""
        for exchange in self.exchanges:
            conversation_text += f"Q: {exchange['question']}\nA: {exchange['answer']}\n"
        
        assessment_system_prompt = """You are an expert at determining when you have gathered enough information to create a personalized coding assistant prompt.

Your assessment criteria:
- Do you understand their experience level and background?
- Do you know what technologies/languages they work with?
- Do you understand their current project or work context?
- Have they shared specific challenges, preferences, or workflow details?
- Can you create a useful, personalized coding assistant prompt from this information?

CRITICAL: Be AGGRESSIVE about detecting shallow or evasive responses:
- Generic answers like "legacy codebase is challenging" or "optimization issues" are RED FLAGS
- Vague mentions without specifics (e.g., "technical debt", "performance bottlenecks") are INSUFFICIENT
- If they mention problems but won't give details about team, testing, deployment, documentation - CONTINUE
- If they sound professional but aren't revealing actual pain points or workflow realities - CONTINUE
- Technical jargon without context about real challenges means you need MORE information
- If conversation feels surface-level or like they're being careful/reserved - PUSH DEEPER

BIAS TOWARD CONTINUING: Unless you have rich, specific details about their actual challenges, team situation, workflow problems, or personal context - CONTINUE asking questions. It's better to ask too many than miss critical information.

Your decision-making philosophy:
- CONTINUE if responses feel generic, professional, or evasive
- CONTINUE if you sense they're holding back important context
- CONTINUE if they mention problems but won't elaborate on impact/details
- CONTINUE if their answers could apply to any developer in their situation
- ONLY STOP when you have specific, actionable insights about their unique situation

Respond with ONLY "CONTINUE" or "STOP" followed by a brief reason."""

        assessment_user_prompt = f"""Based on this conversation, do you have enough information to create a high-quality, personalized coding assistant prompt?

Project Context: {self.project_context}
Conversation:
{conversation_text}
Current Insights: {self.insights}

ANALYSIS CHECKLIST:
- Are their responses specific and detailed, or generic and vague?
- Have they shared actual challenges/pain points, or just mentioned surface-level issues?
- Do their answers reveal real workflow details, or seem to avoid discussing problems?
- Is there a sense they're holding back important information about their situation?
- Would one more targeted question likely reveal critical missing context?

Should I CONTINUE asking questions or STOP here? Respond with "CONTINUE" or "STOP" and brief reasoning."""

        try:
            response = chat(assessment_system_prompt, assessment_user_prompt)
            decision = response.strip().upper()
            
            # Parse the decision
            if decision.startswith("STOP"):
                return False
            elif decision.startswith("CONTINUE"):
                return True
            else:
                # Fallback: if unclear response, use conversation depth as backup
                return self.conversation_depth < 4
                
        except Exception:
            # Fallback: use simple rule if LLM fails
            return self.conversation_depth < 4
    
    def finalize_insights(self):
        """Extract final insights from complete conversation"""
        if len(self.exchanges) > 0:
            self._extract_insights_from_full_conversation()
    
    def get_conversation_summary(self) -> str:
        """Get a summary of what we've learned"""
        summary_parts = []
        
        if self.project_context.get('languages'):
            summary_parts.append(f"Working with: {', '.join(self.project_context['languages'])}")
            
        if self.insights.get('languages'):
            summary_parts.append(f"Uses: {', '.join(self.insights['languages'])}")
            
        if self.insights.get('project_focus'):
            summary_parts.append(f"Focus: {self.insights['project_focus']}")
            
        if self.developer_type:
            summary_parts.append(f"Type: {self.developer_type}")
            
        return " | ".join(summary_parts) if summary_parts else "Learning about developer..."

def generate_next_question(conversation: ConversationState) -> str:
    """Generate the next question using intelligent system prompt-driven approach"""
    
    if conversation.conversation_depth == 0:
        # Opening question with project context awareness
        if conversation.project_context.get('languages'):
            langs = ', '.join(conversation.project_context['languages'])
            return f"I see you're working with {langs} - what brings you to use this coding assistant today?"
        else:
            return "What brings you to use this coding assistant today?"
    
    # Use LLM with system prompt to generate contextual questions
    conversation_text = ""
    for exchange in conversation.exchanges:
        conversation_text += f"Q: {exchange['question']}\nA: {exchange['answer']}\n"
    
    interviewer_system_prompt = """You are an expert technical interviewer conducting a brief conversation to understand a developer's needs for creating a personalized coding assistant prompt. 

Your personality and goals:
- You are professional, friendly, and efficient
- You ask focused questions that reveal key information about their workflow, experience, and preferences
- You adapt your questions based on their responses and project context
- You aim to understand their coding practices, challenges, and goals in 3-4 questions total
- You avoid overwhelming them with too many questions
- You're genuinely interested in helping them get the most relevant coding assistance

Your questioning strategy:
- Build on their previous answers
- Focus on actionable insights about their coding workflow
- Ask about specific challenges or preferences they might have
- Tailor questions to their apparent experience level and project type

Generate the next question that would be most valuable for understanding their coding assistant needs."""

    interviewer_user_prompt = f"""Based on this conversation so far, what should be your next question?

Project Context: {conversation.project_context}
Conversation History:
{conversation_text}

Current insights gathered: {conversation.insights}

Generate one focused question that will help understand their coding workflow and preferences. Keep it conversational and natural."""

    try:
        question = chat(interviewer_system_prompt, interviewer_user_prompt)
        return question.strip()
    except Exception:
        # Fallback to simple questions if LLM fails
        fallback_questions = [
            "What programming languages do you work with most often?",
            "How would you describe your experience level with coding?", 
            "What kind of project are you currently working on?",
            "What do you find most challenging about your current development work?",
        ]
        
        if conversation.conversation_depth <= len(fallback_questions):
            return fallback_questions[conversation.conversation_depth - 1]
        else:
            return "What would be most helpful for your coding workflow?"

def conduct_conversation(show_project_context: bool = True) -> ConversationState:
    """Conduct a full conversational interview"""
    
    # Analyze project context
    project_context = analyze_project_context()
    
    if show_project_context and project_context.get('languages'):
        project_summary = get_project_summary(project_context)
        print(f"📁 Project detected: {project_summary}")
        print("💡 I'll tailor questions based on your project setup.\n")
    
    conversation = ConversationState(project_context)
    
    # Generate opening question
    question = generate_next_question(conversation)
    
    while conversation.should_continue():
        try:
            answer = input(f"{question} > ").strip()
            if not answer:
                break
                
            conversation.add_exchange(question, answer)
            
            if conversation.should_continue():
                question = generate_next_question(conversation)
            else:
                break
                
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Thanks for the conversation!")
            break
    
    # Finalize insights from complete conversation
    conversation.finalize_insights()
    
    # Show summary
    if conversation.exchanges:
        print(f"\n🎯 Great! I have a good understanding of your needs.")
        print(f"Summary: {conversation.get_conversation_summary()}")
    
    return conversation

def conversation_to_prompt_context(conversation: ConversationState) -> Dict[str, Any]:
    """Convert conversation to context for prompt generation"""
    
    # Ensure we have final insights
    conversation.finalize_insights()
    
    # Build a rich context from the conversation
    context = {
        "conversation_history": conversation.exchanges,
        "insights": conversation.insights,
        "developer_type": conversation.developer_type,
        "project_context": conversation.project_context,
        "conversation_summary": conversation.get_conversation_summary(),
    }
    
    # Extract key information for prompt generation
    full_conversation = ""
    for exchange in conversation.exchanges:
        full_conversation += f"Q: {exchange['question']}\n"
        full_conversation += f"A: {exchange['answer']}\n"
    
    context["full_conversation_text"] = full_conversation
    
    return context