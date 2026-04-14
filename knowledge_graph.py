"""
knowledge_graph.py — NetworkX Knowledge Graph for Career Reasoning
===================================================================
Constructs a directed weighted graph with four node types:

  Interest  — e.g. "interest_coding"          (from user selections)
  Skill     — e.g. "skill_programming"         (from user selections)
  Subject   — e.g. "Mathematics"               (from academic slider names)
  Career    — e.g. "Software Engineer"         (recommendation targets)

Every edge carries:
  weight   : float [0, 1] — strength of the relationship
  relation : str          — "requires" | "related_to" | "enhances"

Graph scoring pipeline
----------------------
1. Identify active nodes: interests/skills in working memory + subject nodes
   that map to high_<slug>_score facts.
2. Traverse multi-hop paths (up to 2 hops) from active nodes to Career nodes.
3. Path score = product of edge weights along the path.
4. Career graph score = sum of all valid path scores reaching that career.
5. Normalize all scores to [0, 1].
"""

from itertools import chain
import networkx as nx

# ─────────────────────────────────────────────────────────────────────────────
# GRAPH CONSTRUCTION
# ─────────────────────────────────────────────────────────────────────────────

def build_career_graph() -> nx.DiGraph:
    """Build and return the career knowledge graph (call once; cache the result)."""
    G = nx.DiGraph()

    # ── Interest → Skill edges ────────────────────────────────────────────
    interest_skill = [
        ("interest_coding",                    "skill_programming",         0.9, "requires"),
        ("interest_coding",                    "skill_logical_thinking",    0.8, "enhances"),
        ("interest_coding",                    "skill_problem_solving",     0.8, "enhances"),
        ("interest_data_analysis",             "skill_statistics",          0.9, "requires"),
        ("interest_data_analysis",             "skill_analytical_thinking", 0.8, "requires"),
        ("interest_data_analysis",             "skill_programming",         0.6, "enhances"),
        ("interest_artificial_intelligence",   "skill_programming",         0.8, "requires"),
        ("interest_artificial_intelligence",   "skill_statistics",          0.8, "requires"),
        ("interest_artificial_intelligence",   "skill_logical_thinking",    0.7, "enhances"),
        ("interest_cybersecurity",             "skill_networking",          0.9, "requires"),
        ("interest_cybersecurity",             "skill_problem_solving",     0.8, "requires"),
        ("interest_cybersecurity",             "skill_logical_thinking",    0.7, "enhances"),
        ("interest_cybersecurity",             "skill_programming",         0.6, "enhances"),
        ("interest_web_development",           "skill_programming",         0.8, "requires"),
        ("interest_web_development",           "skill_creativity",          0.7, "enhances"),
        ("interest_engineering",               "skill_problem_solving",     0.9, "requires"),
        ("interest_engineering",               "skill_analytical_thinking", 0.7, "enhances"),
        ("interest_electronics",               "skill_logical_thinking",    0.8, "enhances"),
        ("interest_electronics",               "skill_programming",         0.6, "enhances"),
        ("interest_design",                    "skill_creativity",          0.9, "requires"),
        ("interest_design",                    "skill_visual_thinking",     0.9, "requires"),
        ("interest_business",                  "skill_communication",       0.7, "enhances"),
        ("interest_business",                  "skill_leadership",          0.7, "enhances"),
        ("interest_business",                  "skill_analytical_thinking", 0.6, "enhances"),
        ("interest_finance",                   "skill_analytical_thinking", 0.8, "requires"),
        ("interest_finance",                   "skill_statistics",          0.6, "enhances"),
        ("interest_marketing",                 "skill_creativity",          0.7, "enhances"),
        ("interest_marketing",                 "skill_communication",       0.8, "requires"),
        ("interest_writing",                   "skill_communication",       0.9, "requires"),
        ("interest_writing",                   "skill_creativity",          0.7, "enhances"),
        ("interest_education",                 "skill_communication",       0.9, "requires"),
        ("interest_education",                 "skill_empathy",             0.8, "requires"),
        ("interest_social_work",               "skill_empathy",             0.9, "requires"),
        ("interest_social_work",               "skill_communication",       0.8, "requires"),
        ("interest_law",                       "skill_analytical_thinking", 0.8, "requires"),
        ("interest_law",                       "skill_communication",       0.8, "requires"),
        ("interest_gaming",                    "skill_creativity",          0.7, "enhances"),
        ("interest_gaming",                    "skill_programming",         0.8, "requires"),
        ("interest_psychology",                "skill_empathy",             0.9, "requires"),
        ("interest_psychology",                "skill_communication",       0.7, "enhances"),
        ("interest_medicine",                  "skill_empathy",             0.8, "requires"),
        ("interest_medicine",                  "skill_analytical_thinking", 0.6, "enhances"),
        ("interest_science",                   "skill_analytical_thinking", 0.8, "requires"),
        ("interest_biology",                   "skill_analytical_thinking", 0.7, "enhances"),
        ("interest_environment",               "skill_analytical_thinking", 0.7, "enhances"),
    ]

    # ── Subject → Skill edges ─────────────────────────────────────────────
    subject_skill = [
        ("Mathematics",      "skill_logical_thinking",    0.8, "enhances"),
        ("Mathematics",      "skill_analytical_thinking", 0.8, "enhances"),
        ("Mathematics",      "skill_statistics",          0.7, "related_to"),
        ("Physics",          "skill_problem_solving",     0.8, "enhances"),
        ("Physics",          "skill_analytical_thinking", 0.7, "enhances"),
        ("Statistics",       "skill_statistics",          0.95,"related_to"),
        ("Statistics",       "skill_analytical_thinking", 0.7, "enhances"),
        ("Computer Science", "skill_programming",         0.9, "requires"),
        ("Computer Science", "skill_logical_thinking",    0.8, "enhances"),
        ("Biology",          "skill_analytical_thinking", 0.7, "enhances"),
        ("Chemistry",        "skill_analytical_thinking", 0.7, "enhances"),
        ("Economics",        "skill_analytical_thinking", 0.7, "enhances"),
        ("Economics",        "skill_statistics",          0.6, "enhances"),
        ("Psychology",       "skill_empathy",             0.7, "enhances"),
        ("Design",           "skill_creativity",          0.8, "enhances"),
        ("Design",           "skill_visual_thinking",     0.9, "requires"),
        ("English",          "skill_communication",       0.8, "enhances"),
        ("Law",              "skill_analytical_thinking", 0.8, "enhances"),
        ("Law",              "skill_communication",       0.7, "enhances"),
    ]

    # ── Skill → Career edges ──────────────────────────────────────────────
    skill_career = [
        ("skill_programming",         "Software Engineer",                      0.9, "requires"),
        ("skill_programming",         "Data Scientist",                         0.7, "requires"),
        ("skill_programming",         "AI / Machine Learning Engineer",         0.9, "requires"),
        ("skill_programming",         "Web Developer",                          0.9, "requires"),
        ("skill_programming",         "Game Developer",                         0.8, "requires"),
        ("skill_programming",         "Cybersecurity Analyst",                  0.6, "enhances"),
        ("skill_programming",         "Cloud / DevOps Engineer",                0.7, "requires"),
        ("skill_programming",         "Robotics Engineer",                      0.7, "requires"),
        ("skill_programming",         "Database Administrator",                 0.65, "requires"),
        ("skill_logical_thinking",    "Software Engineer",                      0.8, "enhances"),
        ("skill_logical_thinking",    "Electronics / Embedded Systems Engineer",0.7, "enhances"),
        ("skill_logical_thinking",    "Cybersecurity Analyst",                  0.7, "enhances"),
        ("skill_problem_solving",     "Mechanical Engineer",                    0.8, "requires"),
        ("skill_problem_solving",     "Software Engineer",                      0.7, "enhances"),
        ("skill_problem_solving",     "Cloud / DevOps Engineer",                0.7, "enhances"),
        ("skill_problem_solving",     "Cybersecurity Analyst",                  0.8, "requires"),
        ("skill_problem_solving",     "Robotics Engineer",                      0.8, "requires"),
        ("skill_analytical_thinking", "Data Scientist",                         0.8, "requires"),
        ("skill_analytical_thinking", "Financial Analyst",                      0.9, "requires"),
        ("skill_analytical_thinking", "Business Analyst",                       0.8, "requires"),
        ("skill_analytical_thinking", "Research Scientist",                     0.8, "requires"),
        ("skill_analytical_thinking", "Environmental Scientist",                0.7, "requires"),
        ("skill_analytical_thinking", "Lawyer",                                 0.7, "requires"),
        ("skill_analytical_thinking", "Pharmacist",                             0.7, "requires"),
        ("skill_statistics",          "Data Scientist",                         0.9, "requires"),
        ("skill_statistics",          "AI / Machine Learning Engineer",         0.8, "requires"),
        ("skill_statistics",          "Financial Analyst",                      0.7, "enhances"),
        ("skill_statistics",          "Research Scientist",                     0.6, "enhances"),
        ("skill_creativity",          "Graphic Designer / UI-UX Designer",      0.9, "requires"),
        ("skill_creativity",          "Web Developer",                          0.7, "enhances"),
        ("skill_creativity",          "Content Writer / Journalist",            0.7, "enhances"),
        ("skill_creativity",          "Entrepreneur",                           0.8, "requires"),
        ("skill_creativity",          "Marketing Specialist",                   0.7, "enhances"),
        ("skill_creativity",          "Game Developer",                         0.8, "requires"),
        ("skill_creativity",          "Architect",                              0.8, "requires"),
        ("skill_communication",       "Teacher / Educator",                     0.9, "requires"),
        ("skill_communication",       "Social Worker",                          0.8, "requires"),
        ("skill_communication",       "Business Analyst",                       0.7, "enhances"),
        ("skill_communication",       "Marketing Specialist",                   0.8, "requires"),
        ("skill_communication",       "Lawyer",                                 0.8, "requires"),
        ("skill_communication",       "Psychologist / Counselor",               0.8, "requires"),
        ("skill_communication",       "Human Resources Manager",                0.8, "requires"),
        ("skill_communication",       "Project Manager",                        0.8, "requires"),
        ("skill_communication",       "Content Writer / Journalist",            0.8, "requires"),
        ("skill_empathy",             "Medical Doctor",                         0.9, "requires"),
        ("skill_empathy",             "Psychologist / Counselor",               0.9, "requires"),
        ("skill_empathy",             "Social Worker",                          0.9, "requires"),
        ("skill_empathy",             "Teacher / Educator",                     0.7, "enhances"),
        ("skill_empathy",             "Human Resources Manager",                0.8, "requires"),
        ("skill_leadership",          "Entrepreneur",                           0.9, "requires"),
        ("skill_leadership",          "Project Manager",                        0.8, "requires"),
        ("skill_leadership",          "Human Resources Manager",                0.7, "enhances"),
        ("skill_networking",          "Cybersecurity Analyst",                  0.8, "requires"),
        ("skill_networking",          "Cloud / DevOps Engineer",                0.8, "requires"),
        ("skill_visual_thinking",     "Graphic Designer / UI-UX Designer",      0.9, "requires"),
        ("skill_visual_thinking",     "Architect",                              0.7, "enhances"),
        ("skill_project_management",  "Civil Engineer",                         0.7, "enhances"),
        ("skill_project_management",  "Project Manager",                        0.9, "requires"),
        # ── Newly wired skills ────────────────────────────────────────────
        ("skill_research",            "Research Scientist",                     0.85, "requires"),
        ("skill_research",            "Environmental Scientist",                0.70, "enhances"),
        ("skill_writing",             "Content Writer / Journalist",            0.90, "requires"),
        ("skill_critical_thinking",   "Lawyer",                                 0.80, "requires"),
        ("skill_critical_thinking",   "Research Scientist",                     0.60, "enhances"),
        ("skill_critical_thinking",   "Data Scientist",                         0.55, "enhances"),
        ("skill_attention_to_detail", "Medical Doctor",                         0.75, "requires"),
        ("skill_attention_to_detail", "Financial Analyst",                      0.70, "enhances"),
        ("skill_attention_to_detail", "Database Administrator",                 0.75, "requires"),
        ("skill_mechanical_aptitude", "Mechanical Engineer",                    0.90, "requires"),
        ("skill_mechanical_aptitude", "Robotics Engineer",                      0.75, "enhances"),
        ("skill_data_visualization",  "Data Scientist",                         0.80, "requires"),
        ("skill_data_visualization",  "Financial Analyst",                      0.60, "enhances"),
        ("skill_strategic_thinking",  "Business Analyst",                       0.75, "enhances"),
        ("skill_strategic_thinking",  "Entrepreneur",                           0.80, "requires"),
        ("skill_emotional_intelligence", "Human Resources Manager",             0.85, "requires"),
        ("skill_emotional_intelligence", "Social Worker",                       0.75, "enhances"),
        ("skill_emotional_intelligence", "Teacher / Educator",                  0.70, "enhances"),
        ("skill_public_speaking",     "Teacher / Educator",                     0.80, "requires"),
        ("skill_public_speaking",     "Lawyer",                                 0.70, "enhances"),
        ("skill_public_speaking",     "Marketing Specialist",                   0.70, "enhances"),
        ("skill_decision_making",     "Project Manager",                        0.75, "enhances"),
        ("skill_decision_making",     "Entrepreneur",                           0.70, "enhances"),
        ("skill_negotiation",         "Lawyer",                                 0.65, "enhances"),
        ("skill_negotiation",         "Entrepreneur",                           0.60, "enhances"),
        ("skill_financial_literacy",  "Financial Analyst",                      0.65, "enhances"),
    ]

    # ── Interest → Career direct edges ────────────────────────────────────
    interest_career = [
        ("interest_coding",                  "Software Engineer",                      0.80, "related_to"),
        ("interest_coding",                  "Cloud / DevOps Engineer",                0.60, "related_to"),
        ("interest_data_analysis",           "Data Scientist",                         0.90, "related_to"),
        ("interest_artificial_intelligence", "AI / Machine Learning Engineer",         0.95, "related_to"),
        ("interest_cybersecurity",           "Cybersecurity Analyst",                  0.95, "related_to"),
        ("interest_web_development",         "Web Developer",                          0.90, "related_to"),
        ("interest_engineering",             "Mechanical Engineer",                    0.75, "related_to"),
        ("interest_engineering",             "Civil Engineer",                         0.75, "related_to"),
        ("interest_engineering",             "Robotics Engineer",                      0.60, "related_to"),
        ("interest_electronics",             "Electronics / Embedded Systems Engineer",0.90, "related_to"),
        ("interest_electronics",             "Robotics Engineer",                      0.70, "related_to"),
        ("interest_biology",                 "Biomedical Engineer",                    0.70, "related_to"),
        ("interest_biology",                 "Research Scientist",                     0.60, "related_to"),
        ("interest_science",                 "Research Scientist",                     0.90, "related_to"),
        ("interest_science",                 "Environmental Scientist",                0.60, "related_to"),
        ("interest_medicine",                "Medical Doctor",                         0.90, "related_to"),
        ("interest_medicine",                "Pharmacist",                             0.80, "related_to"),
        ("interest_medicine",                "Biomedical Engineer",                    0.50, "related_to"),
        ("interest_psychology",              "Psychologist / Counselor",               0.95, "related_to"),
        ("interest_business",                "Business Analyst",                       0.70, "related_to"),
        ("interest_business",                "Entrepreneur",                           0.75, "related_to"),
        ("interest_business",                "Human Resources Manager",                0.70, "related_to"),
        ("interest_finance",                 "Financial Analyst",                      0.95, "related_to"),
        ("interest_marketing",               "Marketing Specialist",                   0.95, "related_to"),
        ("interest_design",                  "Graphic Designer / UI-UX Designer",      0.90, "related_to"),
        ("interest_design",                  "Architect",                              0.70, "related_to"),
        ("interest_writing",                 "Content Writer / Journalist",            0.95, "related_to"),
        ("interest_education",               "Teacher / Educator",                     0.95, "related_to"),
        ("interest_social_work",             "Social Worker",                          0.95, "related_to"),
        ("interest_law",                     "Lawyer",                                 0.95, "related_to"),
        ("interest_gaming",                  "Game Developer",                         0.90, "related_to"),
        ("interest_environment",             "Environmental Scientist",                0.90, "related_to"),
        ("interest_coding",                  "Database Administrator",                 0.55, "related_to"),
    ]

    # ── Subject → Career direct edges ─────────────────────────────────────
    subject_career = [
        ("Mathematics",      "Financial Analyst",                   0.70, "related_to"),
        ("Mathematics",      "Software Engineer",                   0.65, "related_to"),
        ("Mathematics",      "Data Scientist",                      0.60, "related_to"),
        ("Statistics",       "Data Scientist",                      0.80, "related_to"),
        ("Statistics",       "Financial Analyst",                   0.70, "related_to"),
        ("Computer Science", "Software Engineer",                   0.90, "related_to"),
        ("Computer Science", "AI / Machine Learning Engineer",      0.70, "related_to"),
        ("Computer Science", "Database Administrator",              0.65, "related_to"),
        ("Biology",          "Medical Doctor",                      0.70, "related_to"),
        ("Biology",          "Biomedical Engineer",                 0.70, "related_to"),
        ("Biology",          "Research Scientist",                  0.60, "related_to"),
        ("Economics",        "Financial Analyst",                   0.75, "related_to"),
        ("Economics",        "Business Analyst",                    0.60, "related_to"),
        ("Psychology",       "Psychologist / Counselor",            0.80, "related_to"),
        ("Design",           "Graphic Designer / UI-UX Designer",   0.90, "related_to"),
        ("English",          "Content Writer / Journalist",         0.80, "related_to"),
        ("Law",              "Lawyer",                              0.90, "related_to"),
    ]

    # Assign node types and add all edges
    def _node_type(name: str) -> str:
        if name.startswith("interest_"):
            return "interest"
        if name.startswith("skill_"):
            return "skill"
        # If not interest/skill, determine by context (added as career or subject below)
        return "unknown"

    for src, dst, w, rel in chain(
        interest_skill, subject_skill,
        skill_career, interest_career, subject_career,
    ):
        # Determine node types
        src_type = _node_type(src)
        if src_type == "unknown":
            src_type = "subject"  # non-interest/skill source = subject

        if dst.startswith("skill_"):
            dst_type = "skill"
        else:
            # Destination is either a skill (handled above) or career
            # For subject_career and interest_career edges, dst is career
            dst_type = "skill" if dst.startswith("skill_") else "career"

        G.add_node(src, node_type=src_type)
        G.add_node(dst, node_type=dst_type)
        G.add_edge(src, dst, weight=w, relation=rel)

    return G


