"""
Intelligent stopping logic for the interview process
"""
import re
from typing import Dict, List
from .schema import ESSENTIAL_FIELDS, ADVANCED_FIELDS

def should_continue_questioning(profile_dict: Dict, missing_fields: List[str]) -> bool:
    """
    Determine if we should continue asking questions based on user profile
    
    Returns True if we should continue, False if we should stop
    """
    
    # Always need essential fields
    missing_essential = [f for f in ESSENTIAL_FIELDS if f in missing_fields]
    if missing_essential:
        return True
    
    # For advanced fields, consider experience level and responses
    experience_level = profile_dict.get('experience_level', '').lower()
    
    # Extract years of experience if mentioned
    years_match = re.search(r'(\d+)\s*(?:years?|yrs?)', experience_level)
    years_experience = int(years_match.group(1)) if years_match else 0
    
    # Determine experience category
    is_beginner = any(word in experience_level for word in [
        'beginner', 'junior', 'student', 'learning', 'new', 'starter',
        'novice', 'self-taught', 'hobby', 'weekend'
    ]) or years_experience <= 2
    
    is_intermediate = any(word in experience_level for word in [
        'mid', 'intermediate', '3', '4', '5'
    ]) or 3 <= years_experience <= 5
    
    is_advanced = any(word in experience_level for word in [
        'senior', 'expert', 'lead', 'architect', 'cto', '6', '7', '8', '9', '10'
    ]) or years_experience >= 6
    
    # Check if intended_use suggests simple needs
    intended_use = profile_dict.get('intended_use', '').lower()
    simple_use_cases = [
        'homework', 'assignment', 'learning', 'tutorial', 'practice',
        'hobby', 'personal', 'weekend', 'spare time', 'family'
    ]
    is_simple_use = any(word in intended_use for word in simple_use_cases)
    
    # Stopping rules based on experience and context
    missing_advanced = [f for f in ADVANCED_FIELDS if f in missing_fields]
    
    # Stop early for beginners if we have enough context
    if is_beginner and len(missing_advanced) <= 3:
        # If they're a beginner and we have most info, that's probably enough
        if is_simple_use or 'student' in experience_level:
            return False
    
    # Stop early for hobby/weekend developers - be more aggressive  
    if is_simple_use and len(missing_advanced) <= 3:
        return False
        
    # Special case: if they mention "hobby", "weekend", "spare time", "busy schedule"
    busy_indicators = ['hobby', 'weekend', 'spare time', 'busy', 'limited time', 'family']
    if any(word in intended_use.lower() + experience_level.lower() for word in busy_indicators):
        if len(missing_advanced) <= 2:
            return False
    
    # Continue for intermediate/advanced developers (they can handle more questions)
    if is_advanced and missing_advanced:
        return True
        
    # If we have most advanced fields, probably enough
    if len(missing_advanced) <= 1:
        return False
        
    return True

def get_stopping_reason(profile_dict: Dict, missing_fields: List[str]) -> str:
    """Generate a friendly message explaining why we're stopping"""
    
    experience_level = profile_dict.get('experience_level', '').lower()
    intended_use = profile_dict.get('intended_use', '').lower()
    
    is_beginner = any(word in experience_level for word in [
        'beginner', 'junior', 'student', 'learning', 'new'
    ])
    
    is_simple_use = any(word in intended_use for word in [
        'homework', 'assignment', 'learning', 'hobby', 'personal'
    ])
    
    if is_beginner or is_simple_use:
        return "Perfect! I have enough information to create a helpful, focused prompt for your needs. 🎯"
    else:
        return "Great! I have sufficient information to generate your personalized coding assistant prompt. ✨"

def get_question_priority_for_experience(profile_dict: Dict, missing_fields: List[str]) -> List[str]:
    """
    Reorder missing fields based on experience level and context
    Returns fields in priority order
    """
    
    experience_level = profile_dict.get('experience_level', '').lower()
    intended_use = profile_dict.get('intended_use', '').lower()
    
    is_beginner = any(word in experience_level for word in [
        'beginner', 'junior', 'student', 'learning', 'new'
    ])
    
    is_simple_use = any(word in intended_use for word in [
        'homework', 'assignment', 'learning', 'hobby', 'personal'
    ])
    
    # Priority order for beginners/simple use cases
    if is_beginner or is_simple_use:
        beginner_priority = [
            "intended_use",
            "primary_languages", 
            "experience_level",
            "current_project",
            "testing_approach",  # Simplified testing is good to know
            "coding_style",      # But keep it simple
            "tooling_preferences", 
            "workflow_process"   # Least important for beginners
        ]
        return [f for f in beginner_priority if f in missing_fields]
    
    # Standard priority for experienced developers
    standard_priority = [
        "intended_use",
        "primary_languages",
        "experience_level", 
        "current_project",
        "workflow_process",
        "testing_approach",
        "coding_style",
        "tooling_preferences"
    ]
    
    return [f for f in standard_priority if f in missing_fields]