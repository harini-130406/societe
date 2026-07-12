# PolicyGuard Enterprise - GIT Repository Setup Guide

## Repository Overview
This guide provides comprehensive instructions for setting up, organizing, and sharing the PolicyGuard Enterprise GIT repository for hackathon submission and open-source distribution.

---

## 1. Repository Structure

### Recommended Directory Structure
```
policyguard-enterprise/
├── .github/
│   ├── workflows/
│   │   └── ci-cd.yml          # GitHub Actions CI/CD pipeline
│   ├── ISSUE_TEMPLATE/
│   │   └── bug_report.md      # Bug report template
│   └── PULL_REQUEST_TEMPLATE.md
├── backend/
│   ├── __init__.py
│   ├── main.py                # FastAPI application
│   ├── pipeline.py            # Analysis pipeline orchestrator
│   ├── parser.py             # Policy document parser
│   ├── topic_classifier.py    # Topic classification module
│   ├── scope_extractor.py     # Scope extraction module
│   ├── conflict_engine.py     # Conflict detection engine
│   ├── redundancy_engine.py   # Redundancy detection engine
│   ├── stale_checker.py       # Staleness checking module
│   ├── evaluation.py          # Evaluation metrics engine
│   ├── pdf_report.py          # PDF report generator
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # Main dashboard
│   ├── index_backup.html      # Original frontend backup
│   └── assets/                # Static assets (if any)
├── sample_data/
│   ├── policies/              # Policy document directory
│   │   ├── policy_01.md
│   │   ├── policy_02.md
│   │   └── ...
│   ├── policy_metadata.json   # Policy metadata
│   ├── obligation_extracts_labels.json  # Ground truth labels
│   ├── findings_labels.json   # Finding labels
│   └── evaluation_results.json # Evaluation output
├── docs/
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── PRESENTATION_OUTLINE.md
│   ├── VIDEO_CREATION_GUIDE.md
│   └── GIT_REPOSITORY_GUIDE.md
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_classifier.py
│   └── test_evaluation.py
├── scripts/
│   ├── setup.sh               # Installation script
│   ├── run_analysis.py        # Analysis runner
│   └── generate_report.py     # Report generator
├── .gitignore                 # GIT ignore rules
├── README.md                  # Main repository README
├── LICENSE                    # License file
└── docker-compose.yml         # Docker configuration (optional)
```

---

## 2. Initial GIT Setup

### 2.1 Initialize Repository
```bash
# Navigate to project directory
cd d:\societe

# Initialize GIT repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: PolicyGuard Enterprise"
```

### 2.2 Create .gitignore File
```bash
# Create .gitignore in root directory
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Data files (large datasets)
sample_data/policies/*.md
sample_data/*.json
!sample_data/policy_metadata.json
!sample_data/obligation_extracts_labels.json
!sample_data/findings_labels.json

# Generated files
backend/analysis.json
sample_data/PolicyGuard_Audit_Report.pdf
sample_data/evaluation_results.json

# Logs
*.log

# OS
Thumbs.db
.DS_Store
EOF
```

### 2.3 Configure GIT
```bash
# Set user name and email
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Set default branch name
git config init.defaultBranch main

# Rename branch to main (if not already)
git branch -M main
```

---

## 3. README.md Creation

### Complete README.md Template
```markdown
# PolicyGuard Enterprise

Automated Policy Conflict & Staleness Detection Platform

![PolicyGuard Logo](https://img.shields.io/badge/PolicyGuard-Enterprise-teal)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

PolicyGuard Enterprise is an automated policy governance platform that detects conflicts, redundancies, and staleness in organizational policy documents using natural language processing (NLP) and rule-based algorithms.

## Features

- **Automated Policy Parsing**: Extracts obligations from markdown policy documents
- **Intelligent Classification**: Categorizes obligations by topic, scope, and strength
- **Conflict Detection**: Identifies contradictory policy requirements
- **Redundancy Detection**: Finds duplicate or overlapping obligations
- **Staleness Checking**: Flags outdated policies based on metadata and content
- **Interactive Dashboard**: Real-time visualization with enterprise-grade UI
- **Multi-Format Export**: PDF, CSV, and JSON reporting capabilities

## Technology Stack

### Backend
- Python 3.9+
- FastAPI (REST API)
- NetworkX (Graph processing)
- spaCy (NLP)
- Sentence Transformers (Embeddings)
- ReportLab (PDF generation)

### Frontend
- HTML5, CSS3, JavaScript
- Tailwind CSS (Styling)
- Chart.js (Charts)
- Vis.js (Network graphs)
- Lucide Icons

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- 4GB RAM minimum
- 2GB disk space

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/policyguard-enterprise.git
cd policyguard-enterprise
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

4. **Prepare data**
```bash
# Copy your policy files to sample_data/policies/
# Copy label files to sample_data/
```

5. **Start the server**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

6. **Access the dashboard**
```
Open your browser to http://localhost:8001
```

## Usage

### Analyzing Policies

The system automatically analyzes all policy documents in the `sample_data/policies/` directory when you access the dashboard or call the `/api/analyze` endpoint.

### Uploading Policies

Use the dashboard upload button or API endpoint:
```bash
curl -X POST http://localhost:8001/api/upload \
  -F "file=@your_policy.md"
