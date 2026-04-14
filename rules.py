"""
rules.py — Knowledge Base for the Career Recommendation Expert System
=======================================================================
This module defines the knowledge base as a structured list of IF-THEN rules.
Each rule contains:
  - conditions : list of facts that must ALL be true (AND logic)
  - career     : the career being recommended
  - explanation: human-readable reasons for this recommendation
  - weight     : confidence contribution (used in neuro-symbolic scoring)

The inference engine (inference.py) matches working memory against these rules
via forward chaining to produce ranked, explainable career recommendations.
"""

CAREER_RULES = [

    # ─────────────────────────────────────────────
    # SOFTWARE / TECHNOLOGY
    # ─────────────────────────────────────────────
    {
        "id": "R01",
        "career": "Software Engineer",
        "conditions": ["interest_coding", "skill_logical_thinking", "skill_problem_solving"],
        "explanation": [
            "You have a strong interest in coding",
            "You demonstrate logical thinking ability",
            "You are skilled at problem solving — core to software development",
        ],
        "weight": 10,
    },
    {
        "id": "R02",
        "career": "Software Engineer",
        "conditions": ["interest_coding", "high_math_score"],
        "explanation": [
            "Interest in coding combined with strong mathematics",
            "Mathematical ability is foundational for algorithms and data structures",
        ],
        "weight": 8,
    },
    {
        "id": "R03",
        "career": "Data Scientist",
        "conditions": ["interest_data_analysis", "skill_statistics", "high_math_score"],
        "explanation": [
            "Interest in data analysis aligns directly with data science",
            "Statistical knowledge is the backbone of data science",
            "Strong mathematics enables advanced modeling",
        ],
        "weight": 10,
    },
    {
        "id": "R04",
        "career": "Data Scientist",
        "conditions": ["interest_data_analysis", "skill_programming", "skill_statistics"],
        "explanation": [
            "Programming skills allow you to manipulate and process large datasets",
            "Statistical reasoning is essential for deriving insights",
            "Interest in data matches the core of this role",
        ],
        "weight": 9,
    },
    {
        "id": "R05",
        "career": "AI / Machine Learning Engineer",
        "conditions": ["interest_artificial_intelligence", "skill_programming", "high_math_score"],
        "explanation": [
            "Passion for AI is the primary driver for this career",
            "Programming is required to build and deploy ML models",
            "High math score indicates readiness for linear algebra and calculus-heavy work",
        ],
        "weight": 10,
    },
    {
        "id": "R06",
        "career": "AI / Machine Learning Engineer",
        "conditions": ["interest_artificial_intelligence", "skill_statistics", "skill_logical_thinking"],
        "explanation": [
            "AI/ML requires statistical foundations for model evaluation",
            "Logical thinking helps in designing intelligent systems",
            "Interest in AI is well matched to this path",
        ],
        "weight": 9,
    },
    {
        "id": "R07",
        "career": "Cybersecurity Analyst",
        "conditions": ["interest_cybersecurity", "skill_networking", "skill_problem_solving"],
        "explanation": [
            "Interest in cybersecurity is the defining factor",
            "Networking knowledge is essential for understanding attack surfaces",
            "Problem-solving skills help in incident response and threat analysis",
        ],
        "weight": 10,
    },
    {
        "id": "R08",
        "career": "Cybersecurity Analyst",
        "conditions": ["interest_cybersecurity", "skill_logical_thinking", "skill_programming"],
        "explanation": [
            "Logical thinking assists in reverse engineering and forensics",
            "Programming enables writing security tools and scripts",
            "Cybersecurity passion drives excellence in this field",
        ],
        "weight": 8,
    },
    {
        "id": "R09",
        "career": "Web Developer",
        "conditions": ["interest_web_development", "skill_creativity", "skill_programming"],
        "explanation": [
            "Web development interest directly matches the role",
            "Creativity is valuable for building engaging user interfaces",
            "Programming skills are the technical foundation",
        ],
        "weight": 10,
    },
    {
        "id": "R10",
        "career": "Cloud / DevOps Engineer",
        "conditions": ["interest_coding", "skill_networking", "skill_problem_solving"],
        "explanation": [
            "Coding interest supports infrastructure-as-code practices",
            "Networking knowledge is critical for cloud architecture",
            "Problem-solving is central to DevOps workflows",
        ],
        "weight": 8,
    },

    # ─────────────────────────────────────────────
    # ENGINEERING & SCIENCES
    # ─────────────────────────────────────────────
    {
        "id": "R11",
        "career": "Mechanical Engineer",
        "conditions": ["interest_engineering", "skill_problem_solving", "high_math_score"],
        "explanation": [
            "Engineering interest aligns with mechanical design and analysis",
            "Problem-solving is core to engineering challenges",
            "Strong math enables thermodynamics, mechanics, and design calculations",
        ],
        "weight": 10,
    },
    {
        "id": "R12",
        "career": "Civil Engineer",
        "conditions": ["interest_engineering", "skill_project_management", "high_math_score"],
        "explanation": [
            "Engineering passion supports structural and infrastructure work",
            "Project management skills are critical in construction projects",
            "Mathematics underpins structural analysis and design",
        ],
        "weight": 9,
    },
    {
        "id": "R13",
        "career": "Electronics / Embedded Systems Engineer",
        "conditions": ["interest_electronics", "skill_logical_thinking", "high_math_score"],
        "explanation": [
            "Interest in electronics directly maps to this career",
            "Logical thinking supports circuit design and debugging",
            "Mathematics is required for signal processing and control systems",
        ],
        "weight": 10,
    },
    {
        "id": "R14",
        "career": "Biomedical Engineer",
        "conditions": ["interest_biology", "interest_engineering", "high_science_score"],
        "explanation": [
            "Biology interest combined with engineering mindset defines biomedical engineering",
            "Strong science score demonstrates the required scientific foundation",
        ],
        "weight": 9,
    },
    {
        "id": "R15",
        "career": "Research Scientist",
        "conditions": ["interest_science", "skill_analytical_thinking", "high_science_score"],
        "explanation": [
            "Scientific curiosity is the primary trait of a researcher",
            "Analytical thinking drives hypothesis formation and data interpretation",
            "High science score confirms academic aptitude for research",
        ],
        "weight": 10,
    },

    # ─────────────────────────────────────────────
    # MEDICINE & HEALTH
    # ─────────────────────────────────────────────
    {
        "id": "R16",
        "career": "Medical Doctor",
        "conditions": ["interest_medicine", "skill_empathy", "high_science_score"],
        "explanation": [
            "Strong interest in medicine is the core motivator",
            "Empathy is critical for patient care and communication",
            "High science score reflects the rigorous academic demands of medicine",
        ],
        "weight": 10,
    },
    {
        "id": "R17",
        "career": "Pharmacist",
        "conditions": ["interest_medicine", "skill_analytical_thinking", "high_science_score"],
        "explanation": [
            "Interest in medicine drives pharmaceutical knowledge",
            "Analytical thinking supports drug interaction analysis",
            "Strong science fundamentals are required for pharmacy studies",
        ],
        "weight": 8,
    },
    {
        "id": "R18",
        "career": "Psychologist / Counselor",
        "conditions": ["interest_psychology", "skill_empathy", "skill_communication"],
        "explanation": [
            "Interest in psychology is essential for understanding human behavior",
            "Empathy allows meaningful connection with clients",
            "Communication skills are necessary for effective therapy",
        ],
        "weight": 10,
    },

    # ─────────────────────────────────────────────
    # BUSINESS & MANAGEMENT
    # ─────────────────────────────────────────────
    {
        "id": "R19",
        "career": "Business Analyst",
        "conditions": ["interest_business", "skill_analytical_thinking", "skill_communication"],
        "explanation": [
            "Business interest provides the domain context",
            "Analytical thinking is needed to evaluate processes and data",
            "Communication skills enable presenting findings to stakeholders",
        ],
        "weight": 10,
    },
    {
        "id": "R20",
        "career": "Entrepreneur",
        "conditions": ["interest_business", "skill_creativity", "skill_leadership"],
        "explanation": [
            "Business interest motivates venture creation",
            "Creativity drives innovation and product ideas",
            "Leadership is essential for building and guiding a team",
        ],
        "weight": 9,
    },
    {
        "id": "R21",
        "career": "Financial Analyst",
        "conditions": ["interest_finance", "high_math_score", "skill_analytical_thinking"],
        "explanation": [
            "Interest in finance aligns with market and investment analysis",
            "Strong mathematics supports financial modelling",
            "Analytical thinking is key for evaluating financial data",
        ],
        "weight": 10,
    },
    {
        "id": "R22",
        "career": "Human Resources Manager",
        "conditions": ["interest_business", "skill_empathy", "skill_communication"],
        "explanation": [
            "Business orientation supports organizational understanding",
            "Empathy is core to managing people and resolving conflicts",
            "Communication skills are fundamental in HR functions",
        ],
        "weight": 8,
    },
    {
        "id": "R23",
        "career": "Marketing Specialist",
        "conditions": ["interest_marketing", "skill_creativity", "skill_communication"],
        "explanation": [
            "Marketing interest drives brand and campaign thinking",
            "Creativity enables compelling content and strategy",
            "Communication is at the heart of marketing outreach",
        ],
        "weight": 10,
    },
    {
        "id": "R24",
        "career": "Project Manager",
        "conditions": ["skill_project_management", "skill_leadership", "skill_communication"],
        "explanation": [
            "Project management skills are directly applicable",
            "Leadership ensures team coordination and motivation",
            "Communication skills keep all stakeholders aligned",
        ],
        "weight": 9,
    },

    # ─────────────────────────────────────────────
    # CREATIVE & ARTS
    # ─────────────────────────────────────────────
    {
        "id": "R25",
        "career": "Graphic Designer / UI-UX Designer",
        "conditions": ["interest_design", "skill_creativity", "skill_visual_thinking"],
        "explanation": [
            "Design interest is the core driver for this creative career",
            "Creativity is essential for producing original visual work",
            "Visual thinking enables intuitive and effective design solutions",
        ],
        "weight": 10,
    },
    {
        "id": "R26",
        "career": "Content Writer / Journalist",
        "conditions": ["interest_writing", "skill_communication", "skill_creativity"],
        "explanation": [
            "Passion for writing is the primary qualification",
            "Communication skill ensures clarity and audience engagement",
            "Creativity differentiates compelling content from average writing",
        ],
        "weight": 10,
    },
    {
        "id": "R27",
        "career": "Architect",
        "conditions": ["interest_design", "skill_creativity", "high_math_score"],
        "explanation": [
            "Design interest applies directly to spatial and structural design",
            "Creativity is fundamental to architectural innovation",
            "Mathematics supports structural analysis and blueprint calculations",
        ],
        "weight": 9,
    },

    # ─────────────────────────────────────────────
    # EDUCATION & SOCIAL
    # ─────────────────────────────────────────────
    {
        "id": "R28",
        "career": "Teacher / Educator",
        "conditions": ["interest_education", "skill_communication", "skill_empathy"],
        "explanation": [
            "Interest in education reflects a passion for teaching and mentoring",
            "Communication skills are fundamental to effective instruction",
            "Empathy enables understanding and supporting diverse learners",
        ],
        "weight": 10,
    },
    {
        "id": "R29",
        "career": "Social Worker",
        "conditions": ["interest_social_work", "skill_empathy", "skill_communication"],
        "explanation": [
            "Interest in social work reflects genuine concern for community welfare",
            "Empathy is the most critical trait for this profession",
            "Communication skills help navigate complex family and social situations",
        ],
        "weight": 10,
    },
    {
        "id": "R30",
        "career": "Lawyer",
        "conditions": ["interest_law", "skill_analytical_thinking", "skill_communication"],
        "explanation": [
            "Interest in law and justice is the foundation",
            "Analytical thinking enables case research and argument construction",
            "Strong communication is essential for oral and written advocacy",
        ],
        "weight": 10,
    },

    # ─────────────────────────────────────────────
    # BONUS / CROSS-DOMAIN RULES
    # ─────────────────────────────────────────────
    {
        "id": "R31",
        "career": "Game Developer",
        "conditions": ["interest_gaming", "skill_programming", "skill_creativity"],
        "explanation": [
            "Passion for gaming drives motivation in this highly competitive field",
            "Programming is the technical backbone of game development",
            "Creativity enables world-building, mechanics, and storytelling",
        ],
        "weight": 10,
    },
    {
        "id": "R32",
        "career": "Robotics Engineer",
        "conditions": ["interest_electronics", "skill_programming", "skill_problem_solving"],
        "explanation": [
            "Electronics interest underpins hardware knowledge in robotics",
            "Programming enables control systems and autonomous behaviour",
            "Problem-solving is required for complex mechatronics challenges",
        ],
        "weight": 9,
    },
    {
        "id": "R33",
        "career": "Environmental Scientist",
        "conditions": ["interest_environment", "skill_analytical_thinking", "high_science_score"],
        "explanation": [
            "Environmental interest aligns with ecological research and conservation",
            "Analytical thinking supports environmental impact assessments",
            "Strong science background provides the necessary academic foundation",
        ],
        "weight": 10,
    },

    # ─────────────────────────────────────────────
    # SUBJECT-LEVEL RULES
    # These fire on per-subject facts emitted by build_working_memory when
    # a subject slider is ≥ 70.  Fact format: high_<subject_slug>_score.
    # Subject slugs come from the dynamic UI (e.g. "Data Structures" →
    # high_data_structures_score).  Keep weights modest (6–8) — subject
    # facts complement, rather than replace, the primary interest+skill rules.
    # ─────────────────────────────────────────────
    {
        "id": "R34",
        "career": "Software Engineer",
        "conditions": ["interest_coding", "high_data_structures_score", "high_algorithms_score"],
        "explanation": [
            "Strong performance in Data Structures and Algorithms",
            "These are the core academic foundations of software engineering",
        ],
        "weight": 8,
    },
    {
        "id": "R35",
        "career": "Database Administrator",
        "conditions": ["interest_coding", "high_dbms_score"],
        "explanation": [
            "Strong DBMS grades indicate database design and query expertise",
            "Interest in coding complements the administrative and scripting side",
        ],
        "weight": 8,
    },
    {
        "id": "R36",
        "career": "Cybersecurity Analyst",
        "conditions": ["interest_cybersecurity", "high_cryptography_score", "high_network_security_score"],
        "explanation": [
            "High marks in Cryptography and Network Security",
            "These academic strengths map directly onto cyber defence work",
        ],
        "weight": 8,
    },
    {
        "id": "R37",
        "career": "Financial Analyst",
        "conditions": ["interest_finance", "high_economics_score", "high_statistics_score"],
        "explanation": [
            "Strong Economics grounding supports market and policy analysis",
            "Statistics enables rigorous financial modelling and forecasting",
        ],
        "weight": 8,
    },
    {
        "id": "R38",
        "career": "Electronics / Embedded Systems Engineer",
        "conditions": ["interest_electronics", "high_circuits_score", "high_electronics_score"],
        "explanation": [
            "Strong Circuits and Electronics marks signal hands-on hardware aptitude",
            "These subjects are the direct academic basis of embedded systems work",
        ],
        "weight": 8,
    },
    {
        "id": "R39",
        "career": "Medical Doctor",
        "conditions": ["interest_medicine", "high_human_anatomy_score", "high_biology_score"],
        "explanation": [
            "Excellent Human Anatomy and Biology grades indicate medical readiness",
            "These are the foundational pre-clinical subjects for doctors",
        ],
        "weight": 8,
    },
    {
        "id": "R40",
        "career": "Lawyer",
        "conditions": ["interest_law", "high_legal_studies_score", "high_political_science_score"],
        "explanation": [
            "High Legal Studies grades reflect doctrinal understanding",
            "Political Science strengthens grasp of constitutional and public law",
        ],
        "weight": 8,
    },
    {
        "id": "R41",
        "career": "Content Writer / Journalist",
        "conditions": ["interest_writing", "high_english_score", "high_writing_skills_score"],
        "explanation": [
            "Strong English and Writing Skills grades confirm linguistic command",
            "Essential for a writing or journalism career",
        ],
        "weight": 8,
    },
    {
        "id": "R42",
        "career": "Teacher / Educator",
        "conditions": ["interest_education", "high_pedagogy_score"],
        "explanation": [
            "High Pedagogy scores indicate formal teaching-methodology training",
            "Reinforces the interest-in-education signal for this career",
        ],
        "weight": 7,
    },
    {
        "id": "R43",
        "career": "Environmental Scientist",
        "conditions": ["interest_environment", "high_environmental_science_score", "high_geography_score"],
        "explanation": [
            "Strong Environmental Science and Geography grades confirm domain readiness",
            "These subjects are core to ecological and sustainability research",
        ],
        "weight": 8,
    },
    {
        "id": "R44",
        "career": "Psychologist / Counselor",
        "conditions": ["interest_psychology", "high_psychology_score"],
        "explanation": [
            "High Psychology marks reflect academic grounding in human behaviour",
            "Complements the interest-driven motivation for this field",
        ],
        "weight": 7,
    },
    {
        "id": "R45",
        "career": "Graphic Designer / UI-UX Designer",
        "conditions": ["interest_design", "high_design_score", "high_creativity_score"],
        "explanation": [
            "Strong Design and Creativity scores translate directly to visual work",
            "These are the primary academic signals for a design career",
        ],
        "weight": 8,
    },
    {
        "id": "R46",
        "career": "Data Scientist",
        "conditions": ["interest_data_analysis", "high_statistics_score", "high_data_interpretation_score"],
        "explanation": [
            "Statistics and Data Interpretation are the academic spine of data science",
            "High marks in both reinforce readiness for the role",
        ],
        "weight": 8,
    },
    {
        "id": "R47",
        "career": "Cloud / DevOps Engineer",
        "conditions": ["interest_coding", "high_operating_systems_score", "high_computer_networks_score"],
        "explanation": [
            "Operating Systems and Computer Networks underpin cloud infrastructure",
            "Strong grades here indicate readiness for DevOps responsibilities",
        ],
        "weight": 8,
    },

    # ─────────────────────────────────────────────
    # NEWLY WIRED SKILLS (R48 – R66)
    # Rules that use skill facts added to SKILL_OPTIONS below.
    # These give the previously-unused skills real scoring weight.
    # ─────────────────────────────────────────────
    {
        "id": "R48",
        "career": "Research Scientist",
        "conditions": ["interest_science", "skill_research", "high_science_score"],
        "explanation": [
            "Research skills are the backbone of scientific inquiry",
            "Strong science scores confirm academic readiness",
            "Scientific curiosity + hands-on research ability is a natural fit",
        ],
        "weight": 9,
    },
    {
        "id": "R49",
        "career": "Environmental Scientist",
        "conditions": ["interest_environment", "skill_research", "skill_analytical_thinking"],
        "explanation": [
            "Research skills are essential for environmental fieldwork and studies",
            "Analytical thinking supports impact assessments and data interpretation",
            "Environment interest drives the core motivation for this career",
        ],
        "weight": 9,
    },
    {
        "id": "R50",
        "career": "Content Writer / Journalist",
        "conditions": ["interest_writing", "skill_writing", "skill_communication"],
        "explanation": [
            "Writing skill combined with a passion for writing is the strongest signal",
            "Communication ability ensures clarity and audience engagement",
        ],
        "weight": 9,
    },
    {
        "id": "R51",
        "career": "Lawyer",
        "conditions": ["interest_law", "skill_critical_thinking", "skill_communication"],
        "explanation": [
            "Critical thinking is the foundation of legal reasoning and argumentation",
            "Communication skills are essential for both written briefs and oral advocacy",
            "Law interest is the core motivator",
        ],
        "weight": 9,
    },
    {
        "id": "R52",
        "career": "Lawyer",
        "conditions": ["interest_law", "skill_public_speaking", "skill_analytical_thinking"],
        "explanation": [
            "Public speaking is critical for courtroom advocacy and negotiations",
            "Analytical thinking enables case strategy and legal research",
        ],
        "weight": 8,
    },
    {
        "id": "R53",
        "career": "Medical Doctor",
        "conditions": ["interest_medicine", "skill_attention_to_detail", "skill_empathy"],
        "explanation": [
            "Attention to detail is vital for accurate diagnosis and treatment",
            "Empathy is essential for patient-centred care",
        ],
        "weight": 8,
    },
    {
        "id": "R54",
        "career": "Financial Analyst",
        "conditions": ["interest_finance", "skill_attention_to_detail", "skill_analytical_thinking"],
        "explanation": [
            "Attention to detail is critical in financial modelling and auditing",
            "Analytical thinking drives investment and market evaluation",
        ],
        "weight": 8,
    },
    {
        "id": "R55",
        "career": "Database Administrator",
        "conditions": ["interest_coding", "skill_attention_to_detail", "skill_problem_solving"],
        "explanation": [
            "Attention to detail is crucial for schema design and query optimisation",
            "Problem-solving is needed for performance tuning and incident resolution",
            "Coding interest provides the scripting and automation foundation",
        ],
        "weight": 7,
    },
    {
        "id": "R56",
        "career": "Mechanical Engineer",
        "conditions": ["interest_engineering", "skill_mechanical_aptitude", "skill_problem_solving"],
        "explanation": [
            "Mechanical aptitude is the defining trait of this engineering discipline",
            "Problem-solving drives design iteration and fault analysis",
            "Engineering interest aligns directly with mechanical systems work",
        ],
        "weight": 10,
    },
    {
        "id": "R57",
        "career": "Robotics Engineer",
        "conditions": ["interest_electronics", "skill_mechanical_aptitude", "skill_programming"],
        "explanation": [
            "Mechanical aptitude supports the hardware and actuator side of robotics",
            "Programming enables control systems and autonomous behaviour",
            "Electronics interest provides the sensor and circuit knowledge needed",
        ],
        "weight": 9,
    },
    {
        "id": "R58",
        "career": "Data Scientist",
        "conditions": ["interest_data_analysis", "skill_data_visualization", "skill_statistics"],
        "explanation": [
            "Data visualisation is how insights are communicated to stakeholders",
            "Statistics underpins every modelling and analysis task in data science",
        ],
        "weight": 8,
    },
    {
        "id": "R59",
        "career": "Business Analyst",
        "conditions": ["interest_business", "skill_strategic_thinking", "skill_analytical_thinking"],
        "explanation": [
            "Strategic thinking helps identify process improvements and growth opportunities",
            "Analytical thinking is needed to evaluate business data and requirements",
        ],
        "weight": 9,
    },
    {
        "id": "R60",
        "career": "Entrepreneur",
        "conditions": ["interest_business", "skill_strategic_thinking", "skill_leadership"],
        "explanation": [
            "Strategic thinking is essential for business planning and market positioning",
            "Leadership is required to build and guide a founding team",
        ],
        "weight": 9,
    },
    {
        "id": "R61",
        "career": "Teacher / Educator",
        "conditions": ["interest_education", "skill_public_speaking", "skill_communication"],
        "explanation": [
            "Public speaking is the primary delivery mechanism in teaching",
            "Communication skills ensure lessons are clear and engaging",
        ],
        "weight": 9,
    },
    {
        "id": "R62",
        "career": "Teacher / Educator",
        "conditions": ["interest_education", "skill_emotional_intelligence", "skill_empathy"],
        "explanation": [
            "Emotional intelligence allows teachers to respond to diverse student needs",
            "Empathy builds trust and a supportive classroom environment",
        ],
        "weight": 8,
    },
    {
        "id": "R63",
        "career": "Human Resources Manager",
        "conditions": ["interest_business", "skill_emotional_intelligence", "skill_communication"],
        "explanation": [
            "Emotional intelligence is the core competency of effective HR professionals",
            "Communication skills facilitate conflict resolution and talent management",
        ],
        "weight": 9,
    },
    {
        "id": "R64",
        "career": "Social Worker",
        "conditions": ["interest_social_work", "skill_emotional_intelligence", "skill_empathy"],
        "explanation": [
            "Emotional intelligence enables nuanced understanding of vulnerable situations",
            "Empathy is the most critical trait for building trust with clients",
        ],
        "weight": 9,
    },
    {
        "id": "R65",
        "career": "Marketing Specialist",
        "conditions": ["interest_marketing", "skill_public_speaking", "skill_communication"],
        "explanation": [
            "Public speaking is key for pitches, presentations, and brand storytelling",
            "Communication skills are at the heart of all marketing work",
        ],
        "weight": 8,
    },
    {
        "id": "R66",
        "career": "Project Manager",
        "conditions": ["skill_decision_making", "skill_leadership", "skill_project_management"],
        "explanation": [
            "Decision-making under uncertainty is central to project delivery",
            "Leadership keeps teams motivated and aligned to project goals",
            "Project management skills are directly applicable to this role",
        ],
        "weight": 8,
    },
]

