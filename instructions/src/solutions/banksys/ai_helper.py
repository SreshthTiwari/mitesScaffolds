"""
ai_helper.py -- the ONLY file that talks to the AI service.

Keeping it isolated means the rest of the app doesn't need to know which AI
service we use. You should not need to edit this file for the core features.
"""

import base64
import io
import os

from dotenv import load_dotenv

load_dotenv()  # reads the .env file (if it exists) into environment variables

DEFAULT_MODEL = "claude-sonnet-5-5"


def has_api_key():
    """True if an API key is configured (otherwise we run in demo mode)."""
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def _image_to_base64(image):
    """Convert a PIL image (what Gradio gives us) into base64 text for the API."""
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=90)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def ask_ai_about_image(image, prompt):
    """
    Send an image and a text prompt to the AI.

    Returns a tuple: (response_text, is_real)
      - is_real is True  when the AI actually looked at the image
      - is_real is False in demo mode, or if something went wrong
    """
    if image is None:
        return "No image was provided.", False

    # ---- DEMO MODE: no key, so we do NOT analyze the image at all. ----
    if not has_api_key():
        demo_text = (
            "⚠️ DEMO MODE - this is NOT real feedback.\n"
            "No API key was found, so the AI never looked at your image.\n"
            "Add ANTHROPIC_API_KEY to your .env file to get a real critique.\n\n"
            "Here is the prompt your code built (use it to check your work):\n"
            "-----\n" + prompt
        )
        return demo_text, False

    # ---- REAL MODE ----
    try:
        import anthropic

        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY automatically
        response = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL),
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": _image_to_base64(image),
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return response.content[0].text, True
    except Exception as error:  # beginner-friendly: show what went wrong
        return f"The AI request failed: {error}", False
