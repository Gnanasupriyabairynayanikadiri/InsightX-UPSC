import streamlit as st
import json
import os
import matplotlib.pyplot as plt

FILE = "storage/scores.json"


# ==============================
# 📂 LOAD SCORES
# ==============================
def load_scores():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


# ==============================
# 📊 DASHBOARD FUNCTION
# ==============================
def show_dashboard(username):

    st.header("📊 Performance Dashboard")

    data = load_scores()

    # ❌ No data case
    if username not in data or not data[username]:
        st.warning("⚠️ No test data available. Take a quiz first!")
        return

    user_data = data[username]

    # ==============================
    # 📈 OVERALL PERFORMANCE
    # ==============================
    total_tests = len(user_data)
    avg_accuracy = sum(d["accuracy"] for d in user_data) / total_tests

    st.subheader("📈 Overall Performance")
    st.write(f"Total Tests: {total_tests}")
    st.write(f"Average Accuracy: {avg_accuracy:.2f}%")

    # ==============================
    # 📊 SUBJECT-WISE PERFORMANCE
    # ==============================
    subject_scores = {}

    for entry in user_data:
        subject = entry["subject"]

        if subject not in subject_scores:
            subject_scores[subject] = []

        subject_scores[subject].append(entry["accuracy"])

    subjects = list(subject_scores.keys())
    avg_scores = [sum(v)/len(v) for v in subject_scores.values()]

    st.subheader("📊 Subject-wise Accuracy")

    fig = plt.figure()
    plt.bar(subjects, avg_scores)
    plt.xlabel("Subjects")
    plt.ylabel("Accuracy (%)")
    plt.title("Performance by Subject")

    st.pyplot(fig)

    # ==============================
    # 🔍 WEAK AREAS
    # ==============================
    st.subheader("🔍 Weak Areas (Below 60%)")

    weak = [d for d in user_data if d["accuracy"] < 60]

    if not weak:
        st.success("🎉 No weak areas. Great job!")
    else:
        for w in weak:
            st.write(
                f"{w['subject']} | {w['class']} | Chapter {w['chapter']} → {w['accuracy']}%"
            )

    # ==============================
    # 📜 RECENT ATTEMPTS
    # ==============================
    st.subheader("📜 Recent Attempts")

    for d in user_data[-5:]:
        st.write(
            f"{d['subject']} | {d['class']} | Chapter {d['chapter']} → {d['accuracy']}%"
        )