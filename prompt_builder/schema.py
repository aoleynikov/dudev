from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class ConversationProfile:
    """
    Free-form conversation profile that captures what we learn about a developer
    through natural conversation, without rigid field constraints.
    """
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.insights: Dict[str, Any] = {}
        self.context_detected: Dict[str, Any] = {}
        
    def add_exchange(self, question: str, answer: str, insight_type: str = None):
        """Add a question-answer exchange to the conversation history"""
        exchange = {
            "question": question,
            "answer": answer,
            "insight_type": insight_type
        }
        self.conversation_history.append(exchange)
        
        # Extract and store insights
        if insight_type:
            self.insights[insight_type] = answer
    
    def get_conversation_text(self) -> str:
        """Get the full conversation as a formatted string"""
        conversation = []
        for exchange in self.conversation_history:
            conversation.append(f"Q: {exchange['question']}")
            conversation.append(f"A: {exchange['answer']}")
        return "\n".join(conversation)
    
    def get_insights_summary(self) -> Dict[str, Any]:
        """Get structured summary of what we've learned"""
        return {
            "conversation_length": len(self.conversation_history),
            "insights_gathered": list(self.insights.keys()),
            "context": self.context_detected,
            "raw_insights": self.insights
        }
    
    def has_sufficient_context(self) -> bool:
        """Determine if we have enough context to generate a good prompt"""
        # Must have at least basic understanding
        essential_insights = ["purpose", "languages", "experience_context"]
        has_essentials = all(insight in self.insights for insight in essential_insights)
        
        # Or have had a meaningful conversation (at least 3 exchanges)
        has_conversation = len(self.conversation_history) >= 3
        
        return has_essentials or has_conversation
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for prompt generation"""
        return {
            "conversation_history": self.conversation_history,
            "insights": self.insights,
            "context": self.context_detected,
            "summary": self.get_insights_summary()
        }

# Context detection patterns for different developer types
DEVELOPER_CONTEXTS = {
    "academic": {
        "indicators": ["student", "homework", "assignment", "learning", "class", "university", "school"],
        "focus_areas": ["learning_goals", "assignment_requirements", "academic_workflow"]
    },
    "enterprise_developer": {
        "indicators": ["senior", "lead", "architect", "team", "production", "enterprise", "corporate"],
        "focus_areas": ["team_workflow", "code_standards", "architecture", "scalability", "team_leadership"]
    },
    "indie_developer": {
        "indicators": ["freelance", "consultant", "indie", "solo", "contract", "client"],
        "focus_areas": ["client_communication", "project_efficiency", "deliverable_focus"]
    },
    "hobbyist": {
        "indicators": ["hobby", "personal", "weekend", "spare time", "family", "side project", "fun"],
        "focus_areas": ["time_efficiency", "learning_preferences", "simplicity", "personal_goals"]
    },
    "startup": {
        "indicators": ["startup", "cto", "mvp", "fast", "agile", "growth", "scaling"],
        "focus_areas": ["speed_vs_quality", "technical_debt", "team_scaling", "investor_communication"]
    },
    "infrastructure": {
        "indicators": ["devops", "sre", "infrastructure", "deployment", "kubernetes", "cloud", "automation"],
        "focus_areas": ["automation_practices", "reliability", "monitoring", "deployment_strategy"]
    }
}

def detect_developer_context(conversation_text: str, insights: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze conversation to detect what type of developer this is
    and what they likely care about
    """
    text_lower = conversation_text.lower()
    detected_contexts = []
    
    for context_type, config in DEVELOPER_CONTEXTS.items():
        matches = sum(1 for indicator in config["indicators"] if indicator in text_lower)
        if matches > 0:
            detected_contexts.append({
                "type": context_type,
                "confidence": matches / len(config["indicators"]),
                "focus_areas": config["focus_areas"]
            })
    
    # Sort by confidence
    detected_contexts.sort(key=lambda x: x["confidence"], reverse=True)
    
    return {
        "primary_context": detected_contexts[0] if detected_contexts else None,
        "all_contexts": detected_contexts,
        "is_multi_context": len(detected_contexts) > 1
    }

# Backwards compatibility for existing code
ESSENTIAL_FIELDS = [
    "intended_use",
    "primary_languages", 
    "experience_level"
]

ADVANCED_FIELDS = [
    "coding_style",
    "testing_approach", 
    "tooling_preferences",
    "workflow_process",
    "current_project"
]

MIN_FIELDS = ESSENTIAL_FIELDS + ADVANCED_FIELDS

class Profile(BaseModel):
    """Legacy Profile class for backwards compatibility"""
    intended_use: Optional[str] = None
    primary_languages: Optional[str] = None
    coding_style: Optional[str] = None
    testing_approach: Optional[str] = None
    tooling_preferences: Optional[str] = None
    workflow_process: Optional[str] = None
    current_project: Optional[str] = None
    experience_level: Optional[str] = None
    
    def dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}