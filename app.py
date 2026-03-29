import streamlit as st
import random
import time

st.set_page_config(page_title="The Final Guess", page_icon="🎮")

st.title("🎮 The Final Guess")

if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.num = 0
    st.session_state.attempts = 0
    st.session_state.max_attempts = 5
    st.session_state.low = 1
    st.session_state.high = 10
    st.session_state.ai_low = 1
    st.session_state.ai_high = 10
    st.session_state.best_score = 0
    st.session_state.streak = 0
    st.session_state.start_time = 0

mode = st.selectbox("Select Mode", ["Classic", "Hard", "Timer"])
difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard", "Boss"])

if st.button("🚀 Start Game"):
    if difficulty == "Easy":
        low, high, max_attempts = 1, 10, 5
    elif difficulty == "Medium":
        low, high, max_attempts = 1, 20, 10
    elif difficulty == "Hard":
        low, high, max_attempts = 1, 50, 15
    else:
        low, high, max_attempts = 1, 100, 10

    st.session_state.low = low
    st.session_state.high = high
    st.session_state.max_attempts = max_attempts
    st.session_state.num = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.ai_low = low
    st.session_state.ai_high = high
    st.session_state.game_started = True
    st.session_state.start_time = time.time()

    st.success(f"Game Started! Guess between {low} and {high}.")

if st.session_state.game_started:

    guess = st.number_input(
        "Enter your guess:",
        min_value=st.session_state.low,
        max_value=st.session_state.high,
        step=1
    )

    if st.button("Guess"):

        if mode == "Timer":
            if time.time() - st.session_state.start_time > 10:
                st.warning("Too slow!")
                st.session_state.attempts += 1

                if st.session_state.attempts >= st.session_state.max_attempts:
                    st.error(f"Game Over! Number was {st.session_state.num}")
                    st.session_state.game_started = False
                st.session_state.start_time = time.time()
                st.stop()

        st.session_state.attempts += 1
        st.session_state.start_time = time.time()

        num = st.session_state.num


        if guess == num:
            score = st.session_state.max_attempts - st.session_state.attempts + 1

            st.success(f"Correct! Score: {score}")

            if st.session_state.attempts == 1:
                st.info("FIRST TRY! GOD MODE!")

            if score > st.session_state.best_score:
                st.session_state.best_score = score

            st.session_state.streak += 1
            st.session_state.game_started = False

        elif guess < num:
            st.warning("Too Low!")
            st.session_state.ai_low = max(st.session_state.ai_low, guess + 1)
        else:
            st.warning("Too High!")
            st.session_state.ai_high = min(st.session_state.ai_high, guess - 1)

        if mode != "Hard" and st.session_state.game_started:
            diff = abs(num - guess)

            if diff <= 2:
                st.write("Extremely Close!")
            elif diff <= 5:
                st.write("Very Close!")
            elif diff <= 10:
                st.write("Getting there...")
            else:
                st.write("Way off!")

            ai = (st.session_state.ai_low + st.session_state.ai_high) // 2
            st.write(f"AI Suggestion: {ai}")

        if st.session_state.attempts >= st.session_state.max_attempts and st.session_state.game_started:
            st.error(f"Game Over! Number was {num}")
            st.session_state.streak = 0
            st.session_state.game_started = False

    st.write(f"Attempts left: {st.session_state.max_attempts - st.session_state.attempts}")
    st.write(f"Best Score: {st.session_state.best_score}")
    st.write(f"Streak: {st.session_state.streak}")



