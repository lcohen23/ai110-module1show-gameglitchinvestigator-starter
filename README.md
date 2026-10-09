# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Purpose:** A number guessing game. You guess a secret number and get "higher" or "lower" hints, with a limited number of attempts depending on difficulty.
- [x] **Bugs found:**
  - Hints were reversed (a low guess said "Go LOWER").
  - Hints flipped on even-numbered attempts, because the secret was compared as text.
  - The attempts counter was one guess behind, invalid or empty inputs used up attempts, and the counter could go negative.
  - Difficulty settings were out of order: Normal had a bigger range than Hard and more attempts than Easy. The prompt always said "1 and 100".
  - New Game didn't reset the game status or history, and switching difficulty didn't restart the game.
  - Scoring was inconsistent: a "Too High" guess added 5 points on even attempts.
- [x] **Fixes applied:**
  - Moved the game logic from `app.py` into `logic_utils.py`.
  - Swapped the hint messages in `check_guess`, so each outcome returns the matching hint.
  - Removed the code that turned the secret into text on even attempts. Guesses are now always compared as numbers, so the hints stay consistent.
  - Attempts only go up after a guess passes `parse_guess`, so invalid inputs no longer cost an attempt.
  - `attempts_left` now stops at 0, so the counter can't go negative.
  - Attempts start at 0, and the attempts box and debug panel are filled in after the guess is processed, so they no longer lag one guess behind.
  - Made ranges grow and attempts shrink with difficulty (Easy 1–20 / 8, Normal 1–50 / 6, Hard 1–100 / 5), and the prompt now uses the current range.
  - New Game and switching difficulty now call one reset function that resets the secret (in the current range), attempts, score, status, and history.
  - `update_score` now takes 5 points for every wrong guess, and a win is worth 100 minus 10 for each extra guess, so scoring no longer depends on whether the attempt number is even.
  - Added pytest cases for the hints, difficulty settings, attempts counter, invalid inputs, and scoring.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start a game on Normal (range 1–50, 6 attempts). The secret is 32. Attempts left: 6.
2. Guess 20 → "Go HIGHER!" Score: -5, attempts left: 5.
3. Guess 40 → "Go LOWER!" Score: -10, attempts left: 4.
4. Type `abc` → "That is not a number." Attempts left stays at 4.
5. Guess 32 → "Correct!" with balloons. "You won! The secret was 32. Final score: 70"
6. The game ends. Click New Game to start a fresh game with 6 attempts.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ py -m pytest
12 passed in 2.19s
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
