# PolicyGuard Enterprise - Technical Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Analysis Algorithms](#analysis-algorithms)
4. [User Interface Design](#user-interface-design)
5. [API Documentation](#api-documentation)
6. [Data Models](#data-models)
7. [Deployment Guide](#deployment-guide)
8. [Troubleshooting](#troubleshooting)

---

## 1. System Overview

### 1.1 Purpose
PolicyGuard Enterprise is an automated policy governance platform that detects conflicts, redundancies, and staleness in organizational policy documents. The system uses natural language processing (NLP) and rule-based algorithms to analyze policy documents and provide actionable insights for compliance teams.

### 1.2 Key Features
- **Automated Policy Parsing**: Extracts obligations from markdown policy documents
- **Topic Classification**: Categorizes obligations into security/compliance topics
- **Scope Extraction**: Identifies affected stakeholders and systems
- **Conflict Detection**: Identifies contradictory policy requirements
- **Redundancy Detection**: Finds duplicate or overlapping obligations
- **Staleness Checking**: Flags outdated policies based on metadata and content
- **Interactive Dashboard**: Real-time visualization of policy health
- **Multi-Format Export**: PDF, CSV, and JSON reporting capabilities

### 1.3 Technology Stack
- **Backend**: Python 3.9+, FastAPI, NetworkX, spaCy, Sentence Transformers
- **Frontend**: HTML5, Tailwind CSS, JavaScript, Chart.js, Vis.js
- **Data Processing**: NumPy, spaCy NLP, scikit-learn
- **Visualization**: Chart.js, Vis.js Network Graph
- **PDF Generation**: ReportLab

---

## 2. Architecture

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Dashboard  │  │ Executive    │  │ Compliance   │          │
│  │   View       │  │   Summary    │  │   Mapping    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                  │
│         └──────────────────┼──────────────────┘                  │
│                            │                                     │
│                    REST API Layer (FastAPI)                      │
└────────────────────────────┼─────────────────────────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────────┐
│                    Backend Processing Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Pipeline   │  │  Evaluation  │  │ PDF Report   │          │
│  │  Orchestrator│  │   Engine     │  │  Generator   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                  │
│  ┌──────┴──────┐  ┌────────┴────────┐  ┌────────┴──────┐       │
│  │   Parser    │  │ Conflict Engine │  │Stale Checker  │       │
│  │   Module    │  │                 │  │               │       │
│  └─────────────┘  └─────────────────┘  └───────────────┘       │
│  ┌─────────────┐  ┌─────────────────┐  ┌───────────────┐       │
│  │Topic Classifier│ │Redundancy Engine│ │Scope Extractor│       │
│  └─────────────┘  └─────────────────┘  └───────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────────┐
│                    Data Layer                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Policy Files │  │   Labels     │  │   Metadata   │          │
│  │  (Markdown)  │  │  (JSON)      │  │   (JSON)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Description

#### 2.2.1 Frontend Layer
- **Dashboard View**: Main interface with metrics, graphs, and findings table
- **Executive Summary**: High-level governance overview
- **Compliance Mapping**: Framework alignment visualization
- **Evaluation Page**: Model performance metrics

#### 2.2.2 API Layer (FastAPI)
- **REST Endpoints**: Standardized HTTP interface for all operations
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **File Upload**: Handles policy document uploads
- **Export Services**: PDF, CSV, JSON generation

#### 2.2.3 Backend Processing Layer

**Pipeline Orchestrator** (`pipeline.py`)
- Coordinates all analysis steps
- Manages data flow between modules
- Generates NetworkX graph structure

**Parser Module** (`parser.py`)
- Extracts YAML frontmatter metadata
- Identifies obligation sentences using keyword matching
- Determines obligation strength (Mandatory/Recommended/Optional)
- Extracts actions, objects, and parameters

**Topic Classifier** (`topic_classifier.py`)
- Classifies obligations into 20+ security topics
- Uses keyword-based classification with spaCy lemmatization
- Supports topics: Password, Encryption, VPN, Logging, MFA, Data Retention, Access Control, Network, Cloud, Backup, Asset, Privacy, Monitoring, API, Mobile, Endpoint, Provisioning, Physical, Change, Patch, HR

**Scope Extractor** (`scope_extractor.py`)
- Identifies affected stakeholders and systems
- Uses keyword matching and spaCy dependency parsing
- Normalizes scopes to ground truth format

**Conflict Engine** (`conflict_engine.py`)
- Detects contradictory policy requirements
- Rule-based conflict detection with confidence scoring
- Supports LLM adjudication for ambiguous cases (optional)

**Redundancy Engine** (`redundancy_engine.py`)
- Identifies duplicate or overlapping obligations
- Uses Sentence Transformers for semantic similarity
- Configurable similarity thresholds

**Stale Checker** (`stale_checker.py`)
- Flags outdated policies based on review dates
- Checks for deprecated technologies and standards
- Incorporates policy metadata for enhanced checking

**Evaluation Engine** (`evaluation.py`)
- Computes precision, recall, F1 scores
- Compares extracted data against ground truth labels
- Generates detailed diagnostic reports

### 2.3 Data Flow

```
1. Policy Upload → 2. Parsing → 3. Topic Classification → 4. Scope Extraction
                                    ↓
5. Conflict Detection ← 6. Redundancy Detection ← 7. Staleness Checking
                                    ↓
8. Graph Building → 9. Analysis Generation → 10. Dashboard Visualization
```

---

## 3. Analysis Algorithms

### 3.1 Obligation Extraction Algorithm

**Input**: Markdown policy document with YAML frontmatter

**Process**:
1. **Metadata Extraction**: Parse YAML frontmatter for title, author, department, version, review date, status
2. **Sentence Segmentation**: Split document into sentences using spaCy
3. **Obligation Identification**: Match sentences containing obligation keywords (must, shall, required, ensure, etc.)
4. **Strength Classification**: Determine obligation strength based on modal verbs
5. **Component Extraction**: Extract action, object, and parameters using dependency parsing
6. **Topic Classification**: Assign security topic using keyword matching
7. **Scope Extraction**: Identify affected stakeholders using pattern matching

**Output**: Structured obligation objects with metadata

```python
{
    "obligation_sentence": "Users must change passwords every 90 days",
    "policy_name": "Password Policy",
    "topic": "password",
    "strength": "Mandatory",
    "scope": ["employees"],
    "action": "change",
    "object": "passwords",
    "parameters": {"frequency": 90}
}
```

### 3.2 Topic Classification Algorithm

**Approach**: Keyword-based classification with spaCy lemmatization

**Algorithm**:
1. **Tokenization**: Tokenize obligation sentence using spaCy
2. **Lemmatization**: Convert tokens to base forms (e.g., "changing" → "change")
3. **Keyword Matching**: Match lemmatized tokens against topic keyword dictionaries
4. **Scoring**: Calculate match score based on keyword frequency and relevance
5. **Selection**: Select topic with highest score above threshold

**Topics Supported**:
- **Password**: password, credential, authentication, login
- **Encryption**: encrypt, decrypt, cipher, cryptographic, tls, ssl
- **VPN**: vpn, virtual private network, remote access, tunnel
- **Logging**: log, audit, record, monitor, track
- **MFA**: mfa, multi-factor, two-factor, 2fa, authentication
- **Data Retention**: retain, keep, store, archive, backup, retention
- **Access Control**: access, permission, authorization, privilege, role
- **Network**: network, firewall, port, protocol, ip address
- **Cloud**: cloud, aws, azure, gcp, saas, paas
- **Backup**: backup, recovery, restore, disaster recovery
- **Asset**: asset, inventory, device, hardware, software
- **Privacy**: privacy, personal data, pii, gdpr, consent
- **Monitoring**: monitor, observe, alert, notify, dashboard
- **API**: api, endpoint, web service, rest, graphql
- **Mobile**: mobile, device, phone, tablet, byod
- **Endpoint**: endpoint, workstation, laptop, desktop
- **Provisioning**: provision, create, setup, configure, onboard
- **Physical**: physical, facility, building, access card, badge
- **Change**: change, modification, update, patch, version
- **Patch**: patch, update, security fix, vulnerability
- **HR**: employee, contractor, personnel, hr, onboarding

### 3.3 Conflict Detection Algorithm

**Approach**: Rule-based detection with confidence scoring

**Conflict Types**:

1. **Direct Conflict**: Mutually exclusive requirements
   - Example: "Must use MD5" vs "Must not use MD5"

2. **Parameter Conflict**: Same action with conflicting parameters
   - Example: "Change password every 30 days" vs "Change password every 90 days"

3. **Temporal Conflict**: Time-based contradictions
   - Example: "Review annually" vs "Review monthly"

4. **Strength Conflict**: Same requirement with different strength levels
   - Example: "Must encrypt" vs "Should encrypt"

5. **Scope Conflict**: Same requirement with different scopes
   - Example: "All employees" vs "Only contractors"

**Algorithm**:
1. **Pair Generation**: Generate all obligation pairs within same topic
2. **Rule Evaluation**: Apply conflict rules to each pair
3. **Confidence Scoring**: Calculate confidence based on rule match strength
4. **Adjudication**: Use LLM for ambiguous cases (optional)
5. **Filtering**: Filter by confidence threshold (default: 0.5)

**Output**: Conflict relations with confidence scores and explanations

### 3.4 Redundancy Detection Algorithm

**Approach**: Semantic similarity using Sentence Transformers

**Algorithm**:
1. **Embedding Generation**: Generate sentence embeddings using all-MiniLM-L6-v2 model
2. **Similarity Calculation**: Compute cosine similarity between obligation pairs
3. **Threshold Filtering**: Filter pairs above similarity threshold (default: 0.85)
4. **Scope Check**: Ensure obligations have overlapping scopes
5. **Topic Check**: Ensure obligations belong to same topic

**Output**: Redundancy relations with similarity scores

### 3.5 Staleness Detection Algorithm

**Approach**: Multi-factor staleness assessment

**Factors**:

1. **Review Date**: Policies not reviewed within threshold (default: 365 days)
2. **Deprecated Technologies**: Mentions of deprecated algorithms/protocols
3. **Deprecated Standards**: References to outdated standards (e.g., SHA-1)
4. **Policy Status**: Retired or draft status from metadata
5. **Missing Metadata**: Incomplete metadata fields

**Algorithm**:
1. **Metadata Check**: Load policy metadata from JSON file
2. **Date Calculation**: Calculate days since last review
3. **Content Analysis**: Scan for deprecated technology keywords
4. **Status Check**: Check policy status field
5. **Score Calculation**: Calculate staleness score based on factors
6. **Threshold Application**: Flag policies above threshold

**Output**: Stale policy list with reasons

### 3.6 Evaluation Algorithm

**Approach**: Comparison against ground truth labels

**Metrics**:

1. **Obligation Extraction**: F1 score based on policy_file + topic matching
2. **Conflict Detection**: Precision, Recall, F1 score
3. **Redundancy Detection**: Precision, Recall, F1 score
4. **Staleness Detection**: Precision, Recall, F1 score
5. **Overall Metrics**: Aggregate precision, recall, F1, accuracy
6. **False Positive Rate**: FP / (FP + TP)

**Algorithm**:
1. **Load Ground Truth**: Load obligation_extracts_labels.json and findings_labels.json
2. **Extract Predictions**: Get extracted obligations and detected findings
3. **Matching**: Match predictions to ground truth using policy_file + topic
4. **Count Metrics**: Calculate TP, FP, FN for each category
5. **Compute Scores**: Calculate precision, recall, F1 scores
6. **Aggregate**: Compute overall metrics

---

## 4. User Interface Design

### 4.1 Design Principles

- **Professional GRC Theme**: Dark mode with teal/brand accent colors
- **Glass-morphism**: Semi-transparent cards with backdrop blur
- **Responsive Design**: Mobile-friendly grid layouts
- **Accessibility**: High contrast ratios, clear typography
- **Performance**: Optimized loading with lazy rendering

### 4.2 Color Palette

```css
Primary Brand: #14b8a6 (Teal)
Secondary: #3b82f6 (Blue)
Success: #22c55e (Green)
Warning: #f59e0b (Amber)
Error: #ef4444 (Red)
Background: #0f172a (Slate 950)
Surface: rgba(15, 23, 42, 0.6) (Glass)
Text Primary: #f8fafc (Slate 50)
Text Secondary: #94a3b8 (Slate 400)
```

### 4.3 Typography

```css
Font Family: Inter (UI), JetBrains Mono (Code)
Headings: 600-700 weight, tight tracking
Body: 400 weight, normal leading
Monospace: 500 weight, for data display
```

### 4.4 Component Library

#### 4.4.1 Metric Cards
- Glass-morphism background
- Icon indicator
- Large value display
- Status badge
- Hover lift effect

#### 4.4.2 Data Tables
- Sticky headers
- Row hover effects
- Truncated text with tooltips
- Status color coding
- Action buttons

#### 4.4.3 Charts
- Doughnut charts for distribution
- Progress bars for metrics
- SVG gauges for scores
- Interactive tooltips

#### 4.4.4 Network Graph
- Vis.js force-directed layout
- Color-coded nodes by type
- Interactive zoom/pan
- Node selection details

#### 4.4.5 Filters
- Search input with icon
- Dropdown selectors
- Apply/Reset buttons
- Real-time filtering

#### 4.4.6 Side Drawer
- Slide-in animation
- Detail view for findings
- Close button
- Scrollable content

### 4.5 Page Layouts

#### 4.5.1 Dashboard Page
- **Header**: Logo, title, export dropdown, refresh button
- **Metrics Row**: 4 metric cards (Health, Policies, Conflicts, Stale)
- **Filters Row**: Search, Department, Topic, Severity filters
- **Main Grid**: 
  - Left: Policy graph + Findings table
  - Right: Compliance gauge + Topic chart + Status bars

#### 4.5.2 Executive Summary Page
- **Header**: Page title and description
- **Key Metrics**: 3 metric cards (Trend, Compliant, Action Required)
- **Risk Summary**: Top risk areas and compliance frameworks
- **Activity Timeline**: Recent policy changes

#### 4.5.3 Recommendations Page
- **Header**: Page title and description
- **Priority List**: Cards sorted by severity (Critical/High/Medium)
- **Action Buttons**: Take Action, View Details
- **Conflict Counts**: Display per recommendation

#### 4.5.4 Compliance Mapping Page
- **Header**: Page title and description
- **Framework Cards**: SOC 2, ISO 27001, GDPR with progress bars
- **Mapping Table**: Policy-to-framework alignment table

#### 4.5.5 Evaluation Page
- **Header**: Page title and description
- **Metrics Grid**: 4 evaluation metrics with progress bars
- **Detailed Metrics**: Precision, Recall, F1 breakdown
- **Diagnostics Log**: JSON output of evaluation results

### 4.6 Responsive Breakpoints

```css
Mobile: < 640px (stacked layout)
Tablet: 640px - 1024px (2-column grid)
Desktop: > 1024px (3-column grid)
```

### 4.7 Loading States

- **Overlay**: Full-screen spinner with backdrop blur
- **Skeleton Loading**: Gray placeholders for data cards
- **Progress Indicators**: Progress bars for long operations

### 4.8 Error Handling

- **API Errors**: Toast notifications with retry option
- **Data Errors**: Fallback to default values
- **Network Errors**: Offline indicator with retry

---

## 5. API Documentation

### 5.1 Base URL
```
http://localhost:8001/api
```

### 5.2 Endpoints

#### 5.2.1 Health Check
```
GET /health
```
**Response**:
```json
{
  "status": "ok",
  "timestamp": "2026-07-11T15:35:40Z"
}
```

#### 5.2.2 Analyze Policies
```
GET /analyze
```
**Description**: Runs full pipeline analysis on all policies in directory

**Response**:
```json
{
  "health_score": 0,
  "metrics": {
    "total_obligations": 343,
    "conflicts": 724,
    "redundancies": 406,
    "stale_policies": 27
  },
  "obligations": [...],
  "relations": [...],
  "graph": {
    "nodes": [...],
    "edges": [...]
  }
}
```

#### 5.2.3 Upload Policy
```
POST /upload
Content-Type: multipart/form-data
```
**Parameters**: `file` (markdown or text file)

**Response**:
```json
{
  "filename": "policy_name.md",
  "message": "Policy uploaded successfully."
}
```

#### 5.2.4 List Policies
```
GET /policies
```
**Response**:
```json
[
  {
    "filename": "policy_01.md",
    "title": "Policy 01",
    "owner": "Unknown Owner",
    "last_reviewed": "2026-01-01",
    "size_bytes": 799
  }
]
```

#### 5.2.5 Delete Policy
```
DELETE /policies/{filename}
```
**Response**:
```json
{
  "message": "Policy 'policy_01.md' deleted successfully."
}
```

#### 5.2.6 Get Evaluation Metrics
```
GET /eval
```
**Response**:
```json
{
  "obligation_extraction_accuracy": 28.28,
  "conflict_detection_rate": 11.95,
  "redundancy_detection_rate": 9.86,
  "staleness_detection_rate": 66.67,
  "conflict_detection": {
    "precision": 6.57,
    "recall": 65.71,
    "f1_score": 11.95
  },
  "redundancy_detection": {
    "precision": 5.28,
    "recall": 73.68,
    "f1_score": 9.86
  },
  "staleness_detection": {
    "precision": 50.0,
    "recall": 100.0,
    "f1_score": 66.67
  },
  "false_positive_rate": 91.75
}
```

#### 5.2.7 Export PDF Report
```
GET /export-pdf
```
**Response**: PDF file download

---

## 6. Data Models

### 6.1 Obligation Object
```json
{
  "obligation_sentence": "Users must change passwords every 90 days",
  "policy_name": "Password Policy",
  "filename": "policy_01.md",
  "topic": "password",
  "strength": "Mandatory",
  "scope": ["employees"],
  "action": "change",
  "object": "passwords",
  "parameters": {
    "frequency": 90,
    "unit": "days"
  },
  "section": "1.1",
  "confidence_score": 0.95
}
```

### 6.2 Relation Object
```json
{
  "id": "rel_001",
  "type": "conflict",
  "source_doc": "policy_01.md",
  "target_doc": "policy_02.md",
  "source_obligation": "ob_001",
  "target_obligation": "ob_002",
  "confidence_score": 0.85,
  "reason": "Parameter conflict: different password change frequencies",
  "severity": "high"
}
```

### 6.3 Graph Node Object
```json
{
  "id": "policy_01",
  "label": "Password Policy",
  "group": "policy",
  "title": "Password Policy",
  "value": 10
}
```

### 6.4 Graph Edge Object
```json
{
  "from": "policy_01",
  "to": "ob_001",
  "color": "#14b8a6",
  "width": 2
}
```

### 6.5 Policy Metadata Object
```json
{
  "file": "policy_01.md",
  "title": "Password Policy",
  "author": "Security Team",
  "department": "Information Security",
  "version": "2.0",
  "last_reviewed": "2026-01-01",
  "status": "active"
}
```

---

## 7. Deployment Guide

### 7.1 Prerequisites
- Python 3.9 or higher
- pip package manager
- 4GB RAM minimum
- 2GB disk space

### 7.2 Installation Steps

1. **Clone Repository**
```bash
git clone <repository-url>
cd societe
```

2. **Create Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

4. **Prepare Data**
```bash
# Copy policy files to sample_data/policies/
# Copy label files to sample_data/
```

5. **Start Backend Server**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

6. **Access Dashboard**
```
Open browser to http://localhost:8001
```

### 7.3 Configuration

**Environment Variables** (optional):
```bash
OPENAI_API_KEY=sk-...  # For LLM adjudication
POLICIES_DIR=./sample_data/policies
SAMPLE_DATA_DIR=./sample_data
```

**Configuration Files**:
- `backend/requirements.txt`: Python dependencies
- `sample_data/policies/`: Policy document directory
- `sample_data/policy_metadata.json`: Policy metadata
- `sample_data/obligation_extracts_labels.json`: Ground truth labels
- `sample_data/findings_labels.json`: Finding labels

### 7.4 Production Deployment

**Using Docker**:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
COPY frontend/ ./frontend/
COPY sample_data/ ./sample_data/
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Using Nginx**:
```nginx
server {
    listen 80;
    server_name policyguard.example.com;
    
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 8. Troubleshooting

### 8.1 Common Issues

**Issue**: Port 8001 already in use
**Solution**: Change port in uvicorn command or stop conflicting process

**Issue**: ModuleNotFoundError for networkx
**Solution**: Install missing dependencies: `pip install networkx`

**Issue**: Frontend not loading data
**Solution**: Check API_BASE in frontend/index.html matches backend port

**Issue**: Low evaluation scores
**Solution**: Ensure ground truth labels match extracted data format

**Issue**: Graph not rendering
**Solution**: Check browser console for Vis.js loading errors

### 8.2 Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check backend logs:
```bash
# Backend logs show in terminal where uvicorn is running
```

Check frontend logs:
```javascript
// Open browser console (F12) to see JavaScript errors
```

### 8.3 Performance Optimization

**For Large Policy Sets**:
- Increase similarity thresholds in redundancy_engine.py
- Limit graph nodes in pipeline.py
- Use pagination in frontend tables

**For Slow Analysis**:
- Cache parsed results
- Use multiprocessing for parallel analysis
- Optimize spaCy pipeline (disable unnecessary components)

---

## 9. Future Enhancements

### 9.1 Planned Features
- Real-time policy monitoring
- Advanced ML-based conflict detection
- Integration with compliance frameworks (SOC 2, ISO 27001)
- Policy version control integration
- Automated remediation suggestions
- Multi-language support
- Role-based access control
- Audit trail and change history

### 9.2 Scalability Improvements
- Database backend (PostgreSQL)
- Distributed processing (Celery)
- Caching layer (Redis)
- Load balancing
- Container orchestration (Kubernetes)

---

## 10. Support and Maintenance

### 10.1 Contact Information
- Project Repository: [GitHub Link]
- Documentation: [Docs Link]
- Issues: [Issues Link]

### 10.2 Maintenance Schedule
- Monthly dependency updates
- Quarterly model retraining
- Annual security audit
- Continuous integration testing

---

*Document Version: 1.0*
*Last Updated: July 12, 2026*