```

### Exporting Reports

Export reports directly from the dashboard or via API:
```bash
# PDF Report
curl http://localhost:8001/api/export-pdf -o report.pdf

# JSON Data
curl http://localhost:8001/api/analyze -o analysis.json
```

## API Documentation

### Endpoints

- `GET /api/health` - Health check
- `GET /api/analyze` - Run full analysis
- `POST /api/upload` - Upload policy file
- `GET /api/policies` - List all policies
- `DELETE /api/policies/{filename}` - Delete policy
- `GET /api/eval` - Get evaluation metrics
- `GET /api/export-pdf` - Generate PDF report

For detailed API documentation, see [API Documentation](docs/TECHNICAL_DOCUMENTATION.md#api-documentation).

## Documentation

- [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md) - Complete system architecture and algorithms
- [Presentation Outline](docs/PRESENTATION_OUTLINE.md) - Slide deck structure for presentations
- [Video Creation Guide](docs/VIDEO_CREATION_GUIDE.md) - Guide for creating solution videos

## Evaluation Results

Based on evaluation against 30-policy dataset:

- **Obligation Extraction Accuracy**: 28.28%
- **Conflict Detection**: Precision 6.57%, Recall 65.71%, F1 11.95%
- **Redundancy Detection**: Precision 5.28%, Recall 73.68%, F1 9.86%
- **Staleness Detection**: Precision 50.0%, Recall 100.0%, F1 66.67%

## Screenshots

### Dashboard
![Dashboard Screenshot](docs/screenshots/dashboard.png)

### Executive Summary
![Executive Summary](docs/screenshots/executive-summary.png)

### Recommendations
![Recommendations](docs/screenshots/recommendations.png)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for [Hackathon Name]
- Uses spaCy for natural language processing
- Uses Sentence Transformers for semantic similarity
- Uses Vis.js for network visualization

## Contact

- **Project Repository**: https://github.com/yourusername/policyguard-enterprise
- **Issues**: https://github.com/yourusername/policyguard-enterprise/issues
- **Email**: your.email@example.com

## Roadmap

### Short-term
- Improve evaluation scores with better matching
- Add more policy templates
- Enhance conflict rule set

### Medium-term
- Real-time policy monitoring
- Integration with compliance frameworks (SOC 2, ISO 27001)
- Automated remediation suggestions

### Long-term
- Multi-language support
- Role-based access control
- ML-based conflict detection
```

---

## 4. License File

### MIT License Template
```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 PolicyGuard Enterprise Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

---

## 5. GitHub Repository Setup

### 5.1 Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Repository name**: `policyguard-enterprise`
3. **Description**: Automated Policy Conflict & Staleness Detection Platform
4. **Visibility**: Public (for hackathon) or Private
5. **Initialize**: Don't initialize with README (we have one)
6. **Click Create repository**

### 5.2 Connect Repository to GitHub
```bash
# Add remote repository
git remote add origin https://github.com/yourusername/policyguard-enterprise.git

# Push to GitHub
git push -u origin main
```

### 5.3 Repository Settings

**Enable Features**:
- **Issues**: For bug tracking and feature requests
- **Projects**: For project management (optional)
- **Wiki**: For additional documentation (optional)
- **Discussions**: For community discussions (optional)

**Repository Topics**:
Add these topics for discoverability:
- `policy`
- `compliance`
- `nlp`
- `governance`
- `security`
- `hackathon`
- `python`
- `fastapi`

---

## 6. GitHub Actions CI/CD (Optional)

### 6.1 Create CI/CD Workflow
```bash
mkdir -p .github/workflows
cat > .github/workflows/ci-cd.yml << 'EOF'
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        python -m pytest tests/ -v

  build:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: |
        docker build -t policyguard:latest .
    
    - name: Run container
      run: |
        docker run -d -p 8001:8001 policyguard:latest
