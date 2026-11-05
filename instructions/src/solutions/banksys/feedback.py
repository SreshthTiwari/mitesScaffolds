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
    if area == "Shading":
        return "Focus on how light and shadow create form and depth."
    elif area == "Composition":
        return ("Focus on how the subjects are arranged in the frame: balance, "
                "focal point, and where the eye travels.")
    elif area == "Color":
        return ("Focus on the color choices: harmony, contrast, and whether the "
                "palette fits the mood.")
    elif area == "Proportions":
        return ("Focus on the relative size and placement of shapes and body "
                "parts: do they look believable?")
    else:
        return "Give feedback on the whole piece: shading, composition, color, and proportions."


# ==================================================
# FEATURE 4: AI Artwork Critique
# ==================================================
def build_prompt(style, area, instructions):
    """Build the full text prompt that is sent to the AI along with the image."""
    prompt = "You are a kind, encouraging art teacher.\n\n"
    prompt += f"The student wants to move toward the {style} style.\n"
    prompt += f"They would like help with: {area}.\n"
    prompt += instructions + "\n\n"
    prompt += (
        "Reply in exactly three labelled sections, in this order:\n"
        "STRENGTHS:\n"
        "AREAS TO IMPROVE:\n"
        "EXERCISES:\n"
        "Keep each section short and use bullet points."
    )
    return prompt


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
    # If the AI ignored our format, show its answer untouched.
    if ("STRENGTHS:" not in ai_text or "AREAS TO IMPROVE:" not in ai_text
            or "EXERCISES:" not in ai_text):
        return ai_text

    before, rest = ai_text.split("STRENGTHS:", 1)
    strengths, rest = rest.split("AREAS TO IMPROVE:", 1)
    improvements, exercises = rest.split("EXERCISES:", 1)

    return (
        "## Strengths\n" + strengths.strip() + "\n\n"
        "## Areas to Improve\n" + improvements.strip() + "\n\n"
        "## Suggested Exercises\n" + exercises.strip()
    )


# BONUS: models sometimes write "**STRENGTHS:**" in bold. After splitting, the
# leftover "**" would show up in the output, so strip it too.
def clean_section(section):
    """Strip whitespace and any stray ** left over from bold section headings."""
    return section.strip().strip("*").strip()
