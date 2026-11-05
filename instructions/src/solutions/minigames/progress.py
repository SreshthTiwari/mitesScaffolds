"""
progress.py -- tracks what the student has finished.

We use ONE dictionary (not classes) to hold everything. It looks like:

    {
        "unlocked":  ["print"],                      # level ids the student may play
        "completed": {"print": {"exercise": True,    # what's done in each level
                                "debug": False,
                                "quiz": False}},
        "quiz_scores": {"print": 2},                 # best quiz score per level
    }

HOW GRADIO STATE WORKS (important!)
-----------------------------------
app.py stores this dictionary in a `gr.State`. That gives every browser tab
its own private copy while the page is open. BUT:
  * It lives in memory only. Refresh the page and it resets to new_progress().
  * It is NOT saved to disk, a database, or an account.
  * Handlers should RETURN the updated dictionary so Gradio saves the change.
If you want progress to survive a refresh, that's an optional extension
(for example, save it to a JSON file).
"""

from levels import LEVEL_ORDER

# Activities a student must finish to complete a level.
REQUIRED_ACTIVITIES = ["exercise", "debug", "quiz"]


def new_progress():
    """Create a fresh progress dictionary. Only the first level is unlocked."""
    completed = {}
    for level_id in LEVEL_ORDER:
        completed[level_id] = {"exercise": False, "debug": False, "quiz": False}
    return {
        "unlocked": [LEVEL_ORDER[0]],
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


# ==================================================
# FEATURE 6: Level progression
# ==================================================
def is_level_complete(progress, level_id):
    """Return True if every required activity in this level is finished."""
    done = progress["completed"][level_id]
    for activity in REQUIRED_ACTIVITIES:
        if not done[activity]:
            return False
    return True


def unlock_next_level(progress, level_id):
    """If `level_id` is complete, add the NEXT level to progress["unlocked"]."""
    if not is_level_complete(progress, level_id):
        return progress

    position = LEVEL_ORDER.index(level_id)
    if position + 1 < len(LEVEL_ORDER):
        next_level = LEVEL_ORDER[position + 1]
        if next_level not in progress["unlocked"]:
            progress["unlocked"].append(next_level)
    return progress
