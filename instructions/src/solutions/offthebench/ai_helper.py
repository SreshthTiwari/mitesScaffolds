"""
ai_helper.py - OPTIONAL feedback from a multimodal AI model.

The app works without this file doing anything. To enable it:
  1. pip install anthropic
  2. copy .env.example to .env and add your API key

PRIVACY: Photos of people are personal. By default NO image is sent anywhere.
The image is only sent if the user ticks an explicit consent box in the UI.

HONESTY: AI-generated coaching is a general suggestion. It is NOT verified
biomechanical analysis, and it can be wrong. Always label it that way.
"""

import base64
import io
import os

from PIL import Image

from sports import get_level_guidance

AI_LABEL = ("AI-generated suggestion, not verified biomechanical analysis. "
            "It may be inaccurate; consult a qualified coach.")


def is_ai_available():
    """Return (available, message). Never raises."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return False, "AI feedback is off: no ANTHROPIC_API_KEY found (see .env.example)."
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False, "AI feedback is off: run `pip install anthropic`."
    return True, "AI feedback is available."


# ==================================================
# FEATURE 6: Build the Prompt
# ==================================================
def build_prompt(sport, level, measurements):
    """
    Create the text we send to the AI.
    A good prompt says: who the user is, what data we have, what we want back,
    and what NOT to claim.
    """
    lines = []
    for m in measurements:
        if m["value"] is not None:
            lines.append(f"- {m['name']}: about {round(m['value'])} degrees ({m['label']})")
    measurement_text = "\n".join(lines) if lines else "(no measurements provided)"

    return (
        f"My sport is {sport} and my skill level is {level}. Here are approximate measurements "
        f"from one photo:\n{measurement_text}\n\n"
        f"{get_level_guidance(level)}\n"
        "Give 2-3 short technique tips. The angles come from a single 2D photo, so "
        "do not claim certainty. If you are unsure about something, say so."
    )


def encode_image_base64(image_array):
    """Convert a NumPy image into a base64 JPEG string (the format APIs accept)."""
    buffer = io.BytesIO()
    Image.fromarray(image_array).convert("RGB").save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# ==================================================
# FEATURE 6: Ask the AI
# ==================================================
def get_ai_feedback(prompt, image=None, user_consented_to_send_image=False):
    """
    Send the prompt (and, ONLY with consent, the image) to the AI.
    Returns a string for the UI; never raises.
    """
    available, message = is_ai_available()
    if not available:
        return message

    import anthropic

    content = []
    if image is not None and user_consented_to_send_image:
        content.append({"type": "image", "source": {
            "type": "base64", "media_type": "image/jpeg",
            "data": encode_image_base64(image)}})
    content.append({"type": "text", "text": prompt})

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model=os.environ.get("AI_MODEL", "claude-sonnet-5-5"),
            max_tokens=500,
            messages=[{"role": "user", "content": content}],
        )
        return response.content[0].text
    except Exception as error:
        return f"AI request failed: {error}"


def format_ai_feedback(raw_text):
    """Format the AI's reply for display."""
    return f"{raw_text.strip()}\n\n---\n_{AI_LABEL}_"
