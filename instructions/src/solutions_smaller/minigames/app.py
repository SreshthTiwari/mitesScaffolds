"""
app.py -- the Gradio user interface.

This file only does two things:
  1. Lays out the screen (the build_app function at the bottom).
  2. Defines "handler" functions that run when the student clicks something.

Handlers should be SHORT: they call functions from the other files
(levels.py, challenges.py, progress.py, ai_helper.py) and return the results.

Run it with:   python app.py
"""

import gradio as gr

import ai_helper
import challenges
import progress as prog
from levels import LEVELS, MAX_QUIZ_QUESTIONS, get_level_choices, get_lesson


# --------------------------------------------------
# Small helpers
# --------------------------------------------------
def render_status(state):
    """Turn the progress dictionary into a Markdown summary."""
    lines = ["### Your progress"]
    for level_id in LEVELS:
        if prog.is_unlocked(state, level_id):
            done = state["completed"][level_id]
            ticks = " | ".join(
                f"{'✅' if done[a] else '⬜'} {a}" for a in prog.REQUIRED_ACTIVITIES
            )
            lines.append(f"- **{LEVELS[level_id]['title']}**: {ticks}")
        else:
            lines.append(f"- 🔒 {LEVELS[level_id]['title']}")
    return "\n".join(lines)


def quiz_updates(level_id):
    """Return one gr.update() per quiz Radio: show the questions that exist, hide the rest."""
    questions = challenges.get_quiz_questions(level_id)
    updates = []
    for i in range(MAX_QUIZ_QUESTIONS):
        if i < len(questions):
            updates.append(gr.update(label=questions[i]["question"],
                                     choices=questions[i]["choices"],
                                     value=None, visible=True))
        else:
            updates.append(gr.update(visible=False, value=None))
    return updates


# --------------------------------------------------
# Handlers
# --------------------------------------------------
# ==================================================
# FEATURE 1: Select a level + show its lesson
# ==================================================
def on_level_change(level_id, state):
    """Runs when the dropdown changes. Fills in every tab for that level."""
    if not prog.is_unlocked(state, level_id):
        locked = "🔒 This level is locked. Finish the previous level first!"
        return [locked, "", "", gr.update(choices=[], value=None), *quiz_updates_empty()]

    lesson = get_lesson(level_id)  # <- Feature 1: you write this in levels.py

    exercise = LEVELS[level_id]["exercise"]
    exercise_text = f"**{exercise['prompt']}**" if exercise else "No exercise written for this level yet."

    challenge = challenges.get_debug_challenge(level_id)
    if challenge:
        buggy_code, question, choices = challenge
        debug_radio = gr.update(label=question, choices=choices, value=None)
    else:
        buggy_code = "# No debugging challenge written for this level yet."
        debug_radio = gr.update(label="Pick an answer", choices=[], value=None)

    return [lesson, exercise_text, buggy_code, debug_radio, *quiz_updates(level_id)]


def quiz_updates_empty():
    return [gr.update(visible=False, value=None) for _ in range(MAX_QUIZ_QUESTIONS)]


# ==================================================
# FEATURE 3: Coding practice (uses check_exercise in challenges.py)
# ==================================================
def on_submit_exercise(level_id, user_answer, state):
    """Runs when the student clicks Submit in the Practice tab."""
    if not prog.is_unlocked(state, level_id):
        return "🔒 Level is locked.", state, render_status(state)

    is_correct, feedback = challenges.check_exercise(level_id, user_answer)
    if is_correct:
        state = prog.record_activity(state, level_id, "exercise")
        state = prog.unlock_next_level(state, level_id)  # <- Feature 5: you write this in progress.py
    prefix = "✅ " if is_correct else "❌ "
    return prefix + feedback, state, render_status(state)


# ==================================================
# Debugging challenge
# ==================================================
def on_submit_debug(level_id, selected_choice, state):
    """Runs when the student clicks Check Answer in the Debug tab."""
    if not prog.is_unlocked(state, level_id):
        return "🔒 Level is locked.", state, render_status(state)

    is_correct, feedback = challenges.check_debug_answer(level_id, selected_choice)
    if is_correct:
        state = prog.record_activity(state, level_id, "debug")
        state = prog.unlock_next_level(state, level_id)
    prefix = "✅ " if is_correct else "❌ "
    return prefix + feedback, state, render_status(state)


# ==================================================
# FEATURE 4: Quiz (uses score_quiz in challenges.py)
# ==================================================
PASSING_FRACTION = 0.6  # student needs 60% to pass. Change it if you like!


