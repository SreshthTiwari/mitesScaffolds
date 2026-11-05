"""
coach.py -- turning an athlete profile into prompts, and prompts into coaching.

A "prompt" is just a string of text we send to the LLM. The LLM knows nothing
about the user, so WE must put the profile into the text. That is the core idea
of this whole project:

    profile dict  ->  prompt string  ->  LLM  ->  personalized advice
"""

from ai_helper import ask_llm, has_api_key

# ==================================================
# Coaching topics for each sport (provided, complete)
# ==================================================
GENERAL_TOPICS = ["Warm-up and recovery", "Mental focus", "Building consistency"]

SPORT_TOPICS = {
    "basketball": ["Shooting form", "Ball handling", "Defense", "Court vision"],
    "soccer": ["Passing", "Dribbling", "Shooting", "Positioning"],
    "volleyball": ["Serving", "Passing", "Setting", "Attacking"],
    "tennis": ["Serve", "Forehand", "Backhand", "Footwork"],
    "dance": ["Technique", "Flexibility", "Rhythm", "Performance"],
}


def get_coaching_topics(sport):
    """Return the coaching topics shown in the UI dropdown for this sport."""
    return SPORT_TOPICS.get(sport, []) + GENERAL_TOPICS


# ==================================================
# Provided: turning the profile into plain text
# ==================================================
def fallback_style_summary(profile):
    """Summarize the profile WITHOUT calling an LLM (complete, provided).

    Simple Python string formatting that always works, even with no API key.
    """
    strengths = ", ".join(profile.get("strengths", [])) or "not provided"
    weaknesses = ", ".join(profile.get("weaknesses", [])) or "not provided"
    style = profile.get("style_text", "").strip() or "not provided"
    return (
        f"**Sport:** {profile.get('sport', '?')}  \n"
        f"**Experience:** {profile.get('experience', '?')}  \n"
        f"**Handedness:** {profile.get('handedness', 'N/A')}  \n"
        f"**Strengths:** {strengths}  \n"
        f"**Areas to improve:** {weaknesses}  \n"
        f"**Preferences:** {profile.get('preferences') or 'not provided'}  \n"
        f"**In your own words:** {style}\n\n"
        "_This is a plain summary built by Python code, not by AI._"
    )


def profile_to_text(profile):
    """Turn the profile dictionary into readable lines for use inside prompts.

    Provided for you. Printing this is a great way to see what the LLM "knows".
    """
    return (
        f"- Sport: {profile.get('sport')}\n"
        f"- Experience level: {profile.get('experience')}\n"
        f"- Handedness: {profile.get('handedness')}\n"
        f"- Strengths: {', '.join(profile.get('strengths', [])) or 'none given'}\n"
        f"- Weaknesses: {', '.join(profile.get('weaknesses', [])) or 'none given'}\n"
        f"- Preferences: {profile.get('preferences') or 'none given'}\n"
        f"- Playing style (user's words): {profile.get('style_text') or 'none given'}"
    )


# ==================================================
# Optional tab: AI playing-style analysis (working starter, see Extensions)
# ==================================================
def build_style_analysis_prompt(profile, include_pro_comparisons=False):
    """Build the prompt asking the LLM to summarize the user's playing style.

    EXTENSION: this basic version works but is not careful. Make it safer by
    telling the model not to invent facts, and by asking it to word its guesses
    as possibilities ("may", "seems"). If include_pro_comparisons is True, you
    could add a clearly labelled, *unverified* comparison section.
    """
    return (
        "Summarize this athlete's playing style in 3-5 sentences.\n\n"
        f"ATHLETE PROFILE:\n{profile_to_text(profile)}\n"
    )


def analyze_style(profile, include_pro_comparisons=False):
    """Return an AI style summary, or the fallback summary when there is no API key."""
    if not has_api_key():
        return (
            "🧪 **DEMO MODE (no API key): the AI analysis is skipped.**\n\n"
            + fallback_style_summary(profile)
        )
    prompt = build_style_analysis_prompt(profile, include_pro_comparisons)
    return ask_llm(
        "You are a careful sports coach who never invents facts.",
        [{"role": "user", "content": prompt}],
    )


# ==================================================
# FEATURE 2: Build the personalized coaching prompt
# ==================================================
def build_coaching_system_prompt(profile):
    """Build the "system prompt" that tells the LLM who it is and who it's coaching.

    The system prompt is sent with EVERY request. Because we rebuild it from the
    profile each time, a changed profile automatically changes the advice.

    Parameters:
        profile (dict): the athlete profile.

    Returns:
        str: the system prompt.
    """
    sport = profile.get("sport", "their sport")

    prompt = (
        f"You are a friendly, knowledgeable {sport} coach.\n\n"
        f"ABOUT THE ATHLETE:\n{profile_to_text(profile)}\n\n"
    )

    # Once the athlete has confirmed an AI style summary, the coach uses it too.
    if profile.get("style_confirmed") and profile.get("style_summary"):
        prompt += f"CONFIRMED SUMMARY OF THEIR PLAYING STYLE:\n{profile['style_summary']}\n\n"

    # TODO 1: Add instructions that depend on the profile. For example, a left-handed
    #         athlete should not get advice that assumes a right hand, a beginner
    #         needs simpler language, and the athlete's preferences should be respected.
    #         Add each one to `prompt` only when it applies.
    #
    # TODO 2: Finish with rules that apply to everyone: a safety rule (the coach
    #         should say so when something is unsafe or ineffective and suggest
    #         a safer alternative) and a rule to keep answers short and practical.
    return prompt


# ==================================================
# FEATURE 3: Connect the profile to the chatbot
# ==================================================
def get_coaching_response(message, history, profile):
    """Produce the coach's reply to the user's newest message.

    Parameters:
        message (str): what the user just typed.
        history (list[dict]): earlier messages, each {"role": ..., "content": ...}.
            The AI has no memory of its own, so we must send the history again
            with every request. That is what makes "What about my left hand?" work.
        profile (dict): the athlete profile.

    Returns:
        str: the coach's reply.
    """
    if not profile:
        return "Please create your profile on the first tab so I can coach you personally."

    # TODO 1: Build the system prompt for this athlete (Feature 2).
    # TODO 2: Build the list of messages to send: the earlier history PLUS the
    #         new user message (same format as the history items).
    # TODO 3: Send both to ask_llm (imported above) and return its reply.
    return "🚧 The coach is not connected yet. Finish Feature 3 in coach.py."