# Module-level singleton — graph is built once on import
_GRAPH: nx.DiGraph | None = None


def get_graph() -> nx.DiGraph:
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = build_career_graph()
    return _GRAPH


# ─────────────────────────────────────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────────────────────────────────────

def score_careers_from_graph(working_memory: set) -> dict:
    """
    Score careers via multi-hop traversal of the knowledge graph.

    Traversal patterns (up to 2 hops):
      - 1-hop : active_node → Career
      - 2-hop : active_node → Skill/Subject → Career

    Path score = product of edge weights.
    Career score = sum of all path scores.

    Returns
    -------
    dict keyed by career name:
      {
        "raw_score"       : float,
        "normalized_score": float [0, 1],
        "top_paths"       : list of {"path": str, "score": float}  (top 3 by score)
      }
    """
    G = get_graph()

    # Build set of active graph nodes from working memory
    active_nodes: set[str] = set()

    # Direct fact nodes (interest_* and skill_*)
    for fact in working_memory:
        if G.has_node(fact):
            active_nodes.add(fact)

    # Subject nodes: map high_<slug>_score → Subject node by slug matching
    subject_nodes = {
        n: n.lower().replace(" ", "_")
        for n, d in G.nodes(data=True)
        if d.get("node_type") == "subject"
    }
    for fact in working_memory:
        if fact.startswith("high_") and fact.endswith("_score"):
            inner = fact[5:-6]  # strip "high_" and "_score"
            for node, slug in subject_nodes.items():
                if slug == inner:
                    active_nodes.add(node)
                    break

    career_scores: dict[str, dict] = {}

    for start in active_nodes:
        # 1-hop: start → career
        for nbr in G.successors(start):
            if G.nodes[nbr].get("node_type") == "career":
                w = G[start][nbr]["weight"]
                _record_path(career_scores, nbr, w, f"{_label(start)} → {nbr}")

        # 2-hop: start → intermediate → career
        for mid in G.successors(start):
            mid_type = G.nodes[mid].get("node_type")
            if mid_type in ("skill", "subject"):
                w1 = G[start][mid]["weight"]
                for nbr in G.successors(mid):
                    if G.nodes[nbr].get("node_type") == "career":
                        w2 = G[mid][nbr]["weight"]
                        path_score = round(w1 * w2, 4)
                        path_label = f"{_label(start)} → {_label(mid)} → {nbr}"
                        _record_path(career_scores, nbr, path_score, path_label)

    # Normalize and pick top-3 paths per career
    max_raw = max((v["raw_score"] for v in career_scores.values()), default=1.0)
    for career, data in career_scores.items():
        data["normalized_score"] = round(data["raw_score"] / max_raw, 4) if max_raw > 0 else 0.0
        data["top_paths"] = sorted(data["_paths"], key=lambda p: p["score"], reverse=True)[:3]
        del data["_paths"]

    return career_scores


def _record_path(store: dict, career: str, score: float, label: str) -> None:
    if career not in store:
        store[career] = {"raw_score": 0.0, "_paths": []}
    store[career]["raw_score"] += score
    store[career]["_paths"].append({"path": label, "score": score})


def _label(node_key: str) -> str:
    """Human-readable label for a node key used in path display strings."""
    if node_key.startswith("interest_"):
        return node_key[9:].replace("_", " ").title()
    if node_key.startswith("skill_"):
        return node_key[6:].replace("_", " ").title()
    return node_key
