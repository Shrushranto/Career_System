"""
symbolic_rules.py — Neuro-Symbolic Rule Engine
================================================
Defines explicit IF-THEN rules that combine boolean facts from working memory
with numeric academic scores.  These rules are:

  - Modular    : each rule is a standalone dict; add/remove without side-effects
  - Interpretable: the "label" field describes exactly what triggered it
  - Deterministic: same inputs always produce the same output

Each triggered rule contributes a "boost" (float) to that career's Rule Score.
All scores are normalized to [0, 1] before being handed to the fusion step.

Rule Score (career) = sum of boosts from triggered rules for that career
                      ÷ global maximum sum across all careers
"""

# ─────────────────────────────────────────────────────────────────────────────
# RULE DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
# Each entry:
#   id        : unique identifier (NS##)
#   career    : target career string (must match CAREER_RULES career names)
#   condition : callable(working_memory: set, academic: dict) -> bool
#   boost     : float — score contribution when rule fires
#   label     : human-readable description for explainability output

NEURO_SYMBOLIC_RULES = [

    # ── Software / Technology ─────────────────────────────────────────────
    {
        "id": "NS01",
        "career": "Software Engineer",
        "condition": lambda wm, ac: "interest_coding" in wm and ac.get("math", 0) >= 70,
        "boost": 0.25,
        "label": "Coding interest + Math ≥ 70 → strong Software Engineer signal",
    },
    {
        "id": "NS02",
        "career": "Data Scientist",
        "condition": lambda wm, ac: "interest_data_analysis" in wm and ac.get("math", 0) >= 70,
        "boost": 0.25,
        "label": "Data Analysis interest + Math ≥ 70 → strong Data Scientist signal",
    },
    {
        "id": "NS03",
        "career": "AI / Machine Learning Engineer",
        "condition": lambda wm, ac: "interest_artificial_intelligence" in wm and ac.get("math", 0) >= 70,
        "boost": 0.30,
        "label": "AI interest + Math ≥ 70 → very strong AI/ML Engineer signal",
    },
    {
        "id": "NS04",
        "career": "AI / Machine Learning Engineer",
        "condition": lambda wm, ac: (
            "interest_artificial_intelligence" in wm
            and "skill_statistics" in wm
            and "skill_programming" in wm
        ),
        "boost": 0.20,
        "label": "AI interest + Statistics + Programming → triple AI/ML Engineer signal",
    },
    {
        "id": "NS05",
        "career": "Cybersecurity Analyst",
        "condition": lambda wm, ac: "interest_cybersecurity" in wm and "skill_networking" in wm,
        "boost": 0.25,
        "label": "Cybersecurity interest + Networking skill → direct Cybersecurity Analyst match",
    },
    {
        "id": "NS06",
        "career": "Web Developer",
        "condition": lambda wm, ac: "interest_web_development" in wm and "skill_programming" in wm,
        "boost": 0.25,
        "label": "Web Development interest + Programming skill → direct Web Developer match",
    },
    {
        "id": "NS07",
        "career": "Cloud / DevOps Engineer",
        "condition": lambda wm, ac: (
            "interest_coding" in wm
            and "skill_networking" in wm
            and "skill_problem_solving" in wm
        ),
        "boost": 0.20,
        "label": "Coding + Networking + Problem Solving → Cloud/DevOps Engineer signal",
    },
    {
        "id": "NS08",
        "career": "Data Scientist",
        "condition": lambda wm, ac: (
            "skill_statistics" in wm
            and "skill_programming" in wm
            and ac.get("overall", 0) >= 80
        ),
        "boost": 0.15,
        "label": "Statistics + Programming skills + Overall ≥ 80 → Data Scientist excellence bonus",
    },

    # ── Design / Creative ─────────────────────────────────────────────────
    {
        "id": "NS09",
        "career": "Graphic Designer / UI-UX Designer",
        "condition": lambda wm, ac: "interest_design" in wm and "skill_creativity" in wm,
        "boost": 0.25,
        "label": "Design interest + Creativity skill → strong UI/UX Designer signal",
    },
    {
        "id": "NS10",
        "career": "Architect",
        "condition": lambda wm, ac: "interest_design" in wm and ac.get("math", 0) >= 65,
        "boost": 0.20,
        "label": "Design interest + Math ≥ 65 → Architect aptitude signal",
    },
    {
        "id": "NS11",
        "career": "Game Developer",
        "condition": lambda wm, ac: "interest_gaming" in wm and "skill_programming" in wm,
        "boost": 0.25,
        "label": "Gaming interest + Programming skill → Game Developer signal",
    },
    {
        "id": "NS12",
        "career": "Content Writer / Journalist",
        "condition": lambda wm, ac: "interest_writing" in wm and "skill_communication" in wm,
        "boost": 0.25,
        "label": "Writing interest + Communication skill → Content Writer/Journalist signal",
    },
    {
        "id": "NS13",
        "career": "Marketing Specialist",
        "condition": lambda wm, ac: "interest_marketing" in wm and "skill_creativity" in wm,
        "boost": 0.25,
        "label": "Marketing interest + Creativity skill → Marketing Specialist signal",
    },

    # ── Finance / Business ────────────────────────────────────────────────
    {
        "id": "NS14",
        "career": "Financial Analyst",
        "condition": lambda wm, ac: "interest_finance" in wm and ac.get("math", 0) >= 70,
        "boost": 0.30,
        "label": "Finance interest + Math ≥ 70 → strong Financial Analyst signal",
    },
    {
        "id": "NS15",
        "career": "Business Analyst",
        "condition": lambda wm, ac: "interest_business" in wm and "skill_analytical_thinking" in wm,
        "boost": 0.20,
        "label": "Business interest + Analytical Thinking → Business Analyst signal",
    },
    {
        "id": "NS16",
        "career": "Entrepreneur",
        "condition": lambda wm, ac: (
            "interest_business" in wm
            and "skill_leadership" in wm
            and "skill_creativity" in wm
        ),
        "boost": 0.25,
        "label": "Business interest + Leadership + Creativity → Entrepreneur signal",
    },

    # ── Medicine / Health ─────────────────────────────────────────────────
    {
        "id": "NS17",
        "career": "Medical Doctor",
        "condition": lambda wm, ac: "interest_medicine" in wm and ac.get("science", 0) >= 70,
        "boost": 0.30,
        "label": "Medicine interest + Science ≥ 70 → strong Medical Doctor signal",
    },
    {
        "id": "NS18",
        "career": "Pharmacist",
        "condition": lambda wm, ac: "interest_medicine" in wm and ac.get("science", 0) >= 65,
        "boost": 0.20,
        "label": "Medicine interest + Science ≥ 65 → Pharmacist signal",
    },
    {
        "id": "NS19",
        "career": "Psychologist / Counselor",
        "condition": lambda wm, ac: "interest_psychology" in wm and "skill_empathy" in wm,
        "boost": 0.25,
        "label": "Psychology interest + Empathy skill → Psychologist/Counselor signal",
    },

    # ── Engineering / Sciences ────────────────────────────────────────────
    {
        "id": "NS20",
        "career": "Research Scientist",
        "condition": lambda wm, ac: "interest_science" in wm and ac.get("science", 0) >= 70,
        "boost": 0.30,
        "label": "Science interest + Science score ≥ 70 → Research Scientist signal",
    },
    {
        "id": "NS21",
        "career": "Mechanical Engineer",
        "condition": lambda wm, ac: "interest_engineering" in wm and ac.get("math", 0) >= 65,
        "boost": 0.20,
        "label": "Engineering interest + Math ≥ 65 → Mechanical Engineer signal",
    },
    {
        "id": "NS22",
        "career": "Electronics / Embedded Systems Engineer",
        "condition": lambda wm, ac: "interest_electronics" in wm and ac.get("math", 0) >= 65,
        "boost": 0.20,
        "label": "Electronics interest + Math ≥ 65 → Embedded Systems Engineer signal",
    },
    {
        "id": "NS23",
        "career": "Robotics Engineer",
        "condition": lambda wm, ac: "interest_electronics" in wm and "skill_programming" in wm,
        "boost": 0.25,
        "label": "Electronics interest + Programming skill → Robotics Engineer signal",
    },
    {
        "id": "NS24",
        "career": "Environmental Scientist",
        "condition": lambda wm, ac: "interest_environment" in wm and ac.get("science", 0) >= 65,
        "boost": 0.25,
        "label": "Environment interest + Science ≥ 65 → Environmental Scientist signal",
    },
    {
        "id": "NS25",
        "career": "Biomedical Engineer",
        "condition": lambda wm, ac: "interest_biology" in wm and "interest_engineering" in wm,
        "boost": 0.25,
        "label": "Biology + Engineering interests → Biomedical Engineer signal",
    },

    # ── Education / Social / Law ──────────────────────────────────────────
    {
        "id": "NS26",
        "career": "Teacher / Educator",
        "condition": lambda wm, ac: "interest_education" in wm and "skill_communication" in wm,
        "boost": 0.25,
        "label": "Education interest + Communication skill → Teacher/Educator signal",
    },
    {
        "id": "NS27",
        "career": "Social Worker",
        "condition": lambda wm, ac: "interest_social_work" in wm and "skill_empathy" in wm,
        "boost": 0.25,
        "label": "Social Work interest + Empathy skill → Social Worker signal",
    },
    {
        "id": "NS28",
        "career": "Lawyer",
        "condition": lambda wm, ac: (
            "interest_law" in wm
            and "skill_communication" in wm
            and "skill_analytical_thinking" in wm
        ),
        "boost": 0.25,
        "label": "Law interest + Communication + Analytical Thinking → Lawyer signal",
    },
    {
        "id": "NS29",
        "career": "Human Resources Manager",
        "condition": lambda wm, ac: (
            "interest_business" in wm
            and "skill_empathy" in wm
            and "skill_communication" in wm
        ),
        "boost": 0.20,
        "label": "Business interest + Empathy + Communication → HR Manager signal",
    },
    {
        "id": "NS30",
        "career": "Project Manager",
        "condition": lambda wm, ac: (
            "skill_project_management" in wm
            and "skill_leadership" in wm
            and "skill_communication" in wm
        ),
        "boost": 0.25,
        "label": "Project Management + Leadership + Communication → Project Manager signal",
    },

    # ── Newly wired skills ────────────────────────────────────────────────
    {
        "id": "NS31",
        "career": "Database Administrator",
        "condition": lambda wm, ac: (
            "interest_coding" in wm
            and "skill_attention_to_detail" in wm
            and "skill_problem_solving" in wm
        ),
        "boost": 0.20,
        "label": "Coding + Attention to Detail + Problem Solving → Database Administrator signal",
    },
    {
        "id": "NS32",
        "career": "Mechanical Engineer",
        "condition": lambda wm, ac: "interest_engineering" in wm and "skill_mechanical_aptitude" in wm,
        "boost": 0.25,
        "label": "Engineering interest + Mechanical Aptitude → Mechanical Engineer signal",
    },
    {
        "id": "NS33",
        "career": "Robotics Engineer",
        "condition": lambda wm, ac: (
            "interest_electronics" in wm
            and "skill_mechanical_aptitude" in wm
            and "skill_programming" in wm
        ),
        "boost": 0.25,
        "label": "Electronics + Mechanical Aptitude + Programming → Robotics Engineer signal",
    },
    {
        "id": "NS34",
        "career": "Research Scientist",
        "condition": lambda wm, ac: "interest_science" in wm and "skill_research" in wm,
        "boost": 0.25,
        "label": "Science interest + Research skill → Research Scientist signal",
    },
    {
        "id": "NS35",
        "career": "Content Writer / Journalist",
        "condition": lambda wm, ac: "interest_writing" in wm and "skill_writing" in wm,
        "boost": 0.20,
        "label": "Writing interest + Writing skill → Content Writer/Journalist signal",
    },
    {
        "id": "NS36",
        "career": "Lawyer",
        "condition": lambda wm, ac: (
            "interest_law" in wm
            and "skill_critical_thinking" in wm
            and "skill_communication" in wm
        ),
        "boost": 0.25,
        "label": "Law interest + Critical Thinking + Communication → Lawyer signal",
    },
    {
        "id": "NS37",
        "career": "Teacher / Educator",
        "condition": lambda wm, ac: "interest_education" in wm and "skill_emotional_intelligence" in wm,
        "boost": 0.20,
        "label": "Education interest + Emotional Intelligence → Teacher/Educator signal",
    },
    {
        "id": "NS38",
        "career": "Entrepreneur",
        "condition": lambda wm, ac: (
            "interest_business" in wm
            and "skill_strategic_thinking" in wm
            and "skill_leadership" in wm
        ),
        "boost": 0.25,
        "label": "Business interest + Strategic Thinking + Leadership → Entrepreneur signal",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def run_symbolic_rules(working_memory: set, academic: dict) -> dict:
    """
    Evaluate all neuro-symbolic rules and return per-career scores.

    Parameters
    ----------
    working_memory : set of str  — active boolean facts
    academic       : dict        — {"math": int, "science": int, "overall": int, ...}

    Returns
    -------
    dict keyed by career name:
      {
        "raw_score"       : float,
        "normalized_score": float [0, 1],
        "triggered_rules" : [{"id": str, "label": str, "boost": float}]
      }
    """
    results: dict = {}

    for rule in NEURO_SYMBOLIC_RULES:
        try:
            fired = rule["condition"](working_memory, academic)
        except Exception:
            fired = False

        if fired:
            career = rule["career"]
            if career not in results:
                results[career] = {"raw_score": 0.0, "triggered_rules": []}
            results[career]["raw_score"] += rule["boost"]
            results[career]["triggered_rules"].append({
                "id"   : rule["id"],
                "label": rule["label"],
                "boost": rule["boost"],
            })

    # Normalize to [0, 1]
    max_raw = max((v["raw_score"] for v in results.values()), default=1.0)
    for data in results.values():
        data["normalized_score"] = round(data["raw_score"] / max_raw, 4) if max_raw > 0 else 0.0

    return results
