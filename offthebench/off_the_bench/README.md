# Off the Bench

A beginner-friendly Python + Gradio scaffold for an AI-assisted sports technique
analyzer. Users pick a sport and skill level, upload a photo, and get technique
suggestions. **The scaffold runs out of the box; you implement the important logic
by completing the `TODO`s.**

> Honesty note: one photo cannot prove a whole movement is right or wrong. Angles
> are approximate and depend on camera angle. AI advice is general, not verified
> biomechanical analysis.

## The flow

```
choose sport -> upload image -> detect landmarks -> analyze -> feedback
 (sports.py)     (app.py)     (pose_analysis.py)  (feedback.py) (feedback.py / ai_helper.py)
```

## What does MediaPipe do?

MediaPipe is a free library from Google. Given a photo, a pre-trained model guesses
where 33 body points ("landmarks") are, such as shoulders, elbows and knees. You get
the coordinates of each point. You do not need to train anything: you use the
coordinates with ordinary Python (`if` statements and a bit of geometry) to take
measurements like an elbow angle. **Detected measurements are facts about the photo;
coaching is your interpretation of them. Keep those separate.**

## Setup

Requires Python 3.9-3.12 (MediaPipe support for newer versions varies).

```bash
cd off_the_bench
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python pose_analysis.py --download   # downloads the ~6 MB pose model to models/
python app.py
```

Open the local URL printed in the terminal.

The app launches even if MediaPipe, the model file, or an API key is missing; the
status area tells you what is unavailable.

**Optional AI feedback:** `pip install anthropic`, copy `.env.example` to `.env`, and
add your key. Photos are only sent if the user ticks the consent box. Never commit `.env`.

## The files

| File | Purpose |
|------|---------|
| `app.py` | Gradio interface and the `analyze` handler that connects everything. |
| `sports.py` | Sports, example skills, skill levels, and per-sport/level text (if/elif/else TODOs). |
| `pose_analysis.py` | MediaPipe wrapper: `detect_pose`, drawing, `get_point`, `calculate_angle`. Isolated from the rest of the app. |
| `feedback.py` | Rules: `analyze_pose` (measurements) and `build_suggestions` (coaching). |
| `ai_helper.py` | Optional LLM prompt building and request, with explicit image consent. |
| `requirements.txt` | Python packages. |
| `.env.example` | Template for optional API settings. |
| `models/` | Where the downloaded `.task` model file lives. |

## Recommended implementation order

1. **Run the app.** Upload a photo with pose detection off; read `describe_image` in `app.py`.
2. **sports.py** TODOs 1-3: sport tips and level guidance (Features 1-2).
3. **app.py** TODOs: image info, nicer display (Feature 3).
4. **pose_analysis.py:** download the model, turn pose detection on, print a landmark, do the practice TODOs (Feature 4).
5. **feedback.py** TODOs 1-5: pick landmarks, measure angles, classify with if/else (Feature 5).
6. **feedback.py** TODOs 6-7: level-aware suggestions.
7. **ai_helper.py** TODOs: prompt, formatting (Feature 6). Test with and without the image consent box.

## Optional extensions (Feature 7)

- Analyze video frame by frame and look at how angles change over time.
- Compare two frames (before and after) or two photos.
- Skill-specific drills in `feedback.py`.
- Draw measured angles on the annotated image.
- Try the `lite` vs `full` vs `heavy` MediaPipe pose models (change `MODEL_URL`).
