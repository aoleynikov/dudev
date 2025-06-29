# DevPrompt Project Instructions

## Script Execution

### System Analysis
- `analyze_system.py` - **Always use 10-minute timeout** (requires LLM API calls for all test personas)
  ```bash
  # Run all personas (10+ personas, ~7+ minutes)
  python3 analyze_system.py
  
  # Quick test with 3 representative personas (~2 minutes)
  python3 analyze_system.py --quick
  
  # Test specific groups
  python3 analyze_system.py --beginners    # 3 personas
  python3 analyze_system.py --advanced     # 4 personas
  python3 analyze_system.py --technical    # 4 personas
  
  # Test specific personas
  python3 analyze_system.py --personas senior_fullstack,data_scientist
  
  # List all available options
  python3 analyze_system.py --list
  ```

### Testing
- `test_devprompt.py` - Standard testing script for individual personas
- Use `-r` flag for review-only output without running interviews

## Development Notes

- New conversational system in `prompt_builder/conversation.py` eliminates rigid field requirements
- Legacy field-based system preserved in `core.py` as `interactive_interview_legacy()` 
- Main interview function `interactive_interview()` now uses conversational approach
- System supports both old Profile objects and new ConversationState for backwards compatibility