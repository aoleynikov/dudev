#!/usr/bin/env python3
"""
DevPrompt - Adaptive Developer Prompt Generation
Interactive CLI for generating personalized coding assistant prompts
"""
import sys
import argparse
from prompt_builder.core import interactive_interview, generate_prompt
from prompt_builder.vendors import write_vendor_output, get_available_vendors

def print_welcome():
    """Print welcome message"""
    print("🤖 DevPrompt - Adaptive Developer Prompt Generation")
    print("=" * 50)
    print("I'll ask you a few questions to create a personalized coding assistant prompt.")
    print("This should take about 2-3 minutes. Let's get started!")
    print()

def print_completion(vendor_key=None, output_path=None):
    """Print completion message"""
    print()
    print("✅ Interview complete! Your personalized prompt has been generated.")
    
    if vendor_key and output_path:
        vendor_name = get_available_vendors()[vendor_key]
        print(f"📁 {vendor_name} rules saved to: {output_path}")
        print(f"Your coding assistant is now configured with your preferences!")
    else:
        print("Use -o flag to save to your preferred coding assistant format.")
    
    print()
    print("Thanks for using DevPrompt! 🚀")

def main():
    parser = argparse.ArgumentParser(
        description="Generate personalized coding assistant prompts through interactive interview",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available output formats:
{chr(10).join(f"  {key:<10} {name}" for key, name in get_available_vendors().items())}

Example usage:
  python3 devprompt.py                    # Interactive mode, display prompt
  python3 devprompt.py -o cursor          # Save to .cursorrules for Cursor AI
  python3 devprompt.py -o continue        # Save to .continuerules for Continue
  python3 devprompt.py -o aider           # Save to .aider.conf.yml for Aider
        """
    )
    
    parser.add_argument(
        "-o", "--output-format",
        choices=list(get_available_vendors().keys()),
        help="Output format for specific coding assistant"
    )
    
    parser.add_argument(
        "--no-welcome",
        action="store_true",
        help="Skip welcome message (useful for scripting)"
    )
    
    args = parser.parse_args()
    
    try:
        # Show welcome message
        if not args.no_welcome:
            print_welcome()
        
        # Run interactive interview
        print("Starting interview...")
        print("-" * 30)
        profile = interactive_interview()
        
        print("-" * 30)
        print("🔄 Generating your personalized prompt...")
        
        # Generate the prompt
        generated_prompt = generate_prompt(profile)
        
        # Handle output
        if args.output_format:
            # Write to vendor-specific file
            profile_dict = profile.dict()
            output_path = write_vendor_output(args.output_format, generated_prompt, profile_dict)
            print_completion(args.output_format, output_path)
        else:
            # Display the prompt
            print()
            print("=" * 80)
            print("📝 YOUR PERSONALIZED CODING ASSISTANT PROMPT")
            print("=" * 80)
            print(generated_prompt)
            print("=" * 80)
            print_completion()
            
    except KeyboardInterrupt:
        print("\n\n👋 Interview cancelled. No files were created.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please try again or report this issue.")
        sys.exit(1)

if __name__ == "__main__":
    main()