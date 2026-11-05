"""
app.py -- the Gradio user interface for The Banksys.

BIG PICTURE
    user clicks/uploads in the browser
        -> Gradio calls one of the Python functions below
        -> that function calls feedback.py / art_styles.py
        -> feedback.py calls ai_helper.py
        -> the returned text travels back and Gradio displays it

Run with:  python app.py
"""

import gradio as gr

from ai_helper import has_api_key
from art_styles import get_style_description, get_style_names
from feedback import IMPROVEMENT_AREAS, get_critique


# ==================================================
# FEATURE 1: Learn About Art Styles (event handler)
# ==================================================
def show_style(style_name):
    # Gradio passes the dropdown's current value in as `style_name`.
    # Whatever we return goes into the output component (a Textbox).
    return get_style_description(style_name)


# ==================================================
# FEATURE 2: Upload Artwork (event handler)
# ==================================================
def handle_upload(image):
    # HOW THE IMAGE TRAVELS:
    #   1. The user drops a file into gr.Image in the browser.
    #   2. Gradio uploads it and, because we set type="pil", converts it to a
    #      PIL Image object.
    #   3. Gradio calls this function and passes that object as `image`.
    #   4. If nothing is uploaded, `image` is None.
    #
    # TODO 1 (optional): Also report the image size.
    #         PIL images have .width and .height, e.g. f"{image.width}x{image.height}"
    if image is None:
        return "No artwork uploaded yet."
    return "✅ Artwork received!"


# ==================================================
# FEATURES 3-5: Critique (event handler)
# ==================================================
def handle_critique(image, style, area):
    # The inputs list on the button (see below) decides the order of these
    # three arguments: image, style, area.
    if image is None:
        return "Please upload artwork in the 'Upload Artwork' tab first."
    if not style:
        return "Please choose a target art style."
    return get_critique(image, style, area)


# ==================================================
# The user interface
# ==================================================
with gr.Blocks(title="The Banksys") as demo:
    gr.Markdown("# 🎨 The Banksys\nYour AI art learning assistant.")

    if not has_api_key():
        gr.Markdown(
            "⚠️ **Demo mode:** no API key found. The AI will NOT analyze images. "
            "See README.md to add a key."
        )

    # The upload component is created here so BOTH tabs can use it.
    # (Components defined inside a tab are still just Python variables!)
    with gr.Tab("1. Learn About Styles"):
        style_dropdown = gr.Dropdown(choices=get_style_names(), label="Choose a style")
        style_output = gr.Textbox(label="Description", lines=4)
        style_dropdown.change(show_style, inputs=style_dropdown, outputs=style_output)

    with gr.Tab("2. Upload Artwork"):
        image_input = gr.Image(type="pil", label="Your artwork")
        upload_status = gr.Textbox(label="Status")
        image_input.change(handle_upload, inputs=image_input, outputs=upload_status)

    with gr.Tab("3. Get Feedback"):
        gr.Markdown("Uses the artwork from the Upload tab.")
        target_style = gr.Dropdown(choices=get_style_names(), label="Target art style")
        area_choice = gr.Radio(choices=IMPROVEMENT_AREAS, value="General feedback",
                               label="What do you want to improve?")
        critique_button = gr.Button("Get feedback", variant="primary")
        critique_output = gr.Markdown(label="Feedback")
        critique_button.click(
            handle_critique,
            inputs=[image_input, target_style, area_choice],
            outputs=critique_output,
        )

if __name__ == "__main__":
    demo.launch()
