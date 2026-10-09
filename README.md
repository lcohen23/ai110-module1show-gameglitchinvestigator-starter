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
  - The attempts counter was one guess behind, and invalid or empty inputs still used up attempts.
  - Difficulty settings were out of order: Normal had a bigger range than Hard and more attempts than Easy.
  - New Game only reset the secret number, and switching difficulty didn't restart the game.
- [x] **Fixes applied:**
  - Moved the game logic from `app.py` into `logic_utils.py`.
  - Swapped the hint messages in `check_guess`.
  - Made ranges grow and attempts shrink with difficulty (Easy 1–20 / 8, Normal 1–50 / 6, Hard 1–100 / 5).
  - Made the guess prompt show the current difficulty's range instead of always "1 and 100".
  - New Game and switching difficulty now fully reset the game, with a secret in the right range.
  - Fixed the attempts counter and debug panel so they update on the same click as the guess.
  - Added pytest cases for the logic fixes (hints, difficulty settings, attempts left).

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start a game on Normal (range 1–50, 6 attempts). The secret is 32. Attempts left: 6.
2. Guess 20 → "Go HIGHER!" Score: -5, attempts left: 5.
3. Guess 40 → "Go LOWER!" Score: 0, attempts left: 4.
4. Guess 32 → "Correct!" with balloons. "You won! The secret was 32. Final score: 60"
5. The game ends. Click New Game to play again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ py -m pytest
7 passed in 0.01s
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
