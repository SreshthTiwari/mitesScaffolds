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
    """Check the student's typed answer. Returns (is_correct, feedback)."""
    exercise = LEVELS[level_id]["exercise"]
    if exercise is None:
        return False, "This level has no exercise yet. Write one in levels.py!"

    cleaned = user_answer.strip()
    squashed = cleaned.replace(" ", "")  # ignore spaces: 'print( "Hi" )' still matches

    for accepted in exercise["accepted_answers"]:
        if squashed == accepted.replace(" ", ""):
            return True, "Correct! Nice work."

    # Not correct: look for common mistakes by comparing with the first accepted answer.
    expected = exercise["accepted_answers"][0]
    if cleaned == "":
        return False, "Type your answer in the box first."
    if "print" in expected and "print" not in cleaned:
        return False, "Did you use print()?"
    if ('"' in expected or "'" in expected) and '"' not in cleaned and "'" not in cleaned:
        return False, "Don't forget the quotes."
    if ")" in expected and ")" not in cleaned:
        return False, "Check your parentheses."
    if expected.endswith(":") and not cleaned.endswith(":"):
        return False, "Don't forget the colon at the end of the line."
    return False, "Not quite. Compare your line with the example in the Learn tab, or press 'Get a hint'."


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
    """Check the answer the student picked. Returns (is_correct, feedback)."""
    if selected_choice is None:
        return False, "Pick an answer first."

    debug = LEVELS[level_id]["debug"]
    if debug is None:
        return False, "This level has no debugging challenge yet."

    if selected_choice == debug["correct"]:
        return True, "Correct! You found the bug."
    return False, (
        "Not that one. Read the buggy code again, one line at a time, and ask: "
        "what would Python complain about first?"
    )


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
    """Score the quiz. Returns (score, total, feedback)."""
    questions = get_quiz_questions(level_id)
    score = 0
    missed = []

    for i in range(len(questions)):
        if user_answers[i] == questions[i]["answer"]:
            score += 1
        else:
            missed.append(f"Question {i + 1}: not quite. Review the Learn tab and try again.")

    feedback = f"You got {score} out of {len(questions)}!"
    if missed:
        feedback += "\n" + "\n".join(missed)
    return score, len(questions), feedback
