import streamlit as st
import time

def pomodoro_timer(task_key, work_min=25, break_min=5):

    if f"pomodoro_state_{task_key}" not in st.session_state:
        st.session_state[f"pomodoro_state_{task_key}"] = "work"
        st.session_state[f"pomodoro_time_{task_key}"] = work_min * 60

    state = st.session_state[f"pomodoro_state_{task_key}"]
    timer = st.session_state[f"pomodoro_time_{task_key}"]

    st.markdown(f"### 🍅 Pomodoro Mode ({state.upper()})")

    mins = timer // 60
    secs = timer % 60
    st.info(f"⏱ {mins:02d}:{secs:02d}")

    if st.button("▶ Start", key=f"start_{task_key}"):
        st.session_state[f"running_{task_key}"] = True

    if st.button("⏸ Pause", key=f"pause_{task_key}"):
        st.session_state[f"running_{task_key}"] = False

    if st.session_state.get(f"running_{task_key}", False):

        if timer > 0:
            st.session_state[f"pomodoro_time_{task_key}"] -= 1
            st.rerun()

        else:
            if state == "work":
                st.success("🎉 Work session done! Break time")
                st.session_state[f"pomodoro_state_{task_key}"] = "break"
                st.session_state[f"pomodoro_time_{task_key}"] = break_min * 60
            else:
                st.success("🔁 Break over! Back to study")
                st.session_state[f"pomodoro_state_{task_key}"] = "work"
                st.session_state[f"pomodoro_time_{task_key}"] = work_min * 60

            st.rerun()