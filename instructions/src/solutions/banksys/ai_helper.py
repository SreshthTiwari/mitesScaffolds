"""
ai_helper.py -- the ONLY file that talks to the AI service.

Keeping it isolated means the rest of the app doesn't need to know which AI
service we use. You should not need to edit this file for the core features.
"""

import io
import os

from dotenv import load_dotenv

load_dotenv()  # reads the .env file (if it exists) into environment variables

DEFAULT_MODEL = "gemini-3.5-flash"


def has_api_key():
    """True if an API key is configured (otherwise we run in demo mode)."""
    return bool(os.getenv("GEMINI_API_KEY"))


def _image_to_jpeg_bytes(image):
    """Convert a PIL image (what Gradio gives us) into JPEG bytes for the API."""
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=90)
    return buffer.getvalue()


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
            "Add GEMINI_API_KEY to your .env file to get a real critique.\n\n"
            "Here is the prompt your code built (use it to check your work):\n"
            "-----\n" + prompt
        )
        return demo_text, False

    # ---- REAL MODE ----
    try:
        from google import genai
        from google.genai import types

        client = genai.Client()  # reads GEMINI_API_KEY automatically
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
            contents=[
                types.Part.from_bytes(data=_image_to_jpeg_bytes(image), mime_type="image/jpeg"),
                prompt,
            ],
            # Gemini counts its "thinking" tokens in this limit, so keep it generous.
            config=types.GenerateContentConfig(max_output_tokens=4096),
        )
        if not response.text:
            return "The AI returned an empty reply. Try again.", False
        return response.text, True
    except Exception as error:  # beginner-friendly: show what went wrong
        return f"The AI request failed: {error}", False
