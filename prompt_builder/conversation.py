"""
Conversational interview system - no rigid fields, just natural dialogue
Uses simple questioning approach without strategy pattern complexity
"""
from typing import Dict, Any, List, Optional
from .llm import chat, ensure_json
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
        
        # Update insights after each exchange
        self._extract_insights(answer)
        self._detect_developer_type()
    
    def _extract_insights(self, answer: str):
        """Extract basic insights from the latest answer"""
        answer_lower = answer.lower()
        
        # Extract languages mentioned
        languages = []
        for lang in ['python', 'javascript', 'typescript', 'java', 'go', 'rust', 'c++', 'swift', 'kotlin', 'php', 'html', 'css']:
            if lang in answer_lower:
                languages.append(lang.title())
        if languages:
            self.insights['languages'] = languages
            
        # Extract basic preferences mentioned  
        if any(word in answer_lower for word in ['testing', 'tests', 'tdd', 'unit test']):
            self.insights['testing_interest'] = True
            
        if any(word in answer_lower for word in ['learning', 'understand', 'best practices', 'why']):
            self.insights['learning_focused'] = True
    
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
        """Decide if we should ask another question"""
        # Simple rule: continue for 2-3 questions to gather context
        return self.conversation_depth < 4
    
    def get_conversation_summary(self) -> str:
        """Get a summary of what we've learned"""
        summary_parts = []
        
        if self.project_context.get('languages'):
            summary_parts.append(f"Working with: {', '.join(self.project_context['languages'])}")
            
        if self.insights.get('languages'):
            summary_parts.append(f"Uses: {', '.join(self.insights['languages'])}")
            
        if self.developer_type:
            summary_parts.append(f"Type: {self.developer_type}")
            
        return " | ".join(summary_parts) if summary_parts else "Learning about developer..."

def generate_next_question(conversation: ConversationState) -> str:
    """Generate the next question based on conversation depth"""
    
    if conversation.conversation_depth == 0:
        # Opening question
        if conversation.project_context.get('languages'):
            langs = ', '.join(conversation.project_context['languages'])
            return f"I see you're working with {langs} - what brings you to use this coding assistant today?"
        else:
            return "What brings you to use this coding assistant today?"
    
    # Use simple fallback questions
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
    
    # Show summary
    if conversation.exchanges:
        print(f"\n🎯 Great! I have a good understanding of your needs.")
        print(f"Summary: {conversation.get_conversation_summary()}")
    
    return conversation

def conversation_to_prompt_context(conversation: ConversationState) -> Dict[str, Any]:
    """Convert conversation to context for prompt generation"""
    
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