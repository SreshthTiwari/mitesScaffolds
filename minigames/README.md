# 🎮 Minigames

A platform for learning Python through interactive levels, built with Python + Gradio.
This repo is a **scaffold**: the app launches and one level works end to end, and
you implement the rest by following the `TODO` comments.

## The game flow

```
select level -> learn -> practice -> debug -> quiz -> unlock next level
```

1. **Select a level** from the dropdown (only unlocked levels are playable).
2. **Learn**: read a short explanation and example.
3. **Practice**: submit a short answer; it is checked against fixed expected answers.
4. **Debug**: look at buggy code and pick what is wrong.
5. **Quiz**: answer multiple-choice questions.
6. **Unlock**: finishing exercise + debug + quiz unlocks the next level.

## Setup and run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open the local URL Gradio prints (usually http://127.0.0.1:7860).

**Optional AI hints:** copy `.env.example` to `.env` and add your API key.
Without a key, the app uses built-in fallback hints, so nothing breaks.

## The files and how they fit together

| File | Job |
|------|-----|
| `app.py` | Gradio screen layout and button handlers. Calls the other files. |
| `levels.py` | Level **data** (lessons, exercises, bugs, quizzes) and `get_lesson()`. |
| `challenges.py` | Checking logic: exercise, debugging, quiz scoring. |
| `progress.py` | One progress dictionary + unlocking logic. |
| `ai_helper.py` | The only file that talks to an LLM. Gives hints, with offline fallback. |

```
app.py  --->  levels.py        (what to show)
   |  --->  challenges.py      (is the answer right?)
   |  --->  progress.py        (what's finished / unlocked?)
   '  --->  ai_helper.py       (give me a hint)
```

`app.py` is the only file that knows about Gradio. The others are plain Python,
so you can test them in a normal Python shell.

### Key design rules
- **We never run student code.** Answers are compared to expected answers.
- **The LLM never decides correctness.** It only writes hints, and it is never sent the answer.
- **Gradio state is temporary.** `gr.State` holds progress while the page is open.
  Refreshing the page resets it, and nothing is saved between sessions.

## What is already working vs. what you build

| Feature | Starter status |
|---------|----------------|
| 1. Select a level | Dropdown works. |
| 2. Learn a concept | `get_lesson()` works for the "print" level only. Generalize it. |
| 3. Coding practice | Basic exact-match checking works. Make it smarter. |
| 4. Debugging challenge | Display works. **You write `check_debug_answer()`.** |
| 5. Quiz | Display works. **You write `score_quiz()`.** |
| 6. Level progression | **You write `is_level_complete()` and `unlock_next_level()`.** |
| 7. AI hints | Fallback + API call work. **You write a better prompt.** |

## Suggested implementation order

1. **Feature 2**: generalize `get_lesson()`, then fill in the other levels' text in `levels.py`.
2. **Feature 3**: improve `check_exercise()`, then write exercises for the other levels.
3. **Feature 4**: implement `check_debug_answer()` and add debug challenges.
4. **Feature 5**: implement `score_quiz()` and add quiz questions.
5. **Feature 6**: implement `is_level_complete()` and `unlock_next_level()`. Now the whole loop works!
6. **Feature 7**: write a good `build_hint_prompt()` and test that it doesn't leak answers.
7. **Stretch**: LLM-generated debugging challenges (`generate_debug_challenge()`).

Tip: until Feature 6 is done you can test later levels by temporarily editing
`new_progress()` so every level starts unlocked.

## Optional extensions

- **Points**: award points per activity, with a bonus for first-try answers.
- **Badges**: "Perfect Quiz", "No Hints Used", "Level 3 Complete".
- **More levels**: lists, dictionaries, string methods, file handling.
- **Save progress**: write the progress dictionary to a JSON file.
- **Lock icons**: show 🔒 in the dropdown labels for locked levels.
- **Hint levels**: hint 1 vague, hint 3 more specific.
- **Difficulty tiers**: easy / medium / hard exercises within a level.
