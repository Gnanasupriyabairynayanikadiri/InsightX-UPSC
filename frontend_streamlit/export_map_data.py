# =====================================================
# FILE: export_map_data.py
# EXPORT PYTHON MAP DATA TO REACT NATIVE TS FILES
# =====================================================

import json
from pathlib import Path

# ==========================
# WORLD
# ==========================

from data.map.world.world_capitals import (
    WORLD_CAPITALS_QUESTIONS
)

from data.map.world.world_continents import (
    WORLD_CONTINENTS_QUESTIONS
)

from data.map.world.world_rivers import (
    WORLD_RIVERS_QUESTIONS
)

from data.map.world.world_mountains import (
    WORLD_MOUNTAINS_QUESTIONS
)

from data.map.world.world_straits import (
    WORLD_STRAITS_QUESTIONS
)

from data.map.world.world_geo_politics import (
    WORLD_GEO_POLITICS_QUESTIONS
)

# ==========================
# INDIA
# ==========================

from data.map.india.indian_states import (
    INDIAN_STATES_QUESTIONS
)

from data.map.india.indian_rivers import (
    INDIAN_RIVERS_QUESTIONS
)

from data.map.india.indian_mountains import (
    INDIAN_MOUNTAINS_QUESTIONS
)

from data.map.india.indian_cities import (
    INDIAN_CITIES_QUESTIONS
)

from data.map.india.indian_biosphere_reserves import (
    INDIAN_BIOSPHERE_RESERVES_QUESTIONS
)

from data.map.india.indian_geo_politics import (
    INDIAN_GEO_POLITICS_QUESTIONS
)

# =====================================================
# EXPORT DIRECTORY
# =====================================================

BASE_DIR = Path("exports/map")

WORLD_DIR = BASE_DIR / "world"
INDIA_DIR = BASE_DIR / "india"

WORLD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

INDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# EXPORT FUNCTION
# =====================================================

def export_ts(
    data,
    variable_name,
    output_file
):
    content = (
        f"export const {variable_name} = "
        + json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
        + ";"
    )

    output_file.write_text(
        content,
        encoding="utf-8"
    )

    print(
        f"✅ Exported: {output_file.name}"
    )

# =====================================================
# WORLD EXPORTS
# =====================================================

export_ts(
    WORLD_CAPITALS_QUESTIONS,
    "WORLD_CAPITALS_QUESTIONS",
    WORLD_DIR / "worldCapitals.ts"
)

export_ts(
    WORLD_CONTINENTS_QUESTIONS,
    "WORLD_CONTINENTS_QUESTIONS",
    WORLD_DIR / "worldContinents.ts"
)

export_ts(
    WORLD_RIVERS_QUESTIONS,
    "WORLD_RIVERS_QUESTIONS",
    WORLD_DIR / "worldRivers.ts"
)

export_ts(
    WORLD_MOUNTAINS_QUESTIONS,
    "WORLD_MOUNTAINS_QUESTIONS",
    WORLD_DIR / "worldMountains.ts"
)

export_ts(
    WORLD_STRAITS_QUESTIONS,
    "WORLD_STRAITS_QUESTIONS",
    WORLD_DIR / "worldStraits.ts"
)

export_ts(
    WORLD_GEO_POLITICS_QUESTIONS,
    "WORLD_GEO_POLITICS_QUESTIONS",
    WORLD_DIR / "worldGeopolitics.ts"
)

# =====================================================
# INDIA EXPORTS
# =====================================================

export_ts(
    INDIAN_STATES_QUESTIONS,
    "INDIAN_STATES_QUESTIONS",
    INDIA_DIR / "indianStates.ts"
)

export_ts(
    INDIAN_RIVERS_QUESTIONS,
    "INDIAN_RIVERS_QUESTIONS",
    INDIA_DIR / "indianRivers.ts"
)

export_ts(
    INDIAN_MOUNTAINS_QUESTIONS,
    "INDIAN_MOUNTAINS_QUESTIONS",
    INDIA_DIR / "indianMountains.ts"
)

export_ts(
    INDIAN_CITIES_QUESTIONS,
    "INDIAN_CITIES_QUESTIONS",
    INDIA_DIR / "indianCities.ts"
)

export_ts(
    INDIAN_BIOSPHERE_RESERVES_QUESTIONS,
    "INDIAN_BIOSPHERE_RESERVES_QUESTIONS",
    INDIA_DIR / "indianBiosphereReserves.ts"
)

export_ts(
    INDIAN_GEO_POLITICS_QUESTIONS,
    "INDIAN_GEO_POLITICS_QUESTIONS",
    INDIA_DIR / "indianGeopolitics.ts"
)

print()
print("🎉 ALL MAP DATA EXPORTED")