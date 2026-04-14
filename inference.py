"""
inference.py — Forward-Chaining Inference Engine
==================================================
This module implements the core AI reasoning component of the expert system.

HOW FORWARD CHAINING WORKS:
  1. User inputs are converted into FACTS and loaded into "Working Memory".
  2. The engine iterates through every rule in the knowledge base.
  3. If ALL conditions of a rule are satisfied by the current facts → rule FIRES.
  4. Fired rules contribute their career recommendation + explanation + weight.
  5. Multiple rules can fire for the same career; scores are accumulated.
  6. Results are sorted by score (descending) to produce a ranked recommendation list.

This makes the system EXPLAINABLE — we can trace exactly which rules fired and why.
"""

from rules import CAREER_RULES


# ─────────────────────────────────────────────────────────────────────────────
# WORKING MEMORY BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def build_working_memory(interests: list, skills: list, academic: dict) -> set:
    """
    Convert raw user inputs into a set of boolean facts (working memory).

    Parameters
    ----------
    interests : list of str  — selected interest fact-keys (e.g. 'interest_coding')
    skills    : list of str  — selected skill fact-keys  (e.g. 'skill_programming')
    academic  : dict         — {'math': int, 'science': int, 'overall': int}
                               scores are expected as percentages (0-100)

    Returns
    -------
    set of str — active facts for forward chaining
    """
    memory = set()

    # Assert interest facts
    for interest in interests:
        memory.add(interest)

    # Assert skill facts
    for skill in skills:
        memory.add(skill)

    # Assert academic performance facts using thresholds
    math_score    = academic.get("math", 0)
    science_score = academic.get("science", 0)
    overall_score = academic.get("overall", 0)

    # Threshold: ≥ 65 → "high" for that subject
    if math_score >= 65:
        memory.add("high_math_score")
    if science_score >= 65:
        memory.add("high_science_score")
    if overall_score >= 70:
        memory.add("high_overall_score")

    # Extra derived facts based on combined scores
    if math_score >= 80 and science_score >= 80:
        memory.add("strong_stem_background")
    if overall_score >= 85:
        memory.add("academic_excellence")

    # Per-subject facts (≥70 → high_<slug>_score).  Subjects originate from
    # the dynamic Academic Performance UI; the slug uses lowercase + underscore
    # so rules can reference `high_data_structures_score`, `high_dbms_score`,
    # `high_cryptography_score`, etc.
    import re
    subjects = academic.get("subjects", {}) or {}
    for name, score in subjects.items():
        try:
            score_i = int(score)
        except (TypeError, ValueError):
            continue
        if score_i >= 70:
            slug = re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")
            if slug:
                memory.add(f"high_{slug}_score")

    return memory


# ─────────────────────────────────────────────────────────────────────────────
# FORWARD CHAINING ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def run_inference(working_memory: set) -> list:
    """
    Execute forward chaining over the knowledge base.

    For each rule in CAREER_RULES:
      - Check if ALL rule conditions are present in working memory
      - If yes → rule fires; accumulate score and explanation for that career

    Parameters
    ----------
    working_memory : set of str — facts derived from user inputs

    Returns
    -------
    list of dict sorted by confidence score (descending):
      [
        {
          "career"      : str,
          "score"       : int,
          "confidence"  : float (0-100 %),
          "rules_fired" : list of rule IDs,
          "explanations": list of str,
        },
        ...
      ]
    """

    # career_data holds aggregated results per career
    career_data = {}

    for rule in CAREER_RULES:
        rule_id    = rule["id"]
        career     = rule["career"]
        conditions = rule["conditions"]
        weight     = rule["weight"]
        explanation = rule["explanation"]

        # ── CONDITION CHECK (AND logic) ───────────────────────────────────────
        matched_conditions = [c for c in conditions if c in working_memory]
        all_matched        = len(matched_conditions) == len(conditions)

        if all_matched:
            # Rule fires ✓
            if career not in career_data:
                career_data[career] = {
                    "career"      : career,
                    "score"       : 0,
                    "rules_fired" : [],
                    "explanations": [],
                }

            career_data[career]["score"]       += weight
            career_data[career]["rules_fired"].append(rule_id)
            # Extend explanations, avoiding duplicate bullet points
            for point in explanation:
                if point not in career_data[career]["explanations"]:
                    career_data[career]["explanations"].append(point)

    if not career_data:
        return []

    # ── NEURO-SYMBOLIC CONFIDENCE SCORING ────────────────────────────────────
    # Compute the theoretical maximum score: sum of weights of rules that
    # could have fired (only those whose career appeared at all).
    # We normalise each career's score against the global maximum to get
    # a meaningful confidence percentage.
    max_possible = sum(r["weight"] for r in CAREER_RULES)  # upper bound
    actual_max   = max(d["score"] for d in career_data.values())

    results = []
    for data in career_data.values():
        # Confidence = score as a fraction of the highest-scoring career × 100
        # This ensures the top career always shows ~100% relative confidence,
        # while others are proportionally ranked.
        relative_confidence = round((data["score"] / actual_max) * 100, 1)

        # Absolute confidence = fraction of theoretical max (shows raw strength)
        absolute_confidence = round((data["score"] / max_possible) * 100, 1)

        results.append({
            "career"             : data["career"],
            "score"              : data["score"],
            "confidence"         : relative_confidence,   # shown in UI
            "absolute_confidence": absolute_confidence,
            "rules_fired"        : data["rules_fired"],
            "explanations"       : data["explanations"],
            "rules_count"        : len(data["rules_fired"]),
        })

    # Sort: primary by score descending, secondary by number of rules fired
    results.sort(key=lambda x: (x["score"], x["rules_count"]), reverse=True)

    return results


# ─────────────────────────────────────────────────────────────────────────────
# CONVENIENCE WRAPPER
# ─────────────────────────────────────────────────────────────────────────────

def get_recommendations(interests: list, skills: list, academic: dict) -> dict:
    """
    High-level entry point called by app.py.

    Returns
    -------
    dict:
      {
        "working_memory"  : list  — active facts (for debug / transparency),
        "recommendations" : list  — ranked career recommendations,
        "top_career"      : dict | None,
        "total_rules_fired": int,
      }
    """
    wm      = build_working_memory(interests, skills, academic)
    results = run_inference(wm)

    return {
        "working_memory"   : sorted(list(wm)),
        "recommendations"  : results,
        "top_career"       : results[0] if results else None,
        "total_rules_fired": sum(r["rules_count"] for r in results),
    }
