"""
inference.py — Hybrid Reasoning Engine
========================================
Combines three complementary reasoning layers:

  1. Classic forward-chaining  (rules.py → CAREER_RULES)
     Boolean IF-THEN rules over working memory facts.
     Produces a per-career Classic Rule Score.

  2. Neuro-Symbolic rules       (symbolic_rules.py → NEURO_SYMBOLIC_RULES)
     Explicit IF-THEN rules that blend boolean facts with numeric thresholds.
     Produces a per-career NS Score.

  3. Knowledge Graph traversal  (knowledge_graph.py)
     Multi-hop paths through an Interest/Skill/Subject/Career graph.
     Produces a per-career Graph Score.

Fusion formula
--------------
  Rule Score   = 0.5 × Classic Score (norm.) + 0.5 × NS Score (norm.)
  Final Score  = α × Graph Score + β × Rule Score
                 α = 0.5,  β = 0.5

All component scores are normalised to [0, 1] before fusion.
The top career always shows 100 % relative confidence.
"""

import re

from rules import CAREER_RULES
from knowledge_graph import score_careers_from_graph
from symbolic_rules import run_symbolic_rules

# Fusion weights (must sum to 1)
ALPHA = 0.5   # knowledge-graph contribution
BETA  = 0.5   # rule-based contribution


# ─────────────────────────────────────────────────────────────────────────────
# WORKING MEMORY BUILDER  (unchanged from original)
# ─────────────────────────────────────────────────────────────────────────────

def build_working_memory(interests: list, skills: list, academic: dict) -> set:
    """
    Convert raw user inputs into a set of boolean facts (working memory).

    Parameters
    ----------
    interests : list of str  — selected interest fact-keys (e.g. 'interest_coding')
    skills    : list of str  — selected skill fact-keys  (e.g. 'skill_programming')
    academic  : dict         — {'math': int, 'science': int, 'overall': int,
                                'subjects': {name: score}}
                               Scores are expected as percentages (0-100).
    """
    memory = set()

    for interest in interests:
        memory.add(interest)
    for skill in skills:
        memory.add(skill)

    math_score    = academic.get("math",    0)
    science_score = academic.get("science", 0)
    overall_score = academic.get("overall", 0)

    if math_score    >= 65: memory.add("high_math_score")
    if science_score >= 65: memory.add("high_science_score")
    if overall_score >= 70: memory.add("high_overall_score")

    if math_score >= 80 and science_score >= 80:
        memory.add("strong_stem_background")
    if overall_score >= 85:
        memory.add("academic_excellence")

    # Per-subject facts  (≥70 → high_<slug>_score)
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
# CLASSIC FORWARD-CHAINING  (unchanged logic, used as one score component)
# ─────────────────────────────────────────────────────────────────────────────

