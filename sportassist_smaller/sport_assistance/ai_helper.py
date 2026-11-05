"""
ai_helper.py -- the ONLY file that talks to the LLM API.

Why isolate it?
  * If you want to switch providers (OpenAI, Claude, ...), you only edit this file.
  * The rest of the app just calls ask_llm(...) and gets text back.
  * Credentials come from environment variables, never from the source code.

You do NOT need to modify this file to complete the project.
"""

import os

from dotenv import load_dotenv  # reads the ".env" file into environment variables

load_dotenv()

# The model name can be changed in your .env file.
MODEL = os.getenv("LLM_MODEL", "gemini-3.5-flash")


def has_api_key():
    """Return True if an API key is configured, otherwise False.

    The rest of the app uses this to decide between "real AI" and "demo mode".
    """
    return bool(os.getenv("GEMINI_API_KEY", "").strip())


def ask_llm(system_prompt, messages, max_tokens=800):
    """Send a conversation to the LLM and return its reply as a string.

    Parameters:
        system_prompt (str): Instructions that define the AI's role and rules
            (for us: "you are a sports coach, here is the athlete's profile...").
        messages (list[dict]): The conversation so far. Each item looks like
            {"role": "user" or "assistant", "content": "text"}.
            The LAST item should be the user's newest message.
        max_tokens (int): Upper limit on the length of the reply.

    Returns:
        str: The AI's reply, or a readable error message if something goes wrong.
    """
    if not has_api_key():
        # DEMO MODE: show what WOULD be sent to the AI. This lets you check your
        # prompt and your chat history without an API key.
        return (
            "🧪 **DEMO MODE: no API key found, so this is not real coaching.**\n\n"
            f"The AI would receive **{len(messages)} message(s)** and this system prompt:\n\n"
            f"```\n{system_prompt}\n```\n"
            "Add a `GEMINI_API_KEY` to your `.env` file to get real, personalized advice."
        )

    try:
        from google import genai  # imported here so demo mode needs no install
        from google.genai import types

        # Gradio may attach extra keys (like "metadata") to messages, so we keep
        # only the role and the text. Gemini calls the AI's role "model", not "assistant".
        contents = [
            types.Content(
                role="model" if m["role"] == "assistant" else "user",
                parts=[types.Part(text=m["content"])],
            )
            for m in messages
        ]

        client = genai.Client()  # automatically reads GEMINI_API_KEY from the environment
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                # Gemini counts its "thinking" tokens in this limit, so keep it generous.
                max_output_tokens=max(max_tokens, 2048),
            ),
        )
        return response.text or "⚠️ The AI returned an empty reply. Try again."
    except Exception as error:  # beginner-friendly: show the problem instead of crashing
        return f"⚠️ The AI request failed: {error}"
