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
    if area == "Shading":
        return "Focus on how light and shadow create form and depth."
    elif area == "Composition":
        return "Focus on how the elements are arranged and where the eye is led."
    elif area == "Color":
        return "Focus on the color palette, contrast, and mood."
    elif area == "Proportions":
        return "Focus on the size and placement of shapes relative to each other."
    else:
        return "Give feedback on the whole artwork: strengths, weaknesses, and next steps."


# ==================================================
# FEATURE 3: Build the AI Prompt
# ==================================================
def build_prompt(style, area, instructions):
    """Build the full text prompt that is sent to the AI along with the image."""
    prompt = "You are a kind, encouraging art teacher.\n"
    prompt += f"The student wants to move toward the {style} style and improve their {area}.\n"
    prompt += instructions + "\n"
    prompt += "Answer in exactly three sections, labelled like this:\n"
    prompt += "STRENGTHS:\nAREAS TO IMPROVE:\nEXERCISES:\n"
    prompt += "Use short bullet points in each section."
    return prompt


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
