# 🎮 Minigames (smaller version)

A web game that teaches Python through levels, built with Python + Gradio.
The app launches as-is; you write five pieces of it by following the `TODO` comments
(see the tutorial PDF).

```
select level -> learn -> practice -> debug -> quiz -> unlock next level
```

## Setup and run

Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Windows (PowerShell or Command Prompt):

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open the local URL Gradio prints (usually http://127.0.0.1:7860).

**Optional AI hints:** copy `.env.example` to `.env` and set `GEMINI_API_KEY`
(get one at aistudio.google.com/apikey). Without a key the game uses built-in hints.

## The files

| File | Job |
|------|-----|
| `app.py` | Screen layout and button handlers. Calls the other files. |
| `levels.py` | Level content (lessons, exercises, bugs, quizzes) and `get_lesson()`. |
| `challenges.py` | Checking logic: practice answers, debugging, quiz scoring. |
| `progress.py` | Tracks what is finished and unlocks the next level. |
| `ai_helper.py` | The only file that talks to the AI (finished for you). |
