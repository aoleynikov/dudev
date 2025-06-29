"""
Project context detection - analyze current directory for tech stack and setup
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Set, Any, Optional

def analyze_project_context() -> Dict[str, Any]:
    """Analyze current directory for comprehensive project context"""
    
    context = {
        "languages": set(),
        "frameworks": set(),
        "tools": set(),
        "project_type": None,
        "package_managers": set(),
        "has_tests": False,
        "has_docker": False,
        "has_git": False,
        "ide_config": set(),
        "linting_tools": set(),
        "ci_cd": set(),
        "dependencies": {},
        "scripts": {},
        "directory_structure": []
    }
    
    # Detect languages and frameworks from key files
    _detect_languages_and_frameworks(context)
    
    # Detect tooling and configuration
    _detect_tooling(context)
    
    # Analyze directory structure
    _analyze_directory_structure(context)
    
    # Parse key configuration files
    _parse_config_files(context)
    
    # Convert sets to lists for JSON serialization
    for key in ["languages", "frameworks", "tools", "package_managers", "ide_config", "linting_tools", "ci_cd"]:
        if isinstance(context[key], set):
            context[key] = sorted(list(context[key]))
    
    return context

def _detect_languages_and_frameworks(context: Dict[str, Any]) -> None:
    """Detect programming languages and frameworks from indicator files"""
    
    indicators = {
        # JavaScript/TypeScript ecosystem
        "package.json": {
            "languages": ["JavaScript"],
            "package_manager": "npm",
            "parse_for_frameworks": True
        },
        "yarn.lock": {
            "package_manager": "yarn"
        },
        "tsconfig.json": {
            "languages": ["TypeScript"]
        },
        
        # Python ecosystem
        "requirements.txt": {
            "languages": ["Python"],
            "package_manager": "pip"
        },
        "pyproject.toml": {
            "languages": ["Python"],
            "package_manager": "pip/poetry"
        },
        "Pipfile": {
            "languages": ["Python"],
            "package_manager": "pipenv"
        },
        "setup.py": {
            "languages": ["Python"]
        },
        "poetry.lock": {
            "package_manager": "poetry"
        },
        
        # Other languages
        "Cargo.toml": {
            "languages": ["Rust"],
            "package_manager": "cargo"
        },
        "go.mod": {
            "languages": ["Go"],
            "package_manager": "go modules"
        },
        "pom.xml": {
            "languages": ["Java"],
            "package_manager": "maven",
            "frameworks": ["Spring"]
        },
        "build.gradle": {
            "languages": ["Java", "Kotlin"],
            "package_manager": "gradle"
        },
        "composer.json": {
            "languages": ["PHP"],
            "package_manager": "composer"
        },
        "Gemfile": {
            "languages": ["Ruby"],
            "package_manager": "bundler"
        }
    }
    
    for file_name, info in indicators.items():
        if Path(file_name).exists():
            if "languages" in info:
                context["languages"].update(info["languages"])
            if "package_manager" in info:
                context["package_managers"].add(info["package_manager"])
            if "frameworks" in info:
                context["frameworks"].update(info["frameworks"])

def _detect_tooling(context: Dict[str, Any]) -> None:
    """Detect development tools and configurations"""
    
    # Development environment
    context["has_git"] = Path(".git").exists()
    context["has_docker"] = any(Path(f).exists() for f in ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"])
    
    # IDE configurations
    ide_configs = {
        ".vscode/": "VS Code",
        ".idea/": "IntelliJ/PyCharm",
        ".eclipse/": "Eclipse",
        ".sublime-project": "Sublime Text"
    }
    
    for path, ide in ide_configs.items():
        if Path(path).exists():
            context["ide_config"].add(ide)
    
    # Linting and formatting tools
    linting_files = {
        ".eslintrc": "ESLint",
        ".eslintrc.js": "ESLint", 
        ".eslintrc.json": "ESLint",
        ".prettierrc": "Prettier",
        ".prettierrc.js": "Prettier",
        ".prettierrc.json": "Prettier",
        ".flake8": "flake8",
        "pyproject.toml": "Black/isort",
        ".pylintrc": "pylint",
        ".golangci.yml": "golangci-lint",
        ".rubocop.yml": "RuboCop"
    }
    
    for file_name, tool in linting_files.items():
        if Path(file_name).exists():
            context["linting_tools"].add(tool)
    
    # CI/CD configurations
    ci_configs = {
        ".github/workflows/": "GitHub Actions",
        ".gitlab-ci.yml": "GitLab CI",
        ".travis.yml": "Travis CI",
        "Jenkinsfile": "Jenkins",
        ".circleci/": "CircleCI"
    }
    
    for path, ci in ci_configs.items():
        if Path(path).exists():
            context["ci_cd"].add(ci)

def _analyze_directory_structure(context: Dict[str, Any]) -> None:
    """Analyze directory structure for project organization patterns"""
    
    # Test directories
    test_dirs = ["test/", "tests/", "__tests__/", "spec/"]
    context["has_tests"] = any(Path(d).exists() for d in test_dirs)
    
    # Common directory patterns
    common_dirs = [
        "src/", "lib/", "app/", "components/", "pages/", "api/",
        "public/", "static/", "assets/", "docs/", "scripts/",
        "config/", "utils/", "helpers/", "models/", "views/",
        "controllers/", "services/", "middleware/"
    ]
    
    existing_dirs = []
    for dir_name in common_dirs:
        if Path(dir_name).exists() and Path(dir_name).is_dir():
            existing_dirs.append(dir_name.rstrip('/'))
    
    context["directory_structure"] = existing_dirs

def _parse_config_files(context: Dict[str, Any]) -> None:
    """Parse key configuration files for additional context"""
    
    # Parse package.json for JavaScript/Node.js projects
    if Path("package.json").exists():
        try:
            with open("package.json", 'r') as f:
                package_data = json.load(f)
                
            # Detect frameworks from dependencies
            all_deps = {}
            all_deps.update(package_data.get("dependencies", {}))
            all_deps.update(package_data.get("devDependencies", {}))
            
            framework_indicators = {
                "react": "React",
                "vue": "Vue.js", 
                "@vue/core": "Vue.js",
                "angular": "Angular",
                "@angular/core": "Angular",
                "next": "Next.js",
                "nuxt": "Nuxt.js",
                "express": "Express.js",
                "fastify": "Fastify",
                "nest": "NestJS",
                "@nestjs/core": "NestJS",
                "svelte": "Svelte",
                "gatsby": "Gatsby",
                "remix": "Remix"
            }
            
            for dep, framework in framework_indicators.items():
                if dep in all_deps:
                    context["frameworks"].add(framework)
            
            # Store scripts
            context["scripts"] = package_data.get("scripts", {})
            
            # Store main dependencies
            context["dependencies"]["npm"] = list(all_deps.keys())[:10]  # Limit to first 10
            
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Parse requirements.txt for Python projects
    if Path("requirements.txt").exists():
        try:
            with open("requirements.txt", 'r') as f:
                requirements = [line.strip().split('==')[0].split('>=')[0].split('~=')[0] 
                             for line in f if line.strip() and not line.startswith('#')]
            
            # Detect Python frameworks
            framework_indicators = {
                "django": "Django",
                "flask": "Flask",
                "fastapi": "FastAPI",
                "tornado": "Tornado",
                "pyramid": "Pyramid",
                "bottle": "Bottle",
                "cherrypy": "CherryPy",
                "sanic": "Sanic"
            }
            
            for req in requirements:
                if req.lower() in framework_indicators:
                    context["frameworks"].add(framework_indicators[req.lower()])
            
            context["dependencies"]["python"] = requirements[:10]  # Limit to first 10
            
        except FileNotFoundError:
            pass

def get_project_summary(context: Dict[str, Any]) -> str:
    """Generate a human-readable summary of the project context"""
    
    summary_parts = []
    
    if context["languages"]:
        summary_parts.append(f"Languages: {', '.join(context['languages'])}")
    
    if context["frameworks"]:
        summary_parts.append(f"Frameworks: {', '.join(context['frameworks'])}")
    
    if context["package_managers"]:
        summary_parts.append(f"Package managers: {', '.join(context['package_managers'])}")
    
    features = []
    if context["has_git"]:
        features.append("Git")
    if context["has_docker"]:
        features.append("Docker")
    if context["has_tests"]:
        features.append("Tests")
    if context["ide_config"]:
        features.append(f"IDE: {', '.join(context['ide_config'])}")
    if context["linting_tools"]:
        features.append(f"Linting: {', '.join(context['linting_tools'])}")
    
    if features:
        summary_parts.append(f"Tools: {', '.join(features)}")
    
    return "; ".join(summary_parts) if summary_parts else "No specific project structure detected"

def should_enhance_questions(context: Dict[str, Any]) -> bool:
    """Determine if we have enough context to enhance questioning"""
    return bool(
        context["languages"] or 
        context["frameworks"] or 
        context["has_git"] or 
        context["has_docker"] or 
        context["has_tests"]
    )