# CareerMind — AI-Based Career Recommendation Expert System

> A **symbolic AI / expert system** built with Python & Flask.  
> Uses **forward-chaining inference** over **33 hand-crafted IF-THEN rules**  
> to recommend careers with full, transparent explanations.

---

## 📁 Project Structure

```
career_system/
│
├── app.py              ← Flask web server & routes
├── rules.py            ← Knowledge base (33 IF-THEN rules + fact vocabulary)
├── inference.py        ← Forward-chaining inference engine + scoring
├── requirements.txt    ← Python dependencies (just Flask)
│
├── templates/
│   ├── index.html      ← Input form (interests, skills, academic scores)
│   ├── results.html    ← Recommendation output + explanations
│   └── about.html      ← System architecture explanation page
│
└── static/
    └── style.css       ← Dark editorial UI design
```

---

## ⚙️ Setup Instructions (Step-by-Step)

### Prerequisites
- Python 3.8 or higher
- pip (comes with Python)

### Step 1 — Clone / Download the project
```bash
# If you have git:
git clone <your-repo-url>
cd career_system

# Or just extract the ZIP and cd into the folder
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

---

## 🎯 Example Inputs and Outputs

### Example 1 — Software Engineer
| Field     | Value                                           |
|-----------|-------------------------------------------------|
| Interests | Coding/Programming, Artificial Intelligence     |
| Skills    | Programming, Logical Thinking, Problem Solving  |
| Math      | 82%  · Science: 70%  · Overall: 78%            |

**Output:**
```
Recommended Career : Software Engineer
Confidence         : 100%  (score: 18, rules fired: R01, R02)
Rules Fired        : 2

Reasoning:
  ✔ You have a strong interest in coding
  ✔ You demonstrate logical thinking ability
  ✔ You are skilled at problem solving — core to software development
  ✔ Interest in coding combined with strong mathematics
  ✔ Mathematical ability is foundational for algorithms and data structures

Also matched: AI/ML Engineer (72%)
```

---

### Example 2 — Medical Doctor
| Field     | Value                                        |
|-----------|----------------------------------------------|
| Interests | Medicine/Healthcare, Biology                 |
| Skills    | Empathy, Communication, Analytical Thinking  |
| Science   | 88%  · Overall: 80%                          |

**Output:**
```
Recommended Career : Medical Doctor
Confidence         : 100%  (rules fired: R16)

Reasoning:
  ✔ Strong interest in medicine is the core motivator
  ✔ Empathy is critical for patient care and communication
  ✔ High science score reflects the rigorous academic demands of medicine
```

---

### Example 3 — Graphic Designer
| Field     | Value                                         |
|-----------|-----------------------------------------------|
| Interests | Design/Art, Writing/Journalism                |
| Skills    | Creativity, Visual/Spatial Thinking, Communication |
| Scores    | Math: 55%  ·  Science: 50%  ·  Overall: 65%  |

**Output:**
```
Recommended Career : Graphic Designer / UI-UX Designer
Confidence         : 100%  (rules fired: R25)
Also matched       : Content Writer / Journalist (90%)
```

---

## 🧠 AI Architecture: How It Works

```
USER INPUT
    │
    ▼
WORKING MEMORY BUILDER
(converts inputs → boolean facts)
    │
    ▼
FORWARD CHAINING ENGINE
    │
    ├─ For each rule in knowledge base:
    │      IF all conditions ∈ working_memory
    │      THEN rule fires → accumulate score + explanations
    │
    ▼
NEURO-SYMBOLIC SCORING
(sum of weights of fired rules → confidence %)
    │
    ▼
