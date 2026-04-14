"""
app.py — Flask Web Application Entry Point
==========================================
This is the main server file. It handles:
  - Serving the input form (GET /)
  - Processing form submissions (POST /)
  - Passing results to the results template
  - A JSON API endpoint (/api/recommend) for programmatic access

Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

import os

from flask import Flask, render_template, request, jsonify
from inference import get_recommendations
from rules import INTEREST_OPTIONS, SKILL_OPTIONS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "career_expert_system_dev_only")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ROUTE
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def index():
    """
    GET  → Render the input form with interest/skill options.
    POST → Collect form data, run inference, render results page.
    """
    if request.method == "GET":
        return render_template(
            "index.html",
            interests=INTEREST_OPTIONS,
            skills=SKILL_OPTIONS,
        )

    # ── Collect POST data ────────────────────────────────────────────────────
    selected_interests = request.form.getlist("interests")   # multi-select
    selected_skills    = request.form.getlist("skills")      # checkboxes

    # Academic scores — derived from dynamic subject sliders.
    # Each subject slider is submitted as name="subject:<category>:<subject name>"
    # where category ∈ {math, science, other}. We aggregate category averages
    # and treat the overall score as the mean across all submitted subjects.
    math_vals, science_vals, all_vals = [], [], []
    subjects_dict = {}
    for field, raw in request.form.items():
        if not field.startswith("subject:"):
            continue
        try:
            val = max(0, min(100, int(raw)))
        except ValueError:
            continue
        parts = field.split(":", 2)
        category = parts[1] if len(parts) >= 2 else "other"
        subject_name = parts[2] if len(parts) >= 3 else field
        subjects_dict[subject_name] = val
        all_vals.append(val)
        if category == "math":
            math_vals.append(val)
        elif category == "science":
            science_vals.append(val)

    def _avg(xs):
        return int(round(sum(xs) / len(xs))) if xs else 0

    math_score    = _avg(math_vals)
    science_score = _avg(science_vals)
    overall_score = _avg(all_vals)

    academic = {
        "math"   : math_score,
        "science": science_score,
        "overall": overall_score,
        "subjects": subjects_dict,
    }

    # ── Run the inference engine ─────────────────────────────────────────────
    result = get_recommendations(selected_interests, selected_skills, academic)

    # ── Build display labels for interests and skills ────────────────────────
    interest_map  = dict(INTEREST_OPTIONS)
    skill_map     = dict(SKILL_OPTIONS)
    interest_labels = [interest_map.get(i, i) for i in selected_interests]
    skill_labels    = [skill_map.get(s, s)    for s in selected_skills]

    # ── Prepare user profile summary ────────────────────────────────────────
    user_profile = {
        "interests"    : interest_labels,
        "skills"       : skill_labels,
        "math_score"   : math_score,
        "science_score": science_score,
        "overall_score": overall_score,
    }

    return render_template(
        "results.html",
        result       = result,
        user_profile = user_profile,
        top_n        = result["recommendations"][:5],
        all_recs     = result["recommendations"],
    )


# ─────────────────────────────────────────────────────────────────────────────
# JSON API  (bonus: lets developers call the engine programmatically)
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    """
    POST /api/recommend
    Body (JSON):
    {
      "interests": ["interest_coding", "interest_data_analysis"],
      "skills"   : ["skill_programming", "skill_statistics"],
      "academic" : {"math": 80, "science": 75, "overall": 78}
    }
    """
    data = request.get_json(force=True)

    interests = data.get("interests", [])
    skills    = data.get("skills",    [])
    academic  = data.get("academic",  {"math": 0, "science": 0, "overall": 0})

    result = get_recommendations(interests, skills, academic)
    return jsonify(result)


# ─────────────────────────────────────────────────────────────────────────────
# ABOUT PAGE
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/about")
def about():
    from rules import CAREER_RULES
    return render_template("about.html", rule_count=len(CAREER_RULES))


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  AI Career Recommendation Expert System")
    print("  Running at http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
