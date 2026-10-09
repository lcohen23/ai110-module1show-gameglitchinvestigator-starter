# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

At first glance the game looked completely normal. The bugs only showed up once I started playing.

**Bugs I noticed:**

1. **Hints are reversed.**
   - *Expected:* A guess that's too low should tell me to go higher, and a guess that's too high should tell me to go lower.
   - *Actual:* It's the opposite. A low guess tells me to go lower, and a high guess tells me to go higher.
   - *Cause:* `check_guess` returned "Go HIGHER!" for "Too High" and "Go LOWER!" for "Too Low".

2. **The attempts counter doesn't go down after the first guess.**
   - *Expected:* Every guess, including the first, uses up one attempt.
   - *Actual:* The "attempts left" counter doesn't change after my first guess. It always seems to be one guess behind.
   - *Cause:* `attempts` started at 1 instead of 0, and the "Attempts left" box was drawn before the submit code added 1 to `attempts`.

3. **Invalid and empty inputs use up attempts.**
   - *Expected:* Empty or non-number inputs should show an error without costing an attempt.
   - *Actual:* Any input, even an empty one, makes the "attempts left" counter go down. Non-number inputs never trigger a game over, but they still count. If I use up all my attempts on non-numbers and then enter a number, I only get one real guess.
   - *Cause:* `attempts += 1` ran before `parse_guess` checked whether the input was valid.

4. **The "attempts left" counter can go negative.**
   - *Expected:* The counter should stop at 0.
   - *Actual:* The counter keeps going below 0.
   - *Cause:* Attempts left was calculated as `attempt_limit - attempts` with no minimum, and invalid inputs never set the game to "lost".

5. **Difficulty settings don't make sense.**
   - *Expected:* Harder modes should have a bigger range and fewer attempts.
   - *Actual:* Normal has the biggest range (1 to 100), while Hard is only 1 to 50. Normal also gives more attempts (8) than Easy (6). The prompt always says "between 1 and 100".
   - *Cause:* `get_range_for_difficulty` and `attempt_limit_map` had the values out of order, and the prompt text was hard-coded.

6. **New Game doesn't reset the game.**
   - *Expected:* Clicking New Game should start completely fresh.
   - *Actual:* It picks a new secret, but a finished game stays on "Game over" and the history carries over. The new secret is always from 1 to 100, even on Easy.
   - *Cause:* The New Game code only reset `attempts` and `secret` (using `randint(1, 100)`). It never reset `status` or `history`, so `st.stop()` still ended the page.

7. **Hints flip on even-numbered attempts** *(found later, while checking my fixes)*.
   - *Expected:* The same guess should always get the same hint.
   - *Actual:* Guessing 9 with a secret of 50 said "Go HIGHER!" on attempt 1 and "Go LOWER!" on attempt 2.
   - *Cause:* On every even-numbered attempt, `app.py` turned the secret into text, so `check_guess` compared `"9"` to `"50"` alphabetically, and `"9"` comes after `"50"`.

8. **Scoring is inconsistent** *(found later, while checking my fixes)*.
   - *Expected:* Every wrong guess should cost the same points, and a first-guess win should be worth the most.
   - *Actual:* Guessing 70 with a secret of 50 gave +5 on attempt 2, then -5 for the same guess on attempt 3.
   - *Cause:* `update_score` added 5 points for "Too High" on even-numbered attempts, and the win formula had an extra `+ 1`, so even a first-guess win lost points.

**Game trace (original starter code, Normal mode, secret set to 50):**

```
Load game                -> sidebar "Attempts allowed: 8", box "Attempts left: 7"
Guess 30                 -> "Go LOWER!"   | Attempts left: 7
Guess 70                 -> "Go HIGHER!"  | Attempts left: 6
New game, submit "abc" 9 times -> "That is not a number." | Attempts left: -1, still playing
Select Hard              -> sidebar "Range: 1 to 50", prompt "Guess a number between 1 and 100"
Select Easy              -> sidebar "Attempts allowed: 6" (Normal has 8)
Lose on Easy, click New Game -> secret 69, still "Game over", history kept
New game, guess 70 twice -> score +5, then 0 (same wrong guess, different points)
```