RANKED RECOMMENDATIONS
(sorted by score, with rule trace and explanations)
```

### Key AI Concepts Used
| Concept              | Implementation                                        |
|----------------------|-------------------------------------------------------|
| Knowledge Base       | `rules.py` — 33 structured IF-THEN rules             |
| Working Memory       | Python `set` of active boolean facts                  |
| Inference Engine     | Forward chaining in `inference.py`                    |
| Explainability       | Rule IDs + explanation bullets on results page        |
| Neuro-Symbolic Layer | Weighted rule accumulation → confidence percentage    |
| Derived Facts        | Academic thresholds auto-assert `high_math_score` etc.|

---

## 🎓 5 Viva Questions & Answers

### Q1. What is an expert system, and how is this project one?
**A:** An expert system is an AI program that emulates the decision-making ability of a human expert in a specific domain. It consists of a **knowledge base** (domain rules), a **working memory** (current facts), and an **inference engine** (reasoning mechanism). This project is an expert system because it encodes career counselling expertise as 33 IF-THEN rules in `rules.py`, stores user inputs as facts in working memory, and uses a forward-chaining inference engine in `inference.py` to derive career recommendations — just as a human career counsellor would reason from known facts.

---

### Q2. What is forward chaining and why did you choose it over backward chaining?
**A:** In **forward chaining** (data-driven), we start from known facts and apply rules to derive new conclusions. In **backward chaining** (goal-driven), we start from a goal and work backwards to find supporting facts.

Forward chaining was chosen here because:
- We don't know the goal (career) in advance — we want to *discover* the best match
- We have all the facts (user inputs) available upfront
- It naturally produces *all* matching careers ranked by score, rather than validating a single hypothesis

Forward chaining is used in production expert systems like CLIPS and Drools.

---

### Q3. How does your system explain its recommendations? Why is this important?
**A:** Every recommendation is explained using:
1. **Rule IDs** (e.g. R01, R02) — tracing exactly which rules fired
2. **Explanation bullets** — human-readable justifications stored in each rule
3. **Working memory display** — showing every active fact used

Explainability is critical in AI because:
- Users need to **trust** the system's output
- In high-stakes domains like career guidance, a black-box answer is unacceptable
- It satisfies the principle of **Explainable AI (XAI)**, which is now a regulatory requirement in many domains (e.g. GDPR Article 22)

---

### Q4. What makes this a "neuro-symbolic" system?
**A:** The system is **symbolic** at its core (rule-based logic, IF-THEN reasoning, explicit knowledge representation). The **neuro** aspect is the **weighted scoring layer**:

- Each rule has a `weight` (e.g. 8, 9, or 10) reflecting its importance
- When multiple rules fire for the same career, their weights **accumulate**
- A **confidence percentage** is computed relative to the highest-scoring career

This mimics how neural networks assign confidence scores to outputs, while the underlying reasoning remains fully interpretable. This hybrid approach is called **neuro-symbolic AI**.

---

### Q5. What are the limitations of your current system and how could it be improved?
**A:** Current limitations:
1. **Binary conditions** — a user either has a skill or doesn't; there's no degree of confidence in inputs
2. **Static knowledge base** — rules must be manually updated to add new careers or facts
3. **No learning** — the system doesn't improve from user interactions
4. **Independence assumption** — rules don't model interactions between facts beyond AND logic

Improvements (see section below for detailed list).

---

## 🚀 5 Possible Improvements

1. **Fuzzy Logic for Soft Conditions**  
   Replace binary facts with fuzzy membership values (e.g. "somewhat interested in coding" = 0.6). Use fuzzy inference to handle uncertainty and partial matches, making recommendations more nuanced.

2. **Machine Learning Hybrid (True Neuro-Symbolic)**  
   Train a small ML model (e.g. Random Forest) on historical career outcome data to assign data-driven weights to rules, replacing the hand-assigned weights. The rules remain symbolic; the weights become learned.

3. **Dynamic Knowledge Base from Ontology**  
   Represent the knowledge base as an OWL ontology (e.g. using Protégé + owlready2). This enables reasoning over class hierarchies (e.g. "Software Engineer IS-A Technology Career") and allows non-programmers to update rules via a UI.

4. **User Feedback Loop**  
   After showing recommendations, ask users to rate their relevance. Store feedback in a database and use it to reweight rules over time — a simple form of online learning.

5. **NLP-Based Input Processing**  
   Replace checkboxes with a free-text input field ("Describe your interests and skills"). Use spaCy or a transformer model to extract facts from natural language, making the interface far more accessible and realistic.

---

## 📡 JSON API (Bonus)

You can also call the inference engine programmatically:

```bash
curl -X POST http://127.0.0.1:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["interest_coding", "interest_data_analysis"],
    "skills": ["skill_programming", "skill_statistics", "skill_logical_thinking"],
    "academic": {"math": 85, "science": 72, "overall": 80}
  }'
```

**Response:**
```json
{
  "top_career": {
    "career": "Data Scientist",
    "score": 19,
    "confidence": 100.0,
    "rules_fired": ["R03", "R04"],
    "explanations": ["..."]
  },
  "recommendations": [...],
  "working_memory": ["high_math_score", "interest_coding", ...],
  "total_rules_fired": 4
}
```

---

## 📚 References

- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach*, 4th Ed.
- Hayes-Roth, F. (1985). *Rule-Based Systems*, CACM.
- Gonzalez Fernandez — Rule-Based System (GitHub inspiration)
- Flask Documentation: https://flask.palletsprojects.com
