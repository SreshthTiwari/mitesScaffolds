"""
levels.py -- the CONTENT of the game.

Everything a student sees (lessons, exercises, debugging puzzles, quizzes)
lives here as plain Python dictionaries. No logic, just data.

Each level looks like this:

    "level_id": {
        "title":       "Level 1: Print Statements",
        "explanation": "Short text shown in the Learn tab.",
        "example":     "A code example shown in the Learn tab.",
        "exercise":    {"prompt": "...", "accepted_answers": ["...", "..."]},
        "debug":       {"buggy_code": "...", "question": "...",
                        "choices": ["...", "..."], "correct": "..."},
        "quiz":        [{"question": "...", "choices": [...], "answer": "..."}],
    }

"print" is COMPLETE so you can see what a finished level looks like.
The other levels are stubs: filling them in is part of your job!
"""

# The order levels unlock in. You will use this list in progress.py
# to figure out which level comes "next".
LEVEL_ORDER = ["print", "variables", "conditionals", "loops", "functions"]

# How many quiz questions the UI has room for (see app.py).
MAX_QUIZ_QUESTIONS = 3


LEVELS = {
    # ------------------------------------------------------------
    # COMPLETED EXAMPLE LEVEL -- study this one, then copy its shape.
    # ------------------------------------------------------------
    "print": {
        "title": "Level 1: Print Statements",
        "explanation": (
            "The `print()` function shows text on the screen. Put the text "
            "you want to show inside quotes, and put the quotes inside the "
            "parentheses."
        ),
        "example": 'print("Hello, World!")',
        "exercise": {
            "prompt": "Write one line of Python that prints exactly: Hello, World!",
            "accepted_answers": [
                'print("Hello, World!")',
                "print('Hello, World!')",
            ],
        },
        "debug": {
            "buggy_code": 'print("Hello, World!"',
            "question": "This code crashes. What is wrong with it?",
            "choices": [
                "The closing parenthesis is missing",
                "print must be capitalized",
                "There must be a colon at the end",
                "Quotes are not allowed inside print()",
            ],
            "correct": "The closing parenthesis is missing",
        },
        "quiz": [
            {
                "question": "Which line prints the word cat?",
                "choices": ['print("cat")', "print(cat", 'Print("cat")', 'print "cat"'],
                "answer": 'print("cat")',
            },
            {
                "question": 'What does print("2" + "2") show?',
                "choices": ["4", "22", "Error", "2 + 2"],
                "answer": "22",
            },
            {
                "question": "What do the quotes around text in print() tell Python?",
                "choices": [
                    "The text is a string, not code",
                    "The text should be hidden",
                    "The text is a number",
                    "Nothing, they are optional",
                ],
                "answer": "The text is a string, not code",
            },
        ],
    },

    # ------------------------------------------------------------
    # STUDENT TASK: finish these levels.
    # Replace each TODO with real content. Use the "print" level above
    # as a model. Leave "exercise" as None until you write one.
    # ------------------------------------------------------------
    "variables": {
        "title": "Level 2: Variables",
        "explanation": "TODO: explain that a variable is a named box that stores a value.",
        "example": "TODO: e.g.  age = 15",
        "exercise": None,  # TODO: {"prompt": ..., "accepted_answers": [...]}
        "debug": None,     # TODO: {"buggy_code": ..., "question": ..., "choices": [...], "correct": ...}
        "quiz": [],        # TODO: a list of up to 3 question dictionaries
    },
    "conditionals": {
        "title": "Level 3: Conditionals",
        "explanation": "TODO: explain if / elif / else.",
        "example": "TODO",
        "exercise": None,
        "debug": None,
        "quiz": [],
    },
    "loops": {
        "title": "Level 4: Loops",
        "explanation": "TODO: explain for and while loops.",
        "example": "TODO",
        "exercise": None,
        "debug": None,
        "quiz": [],
    },
    "functions": {
        "title": "Level 5: Functions",
        "explanation": "TODO: explain def, parameters, and return.",
        "example": "TODO",
        "exercise": None,
        "debug": None,
        "quiz": [],
    },
}


# ==================================================
# FEATURE 1: Select a level
# ==================================================
def get_level_choices():
    """
    Build the list of choices for the Gradio dropdown.

    Gradio dropdowns accept (label, value) pairs: the user SEES the label,
    and our code RECEIVES the value (the level id like "print").

    This one is done for you so the app launches. TODO (optional): add a
    lock icon to the label of levels the student has not unlocked yet.
    That means passing the progress dictionary in as an argument.
    """
    choices = []
    for level_id in LEVEL_ORDER:
        choices.append((LEVELS[level_id]["title"], level_id))
    return choices


# ==================================================
# FEATURE 2: Learn a concept
# ==================================================
def get_lesson(level_id):
    """
    Return the lesson text (a Markdown string) for the chosen level.

    CURRENT STATE: only the "print" level works, using a simple if/else.
    TODO 1: Delete the if/else and instead look the level up in the LEVELS
            dictionary:  level = LEVELS[level_id]
    TODO 2: Use .get() or an `if level_id in LEVELS` check so an unknown
            level id returns a friendly message instead of crashing.
    TODO 3: Build the Markdown string from level["title"],
            level["explanation"] and level["example"] and return it.
            (Hint: the example should be wrapped in a ```python block.)
    TODO 4: If the explanation still starts with "TODO", return a
            "coming soon" message instead. (conditional + string method)
    """
    if level_id == "print":
        level = LEVELS["print"]
        return (
            f"## {level['title']}\n\n"
            f"{level['explanation']}\n\n"
            f"**Example:**\n```python\n{level['example']}\n```"
        )
    else:
        return "This lesson has not been implemented yet. See TODOs in levels.get_lesson()."
