# =========================================================
# 📁 FILE: core/map_learning.py
# AI UPSC MAP LEARNING ENGINE
# FINAL CLEAN VERSION
# =========================================================

import streamlit as st


# =========================================================
# 🌍 IMPORT WORLD DATA
# =========================================================
from data.map.world.world_capitals import (
    WORLD_CAPITALS
)

from data.map.world.continents import (
    CONTINENTS
)

from data.map.world.world_rivers import (
    WORLD_RIVERS
)

from data.map.world.geopolitical_regions import (
    GEOPOLITICAL_REGIONS
)


# =========================================================
# 🇮🇳 IMPORT INDIA DATA
# =========================================================
from data.map.india.indian_states import (
    INDIAN_STATES
)

from data.map.india.indian_rivers import (
    INDIAN_RIVERS
)

from data.map.india.indian_mountains import (
    INDIAN_MOUNTAINS
)

from data.map.india.cities_nicknames import (
    CITIES_NICKNAMES
)


# =========================================================
# 📘 LEARNING CARD
# =========================================================
def render_learning_card(

    title,

    data,

    color="blue"
):

    st.markdown("---")

    st.subheader(title)

    for item in data:

        with st.expander(

            f"📍 {item.get('name', 'Unknown')}"
        ):

            for key, value in item.items():

                if key != "name":

                    st.write(

                        f"**{key.title()} :** "
                        f"{value}"
                    )


# =========================================================
# 🌍 WORLD CAPITALS
# =========================================================
def learn_world_capitals():

    st.title("🌍 Learn World Capitals")

    render_learning_card(

        "World Capitals",

        WORLD_CAPITALS
    )


# =========================================================
# 🌐 CONTINENTS
# =========================================================
def learn_continents():

    st.title("🌐 Learn Continents")

    render_learning_card(

        "Continents",

        CONTINENTS
    )


# =========================================================
# 🌊 WORLD RIVERS
# =========================================================
def learn_world_rivers():

    st.title("🌊 Learn World Rivers")

    render_learning_card(

        "World Rivers",

        WORLD_RIVERS
    )


# =========================================================
# 🌐 GEOPOLITICAL REGIONS
# =========================================================
def learn_geopolitics():

    st.title("🌐 Learn Geopolitics")

    render_learning_card(

        "Geopolitical Hotspots",

        GEOPOLITICAL_REGIONS
    )


# =========================================================
# 🇮🇳 INDIAN STATES
# =========================================================
def learn_indian_states():

    st.title("🇮🇳 Learn Indian States")

    render_learning_card(

        "Indian States",

        INDIAN_STATES
    )


# =========================================================
# 🌊 INDIAN RIVERS
# =========================================================
def learn_indian_rivers():

    st.title("🌊 Learn Indian Rivers")

    render_learning_card(

        "Indian Rivers",

        INDIAN_RIVERS
    )


# =========================================================
# 🏔️ INDIAN MOUNTAINS
# =========================================================
def learn_indian_mountains():

    st.title("🏔️ Learn Indian Mountains")

    render_learning_card(

        "Indian Mountains",

        INDIAN_MOUNTAINS
    )


# =========================================================
# 🏙️ CITIES & NICKNAMES
# =========================================================
def learn_city_nicknames():

    st.title("🏙️ Cities & Nicknames")

    render_learning_card(

        "Important Cities",

        CITIES_NICKNAMES
    )


# =========================================================
# 🎯 QUICK FACTS PANEL
# =========================================================
def render_quick_facts():

    st.markdown("---")

    st.subheader("⚡ Quick UPSC Facts")

    facts = [

        "🌍 Strait of Hormuz is a major oil chokepoint.",

        "🇮🇳 Brahmaputra enters India through Arunachal Pradesh.",

        "🏔️ Himalayas are young fold mountains.",

        "🌊 Nile is the world's longest river.",

        "🌐 South China Sea is geopolitically sensitive.",

        "🏜️ Sahara is the largest hot desert."
    ]

    for fact in facts:

        st.info(fact)


# =========================================================
# 📚 SEARCH ENGINE
# =========================================================
def learning_search_engine():

    st.markdown("---")

    st.subheader("🔍 Search Geography Topic")

    query = st.text_input(

        "Search Country / River / Mountain / State"
    )

    if not query:

        return

    query = query.lower()

    combined_data = (

        WORLD_CAPITALS +
        CONTINENTS +
        WORLD_RIVERS +
        GEOPOLITICAL_REGIONS +
        INDIAN_STATES +
        INDIAN_RIVERS +
        INDIAN_MOUNTAINS +
        CITIES_NICKNAMES
    )

    results = []

    for item in combined_data:

        if query in item.get(

            "name",
            ""
        ).lower():

            results.append(item)

    if results:

        st.success(

            f"{len(results)} result(s) found"
        )

        for result in results:

            with st.expander(

                f"📍 {result.get('name')}"
            ):

                for key, value in result.items():

                    if key != "name":

                        st.write(

                            f"**{key.title()} :** "
                            f"{value}"
                        )

    else:

        st.warning(
            "No matching topic found"
        )


# =========================================================
# 🌍 MAIN LEARNING UI
# =========================================================
def map_learning_ui():

    st.title("📚 AI UPSC Geography Learning")

    st.caption(

        "Interactive Learning Engine "
        "for Geography & Mapping"
    )

    st.markdown("---")

    category = st.selectbox(

        "Choose Learning Category",

        [

            "World Capitals",

            "Continents",

            "World Rivers",

            "Geopolitics",

            "Indian States",

            "Indian Rivers",

            "Indian Mountains",

            "Cities & Nicknames"
        ]
    )

    # =====================================================
    # CATEGORY ROUTING
    # =====================================================
    if category == "World Capitals":

        learn_world_capitals()

    elif category == "Continents":

        learn_continents()

    elif category == "World Rivers":

        learn_world_rivers()

    elif category == "Geopolitics":

        learn_geopolitics()

    elif category == "Indian States":

        learn_indian_states()

    elif category == "Indian Rivers":

        learn_indian_rivers()

    elif category == "Indian Mountains":

        learn_indian_mountains()

    elif category == "Cities & Nicknames":

        learn_city_nicknames()

    # =====================================================
    # SEARCH ENGINE
    # =====================================================
    learning_search_engine()

    # =====================================================
    # QUICK FACTS
    # =====================================================
    render_quick_facts()