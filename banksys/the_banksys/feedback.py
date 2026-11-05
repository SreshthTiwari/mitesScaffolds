"""
feedback.py -- turns the user's choices into an AI request, and turns the
AI's answer into something nice to read.

Flow inside this file:
   choices -> get_improvement_instructions() -> build_prompt()
           -> (ai_helper sends it) -> format_feedback()
"""

from ai_helper import ask_ai_about_image

# ==================================================
# FEATURE 3: Choose an Improvement Area
# ==================================================
IMPROVEMENT_AREAS = ["Shading", "Composition", "Color", "Proportions", "General feedback"]


def get_improvement_instructions(area):
    """Return a sentence telling the AI what to focus on."""
    # TODO 1: Use if / elif / else to compare `area` to each choice.
    #         Example:
    #           if area == "Shading":
    #               return "Focus on how light and shadow create form and depth."
    #
    # TODO 2: Write a different instruction for Composition, Color, and
    #         Proportions. (What should the AI look at for each one?)
    #
    # TODO 3: Use else for "General feedback" (or anything unexpected) and
    #         return an instruction that covers the whole piece.

    return "Give general feedback on this artwork."


# ==================================================
# FEATURE 4: AI Artwork Critique
# ==================================================
def build_prompt(style, area, instructions):
    """Build the full text prompt that is sent to the AI along with the image."""
    # TODO 1: Start with a role, e.g. "You are a kind, encouraging art teacher."
    #
    # TODO 2: Combine strings with + or an f-string to mention the target style
    #         and the improvement area:
    #           f"The student wants to move toward the {style} style."
    #
    # TODO 3: Add `instructions` (from Feature 3) to the prompt.
    #
    # TODO 4: Ask for the answer in three labelled sections so Feature 5 can
    #         split it up: "STRENGTHS:", "AREAS TO IMPROVE:", "EXERCISES:".
    #
    # TODO 5: Return the finished prompt string.

    return "Give feedback on this artwork."


def get_critique(image, style, area):
    """Run the whole pipeline and return the final text. (Already wired up.)"""
    instructions = get_improvement_instructions(area)
    prompt = build_prompt(style, area, instructions)
    ai_text, is_real = ask_ai_about_image(image, prompt)

    if not is_real:
        return ai_text  # demo/error messages are shown as-is, never "formatted"
    return format_feedback(ai_text)


# ==================================================
# FEATURE 5: Personalized Improvement Suggestions
# ==================================================
# Target output format (what the user should see):
#
#   ## ✅ Strengths
#   - Nice use of contrast in the sky
#
#   ## 🔧 Areas to Improve
#   - The hand looks too small compared with the head
#
#   ## 🏋️ Suggested Exercises
#   1. Draw 10 hands from photos, 2 minutes each
#
def format_feedback(ai_text):
    """Organize the AI's raw answer into strengths / improvements / exercises."""
    # TODO 1: If your prompt asked for "STRENGTHS:", "AREAS TO IMPROVE:" and
    #         "EXERCISES:", split ai_text into three pieces.
    #         Hint: ai_text.split("AREAS TO IMPROVE:") gives a list of parts.
    #
    # TODO 2: Strip extra whitespace from each part with .strip().
    #
    # TODO 3: Build one string using the format above and return it.
    #         (Bonus: what if the AI forgot a section? Use if/else to handle it.)

    return ai_text  # for now, just show the raw answer
