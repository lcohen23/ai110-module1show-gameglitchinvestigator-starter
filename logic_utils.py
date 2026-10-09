def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX (with Claude Code): moved from app.py into logic_utils.py.
    # Normal (1-100) had a bigger range than Hard (1-50). Ranges now grow with difficulty.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def get_attempt_limit(difficulty: str):
    """Return how many guesses are allowed for a given difficulty."""
    # FIX (with Claude Code): moved the attempt limits from app.py into this function.
    # Normal (8) allowed more attempts than Easy (6). Attempts now shrink with difficulty.
    if difficulty == "Easy":
        return 8
    if difficulty == "Normal":
        return 6
    if difficulty == "Hard":
        return 5
    return 6


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX (with Claude Code): moved from app.py into logic_utils.py.
    # Hint messages were swapped. A guess that's too high should say go lower, and vice versa.
    # The text-comparison fallback was removed since the secret is always a number now.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX (with Claude Code): a "Too High" guess added 5 points on even attempts,
    # and a first-guess win was only worth 80 because of an extra +1.
    # Now every wrong guess costs 5, and a win is worth 100 minus 10 per extra guess.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


def attempts_left(attempt_limit: int, attempts_used: int):
    """Return how many attempts the player has left."""
    # FIX (with Claude Code): the counter could go negative. It now stops at 0.
    return max(0, attempt_limit - attempts_used)
