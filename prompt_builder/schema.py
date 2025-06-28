from pydantic import BaseModel
from typing import Optional

MIN_FIELDS = [
    "intended_use",
    "primary_languages",
    "coding_style", 
    "testing_approach",
    "tooling_preferences",
    "workflow_process",
    "current_project",
    "experience_level"
]

class Profile(BaseModel):
    intended_use: Optional[str] = None
    primary_languages: Optional[str] = None
    coding_style: Optional[str] = None
    testing_approach: Optional[str] = None
    tooling_preferences: Optional[str] = None
    workflow_process: Optional[str] = None
    current_project: Optional[str] = None
    experience_level: Optional[str] = None
    
    def dict(self):
        return {
            "intended_use": self.intended_use,
            "primary_languages": self.primary_languages,
            "coding_style": self.coding_style,
            "testing_approach": self.testing_approach,
            "tooling_preferences": self.tooling_preferences,
            "workflow_process": self.workflow_process,
            "current_project": self.current_project,
            "experience_level": self.experience_level
        }