"""
feedback.py -- turns the user's choices into an AI request, and turns the
AI's answer into something nice to read.

Flow inside this file:
   choices -> get_improvement_instructions() -> build_prompt()
           -> (ai_helper sends it) -> format_feedback()
"""

from ai_helper import ask_ai_about_image

# ==================================================
# FEATURE 2: Choose an Improvement Area
# ==================================================
IMPROVEMENT_AREAS = ["Shading", "Composition", "Color", "Proportions", "General feedback"]


def get_improvement_instructions(area):
    """Return a sentence telling the AI what to focus on."""
    # TODO (Feature 2): Return a different focus sentence for each area in
    #   IMPROVEMENT_AREAS. Anything unexpected should fall back to an
    #   instruction that covers the whole artwork.

    return "Give general feedback on this artwork."


# ==================================================
# FEATURE 3: Build the AI Prompt
# ==================================================
def build_prompt(style, area, instructions):
    """Build the full text prompt that is sent to the AI along with the image."""
    # TODO (Feature 3): Build and return the prompt string. It should
    #   - give the AI a role (who is it?),
    #   - mention the target `style` and the improvement `area`,
    #   - include `instructions`,
    #   - ask for the answer in three sections labelled exactly
    #     STRENGTHS:, AREAS TO IMPROVE: and EXERCISES:
    #     (format_feedback below splits the answer on those labels).

    return "Give feedback on this artwork."


# ==================================================
# Pipeline and formatting -- already done for you
# ==================================================
def get_critique(image, style, area):
    """Run the whole pipeline and return the final text."""
    instructions = get_improvement_instructions(area)
    prompt = build_prompt(style, area, instructions)
    ai_text, is_real = ask_ai_about_image(image, prompt)

    if not is_real:
        return ai_text  # demo/error messages are shown as-is, never "formatted"
    return format_feedback(ai_text)


def format_feedback(ai_text):
    """Turn the AI's three labelled sections into a nicely headed result.

    If the AI did not use the labels from your prompt, the raw text is shown
    instead, so a prompt that forgets the labels still gives an answer.
    """
    text = ai_text.replace("**", "")  # models sometimes bold the labels
    labels = ["STRENGTHS:", "AREAS TO IMPROVE:", "EXERCISES:"]
    if not all(label in text for label in labels):
        return ai_text

    rest, exercises = text.split("EXERCISES:", 1)
    strengths, improve = rest.split("AREAS TO IMPROVE:", 1)
    strengths = strengths.replace("STRENGTHS:", "").strip()
    return (
        f"## ✅ Strengths\n{strengths}\n\n"
        f"## 🔧 Areas to Improve\n{improve.strip()}\n\n"
        f"## 🏋️ Suggested Exercises\n{exercises.strip()}"
    )
