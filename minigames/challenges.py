"""
challenges.py -- the checking logic for exercises, debugging, and quizzes.

SAFETY RULE: we never run (exec/eval) code a student types. We only compare
their answer to fixed, expected answers. That is safe and also lets us give
precise feedback. The LLM is only used for HINTS, never to decide correct/wrong.

Every checker returns plain values (True/False and a feedback string) and
does NOT touch Gradio. app.py takes care of the UI.
"""

from levels import LEVELS


# ==================================================
# FEATURE 3: Coding practice
# ==================================================
def check_exercise(level_id, user_answer):
    """
    Check the student's typed answer. Returns (is_correct, feedback).

    A basic WORKING version is provided. Your job is to make it better:
    TODO 1: Make comparison forgiving about whitespace inside the answer,
            e.g. 'print( "Hi" )' should match 'print("Hi")'.
            (Hint: str.replace(" ", "") on both sides.)
    TODO 2: Give different feedback for common mistakes using `in`:
            - answer is missing "print"  -> "Did you use print()?"
            - answer is missing a quote  -> "Don't forget the quotes."
            - answer is missing ")"      -> "Check your parentheses."
    TODO 3: Make the feedback friendlier and more helpful.
    """
    exercise = LEVELS[level_id]["exercise"]
    if exercise is None:
        return False, "This level has no exercise yet. Write one in levels.py!"

    cleaned = user_answer.strip()
    for accepted in exercise["accepted_answers"]:
        if cleaned == accepted:
            return True, "Correct! Nice work."
    return False, "Not quite. Try again, or press 'Get a hint'."


# ==================================================
# FEATURE 4: Debugging Challenge
# ==================================================
def get_debug_challenge(level_id):
    """
    Return (buggy_code, question, choices) for a level, or None if it has none.
    This is provided so the UI works. You may leave it as is.
    """
    debug = LEVELS[level_id]["debug"]
    if debug is None:
        return None
    return debug["buggy_code"], debug["question"], debug["choices"]


def check_debug_answer(level_id, selected_choice):
    """
    Check the answer the student picked. Returns (is_correct, feedback).

    TODO 1: Get the answer selected by the user (it's `selected_choice`).
            If it is None (nothing selected), return (False, "Pick an answer first.").
    TODO 2: Get the correct answer: LEVELS[level_id]["debug"]["correct"]
            (Check the level has a debug challenge first!)
    TODO 3: Use if/else to decide whether the answer is correct.
    TODO 4: Return (True/False, feedback). On a wrong answer, explain WHY
            without just giving the answer away.
    """
    return False, "TODO: implement check_debug_answer() in challenges.py"


# STRETCH TODO: Ask the LLM for a brand-new debugging challenge.
# Write ai_helper.generate_debug_challenge() first, then call it here.
# Remember: the LLM should return structured data (buggy_code, choices,
# correct), and YOUR code still does the checking.


# ==================================================
# FEATURE 5: Quiz
# ==================================================
def get_quiz_questions(level_id):
    """Return the list of quiz question dictionaries for a level (may be empty)."""
    return LEVELS[level_id]["quiz"]


def score_quiz(level_id, user_answers):
    """
    Score the quiz. `user_answers` is a list of the choices the student
    picked, in question order (an entry is None if they skipped it).

    Returns (score, total, feedback).

    TODO 1: Get the questions with get_quiz_questions(level_id).
    TODO 2: Create a counter:  score = 0
    TODO 3: Loop over the questions with their position, e.g.
            for i in range(len(questions)):
    TODO 4: Inside the loop, use if/else: if user_answers[i] equals
            questions[i]["answer"], add 1 to score. Otherwise, add a line to
            a feedback list saying which question was missed.
    TODO 5: Return score, len(questions), and a feedback string such as
            "You got 2 out of 3!" plus the missed-question notes.
    """
    questions = get_quiz_questions(level_id)
    return 0, len(questions), "TODO: implement score_quiz() in challenges.py"
