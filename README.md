# DevPrompt - Adaptive Developer Prompt Generation

🤖 **DevPrompt** is an intelligent CLI tool that conducts personalized interviews with developers to generate tailored coding assistant prompts. It uses adaptive LLM-powered questioning to understand your preferences and creates concrete "house rules" for your preferred coding assistant.

## ✨ Features

- **🧠 Adaptive Interviewing**: LLM intelligently chooses the next question based on your previous answers
- **📏 Industry Standards Focus**: Assumes you follow standard conventions, only asks about deviations
- **🎯 Concrete Rules**: Generates actionable "house rules" instead of generic advice
- **🔧 Multi-Vendor Support**: Works with Cursor AI, Continue, Aider, and more
- **💬 Chat-like Interface**: Friendly, conversational CLI experience
- **⚡ Fast**: 2-3 minute interview generates personalized prompts

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd dudev
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   ```bash
   # Option 1: Create key.txt file
   echo "your-openai-api-key-here" > key.txt
   
   # Option 2: Set environment variable
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

### Basic Usage

**Generate prompt for Cursor AI:**
```bash
python3 devprompt.py -o cursor
```

**Generate prompt for Continue VS Code extension:**
```bash
python3 devprompt.py -o continue
```

**Generate prompt for Aider:**
```bash
python3 devprompt.py -o aider
```

**Interactive mode (display prompt only):**
```bash
python3 devprompt.py
```

## 📖 How It Works

### 1. Intelligent Interview Process

DevPrompt asks you focused questions about:

- **Intended Use**: What you'll use the coding assistant for
- **Primary Languages**: Your main programming languages
- **Coding Style**: Formatting preferences, patterns you follow
- **Testing Approach**: Testing frameworks, coverage requirements, TDD/TLD preferences
- **Tooling Preferences**: IDEs, linters, CI/CD tools
- **Workflow Process**: Git workflow, PR process, team conventions
- **Current Project**: Context about what you're building
- **Experience Level**: Junior, mid-level, senior, expert

### 2. Adaptive Question Ordering

The LLM analyzes your previous answers and intelligently chooses the next question that will provide the highest information gain for creating your personalized prompt.

### 3. Industry Standards Assumptions

DevPrompt assumes you follow industry standards by default:
- **JavaScript/TypeScript**: Prettier, ESLint, Jest
- **Python**: Black, flake8, pytest
- **Go**: gofmt, golangci-lint
- **And more...**

It only asks about deviations from these standards, making the interview faster and more focused.

### 4. Concrete Output Generation

Instead of generic advice, DevPrompt generates specific, actionable rules:

❌ **Generic**: "Use consistent code formatting"  
✅ **Concrete**: "Use Black for Python formatting with line length 88"

❌ **Generic**: "Write tests for your code"  
✅ **Concrete**: "Use pytest with 90% coverage minimum, TDD for new features"

## 🎛️ Command Line Options

```bash
python3 devprompt.py [OPTIONS]

Options:
  -o, --output-format FORMAT   Output format for specific coding assistant
                              (cursor, continue, aider)
  --no-welcome                Skip welcome message (useful for scripting)
  -h, --help                  Show help message

Examples:
  python3 devprompt.py                    # Interactive mode, display prompt
  python3 devprompt.py -o cursor          # Save to .cursorrules for Cursor AI
  python3 devprompt.py -o continue        # Save to .continuerules for Continue
  python3 devprompt.py -o aider           # Save to .aider.conf.yml for Aider
```

## 📁 Output Formats

### Cursor AI (`.cursorrules`)
```bash
python3 devprompt.py -o cursor
```
Creates a `.cursorrules` file with formatted header and your personalized rules.

### Continue (`.continuerules`)
```bash
python3 devprompt.py -o continue
```
Creates a `.continuerules` JSON file for the Continue VS Code extension.

### Aider (`.aider.conf.yml`)
```bash
python3 devprompt.py -o aider
```
Creates a `.aider.conf.yml` YAML configuration for Aider AI coding assistant.

## 🧪 Testing & Development

### Run Test Scenarios

The project includes comprehensive test scenarios with 10 different developer profiles:

```bash
# Test specific developer profile
python test_devprompt.py senior_fullstack

# Show dialog + prompt + evaluation
python test_devprompt.py -v junior_frontend

# Show just the dialog
python test_devprompt.py -d data_scientist

# Show just the generated prompt
python test_devprompt.py -p devops_engineer

