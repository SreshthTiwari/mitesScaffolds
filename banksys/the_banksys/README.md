# 🎨 The Banksys — AI Art Learning Assistant

Learn about art styles, upload your artwork, pick something to improve, and get
AI feedback tailored to a target style. This is a **scaffold**: it launches, but
you write the important logic (look for `TODO`).

## Big picture

```
user input -> Gradio (app.py) -> Python function -> AI helper -> result
```

1. You click or upload something in the browser.
2. Gradio calls a Python function in `app.py` and passes in your inputs.
3. That function calls `art_styles.py` or `feedback.py`.
4. `feedback.py` builds a prompt and calls `ai_helper.py`, which talks to the AI.
5. The text comes back, is formatted, and Gradio displays it.

## Files

| File | Purpose |
|------|---------|
| `app.py` | The interface: tabs, buttons, inputs, and event handlers |
| `art_styles.py` | Art style dictionary and lookup (Feature 1) |
| `feedback.py` | Improvement-area logic, prompt building, response formatting (Features 3–5) |
| `ai_helper.py` | The only file that calls the AI API (you shouldn't need to edit it) |
| `requirements.txt` | Python packages to install |
| `.env.example` | Template for your API key |

## Install and launch

```bash
cd the_banksys
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # optional: add your key (see below)
python app.py
```

Open the local URL printed in the terminal (usually http://127.0.0.1:7860).

## API key

- The app uses the Anthropic API (Claude, which can understand images).
- Put your key in `.env` as `ANTHROPIC_API_KEY=...`. Never share or commit it.
- **No key?** The app runs in **demo mode**: the UI works, but the AI never
  looks at your image. It shows a clearly labeled message and your built
  prompt so you can check your work. It is *not* real feedback.

## Recommended order

1. **Feature 1** – `get_style_description()` in `art_styles.py` (dictionaries, if/else)
2. **Feature 2** – read the comments in `handle_upload()` in `app.py`
3. **Feature 3** – `get_improvement_instructions()` in `feedback.py`
4. **Feature 4** – `build_prompt()` in `feedback.py` (check it in demo mode, then with a key)
5. **Feature 5** – `format_feedback()` in `feedback.py`

## Optional extensions

- Add more styles, artists, and example images
- Show image size/format in the upload tab
- Let users pick a skill level (beginner / advanced) that changes the prompt
- Keep a history list of past critiques in the session
- Add a "Compare two drawings" tab
