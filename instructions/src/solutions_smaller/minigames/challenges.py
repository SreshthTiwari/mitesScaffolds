"""
challenges.py -- the checking logic for exercises, debugging, and quizzes.

SAFETY RULE: we never run (exec/eval) code a student types. We only compare
their answer to fixed, expected answers. That is safe and also lets us give
precise feedback. The AI is only used for HINTS, never to decide correct/wrong.

Every checker returns plain values (True/False and a feedback string) and
does NOT touch Gradio. app.py takes care of the UI.
"""

from levels import LEVELS


# ==================================================
# FEATURE 3: Check a practice answer
# ==================================================
def check_exercise(level_id, user_answer):
    """
    Check the student's typed answer. Returns (is_correct, feedback).

    A basic version works already, but it is picky: the answer must match one
    of the "accepted_answers" in levels.py EXACTLY.

    TODO 1: Make it forgiving about spaces, so  print( "Hi" )  still matches
            print("Hi").
    TODO 2: When the answer is wrong, give a more helpful message than
            "Not quite". Look for common mistakes: a missing quote, a missing
            ")" or a missing ":" at the end of a line.
    """
    exercise = LEVELS[level_id]["exercise"]
    if exercise is None:
        return False, "This level has no exercise yet. Write one in levels.py!"

    cleaned = user_answer.strip()
    squashed = cleaned.replace(" ", "")  # ignore spaces: 'print( "Hi" )' still matches

    for accepted in exercise["accepted_answers"]:
        if squashed == accepted.replace(" ", ""):
            return True, "Correct! Nice work."

    # Wrong: compare with the first accepted answer to spot common mistakes.
    expected = exercise["accepted_answers"][0]
    if cleaned == "":
        return False, "Type your answer in the box first."
    if ('"' in expected or "'" in expected) and '"' not in cleaned and "'" not in cleaned:
        return False, "Don't forget the quotes."
    if ")" in expected and ")" not in cleaned:
        return False, "Check your parentheses."
    if expected.endswith(":") and not cleaned.endswith(":"):
        return False, "Don't forget the colon at the end of the line."
    return False, "Not quite. Compare your line with the example in the Learn tab, or press 'Get a hint'."


# ==================================================
# Debugging challenge (provided: you wrote the puzzle data in levels.py)
# ==================================================
def get_debug_challenge(level_id):
    """Return (buggy_code, question, choices) for a level, or None if it has none."""
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


# ==================================================
# FEATURE 4: Score a quiz
# ==================================================
def get_quiz_questions(level_id):
    """Return the list of quiz question dictionaries for a level (may be empty)."""
    return LEVELS[level_id]["quiz"]


def score_quiz(level_id, user_answers):
    """
    Score the quiz. `user_answers` is a list of the choices the student
    picked, in the same order as the questions (an entry is None if they
    skipped it). Each question dictionary has an "answer" key.

    Returns (score, total, feedback):
      score    -- how many answers were correct
      total    -- how many questions there are
      feedback -- a message such as "You got 2 out of 3!" that also says
                  which question numbers were missed

    TODO: write it. Use get_quiz_questions(level_id) to get the questions.
    """
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
