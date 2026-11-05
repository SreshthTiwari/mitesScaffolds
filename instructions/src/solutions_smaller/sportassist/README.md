# 🏅 Sport Assistance (smaller version)

A personalized AI sports coach. You fill in an athlete profile, and an AI coach
gives advice that fits **you** instead of generic tips.

The starter app **runs without an API key** (demo mode). Follow the tutorial PDF
(`sportassist_smaller_instructions.pdf`) and finish the three `TODO` features.

```
 form inputs ──► profile dict ──► prompt string ──► AI ──► personalized advice
 (app.py)        (profile.py)     (coach.py)     (ai_helper.py)   (shown in the chat)
```

| File | Purpose |
|---|---|
| `app.py` | The Gradio screen and the functions that run when you click |
| `profile.py` | **Feature 1:** create the athlete profile |
| `coach.py` | **Feature 2:** the coaching prompt. **Feature 3:** connect it to the chat |
| `ai_helper.py` | The only file that talks to the AI (you never need to edit it) |

## Run it

Mac:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    python app.py

Windows:

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    copy .env.example .env
    python app.py

Open the address it prints (usually http://127.0.0.1:7860). For real AI replies, put a
Gemini key (from aistudio.google.com/apikey) in `.env` as `GEMINI_API_KEY=...`.
Never share the key or commit `.env`.

> `profile.py` shares its name with a rarely used Python standard-library module.
> This is harmless here, but avoid running `python -m cProfile` in this folder.