EOF
```

### 6.2 Push Workflow
```bash
git add .github/workflows/ci-cd.yml
git commit -m "Add CI/CD pipeline"
git push origin main
```

---

## 7. Issue Templates

### 7.1 Bug Report Template
```bash
mkdir -p .github/ISSUE_TEMPLATE
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment**
- OS: [e.g. Windows 10, macOS 11.0]
- Python Version: [e.g. 3.9.0]
- Browser: [e.g. Chrome 91.0]

**Additional context**
Add any other context about the problem here.
EOF
```

### 7.2 Feature Request Template
```bash
cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
EOF
```

---

## 8. Pull Request Template

### PR Template
```bash
cat > .github/PULL_REQUEST_TEMPLATE.md << 'EOF'
## Description
Please include a description of the changes proposed in this PR.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
Describe the tests you ran to verify your changes:

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules
EOF
```

---

## 9. Branching Strategy

### Recommended Branch Names
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/feature-name` - Feature branches
- `bugfix/bug-name` - Bug fix branches
- `hotfix/hotfix-name` - Urgent production fixes

### Branch Workflow
```bash
# Create feature branch
git checkout -b feature/add-new-topic

# Make changes and commit
git add .
git commit -m "Add new topic classification"

# Push to remote
git push origin feature/add-new-topic

# Create pull request on GitHub
# After review and merge, delete branch
git branch -d feature/add-new-topic
```

---

## 10. Tagging and Releases

### 10.1 Create Tags
```bash
# Create annotated tag
git tag -a v1.0.0 -m "Initial release"

# Push tags to remote
git push origin v1.0.0
git push origin --tags
```

### 10.2 Create GitHub Release

1. **Go to GitHub**: Repository → Releases → Create Release
2. **Tag version**: v1.0.0
3. **Release title**: PolicyGuard Enterprise v1.0.0
4. **Description**: 
```markdown
## PolicyGuard Enterprise v1.0.0

### Features
- Automated policy parsing and obligation extraction
- Topic classification with 20+ security topics
- Conflict detection with 5 conflict types
- Redundancy detection using semantic similarity
- Staleness checking with multi-factor assessment
- Interactive dashboard with 5 pages
- Multi-format export (PDF, CSV, JSON)

### Installation
See README.md for installation instructions

### Documentation
- Technical Documentation
- API Documentation
- Video Creation Guide
- Presentation Outline
```

5. **Attach assets**: Add PDF report, screenshots, etc.
6. **Publish release**

---

## 11. Documentation Organization

### 11.1 Docs Directory Structure
```
docs/
├── screenshots/              # Screenshots for README
│   ├── dashboard.png
│   ├── executive-summary.png
│   └── recommendations.png
├── api/                      # API documentation
│   ├── endpoints.md
│   └── examples.md
├── user-guide/               # User guides
│   ├── getting-started.md
│   ├── dashboard-guide.md
│   └── export-guide.md
├── developer-guide/          # Developer documentation
│   ├── architecture.md
│   ├── contributing.md
│   └── testing.md
├── TECHNICAL_DOCUMENTATION.md
├── PRESENTATION_OUTLINE.md
├── VIDEO_CREATION_GUIDE.md
└── GIT_REPOSITORY_GUIDE.md
```

### 11.2 Update README with Links
Ensure README.md links to all documentation:
```markdown
## Documentation

- [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md) - Complete system architecture and algorithms
- [Presentation Outline](docs/PRESENTATION_OUTLINE.md) - Slide deck structure for presentations
- [Video Creation Guide](docs/VIDEO_CREATION_GUIDE.md) - Guide for creating solution videos
- [GIT Repository Guide](docs/GIT_REPOSITORY_GUIDE.md) - Repository setup and management
```

---

## 12. Best Practices

