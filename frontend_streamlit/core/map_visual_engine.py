# =========================================================
# 📁 FILE: core/map_visual_engine.py
# AI UPSC MAP VISUAL ENGINE
# FINAL CLEAN VERSION
# =========================================================

import streamlit as st
import pandas as pd


# =========================================================
# 🌍 IMPORT WORLD DATA
# =========================================================
from data.map.world.world_locations import (
    WORLD_LOCATIONS
)

from data.map.world.geopolitical_locations import (
    GEOPOLITICAL_LOCATIONS
)


# =========================================================
# 🇮🇳 IMPORT INDIA DATA
# =========================================================
from data.map.india.india_locations import (
    INDIA_LOCATIONS
)


# =========================================================
# 🎯 CONVERT TO DATAFRAME
# =========================================================
def create_dataframe(locations):

    return pd.DataFrame(locations)


# =========================================================
# 🌍 SHOW WORLD MAP
# =========================================================
def show_world_map():

    st.subheader("🌍 World Map")

    world_df = create_dataframe(

        WORLD_LOCATIONS
    )

    st.map(world_df)

    st.markdown("---")

    st.dataframe(

        world_df,

        use_container_width=True
    )


# =========================================================
# 🇮🇳 SHOW INDIA MAP
# =========================================================
def show_india_map():

    st.subheader("🇮🇳 India Map")

    india_df = create_dataframe(

        INDIA_LOCATIONS
    )

    st.map(india_df)

    st.markdown("---")

    st.dataframe(

        india_df,

        use_container_width=True
    )


# =========================================================
# 🌐 SHOW GEOPOLITICAL MAP
# =========================================================
def show_geopolitical_map():

    st.subheader("🌐 Geopolitical Hotspots")

    geo_df = create_dataframe(

        GEOPOLITICAL_LOCATIONS
    )

    st.map(geo_df)

    st.markdown("---")

    st.dataframe(

        geo_df,

        use_container_width=True
    )


# =========================================================
# 🌍 GENERIC MAP DISPLAY
# =========================================================
def show_custom_map(

    locations,

    title="Map Visualization"
):

    st.subheader(title)

    df = create_dataframe(locations)

    st.map(df)

    st.markdown("---")

    st.dataframe(

        df,

        use_container_width=True
    )


# =========================================================
# 🎯 MAIN MAP VISUAL UI
# =========================================================
def map_visual_ui():

    st.title("🗺️ UPSC Map Visual Engine")

    st.caption(
        "Interactive Geography Visualization"
    )

    st.markdown("---")

    # =====================================================
    # TABS
    # =====================================================
    tab1, tab2, tab3 = st.tabs([

        "🌍 World Map",

        "🇮🇳 India Map",

        "🌐 Geopolitics"
    ])

    # =====================================================
    # WORLD TAB
    # =====================================================
    with tab1:

        show_world_map()

    # =====================================================
    # INDIA TAB
    # =====================================================
    with tab2:

        show_india_map()

    # =====================================================
    # GEOPOLITICS TAB
    # =====================================================
    with tab3:

        show_geopolitical_map()