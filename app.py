import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    guardrail_ai_guess,
    parse_guess,
    plan_ai_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 12,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
ai_mode = st.sidebar.toggle("Enable AI Guess Strategist", value=True)

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "agent_trace" not in st.session_state:
    st.session_state.agent_trace = []

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

if "active_difficulty" not in st.session_state:
    st.session_state.active_difficulty = difficulty


def _reset_game():
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.agent_trace = []
    st.session_state.last_feedback = None
    st.session_state.active_difficulty = difficulty


if st.session_state.active_difficulty != difficulty:
    _reset_game()

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
    st.write("Agent trace:", st.session_state.agent_trace)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if ai_mode:
    ai_step = st.button("AI Suggest Next Guess 🤖")
else:
    ai_step = False

if new_game:
    _reset_game()
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    elif guess_int < low or guess_int > high:
        st.error(f"Guess must be between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        outcome, message = check_guess(guess_int, st.session_state.secret)
        st.session_state.history.append((guess_int, outcome))

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

if ai_step and st.session_state.status == "playing":
    if st.session_state.attempts >= attempt_limit:
        st.session_state.status = "lost"
        st.error(
            f"Out of attempts! The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}"
        )
    else:
        st.session_state.attempts += 1
        planning_history = [
            (guess, outcome)
            for guess, outcome in st.session_state.history
            if outcome in {"Too Low", "Too High"}
        ]
        plan = plan_ai_guess(low, high, planning_history)
        ai_guess, guardrail_status = guardrail_ai_guess(plan, low, high, planning_history)
        outcome, message = check_guess(ai_guess, st.session_state.secret)
        st.session_state.history.append((ai_guess, outcome))
        st.session_state.agent_trace.append(
            {
                "plan_guess": plan.candidate_guess,
                "final_guess": ai_guess,
                "guardrail": guardrail_status,
                "confidence": plan.confidence,
                "rationale": plan.rationale,
                "outcome": outcome,
            }
        )

        st.info(
            f"AI planned `{plan.candidate_guess}` and used `{ai_guess}` "
            f"(guardrail: {guardrail_status}, confidence: {plan.confidence})."
        )
        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.success(
                f"AI solved it! Secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

st.divider()
st.caption("Built by an AI with planning + guardrail reliability checks.")
