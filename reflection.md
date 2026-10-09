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

2. **The attempts counter doesn't go down after the first guess.**
   - *Expected:* Every guess, including the first, uses up one attempt.
   - *Actual:* The "attempts left" counter doesn't change after my first guess. It always seems to be one guess behind.

3. **Invalid and empty inputs use up attempts.**
   - *Expected:* Empty or non-number inputs should show an error without costing an attempt.
   - *Actual:* Any input, even an empty one, makes the "attempts left" counter go down. Non-number inputs never trigger a game over, but they still count. If I use up all my attempts on non-numbers and then enter a number, I only get one real guess.

4. **The "attempts left" counter can go negative.**
   - *Expected:* The counter should stop at 0.
   - *Actual:* The counter keeps going below 0.

5. **Difficulty settings don't make sense.**
   - *Expected:* Harder modes should have a bigger range and fewer attempts.
   - *Actual:* Normal has the biggest range (1 to 100), while Hard is only 1 to 50. Normal also gives more attempts (8) than Easy (6).

6. **New Game doesn't reset the game.**
   - *Expected:* Clicking New Game should start completely fresh.
   - *Actual:* The only thing it resets is the secret number. Everything else carries over from the old game.

**Bug Reproduction Log**

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|-------------------|-----------------|------------------------|
| Guess lower than the secret | "Go HIGHER" hint | "Go LOWER" hint shown | none |
| First guess of a game | Attempts left goes down by 1 | Attempts left doesn't change | none |
| Empty input or `abc` | Error, no attempt used | Error, and an attempt is used | none |
| Non-number inputs after attempts hit 0 | Counter stops at 0 | Counter goes negative | none |
| Switch to Hard mode | Hardest range (bigger than Normal) | Range is 1–50, smaller than Normal's 1–100 | none |
| Click New Game mid-game | Everything resets | Only the secret changes | none |


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