# ── Fact vocabulary ────────────────────────────────────────────────────────────
# These are all possible facts that can be asserted into working memory.
# Used by the UI to generate checkboxes and dropdowns.

INTEREST_OPTIONS = [
    ("interest_coding",             "Coding / Programming"),
    ("interest_data_analysis",      "Data Analysis"),
    ("interest_artificial_intelligence", "Artificial Intelligence"),
    ("interest_cybersecurity",      "Cybersecurity"),
    ("interest_web_development",    "Web Development"),
    ("interest_engineering",        "Engineering"),
    ("interest_electronics",        "Electronics"),
    ("interest_biology",            "Biology"),
    ("interest_science",            "Science / Research"),
    ("interest_medicine",           "Medicine / Healthcare"),
    ("interest_psychology",         "Psychology"),
    ("interest_business",           "Business / Management"),
    ("interest_finance",            "Finance / Economics"),
    ("interest_marketing",          "Marketing"),
    ("interest_design",             "Design / Art"),
    ("interest_writing",            "Writing / Journalism"),
    ("interest_education",          "Teaching / Education"),
    ("interest_social_work",        "Social Work"),
    ("interest_law",                "Law / Legal Studies"),
    ("interest_gaming",             "Gaming / Game Development"),
    ("interest_environment",        "Environment / Sustainability"),
]

