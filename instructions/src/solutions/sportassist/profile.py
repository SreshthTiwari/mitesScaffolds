"""
profile.py -- creating and updating the athlete profile.

The profile is just a normal Python dictionary. Example of a finished profile:

    {
        "sport": "basketball",                # str  - the selected sport
        "experience": "Intermediate",         # str  - Beginner / Intermediate / Advanced
        "handedness": "Left",                 # str  - "Left", "Right", "Both", or "N/A"
        "strengths": ["passing", "court vision"],   # list[str]
        "weaknesses": ["free throws"],              # list[str]
        "preferences": "short drills, no gym access",   # str - how they like to train
        "style_text": "I like to slow the game down and set up teammates...",  # str
        "style_summary": "",                  # str  - AI or fallback summary of style
        "style_confirmed": False,             # bool - did the user confirm the summary?
    }

Gradio keeps this dictionary in a gr.State so it survives between button clicks.
"""

# Sports where left/right-handedness (or footedness) can change the advice.
SPORTS_WHERE_SIDE_MATTERS = ["basketball", "tennis", "volleyball", "soccer"]


def side_matters(sport):
    """Return True if handedness/footedness is relevant for this sport.

    Provided for you (complete). Dance, for example, returns False.
    """
    return sport in SPORTS_WHERE_SIDE_MATTERS


def split_list(text):
    """Turn "passing, speed ,  defense" into ["passing", "speed", "defense"].

    Provided for you (complete). Gradio textboxes give us ONE string, but a list
    is easier to work with in prompts.
    """
    return [item.strip() for item in text.split(",") if item.strip()]


# ==================================================
# FEATURE 2: Create an athlete profile
# ==================================================
def create_profile(sport, experience, handedness, strengths, weaknesses, preferences):
    """Build a brand-new profile dictionary from the form inputs.

    Parameters:
        sport (str): e.g. "tennis"
        experience (str): "Beginner", "Intermediate" or "Advanced"
        handedness (str): "Left", "Right", "Both" (may be ignored for some sports)
        strengths (str): comma-separated text, e.g. "serve, footwork"
        weaknesses (str): comma-separated text, e.g. "backhand"
        preferences (str): free text, e.g. "short drills, no equipment"

    Returns:
        dict: the profile (see the example at the top of this file).
    """
    # STARTER VERSION: only stores sport and experience, so the app runs.
    profile = {
        "sport": sport,
        "experience": experience,
        "handedness": "N/A",
        "strengths": [],
        "weaknesses": [],
        "preferences": "",
        "style_text": "",
        "style_summary": "",
        "style_confirmed": False,
    }

    if side_matters(sport):
        profile["handedness"] = handedness
    else:
        profile["handedness"] = "N/A"

    profile["strengths"] = split_list(strengths)
    profile["weaknesses"] = split_list(weaknesses)
    profile["preferences"] = preferences.strip()
    return profile


# ==================================================
# FEATURE 7: Update your profile
# ==================================================
def update_profile(profile, field, new_value):
    """Change ONE field of an existing profile and return the updated profile.

    Parameters:
        profile (dict): the current profile.
        field (str): which key to change, e.g. "preferences" or "strengths".
        new_value (str): the new value typed by the user.

    Returns:
        dict: the updated profile (a copy, so the original is untouched).
    """
    updated = dict(profile)  # copy, so we don't accidentally change the original

    if field in updated:
        if field in ("strengths", "weaknesses"):
            updated[field] = split_list(new_value)
        elif field == "style_confirmed":
            updated[field] = new_value is True  # a real True/False, never a string
        else:
            updated[field] = new_value
    return updated


# ==================================================
# FEATURE 3: Describe your playing style
# ==================================================
def add_style_description(profile, style_text):
    """Combine the user's free-text style description with the structured profile.

    Parameters:
        profile (dict): the current profile.
        style_text (str): the user's own words about how they play.

    Returns:
        dict: a copy of the profile that now includes the style text.
    """
    updated = dict(profile)
    updated["style_text"] = style_text.strip()
    updated["style_confirmed"] = False
    return updated
