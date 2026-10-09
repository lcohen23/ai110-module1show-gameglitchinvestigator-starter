import random
import streamlit as st

from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score, attempts_left, get_attempt_limit

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = get_attempt_limit(difficulty)

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")



# FIX (with Claude Code): New Game only reset the secret (always from 1-100),
# and switching difficulty didn't restart the game. Both now use this reset.
def start_new_game():
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = difficulty


if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if st.session_state.get("difficulty", difficulty) != difficulty:
    start_new_game()
st.session_state.difficulty = difficulty

# FIX (with Claude Code): attempts starts at 0 so no attempts are used before the first guess
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# FIX (with Claude Code): reserve a spot for the attempts box and fill it in after the guess is
# processed, so the counter isn't one guess behind
attempts_box = st.empty()


def show_attempts_left():
    attempts_box.info(
        # FIX (with Claude Code): prompt always said "1 and 100", now uses the difficulty's range
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempts_left(attempt_limit, st.session_state.attempts)}"
    )


# FIX (with Claude Code, after I noticed history lagging in the game): like the attempts box, fill the debug info in after the guess is
# processed so it doesn't show the previous guess's values
debug_box = st.container()


def show_debug_info():
    with debug_box.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

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

if new_game:
    start_new_game()
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    show_attempts_left()
    show_debug_info()
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # FIX (with Claude Code): invalid or empty input used to cost an attempt
        # (attempts went up before the input was checked). Now only valid guesses count.
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX (with Claude Code): the secret used to be turned into text on every
        # even-numbered attempt, so guesses were compared alphabetically ("9" > "50").
        # Now the guess is always compared to the real number.
        outcome, message = check_guess(guess_int, st.session_state.secret)

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
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

show_attempts_left()
show_debug_info()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