SKILL_OPTIONS = [
    # ── Technical ──────────────────────────────────────────────────────────
    ("skill_programming",          "Programming"),
    ("skill_logical_thinking",     "Logical Thinking"),
    ("skill_problem_solving",      "Problem Solving"),
    ("skill_networking",           "Networking / IT"),
    ("skill_mechanical_aptitude",  "Mechanical Aptitude"),
    ("skill_data_visualization",   "Data Visualization"),

    # ── Analytical ─────────────────────────────────────────────────────────
    ("skill_analytical_thinking",  "Analytical Thinking"),
    ("skill_critical_thinking",    "Critical Thinking"),
    ("skill_statistics",           "Statistics / Math"),
    ("skill_research",             "Research Skills"),
    ("skill_strategic_thinking",   "Strategic Thinking"),
    ("skill_attention_to_detail",  "Attention to Detail"),
    ("skill_decision_making",      "Decision Making"),

    # ── Creative ───────────────────────────────────────────────────────────
    ("skill_creativity",           "Creativity"),
    ("skill_visual_thinking",      "Visual / Spatial Thinking"),
    ("skill_writing",              "Writing / Documentation"),

    # ── People & Communication ─────────────────────────────────────────────
    ("skill_communication",        "Communication"),
    ("skill_empathy",              "Empathy / People Skills"),
    ("skill_public_speaking",      "Public Speaking"),
    ("skill_negotiation",          "Negotiation / Persuasion"),
    ("skill_emotional_intelligence", "Emotional Intelligence"),

    # ── Management ─────────────────────────────────────────────────────────
    ("skill_leadership",           "Leadership"),
    ("skill_project_management",   "Project Management"),
    ("skill_financial_literacy",   "Financial Literacy"),
]