def on_submit_quiz(level_id, state, *answers):
    """Runs when the student clicks Submit Quiz. `answers` has one entry per Radio."""
    if not prog.is_unlocked(state, level_id):
        return "🔒 Level is locked.", state, render_status(state)

    score, total, feedback = challenges.score_quiz(level_id, list(answers))
    if total > 0 and score / total >= PASSING_FRACTION:
        state = prog.record_activity(state, level_id, "quiz")
        state["quiz_scores"][level_id] = max(score, state["quiz_scores"].get(level_id, 0))
        state = prog.unlock_next_level(state, level_id)
    return f"Score: {score}/{total}\n\n{feedback}", state, render_status(state)


# ==================================================
# AI hints (finished for you; see Optional Extensions)
# ==================================================
def on_hint(level_id, activity, user_attempt):
    """Runs when the student clicks 'Get a hint' (activity is 'exercise' or 'debug')."""
    level = LEVELS[level_id]
    if activity == "exercise" and level["exercise"]:
        question = level["exercise"]["prompt"]
    elif activity == "debug" and level["debug"]:
        question = level["debug"]["question"] + "\n" + level["debug"]["buggy_code"]
    else:
        return "No activity here yet, so no hint available."
    return ai_helper.get_hint(level["title"], activity, question, user_attempt or "")


# --------------------------------------------------
# The screen layout
# --------------------------------------------------
def build_app():
    first_level = get_level_choices()[0][1]

    with gr.Blocks(title="Minigames") as demo:
        gr.Markdown("# 🎮 Minigames: Learn Python by Playing")

        # One shared progress dictionary per browser session.
        # It resets when the page is refreshed (see progress.py).
        state = gr.State(prog.new_progress())

        level_dropdown = gr.Dropdown(
            choices=get_level_choices(), value=first_level, label="Choose a level"
        )
        status_md = gr.Markdown(render_status(prog.new_progress()))

        with gr.Tabs():
            with gr.Tab("1. Learn"):
                lesson_md = gr.Markdown(get_lesson(first_level))

            with gr.Tab("2. Practice"):
                exercise_md = gr.Markdown(f"**{LEVELS[first_level]['exercise']['prompt']}**")
                code_box = gr.Textbox(label="Your answer", lines=3, placeholder="Type your code here")
                with gr.Row():
                    submit_btn = gr.Button("Submit", variant="primary")
                    practice_hint_btn = gr.Button("Get a hint")
                practice_out = gr.Textbox(label="Feedback", interactive=False)

            with gr.Tab("3. Debug"):
                buggy_code, debug_q, debug_choices = challenges.get_debug_challenge(first_level)
                debug_code = gr.Code(value=buggy_code, language="python",
                                     label="Buggy code", interactive=False)
                debug_radio = gr.Radio(choices=debug_choices, label=debug_q)
                with gr.Row():
                    debug_btn = gr.Button("Check answer", variant="primary")
                    debug_hint_btn = gr.Button("Get a hint")
                debug_out = gr.Textbox(label="Feedback", interactive=False)

            with gr.Tab("4. Quiz"):
                quiz_radios = [gr.Radio(choices=[], label=f"Question {i + 1}", visible=False)
                               for i in range(MAX_QUIZ_QUESTIONS)]
                quiz_btn = gr.Button("Submit quiz", variant="primary")
                quiz_out = gr.Textbox(label="Results", interactive=False, lines=4)

        # Show the first level's quiz right away.
        # (Radio components are created hidden, so we refresh them on load.)
        demo.load(lambda: quiz_updates(first_level), outputs=quiz_radios)

        # ---- Wire buttons to handlers ----
        level_dropdown.change(
            on_level_change,
            inputs=[level_dropdown, state],
            outputs=[lesson_md, exercise_md, debug_code, debug_radio, *quiz_radios],
        )
        submit_btn.click(on_submit_exercise,
                         inputs=[level_dropdown, code_box, state],
                         outputs=[practice_out, state, status_md])
        debug_btn.click(on_submit_debug,
                        inputs=[level_dropdown, debug_radio, state],
                        outputs=[debug_out, state, status_md])
        quiz_btn.click(on_submit_quiz,
                       inputs=[level_dropdown, state, *quiz_radios],
                       outputs=[quiz_out, state, status_md])
        practice_hint_btn.click(lambda lvl, txt: on_hint(lvl, "exercise", txt),
                                inputs=[level_dropdown, code_box], outputs=practice_out)
        debug_hint_btn.click(lambda lvl, pick: on_hint(lvl, "debug", pick),
                             inputs=[level_dropdown, debug_radio], outputs=debug_out)

    return demo


if __name__ == "__main__":
    build_app().launch()