### 12.1 Commit Messages
Follow conventional commits format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat(parser): add support for YAML frontmatter"
git commit -m "fix(conflict): resolve parameter conflict detection bug"
git commit -m "docs(readme): update installation instructions"
```

### 12.2 Code Quality
- **PEP 8**: Follow Python style guide
- **Type Hints**: Add type hints for functions
- **Docstrings**: Add docstrings for all functions
- **Comments**: Comment complex logic
- **Tests**: Write unit tests for critical functions

### 12.3 Security
- **API Keys**: Never commit API keys
- **Sensitive Data**: Use environment variables
- **Dependencies**: Keep dependencies updated
- **Secrets**: Use `.env` files (add to .gitignore)

---

## 13. Sharing for Hackathon

### 13.1 Repository Checklist
Before submitting for hackathon:

- [ ] README.md is complete and professional
- [ ] License file is included
- [ ] .gitignore is properly configured
- [ ] All documentation is in docs/ directory
- [ ] Screenshots are included
- [ ] Installation instructions work
- [ ] Demo video is linked (if available)
- [ ] Repository is public (if required)
- [ ] Topics are added for discoverability
- [ ] Issues template is configured
- [ ] CI/CD is set up (optional)

### 13.2 Hackathon Submission
**Required Information**:
- Repository URL: https://github.com/yourusername/policyguard-enterprise
- Demo Video URL: [YouTube/Vimeo link]
- Technical Documentation: Link to docs/TECHNICAL_DOCUMENTATION.md
- Presentation: Link to docs/PRESENTATION_OUTLINE.md

**Description Template**:
```
PolicyGuard Enterprise - Automated Policy Conflict & Staleness Detection Platform

A comprehensive solution for automated policy governance using NLP and rule-based algorithms.

Key Features:
- Automated policy parsing and obligation extraction
- Intelligent topic classification (20+ topics)
- Conflict detection (5 types)
- Redundancy detection (semantic similarity)
- Staleness checking (multi-factor)
- Enterprise-grade dashboard
- Multi-format export (PDF, CSV, JSON)

Technology Stack:
- Backend: Python, FastAPI, spaCy, NetworkX
- Frontend: HTML5, Tailwind CSS, Chart.js, Vis.js

Repository: https://github.com/yourusername/policyguard-enterprise
Documentation: https://github.com/yourusername/policyguard-enterprise/blob/main/docs/TECHNICAL_DOCUMENTATION.md
Demo: [Video Link]
```

---

## 14. Maintenance

### 14.1 Regular Tasks
- **Weekly**: Check for dependency updates
- **Monthly**: Review and close stale issues
- **Quarterly**: Update documentation
- **Annually**: Review and update license if needed

### 14.2 Dependency Updates
```bash
# Check for outdated packages
pip list --outdated

# Update requirements.txt
pip freeze > requirements.txt

# Test after updates
python -m pytest tests/
```

### 14.3 Backup Strategy
- **GitHub**: Primary backup (remote repository)
- **Local**: Regular local commits
- **Tags**: Tag releases for rollback capability
- **Documentation**: Keep docs in repository

---

## 15. Troubleshooting

### 15.1 Common GIT Issues

**Issue**: Permission denied (publickey)
```bash
# Solution: Add SSH key to GitHub
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
# Add key to GitHub settings
```

**Issue**: Remote origin already exists
```bash
# Solution: Remove and add remote
git remote remove origin
git remote add origin https://github.com/yourusername/policyguard-enterprise.git
```

**Issue**: Files too large for GitHub
```bash
# Solution: Use Git LFS or move to external storage
git lfs track "*.pdf"
git lfs track "*.json"
git add .gitattributes
```

### 15.2 Repository Issues

**Issue**: Repository not showing updates
```bash
# Solution: Force push (use carefully)
git push -f origin main
```

**Issue**: Wrong commit in history
```bash
# Solution: Interactive rebase
git rebase -i HEAD~3
# Mark commits to edit/drop
```

---

## 16. Resources

### GIT Resources
- [GIT Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Pro GIT Book](https://git-scm.com/book/en/v2)

### GitHub Resources
- [GitHub Skills](https://skills.github.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages](https://pages.github.com/)

### Open Source Resources
- [Open Source Guides](https://opensource.guide/)
- [Choosing a License](https://choosealicense.com/)
- [Contributor Covenant](https://www.contributor-covenant.org/)

---

## 17. Quick Start Commands

### Complete Setup Script
```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit: PolicyGuard Enterprise"

# Add remote
git remote add origin https://github.com/yourusername/policyguard-enterprise.git

# Push to GitHub
git branch -M main
git push -u origin main

# Create first release
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
git push origin --tags
```

---

*Repository Guide Version: 1.0*
*Last Updated: July 12, 2026*
