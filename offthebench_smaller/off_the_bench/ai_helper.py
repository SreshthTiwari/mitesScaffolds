"""
ai_helper.py - OPTIONAL feedback from a multimodal AI model.

The app works without this file doing anything. To enable it:
  1. pip install google-genai
  2. copy .env.example to .env and add your API key

PRIVACY: Photos of people are personal. By default NO image is sent anywhere.
The image is only sent if the user ticks an explicit consent box in the UI.

HONESTY: AI-generated coaching is a general suggestion. It is NOT verified
biomechanical analysis, and it can be wrong. Always label it that way.
"""

import io
import os

from PIL import Image

from sports import get_level_guidance

AI_LABEL = ("AI-generated suggestion, not verified biomechanical analysis. "
            "It may be inaccurate; consult a qualified coach.")


def is_ai_available():
    """Return (available, message). Never raises."""
    if not os.environ.get("GEMINI_API_KEY"):
        return False, "AI feedback is off: no GEMINI_API_KEY found (see .env.example)."
    try:
        from google import genai  # noqa: F401
    except ImportError:
        return False, "AI feedback is off: run `pip install google-genai`."
    return True, "AI feedback is available."


# ==================================================
# FEATURE 3: Build the Prompt
# ==================================================
def build_prompt(sport, level, measurements):
    """
    Create the text we send to the AI.
    A good prompt says: who the user is, what data we have, what we want back,
    and what NOT to claim.
    """
    # PROVIDED: turn the measurements into a readable text block
    # (measurements whose value is None are skipped).
    lines = []
    for m in measurements:
        if m["value"] is not None:
            lines.append(f"- {m['name']}: about {round(m['value'])} degrees ({m['label']})")
    measurement_text = "\n".join(lines) if lines else "(no measurements provided)"

    # TODO 5: Improve this prompt. Include the level guidance
    #         (get_level_guidance(level), imported above), ask for 2-3 short tips,
    #         and tell the AI to say when it is unsure and not to claim certainty
    #         from a single photo.
    return (f"I am a {level} {sport} athlete. Here are approximate measurements "
            f"from one photo:\n{measurement_text}\n"
            f"Give brief technique suggestions.")


def encode_image_jpeg(image_array):
    """Convert a NumPy image into JPEG bytes (the format the API accepts)."""
    buffer = io.BytesIO()
    Image.fromarray(image_array).convert("RGB").save(buffer, format="JPEG")
    return buffer.getvalue()


# ==================================================
# Ask the AI (PROVIDED, including the photo-consent check)
# ==================================================
def get_ai_feedback(prompt, image=None, user_consented_to_send_image=False):
    """
    Send the prompt (and, ONLY with consent, the image) to the AI.
    Returns a string for the UI; never raises.
    """
    available, message = is_ai_available()
    if not available:
        return message

    from google import genai
    from google.genai import types

    contents = []
    if image is not None and user_consented_to_send_image:
        contents.append(types.Part.from_bytes(
            data=encode_image_jpeg(image), mime_type="image/jpeg"))
    contents.append(prompt)

    try:
        client = genai.Client()  # reads GEMINI_API_KEY automatically
        response = client.models.generate_content(
            model=os.environ.get("AI_MODEL", "gemini-3.5-flash"),
            contents=contents,
            # Gemini counts its "thinking" tokens in this limit, so keep it generous.
            config=types.GenerateContentConfig(max_output_tokens=2048),
        )
        return response.text or "AI request returned an empty reply. Try again."
    except Exception as error:
        return f"AI request failed: {error}"


def format_ai_feedback(raw_text):
    """Format the AI's reply for display. AI_LABEL must always stay visible."""
    return f"{raw_text.strip()}\n\n---\n_{AI_LABEL}_"
