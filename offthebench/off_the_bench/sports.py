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


# TODO 1: Add one more sport to SPORTS above (tennis? swimming? yoga?).
#         Does the rest of the app still work? Why or why not?


def get_sport_instructions(sport):
    """
    Return a short photo-taking tip for the chosen sport.

    Good tips matter because camera angle affects every measurement later!
    """
    # TODO 2: Finish the if/elif/else below. Basketball is done as an example.
    #         Write tips that say which body parts must be visible and
    #         which side the camera should be on.
    if sport == "basketball":
        return ("Photograph from the side at about chest height. Make sure your shooting "
                "arm, shoulder and hip are all in the frame.")
    elif sport == "soccer":
        return "TODO: write a tip for soccer."
    elif sport == "volleyball":
        return "TODO: write a tip for volleyball."
    elif sport == "dance":
        return "TODO: write a tip for dance."
    else:
        return "Make sure your whole body is visible and well lit."


def get_level_guidance(level):
    """
    Return a sentence describing how feedback should be tailored to a level.
    Used by feedback.py and ai_helper.py.
    """
    # TODO 3: Finish this if/elif/else. Think about it: should a beginner
    #         get 1 simple tip or 5 detailed ones? What about an advanced athlete?
    if level == "beginner":
        return "Give one or two simple, encouraging tips. Avoid jargon."
    elif level == "intermediate":
        return "TODO: describe feedback for intermediate athletes."
    elif level == "advanced":
        return "TODO: describe feedback for advanced athletes."
    else:
        return "Give general feedback."
