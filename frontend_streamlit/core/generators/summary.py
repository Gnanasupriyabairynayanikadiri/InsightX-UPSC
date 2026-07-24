# =========================================================
# 📁 FILE: core/generators/summary.py
# UPSC SUMMARY ENGINE
# =========================================================


# =========================================================
# GENERATE UPSC ANALYTICAL SUMMARY
# =========================================================
def generate_summary(title, category):

    # =====================================================
    # ECONOMY
    # =====================================================
    if category == "Economy":

        return (

            f"The issue regarding '{title}' is important in the context "
            f"of India's economic governance, fiscal policy, taxation "
            f"framework, and income regulation mechanisms.\n\n"

            f"UPSC relevance includes:\n"

            f"• Economic reforms\n"
            f"• Fiscal governance\n"
            f"• Revenue administration\n"
            f"• Ease of doing business\n"
            f"• Inclusive growth"
        )

    # =====================================================
    # INTERNATIONAL RELATIONS
    # =====================================================
    elif category == "International Relations":

        return (

            f"The development concerning '{title}' reflects evolving "
            f"geopolitical dynamics and strategic challenges.\n\n"

            f"UPSC relevance includes:\n"

            f"• India's foreign policy\n"
            f"• Strategic interests\n"
            f"• Regional security\n"
            f"• Global diplomacy\n"
            f"• Multilateral institutions"
        )

    # =====================================================
    # ENVIRONMENT
    # =====================================================
    elif category == "Environment":

        return (

            f"The issue related to '{title}' is significant from "
            f"the perspective of environmental sustainability "
            f"and ecological conservation.\n\n"

            f"UPSC relevance includes:\n"

            f"• Climate change\n"
            f"• Biodiversity conservation\n"
            f"• Environmental governance\n"
            f"• Sustainable development"
        )

    # =====================================================
    # POLITY
    # =====================================================
    elif category == "Polity":

        return (

            f"The development regarding '{title}' is important "
            f"from the perspective of constitutional governance "
            f"and institutional accountability.\n\n"

            f"UPSC relevance includes:\n"

            f"• Constitutional provisions\n"
            f"• Governance reforms\n"
            f"• Federalism\n"
            f"• Public administration"
        )

    # =====================================================
    # SCIENCE & TECHNOLOGY
    # =====================================================
    elif category == "Science & Technology":

        return (

            f"The issue concerning '{title}' highlights the growing "
            f"importance of technological innovation and digital transformation.\n\n"

            f"UPSC relevance includes:\n"

            f"• Emerging technologies\n"
            f"• Artificial Intelligence\n"
            f"• Cybersecurity\n"
            f"• Space technology\n"
            f"• Digital governance"
        )

    # =====================================================
    # SOCIAL ISSUES
    # =====================================================
    elif category == "Social Issues":

        return (

            f"The issue concerning '{title}' has implications "
            f"for social justice and inclusive development.\n\n"

            f"UPSC relevance includes:\n"

            f"• Welfare governance\n"
            f"• Human development\n"
            f"• Social empowerment\n"
            f"• Inclusive growth"
        )

    # =====================================================
    # DEFAULT
    # =====================================================
    return (

        f"The development regarding '{title}' has governance, "
        f"economic, social, and policy implications from "
        f"the UPSC perspective."
    )


# =========================================================
# GENERATE BACKGROUND
# =========================================================
def generate_background(category):

    backgrounds = {

        "Polity":
        "The issue is linked with constitutional governance and democratic administration.",

        "Economy":
        "The issue is associated with economic reforms and fiscal management.",

        "International Relations":
        "The issue is connected with India's strategic and diplomatic interests.",

        "Environment":
        "The issue is related to climate governance and sustainability.",

        "Science & Technology":
        "The issue reflects innovation and technological advancement.",

        "Social Issues":
        "The issue highlights challenges associated with social justice and welfare."
    }

    return backgrounds.get(
        category,
        "The issue has relevance for governance and policy-making."
    )


# =========================================================
# PRELIMS FOCUS
# =========================================================
def generate_prelims_focus(category):

    focus = {

        "Polity": [
            "Revise constitutional provisions",
            "Revise important committees"
        ],

        "Economy": [
            "Revise Budget and Economic Survey",
            "Revise taxation reforms"
        ],

        "International Relations": [
            "Revise international organizations",
            "Revise strategic groupings"
        ],

        "Environment": [
            "Revise climate conventions",
            "Revise biodiversity hotspots"
        ],

        "Science & Technology": [
            "Revise emerging technologies",
            "Revise AI and space missions"
        ],

        "Social Issues": [
            "Revise welfare schemes",
            "Revise social indicators"
        ]
    }

    return focus.get(
        category,
        ["Revise current affairs linked with static syllabus"]
    )