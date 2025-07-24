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
        },
        
        "data_scientist": {
            # ML project analyzing customer behavior
            "languages": ["Python", "R", "SQL"],
            "frameworks": ["pandas", "scikit-learn", "TensorFlow", "Plotly"],
            "tools": ["Jupyter", "Anaconda", "Docker"],
            "project_type": "data_analysis",
            "package_managers": ["conda", "pip"],
            "has_tests": True,
            "has_docker": True,
            "has_git": True,
            "ide_config": [".vscode", "jupyter_config.py"],
            "linting_tools": ["flake8", "black"],
            "ci_cd": [".github/workflows"],
            "dependencies": {
                "pandas": "^2.0.0",
                "numpy": "^1.24.0",
                "scikit-learn": "^1.3.0",
                "tensorflow": "^2.13.0",
                "plotly": "^5.15.0",
                "jupyter": "^1.0.0",
                "pytest": "^7.4.0"
            },
            "scripts": {
                "train": "python src/train_model.py",
                "evaluate": "python src/evaluate.py",
                "notebook": "jupyter lab",
                "test": "pytest tests/",
                "lint": "flake8 src/ && black src/"
            },
            "directory_structure": [
                "notebooks/",
                "src/models/",
                "src/data/",
                "src/features/",
                "data/raw/",
                "data/processed/",
                "models/",
                "requirements.txt",
                "environment.yml",
                "tests/"
            ]
        },
        
        "devops_engineer": {
            # Kubernetes migration project with GitOps
            "languages": ["Python", "Bash", "YAML", "Go"],
            "frameworks": ["Kubernetes", "Terraform", "Ansible"],
            "tools": ["Docker", "Helm", "ArgoCD", "Prometheus", "Grafana"],
            "project_type": "infrastructure",
            "package_managers": ["pip", "go mod"],
            "has_tests": True,
            "has_docker": True,
            "has_git": True,
            "ide_config": [".vscode", ".editorconfig"],
            "linting_tools": ["yamllint", "shellcheck", "golangci-lint"],
            "ci_cd": [".github/workflows", ".gitlab-ci.yml"],
            "dependencies": {
                "kubernetes": "v1.27.0",
                "terraform": "^1.5.0",
                "ansible": "^8.0.0",
                "prometheus": "^2.45.0",
                "grafana": "^10.0.0"
            },
            "scripts": {
                "deploy": "terraform apply && kubectl apply -f k8s/",
                "test": "pytest tests/ && bats tests/",
                "lint": "yamllint . && shellcheck scripts/*.sh",
                "monitoring": "kubectl port-forward svc/grafana 3000:3000"
            },
            "directory_structure": [
                "terraform/",
                "k8s/manifests/",
                "helm/charts/",
                "ansible/playbooks/",
                "scripts/",
                "monitoring/",
                "tests/",
                "docker/",
                "Dockerfile",
                "docker-compose.yml"
            ]
        },
        
        "reserved_developer": {
            # High-frequency trading system with serious technical debt
            "languages": ["C++", "Python", "Rust"],
            "frameworks": ["boost", "pandas"],
            "tools": ["Make", "CMake", "gdb", "valgrind"],
            "project_type": "financial_system",
            "package_managers": ["pip", "conan"],
            "has_tests": False,  # Part of the technical debt problem
            "has_docker": False,
            "has_git": True,
            "ide_config": [".vscode"],
            "linting_tools": [],  # Another sign of technical debt
            "ci_cd": [],  # Manual deployment issues
            "dependencies": {
                "boost": "^1.82.0",
                "pandas": "^2.0.0",
                "numpy": "^1.24.0",
                "cpprest": "^2.10.0"
            },
            "scripts": {
                "build": "make -j8",
                "run": "./bin/trading_engine",
                "debug": "gdb ./bin/trading_engine"
            },
            "directory_structure": [
                "src/legacy/",
                "src/core/",
                "src/market_data/",
                "src/risk/",
                "Makefile",
                "bin/",
                "lib/",
                "config/",
                "logs/"
            ]
        },
        
        "extremely_reserved": {
            # Critical medical device control system - extremely dangerous legacy setup
            "languages": ["C"],
            "frameworks": [],
            "tools": ["GCC", "gdb", "oscilloscope", "JTAG"],
            "project_type": "embedded_medical",
            "package_managers": [],
            "has_tests": False,  # Critical absence of testing
            "has_docker": False,
            "has_git": False,  # No version control - major red flag
            "ide_config": [],
            "linting_tools": [],
            "ci_cd": [],
            "dependencies": {},
            "scripts": {
                "compile": "gcc -o monitor monitor.c",
                "deploy": "manual_flash_procedure.txt"
            },
            "directory_structure": [
                "monitor.c",
                "legacy_drivers/",
                "device_config/",
                "manual_flash_procedure.txt",
                "emergency_contacts.txt"
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
        "junior_frontend": "React + Tailwind CSS portfolio website",
        "data_scientist": "Python/R ML project analyzing customer behavior",
        "devops_engineer": "Kubernetes migration with GitOps and monitoring",
        "reserved_developer": "C++/Python/Rust high-frequency trading system with technical debt",
        "extremely_reserved": "C embedded medical device control system (CRITICAL - life support)"
    }
    
    return summaries.get(persona_name, "Unknown project")