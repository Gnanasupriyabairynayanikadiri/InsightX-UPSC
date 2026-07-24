# =========================================================
# 📁 FILE: core/ai_model_answer.py
# =========================================================

import re


# =========================================================
# CLEAN TEXT
# =========================================================
def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^\w\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# EXTRACT KEYWORDS
# =========================================================
def extract_keywords(question):

    stop_words = [

        "the",
        "is",
        "are",
        "was",
        "were",
        "a",
        "an",
        "of",
        "in",
        "on",
        "with",
        "and",
        "or",
        "to",
        "for",
        "from",
        "by",
        "discuss",
        "explain",
        "examine",
        "evaluate",
        "analyze",
        "analyse",
        "write",
        "note",
        "short",
        "features",
        "main",
        "major"
    ]

    question = clean_text(question)

    words = question.split()

    keywords = []

    for word in words:

        if word not in stop_words and len(word) > 2:

            keywords.append(word)

    return list(set(keywords))


# =========================================================
# MODEL ANSWER GENERATOR
# =========================================================
def generate_model_answer(question):

    question = clean_text(question)

    # =====================================================
    # HARAPPAN
    # =====================================================
    if "harappan" in question:

        return """

Introduction

The Harappan Civilization (c. 2600–1900 BCE) represents one of the earliest urban civilizations in the world. Its architecture reflects advanced town planning and engineering skills.

Body

1. Planned Urban Layout
• Cities followed grid-pattern planning.
• Roads intersected at right angles.

2. Advanced Drainage System
• Covered underground drainage network.
• Scientific sanitation arrangements.

3. Citadel and Lower Town
• Cities divided into administrative and residential sections.

4. Public Buildings
• Great Bath at Mohenjodaro.
• Granaries at Harappa.

5. Standardized Construction
• Uniform baked bricks used extensively.

📌 Examples:
Harappa, Mohenjodaro, Dholavira, Lothal.

Conclusion

Harappan architecture demonstrates remarkable urban planning, engineering efficiency, and civic administration that were far ahead of their time.
"""

    # =====================================================
    # VIJAYANAGARA
    # =====================================================
    elif "vijayanagara" in question:

        return """

Introduction

The Vijayanagara Empire significantly contributed to the evolution of South Indian temple architecture between the 14th and 17th centuries.

Body

1. Massive Gopurams
• Tall entrance towers became dominant features.
• Decorated with stucco sculptures.

2. Mandapas
• Large pillared halls introduced.
• Kalyana mandapas and ranga mandapas developed.

3. Temple Complexes
• Temples became urban and economic centres.
• Integrated bazaars and tanks.

4. Sculptural Art
• Intricate carvings of deities and mythological scenes.

5. Granite Construction
• Extensive use of durable granite.

📌 Examples:
Virupaksha Temple, Vittala Temple, Hampi complex.

Conclusion

Vijayanagara rulers transformed temple architecture into a grand synthesis of religion, politics, and artistic excellence.
"""

    # =====================================================
    # ODISHA
    # =====================================================
    elif "odisha" in question:

        return """

Introduction

Odisha temple architecture represents a distinctive regional style of the Nagara school characterized by monumental towers and rich sculptural ornamentation.

Body

1. Rekha Deula
• Curvilinear shikhara above sanctum.

2. Jagamohana
• Assembly hall with pyramidal roof.

3. Temple Components
• Vimana, Jagamohana, Natamandira, Bhogamandapa.

4. Rich Sculptural Decoration
• Floral motifs and mythological carvings.

5. Kalinga Style
• Distinct regional variation of Nagara architecture.

📌 Examples:
Konark Sun Temple, Lingaraja Temple, Jagannath Temple.

Conclusion

Odisha temple architecture reflects artistic excellence, regional innovation, and religious devotion in medieval India.
"""

    # =====================================================
    # KHAJURAHO
    # =====================================================
    elif "khajuraho" in question:

        return """

Introduction

Khajuraho temples, built by the Chandela rulers, represent one of the finest examples of Nagara style architecture in medieval India.

Body

1. Nagara Style
• Curvilinear shikharas.
• Elevated temple platforms.

2. Sculptural Excellence
• Intricate carvings of gods, apsaras, and social scenes.
• Famous erotic sculptures symbolize spiritual harmony.

3. Temple Layout
• Garbhagriha, mandapa, maha-mandapa arrangement.

4. Sandstone Construction
• Rich decorative ornamentation throughout temple walls.

📌 Examples:
Kandariya Mahadeva Temple, Lakshmana Temple.

Conclusion

Khajuraho temples symbolize the artistic brilliance and cultural richness of medieval Indian temple architecture.
"""

    # =====================================================
    # PALLAVA / CHOLA / PANDYA
    # =====================================================
    elif (

        "pallava" in question
        or "chola" in question
        or "pandya" in question
    ):

        return """

Introduction

The Pallavas, Cholas, and Pandyas played a crucial role in the evolution of Dravidian temple architecture in South India.

Body

1. Pallava Contributions
• Transition from rock-cut to structural temples.
• Development of early Dravidian style.

📌 Examples:
Shore Temple, Mahabalipuram.
Kailasanatha Temple, Kanchipuram.

2. Chola Contributions
• Construction of massive vimanas.
• Highly developed bronze sculpture tradition.
• Monumental temple complexes.

📌 Examples:
Brihadeeswara Temple, Thanjavur.
Gangaikonda Cholapuram Temple.

3. Pandya Contributions
• Expansion of temple complexes.
• Development of elaborate gopurams.
• Rich decorative sculpture.

📌 Examples:
Meenakshi Temple, Madurai.

Conclusion

The Pallavas, Cholas, and Pandyas collectively transformed South Indian temple architecture into a highly sophisticated and monumental tradition.
"""

    # =====================================================
    # NAGARA VS DRAVIDIAN
    # =====================================================
    elif "nagara" in question and "dravidian" in question:

        return """

Introduction

Nagara and Dravidian are the two major styles of Indian temple architecture that evolved in northern and southern India respectively.

Body

Nagara Style
• Curvilinear shikhara.
• Temples built on raised platforms.
• No large boundary walls.

📌 Examples:
Khajuraho temples, Konark Temple.

Dravidian Style
• Pyramid-shaped vimana.
• Large temple complexes with gopurams.
• Enclosed boundary walls.

📌 Examples:
Brihadeeswara Temple, Meenakshi Temple.

Conclusion

Both Nagara and Dravidian styles reflect regional diversity and artistic excellence in Indian temple architecture.
"""

    # =====================================================
    # DEFAULT
    # =====================================================
    return """

Introduction

The topic is important from the UPSC examination perspective and requires conceptual and analytical understanding.

Body

• Define the concept clearly.
• Mention major features.
• Add examples and significance.
• Explain impact and broader relevance.

Conclusion

A balanced and analytical approach is necessary for writing a good UPSC Mains answer.
"""


