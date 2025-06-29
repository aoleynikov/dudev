"""
Mock project environments for testing personas
Each persona gets a realistic project context
"""

def get_mock_project_context(persona_name: str):
    """Return mock project context for different personas"""
    
    environments = {
        "curious_beginner": {
            # Personal blog platform - simple Node.js project
            "languages": ["JavaScript", "HTML", "CSS"],
            "frameworks": ["Express.js"],
            "tools": ["npm"],
            "project_type": "web_application",
            "package_managers": ["npm"],
            "has_tests": False,
            "has_docker": False,
            "has_git": True,
            "ide_config": [".vscode"],
            "linting_tools": [],
            "ci_cd": [],
            "dependencies": {
                "express": "^4.18.0",
                "ejs": "^3.1.8",
                "nodemon": "^2.0.20"
            },
            "scripts": {
                "start": "node app.js",
                "dev": "nodemon app.js"
            },
            "directory_structure": [
                "app.js",
                "package.json",
                "views/",
                "public/css/",
                "public/js/",
                "routes/"
            ]
        },
        
        "emergency_manager": {
            # Broken customer portal - existing production system
            "languages": ["PHP", "JavaScript", "SQL"],
            "frameworks": ["WordPress", "jQuery"],
            "tools": ["MySQL", "Apache"],
            "project_type": "cms_application",
            "package_managers": ["composer"],
            "has_tests": False,
            "has_docker": False,
            "has_git": True,
            "ide_config": [],
            "linting_tools": [],
            "ci_cd": [],
            "dependencies": {
                "wordpress": "6.2",
                "woocommerce": "7.8.0",
                "custom-theme": "1.0.0"
            },
            "scripts": {},
            "directory_structure": [
                "wp-config.php",
                "wp-content/themes/custom-theme/",
                "wp-content/plugins/",
                "wp-admin/",
                "wp-includes/",
                ".htaccess"
            ]
        },
        
        "senior_fullstack": {
            # Microservices e-commerce platform
            "languages": ["TypeScript", "Python", "Go"],
            "frameworks": ["React", "Next.js", "FastAPI", "Gin"],
            "tools": ["Docker", "Kubernetes", "Redis", "PostgreSQL"],
            "project_type": "microservices",
            "package_managers": ["npm", "pip", "go mod"],
            "has_tests": True,
            "has_docker": True,
            "has_git": True,
            "ide_config": [".vscode", ".editorconfig"],
            "linting_tools": ["ESLint", "Prettier", "Black", "golangci-lint"],
            "ci_cd": [".github/workflows", "Dockerfile"],
            "dependencies": {
                "react": "^18.2.0",
                "next": "^13.4.0",
                "fastapi": "^0.100.0",
                "gin-gonic/gin": "v1.9.1"
            },
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "test": "jest",
                "lint": "eslint . && black . && golangci-lint run"
            },
            "directory_structure": [
                "frontend/",
                "api-gateway/",
                "user-service/",
                "product-service/",
                "docker-compose.yml",
                "k8s/",
                "tests/"
            ]
        },
        
        "computer_science_student": {
            # Student management system capstone
            "languages": ["Java", "Python", "SQL"],
            "frameworks": ["Spring Boot", "React"],
            "tools": ["Maven", "H2", "npm"],
            "project_type": "web_application",
            "package_managers": ["maven", "npm"],
            "has_tests": True,
            "has_docker": False,
            "has_git": True,
            "ide_config": [".idea", ".vscode"],
            "linting_tools": ["Checkstyle"],
            "ci_cd": [],
            "dependencies": {
                "spring-boot-starter-web": "2.7.0",
                "spring-boot-starter-data-jpa": "2.7.0",
                "react": "^18.0.0",
                "junit-jupiter": "5.8.2"
            },
            "scripts": {
                "start": "mvn spring-boot:run",
                "test": "mvn test",
                "frontend": "cd frontend && npm start"
            },
            "directory_structure": [
                "src/main/java/",
                "src/test/java/",
                "frontend/src/",
                "pom.xml",
                "README.md",
                "docs/"
            ]
        },
        
        "junior_frontend": {
            # Portfolio website
            "languages": ["JavaScript", "HTML", "CSS"],
            "frameworks": ["React", "Tailwind CSS"],
            "tools": ["Vite", "npm"],
            "project_type": "portfolio",
            "package_managers": ["npm"],
            "has_tests": False,
            "has_docker": False,
            "has_git": True,
            "ide_config": [".vscode"],
            "linting_tools": ["ESLint"],
            "ci_cd": [],
            "dependencies": {
                "react": "^18.2.0",
                "vite": "^4.3.0",
                "tailwindcss": "^3.3.0",
                "eslint": "^8.42.0"
            },
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "directory_structure": [
                "src/components/",
                "src/pages/",
                "src/assets/",
                "public/",
                "package.json",
                "tailwind.config.js"
            ]
        }
    }
    
    # Return mock context or empty context if persona not found
    return environments.get(persona_name, {})

def get_project_summary_for_persona(persona_name: str) -> str:
    """Get a human-readable project summary for the persona"""
    
    summaries = {
        "curious_beginner": "Node.js/Express personal blog platform",
        "emergency_manager": "WordPress/WooCommerce customer portal (BROKEN)",
        "senior_fullstack": "TypeScript/Python/Go microservices e-commerce platform", 
        "computer_science_student": "Java Spring Boot + React student management system",
        "junior_frontend": "React + Tailwind CSS portfolio website"
    }
    
    return summaries.get(persona_name, "Unknown project")