**Bug Reproduction Log**

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|-------------------|-----------------|------------------------|
| Secret 50, guess 30 | "Go HIGHER!" hint | "Go LOWER!" hint shown | none |
| First guess of a game (30) | Attempts left goes from 8 to 7 | Starts at 7 and stays at 7 | none |
| Submit `abc` | Error, attempts left stays the same | "That is not a number.", and attempts left goes down by 1 | none |
| Submit `abc` 9 times on Normal | Counter stops at 0 | "Attempts left: -1", game still playing | none |
| Select Hard | Bigger range than Normal's 1–100 | "Range: 1 to 50", prompt still says "1 and 100" | none |
| Lose on Easy, click New Game | Fresh game with a secret from 1–20 | Secret 69, still "Game over" | none |
| Secret 50, guess 9 twice | "Go HIGHER!" both times | "Go HIGHER!" then "Go LOWER!" | none |
| Secret 50, guess 70 twice | Score -5, then -10 | Score +5, then 0 | none |


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude Code in VS Code.

**Correct suggestion:** Claude found that `check_guess` had its hint messages swapped and suggested moving it into `logic_utils.py` and flipping them. This was correct. I verified it with a pytest case (60 vs. 50 returns "Too High" with a "Go LOWER" hint) and by playing the game.

**Incorrect/misleading suggestion:** For the attempts counter, Claude started attempts at 0 and made the counter update after each guess, then said it was fixed. When I played, the history in the debug panel still didn't update until a later click. Claude simulated clicks and found the saved data was correct, but the debug panel was drawn before the guess was processed. So the first fix was incomplete. After the second fix, I verified that the counter and the debug panel both update on the same click.

**Not accepted as written:** For the attempts counter bug, Claude moved the math into a new `attempts_left` function in `logic_utils.py` and added a test for it. I questioned whether this really counted as fixing core logic, since the function was just one subtraction and the real bug was in the order the page was drawn. Claude agreed, so I kept that fix but chose the difficulty settings bug as my second core logic fix instead. I verified it with tests checking that harder difficulties have bigger ranges and fewer attempts.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

A bug counted as fixed when a pytest case for it passed and the game behaved correctly when I played it. I ran `pytest` after each fix, and all 12 tests passed at the end. One test checks that harder difficulties have bigger ranges and fewer attempts. It showed me the new ranges and attempt limits were in the right order. Claude also pointed out that the starter tests compared `check_guess` to a single string, even though it returns an (outcome, message) pair. They only checked the outcome, which was never the problem, so they couldn't catch the reversed hints. That's why my new test also checks the hint message. Some fixes, like the guess prompt, New Game, and switching difficulty, are UI behavior, so I checked those by playing the game instead of with pytest. For the even-attempt hint bug and invalid inputs, Claude used Streamlit's built-in test runner (`AppTest`) to write tests that click Submit in a simulated game, which showed the same guess now gets the same hint every time.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click or type something, Streamlit reruns the whole script from top to bottom. Normal variables get reset on every rerun, so anything that needs to last, like the secret number or attempts, has to go in `st.session_state`. Because the page is drawn in order, anything shown above the code that updates the state shows the old value. That's what caused the attempts counter to lag one guess behind.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

**Habit to reuse:** Writing a small pytest case for each fix, and also checking it in the actual app, since some bugs (like the lagging counter) only show up when you play.

**What I'd do differently:** Test the AI's fix myself before accepting it. Claude said the counter was fixed, but I only found the debug panel lag by playing the game.

**How my thinking changed:** AI-generated code can look fine and still be full of logic bugs, so I now treat it as a draft that needs testing, not finished code.
