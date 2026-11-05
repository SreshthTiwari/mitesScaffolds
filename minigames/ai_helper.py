"""
ai_helper.py -- everything that talks to an LLM lives in THIS file.

Keeping it isolated means the rest of the app never needs to know whether an
LLM is available. If there is no API key (or the call fails), we return a
built-in fallback hint instead.

RULES FOR USING THE LLM IN THIS PROJECT
  * The LLM gives HINTS and EXPLANATIONS only.
  * The LLM never decides whether an answer is correct. challenges.py does.
  * We never send the correct answer to the LLM, so it can't leak it.
"""

import os

# Load variables from a local .env file if python-dotenv is installed.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODEL = os.getenv("LLM_MODEL", "gemini-3.5-flash")


def llm_available():
    """True if an API key is configured."""
    return bool(os.getenv("GEMINI_API_KEY"))


# ==================================================
# FEATURE 7: AI hints
# ==================================================
FALLBACK_HINTS = {
    "exercise": "Re-read the example in the Learn tab. What is the same in your code and the example? What's different?",
    "debug": "Read the buggy code slowly, one character at a time. Does everything that is opened also get closed?",
}


def fallback_hint(activity):
    """Hint used when there is no API key. Works offline, no setup needed."""
    return FALLBACK_HINTS.get(activity, "Re-read the lesson and try again.")


def build_hint_prompt(level_title, activity, question, user_attempt):
    """
    Build the text we send to the LLM.

    The prompt is where you control behavior. A starter version is provided;
    your job is to make it much better.

    TODO 1: Tell the model its ROLE (a patient Python tutor for beginners).
    TODO 2: Tell it NOT to reveal the answer or write the full solution.
    TODO 3: Tell it to give ONE small nudge, in at most 2 sentences.
    TODO 4: Include the student's attempt and ask the model to point at the
            general area of the mistake, not fix it for them.
    TODO 5: Test it! Try to trick your own tutor into revealing the answer,
            then tighten the prompt until it holds up.
    """
    return (
        f"You are a Python tutor. Level: {level_title}. Activity: {activity}.\n"
        f"Question: {question}\n"
        f"Student's attempt: {user_attempt or '(nothing yet)'}\n"
        "Give a short hint."
    )


def call_llm(prompt):
    """Send a prompt to the LLM and return its text reply. Provided for you."""
    from google import genai  # imported here so the app runs even if it isn't installed
    from google.genai import types

    client = genai.Client()  # reads GEMINI_API_KEY from the environment
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        # Gemini counts its "thinking" tokens in this limit, so keep it generous.
        # (The prompt itself asks for a short hint.)
        config=types.GenerateContentConfig(max_output_tokens=1024),
    )
    return response.text or "(The AI returned an empty reply.)"


def get_hint(level_title, activity, question, user_attempt=""):
    """
    The one function app.py calls. Returns a hint string.

    TODO 1 (optional): Add a `hint_number` argument and make later hints
            more specific than earlier ones (hint 1 vague, hint 3 clearer).
    TODO 2 (optional): Show a friendlier message when the call fails.
    """
    if not llm_available():
        return fallback_hint(activity) + "\n\n(No API key set, so this is a built-in hint.)"

    prompt = build_hint_prompt(level_title, activity, question, user_attempt)
    try:
        return call_llm(prompt)
    except Exception as error:  # network problems, bad key, etc.
        return fallback_hint(activity) + f"\n\n(The AI helper had a problem: {error})"


# STRETCH TODO (supports FEATURE 4): generate a new debugging challenge.
def generate_debug_challenge(level_title):
    """
    Ask the LLM for a new buggy snippet and return a dictionary shaped like
    the "debug" entries in levels.py:
        {"buggy_code": ..., "question": ..., "choices": [...], "correct": ...}

    Ideas: ask the model to reply in JSON, parse it with json.loads(), and
    validate that all four keys exist before using it. Return None on failure.
    """
    return None  # TODO