# Generate vendor output
python test_devprompt.py -o cursor security_engineer
```

### Available Test Profiles

- `senior_fullstack` - TypeScript/Python/Go expert, microservices
- `junior_frontend` - Learning React, building portfolio
- `data_scientist` - Python/R/SQL, ML model development
- `computer_science_student` - Java/Python/C++, academic projects
- `hobbyist_parent` - Weekend coding, family projects
- `devops_engineer` - Infrastructure automation, Kubernetes
- `mobile_developer` - Swift/Kotlin/Flutter, app development
- `freelance_consultant` - Multi-language client projects
- `security_engineer` - Security analysis, penetration testing
- `startup_cto` - Technical leadership, team scaling

## 🏗️ Architecture

### Project Structure

```
dudev/
├── devprompt.py              # Main CLI entry point
├── prompt_builder/           # Core package
│   ├── __init__.py
│   ├── core.py              # Interview and generation logic
│   ├── llm.py               # OpenAI integration
│   ├── planner.py           # LLM-powered question ordering
│   ├── prompts.py           # Jinja2 templates
│   ├── schema.py            # Data models and field priorities
│   └── vendors.py           # Multi-vendor output system
├── test_devprompt.py        # Test harness with developer profiles
├── requirements.txt         # Dependencies
└── README.md               # This file
```

### Key Design Principles

1. **Open-Closed Principle**: Easy to add new vendor outputs without modifying existing code
2. **Adaptive Intelligence**: LLM-powered question ordering for personalized interviews
3. **Industry Standards**: Assumes best practices, focuses on deviations
4. **Concrete Output**: Generates actionable rules, not generic advice

## 🔧 Configuration

### API Key Setup

DevPrompt looks for your OpenAI API key in this order:

1. `key.txt` file in the project directory
2. `OPENAI_API_KEY` environment variable

### Customizing Templates

The interview questions and prompt generation use Jinja2 templates in `prompt_builder/prompts.py`. You can modify these to customize:

- Question phrasing and tone
- Generated prompt structure
- Industry standard assumptions

## 🤝 Contributing

### Adding New Vendor Support

To add support for a new coding assistant:

1. Create a new handler class in `prompt_builder/vendors.py`:
   ```python
   class NewVendorHandler(VendorOutputHandler):
       def get_output_filename(self) -> str:
           return ".newvendor.conf"
       
       def format_prompt(self, prompt: str, profile_data: Dict[str, Any]) -> str:
           # Format prompt for new vendor
           return formatted_content
       
       def get_vendor_name(self) -> str:
           return "New Vendor"
   ```

2. Register it in the `VENDOR_HANDLERS` dictionary:
   ```python
   VENDOR_HANDLERS = {
       # ... existing vendors
       "newvendor": NewVendorHandler(),
   }
   ```

3. Test with: `python3 devprompt.py -o newvendor`

### Modifying Question Logic

The adaptive questioning logic is in `prompt_builder/planner.py`. You can customize:

- Question selection criteria
- Fallback behavior when LLM fails
- Information gain calculations

## 📊 Examples

### Example Interview Flow

```
🤖 DevPrompt - Adaptive Developer Prompt Generation
==================================================
I'll ask you a few questions to create a personalized coding assistant prompt.
This should take about 2-3 minutes. Let's get started!

Starting interview...
------------------------------

🤖 What will you primarily use this coding assistant for?
👨‍💻 Daily coding workflow, code reviews, and architectural decisions

🤖 What are your primary programming languages?
👨‍💻 TypeScript, Python, Go

🤖 Any specific coding style preferences or deviations from standard conventions?
👨‍💻 Prefer functional patterns, strict TypeScript config

🤖 What's your approach to testing?
👨‍💻 Jest for TS, pytest for Python, 90% coverage minimum, TDD preferred

[... continued interview ...]

✅ Interview complete! Your personalized prompt has been generated.
📁 Cursor AI rules saved to: .cursorrules
Your coding assistant is now configured with your preferences!

Thanks for using DevPrompt! 🚀
```

### Example Generated Output

```markdown
# Generated with DevPrompt - Adaptive Developer Prompt Generation
# Profile: Senior (8+ years) TypeScript, Python, Go
# Generated on: 2025-06-28
# Intended use: Daily coding workflow, code reviews, and architectural decisions

### Coding Rules for E-commerce Microservices Project

#### Tooling Preferences
- **TypeScript**: Use **Jest** for testing over other frameworks
- **Python**: Use **pytest** exclusively for testing
- **Go**: Use **gofmt** and **golangci-lint** for formatting and linting

#### Project-Specific Requirements
- **Directory Structure**: Follow standard structure with `docs/` for architecture
- **Testing Coverage**: Minimum 90% coverage across all services
- **Strict TypeScript**: Enable strict mode, no `any` types

#### Team Workflow Preferences
- **Branch Naming**: `feature/<JIRA-ID>-description` format
- **Testing First**: Follow TDD principles for new functionality
- **Pull Request Process**: Minimum two reviewers, all tests pass

[... detailed concrete rules ...]
```

## 🐛 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Ensure `key.txt` exists with your API key, or set `OPENAI_API_KEY` environment variable

**"Unknown vendor: xyz"**
- Check available vendors with: `python3 devprompt.py --help`
- Supported vendors: cursor, continue, aider

**"Interview fails with JSON error"**
- This is rare; the system automatically falls back to predefined questions
- Check your internet connection and API key validity

**"Generated file is empty"**
- Ensure you complete the full interview (answer all questions)
- Check file permissions in the current directory

### Getting Help

1. **Check the help**: `python3 devprompt.py --help`
2. **Run test scenarios**: `python test_devprompt.py -v senior_fullstack`
3. **Check API key**: Verify your OpenAI API key is valid and has credits

## 📝 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with OpenAI's GPT models for adaptive questioning
- Inspired by industry best practices and developer workflow research
- Template system powered by Jinja2

---

**Happy coding!** 🚀 Generate your personalized coding assistant prompt in under 3 minutes.