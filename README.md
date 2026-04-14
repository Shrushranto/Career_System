# CareerMind — Hybrid AI Career Recommendation Expert System

> A **hybrid neuro-symbolic expert system** built with Python & Flask.  
> Combines **forward-chaining rules**, **symbolic rules with numeric thresholds**, and a **NetworkX knowledge graph** to recommend careers with full, transparent explanations.

---

## Project Structure

```
career_system/
│
├── app.py                ← Flask web server & routes
├── rules.py              ← Knowledge base (66 IF-THEN rules + fact vocabulary)
├── inference.py          ← Hybrid fusion engine (forward chaining + graph + symbolic)
├── symbolic_rules.py     ← 38 neuro-symbolic rules with numeric thresholds
├── knowledge_graph.py    ← NetworkX directed graph (Interest → Skill → Career)
├── requirements.txt      ← Python dependencies
│
├── templates/
│   ├── index.html        ← Input form (grouped interests, skills, academic scores)
│   ├── results.html      ← Ranked recommendations + full score breakdown
│   └── about.html        ← System architecture explanation page
│
└── static/
    ├── style.css         ← UI design (Midnight Blueprint theme)
    └── theme.js          ← Dark / light mode toggle
```

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (comes with Python)

### Step 1 — Clone the repository
```bash
git clone https://github.com/Shrushranto/Career_System.git
cd Career_System
```

### Step 2 — (Optional) Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the application
```bash
python app.py
```

### Step 5 — Open in browser
```
http://127.0.0.1:5000
```

> **Environment variable:** Set `SECRET_KEY` for production deployments. The dev server uses a hardcoded fallback.

---

## Example Inputs and Outputs

### Example 1 — Data Scientist
| Field     | Value                                               |
|-----------|-----------------------------------------------------|
| Interests | Data Analysis, Coding / Programming                 |
| Skills    | Programming, Statistics / Math, Attention to Detail |
| Math      | 85% · Science: 70% · Overall: 78%                  |

**Output:**
```
Top Recommendation : Data Scientist
Confidence         : 100%
Final Score        : 1.0  (α=0.5 × Graph + β=0.5 × Rule)

Rules fired        : R03, R04, R46, R58  (classic forward-chaining)
Symbolic rules     : NS02, NS08          (neuro-symbolic layer)
Graph paths        : Data Analysis → skill_statistics → Data Scientist (0.81)

Also matched: Software Engineer (78%), AI/ML Engineer (38%)
```

---

### Example 2 — Medical Doctor
| Field     | Value                                           |
|-----------|-------------------------------------------------|
| Interests | Medicine / Healthcare                           |
| Skills    | Empathy / People Skills, Attention to Detail    |
| Science   | 88% · Overall: 80%                              |

**Output:**
```
Top Recommendation : Medical Doctor
Confidence         : 100%

Rules fired        : R16, R39, R53
Symbolic rules     : NS17, NS18
```

---

### Example 3 — Database Administrator
| Field     | Value                                              |
|-----------|----------------------------------------------------|
| Interests | Coding / Programming                               |
| Skills    | Programming, Attention to Detail, Problem Solving  |
| Subjects  | DBMS: 80%                                          |

**Output:**
```
Top Recommendation : Database Administrator
Confidence         : 83.5%

Rules fired        : R35, R55
Symbolic rules     : NS31
```

---

## AI Architecture: How It Works

```
USER INPUT
    │
    ▼
WORKING MEMORY BUILDER
(interests + skills → fact set; academic scores → derived facts)
    │
    ├────────────────────────────────────────┐
    ▼                                        ▼
LAYER 1                                  LAYER 2
Classic Forward Chaining                 Symbolic Rules
(66 IF-THEN rules in rules.py)           (38 rules in symbolic_rules.py)
Fires when all conditions ∈ WM           Blends boolean facts + numeric
Accumulates weighted scores              thresholds (e.g. Math ≥ 70)
    │                                        │
    └──────────────┬─────────────────────────┘
                   │
    ┌──────────────┘
    ▼
LAYER 3
Knowledge Graph Traversal
(NetworkX graph in knowledge_graph.py)
Multi-hop paths: Interest → Skill → Career
Path score = product of edge weights
    │
    ▼
FUSION
Final Score = α × Graph Score + β × Rule Score
             (α = β = 0.5)
Rule Score  = 0.5 × Classic (norm.) + 0.5 × Symbolic (norm.)
    │
    ▼
RANKED RECOMMENDATIONS
(sorted by Final Score, with full rule trace and explanations)
```

### Key Components
| Component            | Implementation                                               |
|----------------------|--------------------------------------------------------------|
| Knowledge Base       | `rules.py` — 66 structured IF-THEN rules (R01–R66)          |
| Symbolic Rules       | `symbolic_rules.py` — 38 rules with numeric thresholds      |
| Knowledge Graph      | `knowledge_graph.py` — NetworkX directed graph, 4 node types|
| Working Memory       | Python `set` of active boolean facts                         |
| Inference Engine     | Forward chaining in `inference.py`                           |
| Fusion               | Weighted combination of all three layer scores               |
| Explainability       | Rule IDs, explanation bullets, graph paths on results page   |
| Derived Facts        | Academic thresholds auto-assert `high_math_score` etc.       |

---

## JSON API

Call the inference engine programmatically:

```bash
curl -X POST http://127.0.0.1:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["interest_coding", "interest_data_analysis"],
    "skills": ["skill_programming", "skill_statistics"],
    "academic": {
      "math": 85,
      "science": 72,
      "overall": 80,
      "subjects": {"Data Structures": 88, "Statistics": 82}
    }
  }'
```

**Response shape:**
```json
{
  "top_career": {
    "career": "Data Scientist",
    "final_score": 1.0,
    "graph_score": 1.0,
    "rule_score": 1.0,
    "classic_score": 1.0,
    "ns_score": 1.0,
    "confidence": 100.0,
    "rules_fired": ["R03", "R04", "R46"],
    "triggered_ns_rules": [{"id": "NS02", "label": "...", "boost": 0.25}],
    "top_paths": [{"path": "Data Analysis → skill_statistics → Data Scientist", "score": 0.81}],
    "explanations": ["..."]
  },
  "recommendations": [...],
  "working_memory": ["high_math_score", "interest_coding", "interest_data_analysis", "..."],
  "total_rules_fired": 6,
  "alpha": 0.5,
  "beta": 0.5
}
```

---

## Possible Improvements

1. **Fuzzy Logic for Soft Conditions**  
   Replace binary facts with fuzzy membership values (e.g. "somewhat interested in coding" = 0.6). Use fuzzy inference to handle uncertainty and partial matches.

2. **Machine Learning for Rule Weights**  
   Train a model on historical career outcome data to assign data-driven weights, replacing hand-assigned values. Rules remain symbolic; weights become learned.

3. **Dynamic Knowledge Base from Ontology**  
   Represent the knowledge base as an OWL ontology (e.g. Protégé + owlready2). Enables class hierarchy reasoning and allows non-programmers to update rules via a UI.

4. **User Feedback Loop**  
   After showing recommendations, ask users to rate relevance. Store feedback and use it to reweight rules over time — a simple form of online learning.

5. **NLP-Based Input Processing**  
   Replace checkboxes with free-text input. Use spaCy or a transformer to extract facts from natural language, making the interface far more accessible.

---

## References

- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach*, 4th Ed.
- Hayes-Roth, F. (1985). *Rule-Based Systems*, CACM.
- Flask Documentation: https://flask.palletsprojects.com
- NetworkX Documentation: https://networkx.org
