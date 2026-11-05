"""
progress.py -- tracks what the student has finished.

We use ONE dictionary to hold everything. It looks like:

    {
        "unlocked":  ["print"],                      # level ids the student may play
        "completed": {"print": {"exercise": True,    # what's done in each level
                                "debug": False,
                                "quiz": False}},
        "quiz_scores": {"print": 2},                 # best quiz score per level
    }

HOW GRADIO STATE WORKS
----------------------
app.py stores this dictionary in a `gr.State`: every browser tab gets its own
copy. It lives in memory only, so refreshing the page resets it. Handlers
RETURN the updated dictionary so Gradio saves the change.
"""

from levels import LEVEL_ORDER

# Activities a student must finish to complete a level.
REQUIRED_ACTIVITIES = ["exercise", "debug", "quiz"]

# While you test your own level, set this to True so every level starts
# unlocked. Set it back to False before you finish, or unlocking never runs!
UNLOCK_ALL_FOR_TESTING = False


def new_progress():
    """Create a fresh progress dictionary. Only the first level is unlocked."""
    completed = {}
    for level_id in LEVEL_ORDER:
        completed[level_id] = {"exercise": False, "debug": False, "quiz": False}
    unlocked = list(LEVEL_ORDER) if UNLOCK_ALL_FOR_TESTING else [LEVEL_ORDER[0]]
    return {
        "unlocked": unlocked,
        "completed": completed,
        "quiz_scores": {},
    }


def is_unlocked(progress, level_id):
    """True if the student is allowed to play this level."""
    return level_id in progress["unlocked"]


def record_activity(progress, level_id, activity):
    """Mark one activity ("exercise", "debug", or "quiz") as done. Returns progress."""
    progress["completed"][level_id][activity] = True
    return progress


def is_level_complete(progress, level_id):
    """True if every required activity in this level is finished."""
    done = progress["completed"][level_id]
    return all(done[activity] for activity in REQUIRED_ACTIVITIES)


# ==================================================
# FEATURE 5: Unlock the next level
# ==================================================
def unlock_next_level(progress, level_id):
    """
    If `level_id` is complete, make the NEXT level in LEVEL_ORDER playable by
    adding its id to progress["unlocked"]. Always return progress.

    app.py calls this after every correct activity, so it will run several
    times for the same level. Be careful not to add the same level twice,
    and remember the last level has no "next" one.

    TODO: write it. (is_level_complete() above is ready to use.)
    """
    if not is_level_complete(progress, level_id):
        return progress

    position = LEVEL_ORDER.index(level_id)
    if position + 1 < len(LEVEL_ORDER):
        next_level = LEVEL_ORDER[position + 1]
        if next_level not in progress["unlocked"]:
            progress["unlocked"].append(next_level)
    return progress
