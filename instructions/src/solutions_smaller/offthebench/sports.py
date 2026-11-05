"""
sports.py - Sport and skill-level options.

This file answers two questions:
  1. Which sports can the user pick, and which skills can we analyze?
  2. What should we tell users of different experience levels?

app.py builds its dropdowns from this file, and feedback.py and ai_helper.py
both call get_level_guidance().
"""

# ==================================================
# FEATURE 1: Sports and Skill Levels
# ==================================================
# A dictionary maps each sport to a list of skills a student could analyze.
SPORTS = {
    "basketball": ["jump shot (release)", "free throw stance", "dribbling stance", "layup takeoff"],
    "soccer": ["instep kick (plant foot)", "throw-in", "goalkeeper ready stance", "header setup"],
    "volleyball": ["overhead set", "forearm pass (platform)", "spike approach", "serve toss"],
    "dance": ["arabesque", "plie", "arm positions", "balance pose"],
    "tennis": ["forehand ready position", "serve toss", "backhand stance", "volley stance"],
}

SKILL_LEVELS = ["beginner", "intermediate", "advanced"]


def get_sport_names():
    """Return the list of sports for the dropdown."""
    return list(SPORTS.keys())


def get_skills(sport):
    """Return the example skills for a sport (empty list if unknown)."""
    return SPORTS.get(sport, [])


def get_sport_instructions(sport):
    """
    Return a short photo-taking tip for the chosen sport.
    (Camera angle changes every measurement later, so these tips matter.)
    """
    if sport == "basketball":
        return ("Photograph from the side at about chest height. Make sure your shooting "
                "arm, shoulder and hip are all in the frame.")
    elif sport == "soccer":
        return ("Photograph from the side at about hip height, at the moment the foot "
                "plants. Show the hip, knee and ankle of the planted leg.")
    elif sport == "volleyball":
        return ("Photograph from the side or slightly in front. Make sure both arms, "
                "shoulders and hips are visible.")
    elif sport == "dance":
        return ("Photograph from the front or side with the whole body in frame, "
                "from head to feet, against a plain background.")
    else:
        return "Make sure your whole body is visible and well lit."


def get_level_guidance(level):
    """
    Return one sentence describing how feedback should be tailored to a level.
    It is shown to the user AND passed to the AI in ai_helper.py.
    """
    if level == "beginner":
        return "Give one or two simple, encouraging tips. Avoid jargon."
    elif level == "intermediate":
        return "Give two or three tips that connect the measurements to the movement."
    elif level == "advanced":
        return "Give three or four specific, technical tips and mention small details."
    else:
        return "Give general feedback."
