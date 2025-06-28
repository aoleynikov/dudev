"""
OCP-compliant vendor output system for different coding assistant tools
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import os
from pathlib import Path

class VendorOutputHandler(ABC):
    """Abstract base class for vendor-specific output handlers"""
    
    @abstractmethod
    def get_output_filename(self) -> str:
        """Return the filename where this vendor expects rules"""
        pass
    
    @abstractmethod
    def format_prompt(self, prompt: str, profile_data: Dict[str, Any]) -> str:
        """Format the prompt for this vendor's expected format"""
        pass
    
    @abstractmethod
    def get_vendor_name(self) -> str:
        """Return human-readable vendor name"""
        pass

class CursorVendorHandler(VendorOutputHandler):
    """Handler for Cursor AI IDE"""
    
    def get_output_filename(self) -> str:
        return ".cursorrules"
    
    def format_prompt(self, prompt: str, profile_data: Dict[str, Any]) -> str:
        header = f"""# Generated with DevPrompt - Adaptive Developer Prompt Generation
# Profile: {profile_data.get('experience_level', 'Developer')} {profile_data.get('primary_languages', '')}
# Generated on: {os.popen('date +"%Y-%m-%d"').read().strip()}
# Intended use: {profile_data.get('intended_use', 'Coding assistance')}

"""
        return header + prompt
    
    def get_vendor_name(self) -> str:
        return "Cursor AI"

class ContinueVendorHandler(VendorOutputHandler):
    """Handler for Continue VS Code extension"""
    
    def get_output_filename(self) -> str:
        return ".continuerules"
    
    def format_prompt(self, prompt: str, profile_data: Dict[str, Any]) -> str:
        # Continue might use JSON format
        escaped_prompt = prompt.replace('"', '\\"').replace('\n', '\\n')
        header = f"""{{
  "systemMessage": "{escaped_prompt}",
  "generatedBy": "DevPrompt",
  "profile": {{
    "languages": "{profile_data.get('primary_languages', '')}",
    "experience": "{profile_data.get('experience_level', '')}",
    "project": "{profile_data.get('current_project', '')}"
  }}
}}"""
        return header
    
    def get_vendor_name(self) -> str:
        return "Continue"

class AiderVendorHandler(VendorOutputHandler):
    """Handler for Aider AI coding assistant"""
    
    def get_output_filename(self) -> str:
        return ".aider.conf.yml"
    
    def format_prompt(self, prompt: str, profile_data: Dict[str, Any]) -> str:
        # Aider uses YAML configuration
        yaml_content = f"""# Generated with DevPrompt
# Profile: {profile_data.get('experience_level', 'Developer')}
# Languages: {profile_data.get('primary_languages', '')}

system-message: |
{self._indent_text(prompt, 2)}

auto-commits: false
dirty-commits: true
"""
        return yaml_content
    
    def _indent_text(self, text: str, spaces: int) -> str:
        """Indent each line of text by specified number of spaces"""
        indent = " " * spaces
        return "\n".join(f"{indent}{line}" for line in text.split("\n"))
    
    def get_vendor_name(self) -> str:
        return "Aider"

# Registry of available vendors
VENDOR_HANDLERS: Dict[str, VendorOutputHandler] = {
    "cursor": CursorVendorHandler(),
    "continue": ContinueVendorHandler(), 
    "aider": AiderVendorHandler(),
}

def get_available_vendors() -> Dict[str, str]:
    """Return mapping of vendor keys to human-readable names"""
    return {key: handler.get_vendor_name() for key, handler in VENDOR_HANDLERS.items()}

def write_vendor_output(vendor_key: str, prompt: str, profile_data: Dict[str, Any], output_dir: str = ".") -> str:
    """Write prompt to vendor-specific file format"""
    if vendor_key not in VENDOR_HANDLERS:
        raise ValueError(f"Unknown vendor: {vendor_key}. Available: {list(VENDOR_HANDLERS.keys())}")
    
    handler = VENDOR_HANDLERS[vendor_key]
    filename = handler.get_output_filename()
    formatted_content = handler.format_prompt(prompt, profile_data)
    
    output_path = Path(output_dir) / filename
    
    with open(output_path, 'w') as f:
        f.write(formatted_content)
    
    return str(output_path)