# =========================================================
# FEEDBACK GENERATOR
# =========================================================
def generate_feedback(answer, question):

    answer_lower = clean_text(answer)

    feedback = []

    # =====================================================
    # INTRODUCTION
    # =====================================================
    if "introduction" in answer_lower:

        feedback.append(

            "Good introduction present."
        )

    else:

        feedback.append(

            "Add a proper introduction."
        )

    # =====================================================
    # CONCLUSION
    # =====================================================
    if "conclusion" in answer_lower:

        feedback.append(

            "Conclusion is present."
        )

    else:

        feedback.append(

            "Add a proper conclusion."
        )

    # =====================================================
    # KEYWORDS
    # =====================================================
    keywords = extract_keywords(question)

    matched = 0

    for keyword in keywords:

        if keyword in answer_lower:

            matched += 1

    if len(keywords) > 0:

        ratio = matched / len(keywords)

        if ratio >= 0.7:

            feedback.append(

                "Excellent topic coverage."
            )

        elif ratio >= 0.4:

            feedback.append(

                "Moderate topic relevance."
            )

        else:

            feedback.append(

                "Poor topic relevance."
            )

    # =====================================================
    # ANALYTICAL DEPTH
    # =====================================================
    analytical_words = [

        "however",
        "therefore",
        "impact",
        "significance",
        "importance",
        "thus"
    ]

    analytical_found = False

    for word in analytical_words:

        if word in answer_lower:

            analytical_found = True

            break

    if analytical_found:

        feedback.append(

            "Analytical dimensions included."
        )

    else:

        feedback.append(

            "Add analytical dimensions."
        )

    # =====================================================
    # EXAMPLES
    # =====================================================
    if (

        "example" in answer_lower
        or "temple" in answer_lower
        or "e.g" in answer_lower
    ):

        feedback.append(

            "Examples used effectively."
        )

    else:

        feedback.append(

            "Add relevant examples."
        )

    # =====================================================
    # STRUCTURE
    # =====================================================
    if len(answer.split("\n")) > 5:

        feedback.append(

            "Presentation structure is good."
        )

    else:

        feedback.append(

            "Improve formatting and structure."
        )

    return " ".join(feedback)


# =========================================================
# IMPROVE ANSWER
# =========================================================
def improve_answer(answer, question):

    model_answer = generate_model_answer(question)

    improved = f"""

{model_answer}

Additional Improvement Suggestions:
• Use more keywords from the question.
• Add analytical dimensions.
• Add more examples.
• Use headings and subheadings.
• Write concise and structured points.
"""

    return improved.strip()