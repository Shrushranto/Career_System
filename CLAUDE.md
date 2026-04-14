# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Install: `pip install -r requirements.txt`
- Run dev server: `python app.py` → http://127.0.0.1:5000 (debug mode, port 5000)
- Secret key: set `SECRET_KEY` env var for production; dev falls back to a hardcoded string.
- No test suite, linter, or build step exists.

## Architecture

CareerMind is a **hybrid neuro-symbolic expert system** — not an ML project. Five files form the pipeline:

1. **`rules.py`** — the knowledge base.
   - `CAREER_RULES`: list of dicts with `id`, `career`, `conditions` (ANDed fact strings), `explanation`, and `weight`. Currently R01–R66 (66 rules). Next rule ID: `R67`.
   - `INTEREST_OPTIONS`: tuples of `(fact_key, label)` — drives the interests chip grid.
   - `SKILL_OPTIONS`: 24 skills grouped into 5 categories (Technical, Analytical, Creative, People & Communication, Management). Every skill listed here must appear in at least one rule condition or graph edge — do not add dead skills.
   - Fact-key naming convention: `interest_*`, `skill_*`, plus derived academic facts (`high_math_score`, `high_science_score`, `high_overall_score`, `strong_stem_background`, `academic_excellence`, `high_<subject_slug>_score`).

2. **`inference.py`** — the hybrid fusion engine.
   - `build_working_memory(interests, skills, academic)`: converts raw inputs into a `set` of boolean facts. Academic thresholds: math/science ≥65, overall ≥70, STEM ≥80+80, excellence ≥85. Per-subject facts emitted as `high_<slug>_score` when subject score ≥70.
   - `run_inference(wm)`: classic forward-chaining over `CAREER_RULES`. Returns results sorted by score. Used internally by `get_recommendations`.
   - `get_recommendations(interests, skills, academic)`: high-level entry point. Runs all three layers, fuses scores, returns the full result dict.
   - **Fusion formula**: `Final = α × graph_score + β × rule_score` where `α = β = 0.5`. `rule_score = 0.5 × classic_norm + 0.5 × ns_norm` (consistent average — do NOT revert to the old conditional logic).
   - `absolute_confidence`: score ÷ max achievable score *for that career specifically* (not across all rules).
   - `confidence` in the UI is **relative** (score ÷ top career score × 100), so the top career is always 100%.

3. **`symbolic_rules.py`** — neuro-symbolic rules.
   - `NEURO_SYMBOLIC_RULES`: list of dicts with `id` (NS##), `career`, `condition` (lambda over working memory + academic dict), `boost` (float), `label`. Currently NS01–NS38. Next ID: `NS39`.
   - `run_symbolic_rules(wm, academic)`: evaluates all rules, returns per-career normalised scores and triggered rule lists.

4. **`knowledge_graph.py`** — NetworkX directed graph.
   - Four node types: Interest, Skill, Subject, Career. Each edge has `weight` [0,1] and `relation` ("requires" | "enhances" | "related_to").
   - Traversal up to 2 hops: active nodes → intermediate (skill/subject) → career. Path score = product of edge weights.
   - `score_careers_from_graph(wm)`: returns per-career normalised scores and top-3 paths.
   - Graph is built once on import (`_GRAPH` module-level singleton).

5. **`app.py`** — Flask routes.
   - `GET/POST /` — form and results. POST passes `result`, `user_profile`, `top_n` (top 5), and `all_recs` (full ranked list) to `results.html`.
   - `POST /api/recommend` — JSON API.
   - `GET /about` — architecture page.
   - Input scores clamped 0–100 server-side.

### Adding a new career rule
1. Append a dict to `CAREER_RULES` in `rules.py` with a unique `id` (next: `R67`). Weights typically 7–10.
2. All `conditions` must be fact keys already asserted by `build_working_memory`. If you need a new skill/interest, also add it to `SKILL_OPTIONS`/`INTEREST_OPTIONS` AND add at least one edge in `knowledge_graph.py`.
3. Optionally add a matching NS rule in `symbolic_rules.py` (next: `NS39`).

### Adding a new skill
Skills must be useful — every skill in `SKILL_OPTIONS` must appear in at least one `CAREER_RULES` condition AND have at least one edge in the knowledge graph. Adding a skill requires all three:
- Entry in `SKILL_OPTIONS` (with category comment)
- One or more rules in `CAREER_RULES` using it
- One or more `skill_career` edges in `knowledge_graph.py`

### Key invariant
Rule conditions are pure AND. There is no OR, NOT, or chaining of derived facts across rules — working memory is built once, then read-only during inference. Keep it that way unless intentionally extending the engine.

## UI editing convention
When updating UI components (HTML templates under `templates/`, user-visible labels, rendered strings), wrap the changed/updated text in bold (`<strong>` or `<b>` in HTML, `**...**` in markdown). Applies only to UI-facing text — do NOT bold code, Python logic, or comments.

## Skill grouping (index.html)
Skills are displayed in 5 labelled groups in the form. When adding a new skill, place its chip in the correct group in `templates/index.html` as well as `SKILL_OPTIONS` in `rules.py`:
- **Technical**: programming, logical thinking, problem solving, networking, mechanical aptitude, data visualization
- **Analytical**: analytical thinking, critical thinking, statistics, research, strategic thinking, attention to detail, decision making
- **Creative**: creativity, visual thinking, writing
- **People & Communication**: communication, empathy, public speaking, negotiation, emotional intelligence
- **Management**: leadership, project management, financial literacy
