# =========================================================
# 📁 FILE: core/ca_geointel.py
# UPSC GEOPOLITICAL + GEOINTELLIGENCE ENGINE
# =========================================================


# =========================================================
# DETECT GEO INTELLIGENCE
# =========================================================
def detect_geo_intelligence(title, description=""):

    text = f"{title} {description}".lower()

    # =====================================================
    # WEST ASIA / MIDDLE EAST
    # =====================================================
    if any(word in text for word in [

        "iran",
        "israel",
        "gaza",
        "hamas",
        "saudi",
        "uae",
        "west asia",
        "middle east",
        "hormuz",
        "oil prices"
    ]):

        return {

            "region": "West Asia",

            "type": "Energy & Strategic Region",

            "importance": (
                "Important for India's energy security, diaspora "
                "interests, and geopolitical stability."
            ),

            "upsc_link": (
                "GS2 International Relations + GS3 Energy Security"
            )
        }

    # =====================================================
    # INDO-PACIFIC / CHINA
    # =====================================================
    elif any(word in text for word in [

        "china",
        "taiwan",
        "south china sea",
        "indo-pacific",
        "beijing",
        "xi jinping"
    ]):

        return {

            "region": "Indo-Pacific",

            "type": "Strategic Maritime Region",

            "importance": (
                "Critical for global trade routes, India's maritime "
                "security, and Indo-Pacific strategy."
            ),

            "upsc_link": (
                "GS2 IR + GS3 Security"
            )
        }

    # =====================================================
    # RUSSIA - UKRAINE
    # =====================================================
    elif any(word in text for word in [

        "russia",
        "ukraine",
        "nato",
        "putin",
        "zelensky"
    ]):

        return {

            "region": "Europe",

            "type": "Conflict Zone",

            "importance": (
                "Impacts global energy prices, food security, "
                "defence diplomacy, and strategic alignments."
            ),

            "upsc_link": (
                "GS2 IR + GS3 Economy"
            )
        }

    # =====================================================
    # AFRICA
    # =====================================================
    elif any(word in text for word in [

        "africa",
        "sudan",
        "ethiopia",
        "nigeria"
    ]):

        return {

            "region": "Africa",

            "type": "Emerging Strategic Region",

            "importance": (
                "Important for India's trade, energy access, "
                "diaspora engagement, and Global South diplomacy."
            ),

            "upsc_link": (
                "GS2 International Relations"
            )
        }

    # =====================================================
    # INDIA DOMESTIC
    # =====================================================
    elif any(word in text for word in [

        "supreme court",
        "parliament",
        "cabinet",
        "government",
        "ministry",
        "india",
        "state government",
        "chief minister"
    ]):

        return {

            "region": "India",

            "type": "Domestic Governance",

            "importance": (
                "Relevant for governance, polity, social justice, "
                "economic reforms, or public administration."
            ),

            "upsc_link": (
                "GS2 Governance / Polity"
            )
        }

    # =====================================================
    # DEFAULT
    # =====================================================
    return {

        "region": "Global",

        "type": "General Issue",

        "importance": (
            "Relevant from a multidimensional UPSC perspective."
        ),

        "upsc_link": (
            "General Studies"
        )
    }