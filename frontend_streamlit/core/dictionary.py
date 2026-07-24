# core/dictionary.py

import streamlit as st
import requests
import json
import os

from datetime import datetime

from core.xp import add_xp

# ==============================
# FILE
# ==============================
FILE = "storage/dictionary_history.json"


# ==============================
# LOAD HISTORY
# ==============================
def load_history():

    if not os.path.exists(FILE):
        return {}

    try:
        with open(FILE, "r") as f:
            return json.load(f)

    except Exception:
        return {}


# ==============================
# SAVE HISTORY
# ==============================
def save_history(data):

    os.makedirs("storage", exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ==============================
# SAVE SEARCH
# ==============================
def save_search(user, word):

    data = load_history()

    if user not in data:
        data[user] = []

    # avoid duplicates
    existing_words = [
        item["word"].lower()
        for item in data[user]
    ]

    if word.lower() not in existing_words:

        data[user].append({

            "word": word,

            "date": str(datetime.now())
        })

        save_history(data)


# ==============================
# GET HISTORY
# ==============================
def get_history(user):

    data = load_history()

    return data.get(user, [])


# ==============================
# FETCH WORD DATA
# ==============================
def fetch_word(word):

    url = (
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:
            return None

        return response.json()

    except Exception:
        return None


# ==============================
# DISPLAY MEANINGS
# ==============================
def display_meanings(data):

    try:

        entry = data[0]

        # --------------------------
        # WORD
        # --------------------------
        st.markdown(
            f"# 📘 {entry.get('word', '').capitalize()}"
        )

        # --------------------------
        # PHONETIC
        # --------------------------
        phonetic = entry.get("phonetic")

        if phonetic:
            st.info(f"🔊 {phonetic}")

        # --------------------------
        # AUDIO
        # --------------------------
        phonetics = entry.get("phonetics", [])

        for p in phonetics:

            audio = p.get("audio")

            if audio:
                st.audio(audio)
                break

        # --------------------------
        # MEANINGS
        # --------------------------
        meanings = entry.get("meanings", [])

        for meaning in meanings:

            part = meaning.get(
                "partOfSpeech",
                "Unknown"
            )

            st.markdown(
                f"## 📌 {part.capitalize()}"
            )

            definitions = meaning.get(
                "definitions",
                []
            )

            for i, definition in enumerate(definitions, 1):

                st.markdown(
                    f"### Definition {i}"
                )

                st.write(
                    f"👉 {definition.get('definition', '')}"
                )

                # Example
                example = definition.get("example")

                if example:
                    st.info(
                        f"💡 Example: {example}"
                    )

                # Synonyms
                synonyms = definition.get(
                    "synonyms",
                    []
                )

                if synonyms:

                    st.success(
                        "🔁 Synonyms: "
                        + ", ".join(synonyms[:5])
                    )

                # Antonyms
                antonyms = definition.get(
                    "antonyms",
                    []
                )

                if antonyms:

                    st.error(
                        "↔️ Antonyms: "
                        + ", ".join(antonyms[:5])
                    )

                st.markdown("---")

    except Exception as e:

        st.error("⚠️ Failed to parse dictionary data")

        st.write(e)


# ==============================
# WORD OF THE DAY
# ==============================
def word_of_the_day():

    words = [

        {
            "word": "Pragmatic",
            "meaning":
            "Dealing with things practically."
        },

        {
            "word": "Resilient",
            "meaning":
            "Able to recover quickly from difficulties."
        },

        {
            "word": "Ambiguous",
            "meaning":
            "Having more than one meaning."
        },

        {
            "word": "Meticulous",
            "meaning":
            "Showing great attention to detail."
        },

        {
            "word": "Constitutional",
            "meaning":
            "Related to constitution or governance."
        }
    ]

    import random

    return random.choice(words)


# ==============================
# MAIN UI
# ==============================
def dictionary_ui(user):

    st.title("📘 Smart UPSC Dictionary")

    st.markdown(
        f"👤 Logged in as: **{user}**"
    )

    # ==============================
    # WORD OF DAY
    # ==============================
    wod = word_of_the_day()

    st.markdown("## 🌟 Word of the Day")

    st.success(
        f"📖 {wod['word']} — {wod['meaning']}"
    )

    st.markdown("---")

    # ==============================
    # SEARCH
    # ==============================
    word = st.text_input(
        "🔍 Enter a word",
        placeholder="Example: Federalism"
    )

    # ==============================
    # SEARCH BUTTON
    # ==============================
    if st.button("🚀 Search Word"):

        if not word.strip():

            st.warning(
                "Please enter a word."
            )

            return

        with st.spinner(
            "Fetching meaning..."
        ):

            result = fetch_word(word)

        if not result:

            st.error(
                "❌ Word not found."
            )

            return

        # XP
        add_xp(user, 1)

        # SAVE HISTORY
        save_search(user, word)

        # DISPLAY
        display_meanings(result)

    st.markdown("---")

    # ==============================
    # HISTORY
    # ==============================
    st.markdown("## 🕘 Recent Searches")

    history = get_history(user)

    if not history:

        st.info(
            "No recent searches."
        )

    else:

        for item in reversed(history[-10:]):

            st.write(
                f"📖 {item['word']} "
                f"({item['date'][:10]})"
            )