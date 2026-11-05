"""
app.py - The Gradio user interface for "Off the Bench".

Run with:  python app.py   then open the link shown in the terminal.

FLOW: choose sport -> upload image -> detect landmarks -> analyze -> feedback
"""

import gradio as gr

try:  # optional: load API keys from .env
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import ai_helper
import feedback
import pose_analysis
import sports


# ==================================================
# FEATURE 1: Choose a Sport (helper for the UI)
# ==================================================
def show_sport_info(sport):
    """Runs when the sport dropdown changes."""
    skills = ", ".join(sports.get_skills(sport))
    return f"**Example skills to analyze:** {skills}\n\n**Photo tip:** {sports.get_sport_instructions(sport)}"


# ==================================================
# FEATURE 3: Upload a Technique Image
# ==================================================
# HOW IMAGES WORK IN PYTHON:
#   An image is a NumPy array of numbers with shape (height, width, 3).
#   The 3 is red, green, blue; each value is 0-255. Gradio hands us this array
#   (because we set type="numpy"), and we pass the same array to other functions.
def describe_image(image):
    """Return a short description of the uploaded image, or an error message."""
    if image is None:
        return "No image uploaded yet."
    height, width = image.shape[:2]
    # TODO 1: Also report the number of color channels (image.shape[2]).
    #         Why might a PNG have 4 channels?
    return f"Image received: {width} x {height} pixels."


# ==================================================
# Main handler: connects every feature
# ==================================================
def analyze(sport, level, image, use_pose, use_ai, consent_to_send_image):
    """Runs when the user clicks "Analyze". Returns one value per output component."""
    # Step 1: validate the upload
    if image is None:
        return "Please upload an image first.", None, "", "", ""
    status = describe_image(image)
    shown_image = image
    measurements_text, suggestions_text, ai_text = "", "", ""
    measurements = []

    # Step 2: detect landmarks (optional)
    if use_pose:
        pose = pose_analysis.detect_pose(image)
        status += f"\n\nPose: {pose['status']}"
        shown_image = pose["annotated_image"]

        # Step 3: measure (facts from the photo)
        if pose["found"]:
            measurements = feedback.analyze_pose(pose["landmarks"], sport)
            lines = []
            for m in measurements:
                value = "n/a" if m["value"] is None else f"~{m['value']:.0f} degrees"
                lines.append(f"- {m['name']}: {value} ({m['label']})")
            measurements_text = "\n".join(lines)
            # TODO 2: Improve how measurements are displayed (rounding, units, grouping).

    # Step 4: coaching suggestions (interpretation of the facts)
    suggestions = feedback.build_suggestions(sport, level, measurements)
    # TODO 3: Format `suggestions` nicely (numbered list? headings?).
    suggestions_text = "\n".join(f"- {s}" for s in suggestions) + f"\n\n_{feedback.DISCLAIMER}_"

    # Step 5: optional AI feedback
    if use_ai:
        prompt = ai_helper.build_prompt(sport, level, measurements)
        raw = ai_helper.get_ai_feedback(prompt, image, consent_to_send_image)
        ai_text = ai_helper.format_ai_feedback(raw)

    return status, shown_image, measurements_text, suggestions_text, ai_text


# ==================================================
# The Gradio layout
# ==================================================
pose_ready, pose_message = pose_analysis.check_pose_setup()
ai_ready, ai_message = ai_helper.is_ai_available()

with gr.Blocks(title="Off the Bench") as demo:
    gr.Markdown("# Off the Bench\nUpload a photo of a movement and get technique ideas.\n\n"
                "_Single photos can't prove a whole movement is right or wrong._")
    gr.Markdown(f"Setup status: {pose_message} | {ai_message}")

    with gr.Row():
        with gr.Column():
            sport = gr.Dropdown(sports.get_sport_names(), value="basketball", label="Sport")
            level = gr.Radio(sports.SKILL_LEVELS, value="beginner", label="Skill level")
            sport_info = gr.Markdown(show_sport_info("basketball"))
            image = gr.Image(type="numpy", label="Upload your technique photo")
            use_pose = gr.Checkbox(value=pose_ready, label="Detect body landmarks (MediaPipe, runs locally)")
            use_ai = gr.Checkbox(value=False, label="Also ask an AI model for suggestions (optional)")
            consent = gr.Checkbox(value=False, label="I consent to sending my photo to the AI service "
                                                     "(otherwise only text measurements are sent)")
            button = gr.Button("Analyze", variant="primary")
        with gr.Column():
            status = gr.Textbox(label="Status", lines=3)
            output_image = gr.Image(label="Detected landmarks")
            gr.Markdown("### Measurements (from the photo)")
            measurements_out = gr.Markdown()
            gr.Markdown("### Coaching suggestions (interpretation)")
            suggestions_out = gr.Markdown()
            gr.Markdown("### AI suggestions (optional)")
            ai_out = gr.Markdown()

    sport.change(show_sport_info, inputs=sport, outputs=sport_info)
    button.click(analyze,
                 inputs=[sport, level, image, use_pose, use_ai, consent],
                 outputs=[status, output_image, measurements_out, suggestions_out, ai_out])

if __name__ == "__main__":
    demo.launch()
