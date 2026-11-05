# 🏅 Sport Assistance

A personalized conversational AI sports coach. You describe your sport, experience,
playing style, strengths, weaknesses and preferences, and an LLM coaches **you**
rather than giving generic tips.

The starter app **runs without an API key** (demo mode). Your job is to fill in the
`TODO`s so it becomes a real, personalized coach.

## How it works

```
 form inputs ──► profile dict ──► prompt string ──► LLM ──► personalized advice
 (Gradio)        (profile.py)     (coach.py)    (ai_helper.py)   (shown in Gradio)
```

1. **Profile.** The form values become a Python dictionary (`profile.py`), stored in a `gr.State` so it persists during the session.
2. **Prompt construction.** `coach.py` turns the dictionary into text (a *system prompt*): "You are a basketball coach. The athlete is left-handed, a beginner..." The LLM knows nothing about the user except what we write here.
3. **LLM call.** `ai_helper.py` sends the system prompt and the conversation to the API.
4. **Response.** The reply is shown in the Gradio chatbot.

### How the profile and chat history are used
- **Profile** is rebuilt into the system prompt on *every* message. If the user updates it (Feature 7), the next reply automatically reflects the change.
- **Chat history** (also in a `gr.State`) is sent along with each new message. LLMs have no memory of their own; without history, "what about my left hand?" would be meaningless to the model.

## Files

| File | Purpose |
|---|---|
| `app.py` | Gradio interface: profile form, style tab, chatbot, update tab. Contains one fully worked example handler (`handle_save_profile`). |
| `profile.py` | Create/update the profile dictionary (Features 2, 3, 7). |
| `coach.py` | Coaching topics, prompt building, demo/fallback responses (Features 1, 3, 4, 5, 6). |
| `ai_helper.py` | The only file that talks to the LLM API. You shouldn't need to edit it. |
| `requirements.txt` | Python packages. |
| `.env.example` | Template for your API key. |

> Note: `profile.py` shares its name with a rarely used Python standard-library module. This is harmless here, but avoid running `python -m cProfile` in this folder.

## Setup and launch

```bash
cd sport_assistance
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # optional: add your GEMINI_API_KEY
python app.py
```

Open the local URL printed in the terminal (usually http://127.0.0.1:7860).
With no key, a banner says you're in demo mode and coach replies are clearly labeled canned examples.

## Recommended implementation order

1. **Read `handle_save_profile` in `app.py`**, the complete example of input → Python → output. Run the app and click around.
2. **Feature 2: `create_profile`** (`profile.py`). Fill in all fields; print the dict to check it.
3. **Feature 1: `get_coaching_topics`** (`coach.py`). Add the other sports with `elif`.
4. **Feature 3: `add_style_description`** and try the "Quick summary (no AI)" button.
5. **Feature 5: `build_coaching_system_prompt`** (`coach.py`). Print the prompt and read it as if you were the LLM. Test with a left-handed profile.
6. **Feature 6**: trace `handle_chat` → `get_coaching_response` → `ask_llm`. Add your API key and chat. Watch how history gives follow-ups context.
7. **Feature 4: `build_style_analysis_prompt`** and `handle_confirm_style`. Check the summary doesn't invent facts and that pro comparisons are labeled illustrative.
8. **Feature 7: `update_profile`**. Change a preference, then confirm the next chat answer reflects it.

## Testing tips
- Compare coaching answers for two different profiles (e.g. left vs right-handed). If they're identical, the profile isn't reaching the prompt.
- Ask for something unsafe or ineffective; the coach should explain the risk rather than just comply.
- Treat pro-athlete comparisons as *illustrative only*. LLMs can be wrong about facts.

## Optional extensions
- **Save/load profiles** as a JSON file (`json.dump` / `json.load`) with a Download/Upload button.
- **Goal tracking:** add a `goals` list to the profile, mark goals done, and mention progress in the prompt.
- **Training plans:** a "Generate a weekly plan" button that uses profile + chosen topic.
- **Streaming replies** so text appears as it's written.
- **Swap the LLM provider** by editing only `ai_helper.py`.
