"""
coach.py -- turning an athlete profile into prompts, and prompts into coaching.

A "prompt" is just a string of text we send to the LLM. The LLM knows nothing
about the user, so WE must put the profile into the text. That is the core idea
of this whole project:

    profile dict  ->  prompt string  ->  LLM  ->  personalized advice
"""

from ai_helper import ask_llm, has_api_key

# ==================================================
# FEATURE 1: Choose a sport
# ==================================================
GENERAL_TOPICS = ["Warm-up and recovery", "Mental focus", "Building consistency"]


def get_coaching_topics(sport):
    """Return a list of coaching topics that make sense for the chosen sport.

    Parameters:
        sport (str): e.g. "basketball"

    Returns:
        list[str]: topic names shown in the UI dropdown.
    """
    # Basketball is done for you as an example of the pattern:
    if sport == "basketball":
        return ["Shooting form", "Ball handling", "Defense", "Court vision"] + GENERAL_TOPICS

    # TODO 1: Add elif branches for soccer, volleyball, tennis and dance.
    #         Give each 3-4 topics specific to that sport.
    # TODO 2: Keep the final `else` so unknown sports still get the general topics.
    else:
        return GENERAL_TOPICS


# ==================================================
# FEATURE 3: Describe your playing style (no-LLM fallback)
# ==================================================
def fallback_style_summary(profile):
    """Summarize the profile WITHOUT calling an LLM (complete, provided).

    This is a "fallback": simple Python string formatting that always works,
    even with no API key or internet.
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
# FEATURE 4: AI playing-style analysis
# ==================================================
def build_style_analysis_prompt(profile, include_pro_comparisons=False):
    """Build the prompt asking the LLM to summarize the user's playing style.

    Parameters:
        profile (dict): the athlete profile (including "style_text").
        include_pro_comparisons (bool): if True, ask for OPTIONAL illustrative
            comparisons to professional athletes.

    Returns:
        str: the prompt to send to the LLM.
    """
    prompt = (
        "Summarize this athlete's playing style in 3-5 sentences.\n\n"
        f"ATHLETE PROFILE:\n{profile_to_text(profile)}\n"
    )

    # TODO 1: Add rules so the model does NOT invent facts. For example:
    #         "Only use information given above. If something is unknown, say so."
    # TODO 2: Ask for two short lists: "Possible strengths" and "Possible tendencies",
    #         and tell the model to word them as possibilities ("may", "seems").
    # TODO 3: End by asking the athlete to confirm or correct the summary.

    # TODO 4: Use if/else on include_pro_comparisons. When True, append a section
    #         titled "Illustrative comparisons (NOT verified matches)" asking for
    #         1-2 well-known athletes with a similar *described* style, and tell the
    #         model to avoid claiming statistics or facts it is not sure about.
    return prompt


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
# FEATURE 5: Personalized Coaching
# ==================================================
def build_coaching_system_prompt(profile):
    """Build the "system prompt" that tells the LLM who it is and who it's coaching.

    The system prompt is sent with EVERY request. Because we rebuild it from the
    profile each time, profile updates (Feature 7) automatically affect the advice.

    Parameters:
        profile (dict): the athlete profile.

    Returns:
        str: the system prompt.
    """
    # TODO 1: Get the athlete's sport and playing style from the profile.
    sport = profile.get("sport", "their sport")

    prompt = (
        f"You are a friendly, knowledgeable {sport} coach.\n\n"
        f"ABOUT THE ATHLETE:\n{profile_to_text(profile)}\n\n"
    )

    # TODO 2: Use if/else to identify relevant preferences. For example:
    #   - If handedness is "Left", add: "The athlete is left-handed. Do not assume
    #     right-handed technique; mirror any right-handed examples."
    #   - If handedness is "Both", mention both sides can be trained.
    #   - If the experience is "Beginner", ask for simpler language and basics first.
    #   - If the preferences text is not empty, tell the model to respect it.
    #
    # TODO 3: Add these details to the prompt string (prompt += "...").
    #
    # TODO 4 (safety): Add a rule such as: "Respect the athlete's preferences, but
    #   if a technique could be unsafe or ineffective, say so clearly, explain why,
    #   and suggest a safer alternative. Do not make claims about professional
    #   athletes or performance results you are not sure about."
    #
    # TODO 5: Add a rule about style: keep answers concise and practical.
    return prompt


def get_coaching_response(message, history, profile):
    """Produce the coach's reply to the user's newest message.

    Parameters:
        message (str): what the user just typed.
        history (list[dict]): earlier messages, each {"role": ..., "content": ...}.
            Sending history lets the AI remember what was already said, so
            "What about my left hand?" makes sense as a follow-up.
        profile (dict): the athlete profile.

    Returns:
        str: the coach's reply.
    """
    # TODO (optional): If the profile is empty, return a friendly reminder to
    #                  fill in the profile first.

    if not has_api_key():
        return demo_response(message, profile)

    system_prompt = build_coaching_system_prompt(profile)           # who the AI is + athlete info
    messages = list(history) + [{"role": "user", "content": message}]  # past + new message
    return ask_llm(system_prompt, messages)


def demo_response(message, profile):
    """Canned reply used when there is no API key (complete, provided).

    Clearly labeled as demo behavior. It proves the UI, state, and profile
    plumbing work, but it is NOT real coaching.
    """
    sport = profile.get("sport", "your sport")
    side = profile.get("handedness", "N/A")
    side_note = f" I can see you're **{side}**-sided." if side not in ("N/A", None) else ""
    topics = ", ".join(get_coaching_topics(profile.get("sport", ""))[:3])
    return (
        "🧪 **DEMO MODE: no API key found, so this is a canned reply, not real AI.**\n\n"
        f"You said: \"{message}\"\n\n"
        f"I would coach you on **{sport}**.{side_note} "
        f"Topics I could cover: {topics}.\n\n"
        "Add an `ANTHROPIC_API_KEY` to your `.env` file to get real, personalized advice."
    )
