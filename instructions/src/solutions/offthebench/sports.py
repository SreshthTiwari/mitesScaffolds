"""
sports.py - Sport and skill-level options.

This file answers two questions:
  1. Which sports can the user pick, and which skills can we analyze?
  2. What should we tell users of different experience levels?
"""

# ==================================================
# FEATURE 1: Choose a Sport
# ==================================================
# A dictionary maps each sport to a list of skills a student could analyze.
SPORTS = {
    "basketball": ["jump shot (release)", "free throw stance", "dribbling stance", "layup takeoff"],
    "soccer": ["instep kick (plant foot)", "throw-in", "goalkeeper ready stance", "header setup"],
    "volleyball": ["overhead set", "forearm pass (platform)", "spike approach", "serve toss"],
    "dance": ["arabesque", "plie", "arm positions", "balance pose"],
    "tennis": ["serve toss", "forehand contact", "backhand preparation", "ready position"],
}

# ==================================================
# FEATURE 2: Choose a Skill Level
# ==================================================
SKILL_LEVELS = ["beginner", "intermediate", "advanced"]


def get_sport_names():
    """Return the list of sports for the dropdown."""
    return list(SPORTS.keys())


def get_skills(sport):
    """Return the example skills for a sport (empty list if unknown)."""
    return SPORTS.get(sport, [])


# (Done: "tennis" was added to SPORTS above.)


def get_sport_instructions(sport):
    """
    Return a short photo-taking tip for the chosen sport.

    Good tips matter because camera angle affects every measurement later!
    """
    if sport == "basketball":
        return ("Photograph from the side at about chest height. Make sure your shooting "
                "arm, shoulder and hip are all in the frame.")
    elif sport == "soccer":
        return ("Photograph from the side, at about knee height, so the kicking leg, the "
                "plant-foot knee and the ankle are all in the frame.")
    elif sport == "tennis":
        return ("Photograph from the side or slightly behind, at about waist height. "
                "Keep the hitting arm, shoulder, hip and both knees in the frame.")
    elif sport == "volleyball":
        return ("Photograph from the side at about chest height. Make sure both arms, "
                "both shoulders and both knees are in the frame.")
    elif sport == "dance":
        return ("Photograph from the front or the side against a plain background. Wear "
                "fitted clothing and keep your whole body, head to toes, in the frame.")
    else:
        return "Make sure your whole body is visible and well lit."


def get_level_guidance(level):
    """
    Return a sentence describing how feedback should be tailored to a level.
    Used by feedback.py and ai_helper.py.
    """
    if level == "beginner":
        return "Give one or two simple, encouraging tips. Avoid jargon."
    elif level == "intermediate":
        return "Give two or three tips that mention specific body positions, with a short reason for each."
    elif level == "advanced":
        return "Give detailed, technical tips about small adjustments, and mention trade-offs."
    else:
        return "Give general feedback."
