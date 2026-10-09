from streamlit.testing.v1 import AppTest
from logic_utils import check_guess, attempts_left, update_score, get_range_for_difficulty, get_attempt_limit

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    outcome, message = result
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    outcome, message = result
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    outcome, message = result
    assert outcome == "Too Low"


def test_hint_direction_is_correct():
    # Bug fix: hints were reversed. A too-high guess should say go LOWER,
    # and a too-low guess should say go HIGHER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_attempts_left_counts_first_guess():
    # Bug fix: the first guess didn't count. With 8 allowed, no guesses should
    # leave 8, and one guess should leave 7.
    assert attempts_left(8, 0) == 8
    assert attempts_left(8, 1) == 7



def test_harder_difficulty_has_bigger_range():
    # Bug fix: Normal (1-100) had a bigger range than Hard (1-50).
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high


def test_harder_difficulty_has_fewer_attempts():
    # Bug fix: Normal (8) allowed more attempts than Easy (6).
    assert get_attempt_limit("Easy") > get_attempt_limit("Normal") > get_attempt_limit("Hard")



def test_attempts_left_never_negative():
    # Bug fix: the counter could go below 0.
    assert attempts_left(8, 10) == 0


def test_same_guess_gets_same_hint_every_attempt():
    # Bug fix: on even-numbered attempts the secret was compared as text,
    # so guessing 9 against 50 flipped between "Go HIGHER" and "Go LOWER".
    at = AppTest.from_file("app.py").run()
    at.session_state.secret = 50
    for _ in range(2):
        at.text_input[0].input("9")
        at.button[0].click().run()
        assert "HIGHER" in at.warning[0].value


def test_invalid_input_does_not_use_attempt():
    # Bug fix: empty or non-number inputs used to cost an attempt.
    at = AppTest.from_file("app.py").run()
    at.text_input[0].input("abc")
    at.button[0].click().run()
    assert at.session_state.attempts == 0



def test_wrong_guesses_always_cost_points():
    # Bug fix: a "Too High" guess added 5 points on even attempts.
    for attempt in (1, 2, 3, 4):
        assert update_score(0, "Too High", attempt) == -5
        assert update_score(0, "Too Low", attempt) == -5


def test_win_on_first_guess_is_worth_100():
    # Bug fix: an extra +1 made a first-guess win worth only 80.
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 3) == 80
