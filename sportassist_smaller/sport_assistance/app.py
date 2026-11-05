"""
app.py -- the Gradio user interface.

Run with:  python app.py   (then open the link printed in the terminal)

How Gradio works in one paragraph:
  You create components (Textbox, Dropdown, Button...). You connect a button to a
  Python function with  button.click(fn, inputs=[...], outputs=[...]).
  When clicked, Gradio passes the current values of `inputs` to `fn` as arguments,
  and puts whatever `fn` returns into `outputs`.

gr.State holds Python values (like our profile dictionary) that are remembered
between clicks for ONE browser session. Each visitor gets their own copy.
"""

import gradio as gr

from ai_helper import has_api_key
from coach import (
    analyze_style,
    fallback_style_summary,
    get_coaching_response,
    get_coaching_topics,
)
from profile import add_style_description, create_profile, side_matters, update_profile

SPORTS = ["basketball", "soccer", "volleyball", "tennis", "dance"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
SIDES = ["Right", "Left", "Both"]
EDITABLE_FIELDS = ["preferences", "strengths", "weaknesses", "experience", "handedness"]

NEED_PROFILE = "⚠️ Please create your profile on the first tab."


# ==================================================
# COMPLETE EXAMPLE: connecting Gradio input -> Python -> Gradio output
# ==================================================
# Read this one carefully; the other handlers follow the same pattern.
#
#   inputs  (from the UI) : sport, experience, handedness, strengths, weaknesses, preferences
#   outputs (to the UI)   : profile_state (stored dict), a status message, topic dropdown
def handle_save_profile(sport, experience, handedness, strengths, weaknesses, preferences):
    # 1. Turn raw form values into a profile dictionary (your Feature 1 code).
    profile = create_profile(sport, experience, handedness, strengths, weaknesses, preferences)

    # 2. Build the text we'll show the user.
    topics = get_coaching_topics(sport)
    message = f"✅ Profile saved for **{sport}**.\n\n" + fallback_style_summary(profile)

    # 3. Return one value per output component, in the same order as `outputs=[...]`.
    #    gr.update(...) changes a component's properties (here: the dropdown choices).
    return profile, message, gr.update(choices=topics, value=topics[0])


def handle_sport_change(sport):
    """When the sport dropdown changes, show/hide handedness and refresh topics."""
    topics = get_coaching_topics(sport)
    return (
        gr.update(visible=side_matters(sport)),
        gr.update(choices=topics, value=topics[0]),
    )


# ---------- Optional tab: playing style ----------
def handle_style_fallback(profile, style_text):
    if not profile:
        return profile, NEED_PROFILE
    profile = add_style_description(profile, style_text)
    return profile, fallback_style_summary(profile)


def handle_style_ai(profile, style_text, include_pros):
    if not profile:
        return profile, NEED_PROFILE, ""
    profile = add_style_description(profile, style_text)
    summary = analyze_style(profile, include_pros)
    return profile, summary, summary  # second copy fills the editable "confirm" box


def handle_confirm_style(profile, edited_summary):
    """The user confirms (or corrects, by editing) the style summary."""
    if not profile:
        return profile, NEED_PROFILE
    if not edited_summary.strip():
        return profile, "Nothing to confirm yet. Run a style analysis first."
    profile = update_profile(profile, "style_summary", edited_summary.strip())
    profile = update_profile(profile, "style_confirmed", True)
    return profile, "Summary confirmed. Your coach will use it in every answer."


# ---------- Feature 3: chat ----------
def handle_chat(message, chat_history, profile):
    """Called when the user sends a chat message.

    chat_history is a list like:
        [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    Because it lives in gr.State, it is still there on the next message, and we
    send it to the AI so it can answer follow-up questions in context.
    """
    if not message.strip():
        return "", chat_history, chat_history
    if not profile:
        profile = {}  # coach.py handles an empty profile in demo mode

    # This is finished. Follow the call into coach.get_coaching_response (Feature 3).
    reply = get_coaching_response(message, chat_history, profile)

    chat_history = chat_history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    # Outputs: clear the textbox, update the visible Chatbot, update the saved State.
    return "", chat_history, chat_history


# ---------- Optional tab: update profile ----------
def handle_update_profile(profile, field, new_value):
    if not profile:
        return profile, NEED_PROFILE
    profile = update_profile(profile, field, new_value)
    return profile, "Updated profile:\n\n" + fallback_style_summary(profile)


# ==================================================
# The page layout
# ==================================================
with gr.Blocks(title="Sport Assistance") as demo:
    gr.Markdown("# 🏅 Sport Assistance\nA personalized AI sports coach.")
    if not has_api_key():
        gr.Markdown(
            "> 🧪 **Demo mode:** no `GEMINI_API_KEY` found. "
            "The app works, but coach replies are canned examples."
        )

    # Session state: one copy per visitor, remembered between clicks.
    profile_state = gr.State({})   # the athlete profile dictionary
    chat_state = gr.State([])      # the conversation history (list of message dicts)

    with gr.Tabs():
        # ---------------- Tab 1: Feature 1 ----------------
        with gr.Tab("1. Profile"):
            sport = gr.Dropdown(SPORTS, value="basketball", label="Sport")
            experience = gr.Radio(LEVELS, value="Beginner", label="Experience level")
            handedness = gr.Radio(SIDES, value="Right", label="Dominant hand / foot")
            strengths = gr.Textbox(label="Strengths (comma-separated)", placeholder="passing, speed")
            weaknesses = gr.Textbox(label="Weaknesses (comma-separated)", placeholder="free throws")
            preferences = gr.Textbox(label="Preferences", placeholder="short drills, no gym access")
            topics = gr.Dropdown(get_coaching_topics("basketball"), label="Coaching topics for this sport")
            save_btn = gr.Button("Save profile", variant="primary")
            profile_msg = gr.Markdown()

            sport.change(handle_sport_change, inputs=sport, outputs=[handedness, topics])
            save_btn.click(
                handle_save_profile,
                inputs=[sport, experience, handedness, strengths, weaknesses, preferences],
                outputs=[profile_state, profile_msg, topics],
            )

        # ---------------- Tab 2: optional (playing style) ----------------
        with gr.Tab("2. Playing style"):
            style_text = gr.Textbox(
                lines=4, label="Describe how you play, in your own words",
                placeholder="I'm patient, I like to set up teammates, I avoid driving left...",
            )
            include_pros = gr.Checkbox(label="Include illustrative pro-athlete comparisons (optional, not verified)")
            with gr.Row():
                fallback_btn = gr.Button("Quick summary (no AI)")
                ai_btn = gr.Button("AI style analysis", variant="primary")
            style_out = gr.Markdown()
            style_edit = gr.Textbox(lines=5, label="Confirm or correct the summary (edit the text, then confirm)")
            confirm_btn = gr.Button("Confirm summary")
            confirm_msg = gr.Markdown()

            fallback_btn.click(handle_style_fallback, [profile_state, style_text], [profile_state, style_out])
            ai_btn.click(handle_style_ai, [profile_state, style_text, include_pros], [profile_state, style_out, style_edit])
            confirm_btn.click(handle_confirm_style, [profile_state, style_edit], [profile_state, confirm_msg])

        # ---------------- Tab 3: Features 2 & 3 (the chat) ----------------
        with gr.Tab("3. Chat with your coach"):
            chatbot = gr.Chatbot(type="messages", height=380, label="Coach", allow_tags=False)
            msg_box = gr.Textbox(label="Your message", placeholder="How can I improve my...?")
            msg_box.submit(handle_chat, [msg_box, chat_state, profile_state], [msg_box, chatbot, chat_state])

        # ---------------- Tab 4: optional (update profile) ----------------
        with gr.Tab("4. Update profile"):
            gr.Markdown("Change something or correct the coach's understanding. Later chat replies will use it.")
            field = gr.Dropdown(EDITABLE_FIELDS, value="preferences", label="Field to change")
            new_value = gr.Textbox(label="New value (use commas for strengths/weaknesses)")
            update_btn = gr.Button("Update")
            update_msg = gr.Markdown()
            update_btn.click(handle_update_profile, [profile_state, field, new_value], [profile_state, update_msg])

if __name__ == "__main__":
    demo.launch()