def run_inference(working_memory: set) -> list:
    """
    Execute forward chaining over CAREER_RULES.
    Returns a list of career dicts sorted by score (descending).
    This is kept as a standalone function for backwards compatibility
    and is called internally by get_recommendations.
    """
    career_data: dict = {}

    for rule in CAREER_RULES:
        if all(c in working_memory for c in rule["conditions"]):
            career = rule["career"]
            if career not in career_data:
                career_data[career] = {
                    "career": career, "score": 0,
                    "rules_fired": [], "explanations": [],
                }
            career_data[career]["score"]       += rule["weight"]
            career_data[career]["rules_fired"].append(rule["id"])
            for point in rule["explanation"]:
                if point not in career_data[career]["explanations"]:
                    career_data[career]["explanations"].append(point)

    if not career_data:
        return []

    actual_max = max(d["score"] for d in career_data.values())
    # absolute_confidence: score as % of the highest theoretically achievable
    # score for that specific career (sum of weights of rules that target it).
    career_max_possible: dict[str, int] = {}
    for r in CAREER_RULES:
        career_max_possible[r["career"]] = career_max_possible.get(r["career"], 0) + r["weight"]

    results = []
    for data in career_data.values():
        max_for_career = career_max_possible.get(data["career"], 1)
        results.append({
            **data,
            "confidence"         : round(data["score"] / actual_max * 100, 1),
            "absolute_confidence": round(data["score"] / max_for_career * 100, 1),
            "rules_count"        : len(data["rules_fired"]),
        })

    results.sort(key=lambda x: (x["score"], x["rules_count"]), reverse=True)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# HYBRID FUSION ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def get_recommendations(interests: list, skills: list, academic: dict) -> dict:
    """
    High-level entry point called by app.py.

    Runs all three reasoning layers and fuses their scores.

    Returns
    -------
    dict:
      {
        "working_memory"    : list  — active facts (for transparency),
        "recommendations"   : list  — ranked career recommendations,
        "top_career"        : dict | None,
        "total_rules_fired" : int,
        "alpha"             : float — graph weight used in fusion,
        "beta"              : float — rule weight used in fusion,
      }

    Each recommendation dict contains:
      career, final_score, graph_score, rule_score, classic_score, ns_score,
      confidence (relative %), score (0–100 display int),
      explanations, rules_fired, triggered_ns_rules, top_paths, rules_count
    """
    wm = build_working_memory(interests, skills, academic)

    # ── Layer 1: Classic forward-chaining ────────────────────────────────
    classic_results = run_inference(wm)
    classic_by_career = {r["career"]: r for r in classic_results}
    classic_max = max((r["score"] for r in classic_results), default=1)

    # ── Layer 2: Neuro-symbolic rules ────────────────────────────────────
    ns_results = run_symbolic_rules(wm, academic)

    # ── Layer 3: Knowledge graph traversal ───────────────────────────────
    graph_results = score_careers_from_graph(wm)

    # ── Fusion ───────────────────────────────────────────────────────────
    all_careers = (
        set(classic_by_career.keys())
        | set(ns_results.keys())
        | set(graph_results.keys())
    )

    fused = []
    for career in all_careers:
        # Classic score normalised to [0, 1]
        if career in classic_by_career and classic_max > 0:
            classic_norm = round(classic_by_career[career]["score"] / classic_max, 4)
        else:
            classic_norm = 0.0

        # NS score (already normalised in symbolic_rules.py)
        ns_norm = ns_results[career]["normalized_score"] if career in ns_results else 0.0

        # Combined rule score: fixed 50/50 average of both normalised signals.
        # Using a consistent formula regardless of which layers fired prevents the
        # old bug where dual-layer agreement scored the same as single-layer evidence.
        rule_score = round(0.5 * classic_norm + 0.5 * ns_norm, 4)

        # Graph score (already normalised in knowledge_graph.py)
        graph_score = (
            graph_results[career]["normalized_score"] if career in graph_results else 0.0
        )

        # Final fused score
        final_score = round(ALPHA * graph_score + BETA * rule_score, 4)

        # Explainability data
        explanations  = classic_by_career[career]["explanations"]  if career in classic_by_career else []
        rules_fired   = classic_by_career[career]["rules_fired"]   if career in classic_by_career else []
        ns_rules      = ns_results[career]["triggered_rules"]      if career in ns_results       else []
        top_paths     = graph_results[career]["top_paths"]         if career in graph_results    else []

        fused.append({
            "career"           : career,
            "final_score"      : final_score,
            "graph_score"      : round(graph_score, 4),
            "rule_score"       : round(rule_score,  4),
            "classic_score"    : round(classic_norm, 4),
            "ns_score"         : round(ns_norm,      4),
            "explanations"     : explanations,
            "rules_fired"      : rules_fired,
            "triggered_ns_rules": ns_rules,
            "top_paths"        : top_paths,
            "rules_count"      : len(rules_fired),
        })

    # Sort by final score descending
    fused.sort(key=lambda x: x["final_score"], reverse=True)

    # Add relative confidence and integer display score
    top_final = fused[0]["final_score"] if fused else 1.0
    for rec in fused:
        rec["confidence"] = round(rec["final_score"] / top_final * 100, 1) if top_final > 0 else 0.0
        rec["score"]      = round(rec["final_score"] * 100)  # 0–100 display int

    return {
        "working_memory"    : sorted(list(wm)),
        "recommendations"   : fused,
        "top_career"        : fused[0] if fused else None,
        "total_rules_fired" : sum(r["rules_count"] for r in fused),
        "alpha"             : ALPHA,
        "beta"              : BETA,
    }
