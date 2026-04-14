# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Install: `pip install -r requirements.txt` (only dep: Flask)
- Run dev server: `python app.py` → http://127.0.0.1:5000 (debug mode, port 5000)
- No test suite, linter, or build step exists.

## Architecture

CareerMind is a symbolic / neuro-symbolic **expert system** — not an ML project. Three files form the pipeline:

1. **`rules.py`** — the knowledge base. `CAREER_RULES` is a list of dicts, each with `id`, `career`, `conditions` (list of fact strings, ANDed), `explanation`, and `weight`. Also exports `INTEREST_OPTIONS` and `SKILL_OPTIONS` (tuples of `(fact_key, label)`) that drive the form UI. Fact-key naming convention: `interest_*`, `skill_*`, plus derived academic facts (`high_math_score`, `high_science_score`, `high_overall_score`, `strong_stem_background`, `academic_excellence`).

2. **`inference.py`** — the forward-chaining engine.
   - `build_working_memory(interests, skills, academic)`: converts raw inputs into a `set` of boolean facts. Academic thresholds are hard-coded here (math/science ≥65, overall ≥70, STEM ≥80+80, excellence ≥85). Adding a new derived fact requires editing this function AND referencing it in rules.
   - `run_inference(wm)`: iterates every rule; fires when all conditions ⊆ working memory; aggregates per-career `score` (sum of fired rule weights), `rules_fired`, de-duplicated `explanations`.
   - Confidence: `confidence` shown in UI is **relative** (score ÷ top score × 100), so the top career is always 100%. `absolute_confidence` is score ÷ sum-of-all-rule-weights.

3. **`app.py`** — Flask routes. `GET/POST /` renders form/results; `POST /api/recommend` is the JSON API (see README for payload shape); `GET /about` shows architecture info. Input scores are clamped 0–100.

### Adding a new career rule
Append a dict to `CAREER_RULES` in `rules.py`. The `id` must be unique (convention: `R##`). Conditions must use fact keys already asserted by `build_working_memory` — if you need a new interest/skill, also add it to `INTEREST_OPTIONS` or `SKILL_OPTIONS` so the form offers it. Weights are typically 7–10; higher = stronger signal.

### Key invariant
Rule conditions are pure AND. There is no OR, NOT, or chaining of derived facts across rules — working memory is built once, then read-only during inference. Keep it that way unless intentionally extending the engine.

## UI editing convention
When updating UI components (HTML templates under `templates/`, user-visible labels, rendered strings), wrap the changed/updated text in bold (`<strong>` or `<b>` in HTML, `**...**` in markdown). Applies only to UI-facing text — do NOT bold code, Python logic, or comments.
