# Off the Bench (short version)

A beginner-friendly Python + Gradio app: pick a sport and skill level, upload a
photo, and get technique suggestions. **The app runs out of the box; you write the
important logic by completing the `TODO`s.** Follow the `offthebench_smaller` PDF.

> Honesty note: one photo cannot prove a whole movement is right or wrong. Angles
> are approximate and depend on camera angle. AI advice is general, not verified
> biomechanical analysis.

## Setup

Requires Python 3.9-3.12 (MediaPipe support for newer versions varies).

**Mac:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python pose_analysis.py --download   # optional: ~6 MB pose model
python app.py
```

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python pose_analysis.py --download
python app.py
```

The app launches even if MediaPipe, the model file or an API key is missing; the status
area tells you what is unavailable. For AI feedback, put a Gemini key
(aistudio.google.com/apikey) in `.env` as `GEMINI_API_KEY=...`. Never commit `.env`.

## The files

| File | Purpose |
|------|---------|
| `app.py` | Gradio interface and the `analyze` handler that connects everything. |
| `sports.py` | **Yours:** sports, skill levels and level guidance (TODOs 1-2). |
| `pose_analysis.py` | MediaPipe wrapper (provided): finds body landmarks, draws them, measures angles. |
| `feedback.py` | **Yours:** `classify_angle` (TODO 3) and `build_suggestions` (TODO 4). |
| `ai_helper.py` | **Yours:** `build_prompt` (TODO 5). The photo-consent check is provided. |
| `models/` | Where the downloaded pose model lives. |
