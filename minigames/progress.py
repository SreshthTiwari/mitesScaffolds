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
    """
    Return True if every required activity in this level is finished.

    TODO 1: Get the level's dictionary:  progress["completed"][level_id]
    TODO 2: Loop over REQUIRED_ACTIVITIES.
    TODO 3: If ANY activity is False, return False right away.
    TODO 4: If the loop finishes without returning, return True.
    """
    return False  # placeholder so the app runs -- replace this!


def unlock_next_level(progress, level_id):
    """
    If `level_id` is complete, add the NEXT level to progress["unlocked"].

    TODO 1: Call is_level_complete(). If it's False, return progress unchanged.
    TODO 2: Find the position of level_id in LEVEL_ORDER (list.index()).
    TODO 3: If there IS a next level (position + 1 < len(LEVEL_ORDER)),
            get its id.
    TODO 4: If it isn't already in progress["unlocked"], append it.
    TODO 5: Return progress.
    TODO 6 (stretch): return a message too, like "You unlocked Variables!",
            so app.py can show it to the student.
    """
    return progress  # placeholder -- replace this!
