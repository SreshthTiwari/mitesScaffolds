"""
levels.py -- the CONTENT of the game.

Everything a student sees (lessons, exercises, debugging puzzles, quizzes)
lives here as plain Python dictionaries. Each level looks like this:

    "level_id": {
        "title":       "Level 1: Print Statements",
        "explanation": "Short text shown in the Learn tab.",
        "example":     "A code example shown in the Learn tab.",
        "exercise":    {"prompt": "...", "accepted_answers": ["...", "..."]},
        "debug":       {"buggy_code": "...", "question": "...",
                        "choices": ["...", "..."], "correct": "..."},
        "quiz":        [{"question": "...", "choices": [...], "answer": "..."}],
    }

Four levels are finished, so you can see what good content looks like.
YOUR JOB: write the "loops" level (FEATURE 2) and get_lesson() (FEATURE 1).
"""

# The order levels unlock in (progress.py uses this list).
LEVEL_ORDER = ["print", "variables", "conditionals", "loops", "functions"]

# How many quiz questions the screen has room for (see app.py).
MAX_QUIZ_QUESTIONS = 3


LEVELS = {
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

    "variables": {
        "title": "Level 2: Variables",
        "explanation": "A variable is a named box that stores a value. Write name = value to fill the box.",
        "example": 'age = 15\nname = "Sam"\nprint(age)',
        "exercise": {
            "prompt": "Write one line of Python that creates a variable age storing the number 15.",
            "accepted_answers": ["age = 15"],
        },
        "debug": {
            "buggy_code": 'my name = "Sam"\nprint(my name)',
            "question": "This code crashes. What is wrong with it?",
            "choices": ["Strings must use single quotes", "print cannot show variables",
                        "Variable names cannot contain spaces", "The = must be written =="],
            "correct": "Variable names cannot contain spaces",
        },
        "quiz": [
            {
                "question": "Which line stores the number 7 in a variable called lives?",
                "choices": ["7 = lives", "lives = 7", "lives == 7", "store lives 7"],
                "answer": "lives = 7",
            },
            {
                "question": "After x = 5 and then x = 9, what does print(x) show?",
                "choices": ["5", "14", "9", "Error"],
                "answer": "9",
            },
            {
                "question": "Which of these values is a string?",
                "choices": ["15", '"15"', "15.5", "True"],
                "answer": '"15"',
            },
        ],
    },

    "conditionals": {
        "title": "Level 3: Conditionals",
        "explanation": (
            "An if statement lets your program make a decision. Python checks "
            "the condition after if. If it is True, the indented lines run. Use "
            "elif to check another condition, and else for everything left over. "
            "The if line must end with a colon, and the lines inside must be indented."
        ),
        "example": (
            "temperature = 30\n"
            "if temperature > 25:\n"
            '    print("It is hot")\n'
            "elif temperature > 15:\n"
            '    print("It is nice")\n'
            "else:\n"
            '    print("It is cold")'
        ),
        "exercise": {
            "prompt": "Write the first line of an if statement that checks whether score is greater than 10. (Include the colon.)",
            "accepted_answers": ["if score > 10:"],
        },
        "debug": {
            "buggy_code": 'age = 16\nif age >= 16\n    print("You can drive")',
            "question": "This code crashes with a SyntaxError. What is wrong with it?",
            "choices": [
                "age must be written in quotes",
                "print must come before if",
                "else is required after every if",
                "The if line is missing a colon at the end",
            ],
            "correct": "The if line is missing a colon at the end",
        },
        "quiz": [
            {
                "question": "What does == do in Python?",
                "choices": ["Stores a value", "Compares two values", "Prints a value", "Ends the program"],
                "answer": "Compares two values",
            },
            {
                "question": "With x = 3, which part runs: if x > 5: ... else: ... ?",
                "choices": ["The if part", "Both parts", "The else part", "Neither part"],
                "answer": "The else part",
            },
            {
                "question": "How does Python know which lines belong inside an if?",
                "choices": [
                    "They are in quotes",
                    "They are indented",
                    "They end with a semicolon",
                    "They are in capital letters",
                ],
                "answer": "They are indented",
            },
        ],
    },

    "loops": {
        "title": "Level 4: Loops",
        "explanation": (
            "A loop repeats code. A for loop repeats a set number of times, "
            "often with range(). A while loop keeps repeating as long as its "
            "condition is True, so something inside the loop must eventually "
            "make the condition False."
        ),
        "example": (
            "for i in range(3):\n"
            '    print("Hello")\n'
            "\n"
            "count = 0\n"
            "while count < 3:\n"
            "    count = count + 1"
        ),
        "exercise": {
            "prompt": "Write the first line of a for loop that uses the variable i and repeats 5 times using range. (Include the colon.)",
            "accepted_answers": ["for i in range(5):"],
        },
        "debug": {
            "buggy_code": "count = 0\nwhile count < 3:\n    print(count)",
            "question": "This program never stops. What is wrong with it?",
            "choices": [
                "range is missing",
                "count is never increased, so the condition is always True",
                "print cannot be used in a loop",
                "while must be written With a capital W",
            ],
            "correct": "count is never increased, so the condition is always True",
        },
        "quiz": [
            {
                "question": "How many times does a loop with range(4) repeat?",
                "choices": ["3", "5", "4", "0"],
                "answer": "4",
            },
            {
                "question": "Which loop keeps going while a condition is True?",
                "choices": ["for", "while", "if", "def"],
                "answer": "while",
            },
            {
                "question": "What numbers does range(3) produce?",
                "choices": ["1, 2, 3", "0, 1, 2, 3", "3", "0, 1, 2"],
                "answer": "0, 1, 2",
            },
        ],
    },

    "functions": {
        "title": "Level 5: Functions",
        "explanation": (
            "A function is a named block of code you can reuse. Start it with "
            "def, give it a name, and list its parameters in parentheses. Use "
            "return to send a value back to whoever called the function. "
            "Defining a function does not run it: you must call it."
        ),
        "example": "def add(a, b):\n    return a + b\n\nprint(add(2, 3))",
        "exercise": {
            "prompt": "Write the first line of a function named greet that takes one parameter called name. (Include the colon.)",
            "accepted_answers": ["def greet(name):"],
        },
        "debug": {
            "buggy_code": "def double(x):\n    x * 2\n\nprint(double(4))",
            "question": "This prints None instead of 8. What is wrong with it?",
            "choices": [
                "x must be written in quotes",
                "The function never returns the result",
                "def must be capitalized",
                "double is a reserved word",
            ],
            "correct": "The function never returns the result",
        },
        "quiz": [
            {
                "question": "Which keyword starts a function definition?",
                "choices": ["func", "define", "def", "function"],
                "answer": "def",
            },
            {
                "question": "What does return do?",
                "choices": [
                    "Prints a value on the screen",
                    "Sends a value back to the caller",
                    "Repeats the function",
                    "Deletes the function",
                ],
                "answer": "Sends a value back to the caller",
            },
            {
                "question": "In def add(a, b), what are a and b called?",
                "choices": ["Loops", "Quotes", "Modules", "Parameters"],
                "answer": "Parameters",
            },
        ],
    },
}


def get_level_choices():
    """
    Build the list of choices for the Gradio dropdown. Provided for you.

    Gradio dropdowns accept (label, value) pairs: the user SEES the label,
    and our code RECEIVES the value (the level id like "print").
    """
    choices = []
    for level_id in LEVEL_ORDER:
        choices.append((LEVELS[level_id]["title"], level_id))
    return choices


# ==================================================
# FEATURE 1: Show a lesson
# ==================================================
def get_lesson(level_id):
    """Return the lesson text (a Markdown string) for the chosen level."""
    if level_id not in LEVELS:
        return "Unknown level. Please choose a level from the dropdown."

    level = LEVELS[level_id]

    if level["explanation"].startswith("TODO"):
        return f"## {level['title']}\n\nComing soon! This lesson has not been written yet."

    return (
        f"## {level['title']}\n\n"
        f"{level['explanation']}\n\n"
        f"**Example:**\n```python\n{level['example']}\n```"
    )
