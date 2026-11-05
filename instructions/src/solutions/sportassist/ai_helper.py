"""
ai_helper.py -- the ONLY file that talks to the LLM API.

Why isolate it?
  * If you want to switch providers (OpenAI, Gemini, ...), you only edit this file.
  * The rest of the app just calls ask_llm(...) and gets text back.
  * Credentials come from environment variables, never from the source code.

You do NOT need to modify this file to complete the project.
"""

import os

from dotenv import load_dotenv  # reads the ".env" file into environment variables

load_dotenv()

# The model name can be changed in your .env file.
MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")


def has_api_key():
    """Return True if an API key is configured, otherwise False.

    The rest of the app uses this to decide between "real AI" and "demo mode".
    """
    return bool(os.getenv("ANTHROPIC_API_KEY", "").strip())


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
        return "(No API key found. Add ANTHROPIC_API_KEY to your .env file.)"

    # Gradio may attach extra keys (like "metadata") to messages; the API only
    # accepts "role" and "content", so we keep just those.
    clean_messages = [{"role": m["role"], "content": m["content"]} for m in messages]

    try:
        from anthropic import Anthropic  # imported here so demo mode needs no install

        client = Anthropic()  # automatically reads ANTHROPIC_API_KEY from the environment
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=clean_messages,
        )
        return response.content[0].text
    except Exception as error:  # beginner-friendly: show the problem instead of crashing
        return f"⚠️ The AI request failed: {error}"
