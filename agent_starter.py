"""
FROM CHATBOT TO AGENT (STARTER)

You will build, step by step:
  PART 1  an AI assistant (Study Buddy) that explains things and remembers the chat
  PART 2  turn it into an AI AGENT that writes your portfolio website into a folder

The difference:
  assistant:  you ask  ->  the AI answers with text for a HUMAN
  agent:      you ask  ->  the AI answers  ->  OUR CODE acts (saves files)  ->  you look and ask again

Your mission: finish the 5 TODOs below with your AI helper (vibe coding).
Rules:
  - Write a precise prompt (Context, Target, Constraints, Format).
  - One TODO at a time. Test after each one.
  - If something breaks, paste the FULL error message to your AI.
  - Read the code your AI writes before you run it.
  - Use FAKE or minimal personal info (free models may log prompts).
  - Never put your API key in the code. It lives in .env.

Run:  python agent_starter.py
"""
import os
import re
import shutil
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    timeout=float(os.getenv("TIMEOUT", "30")),  # seconds to wait for ONE model
    max_retries=0,
)

# Free models fail often (rate limits, empty answers), so we try several, one after another.
MODELS = [m.strip() for m in os.getenv("MODELS", "").split(",") if m.strip()]
MAX_TRIES = int(os.getenv("MAX_TRIES", "6"))  # max models tried for ONE question

calls = 0  # every request counts against your free daily quota (about 50)


# ---------------------------------------------------------------------------
# DONE FOR YOU: sends messages to the model, with automatic fallback.
# Returns (answer_text, model_used). You do not need to edit it.
# ---------------------------------------------------------------------------
def ask_model(messages, max_tokens=3500):
    global calls
    last_error = "no model configured (check MODELS in .env)"
    for model in MODELS[:MAX_TRIES]:
        try:
            calls += 1
            r = client.chat.completions.create(
                model=model, messages=messages, max_tokens=max_tokens
            )
            text = r.choices[0].message.content
            if text and text.strip():
                return text, model
            last_error = "empty answer"
        except Exception as e:
            last_error = type(e).__name__
        print(f"  ({model} failed: {last_error}. Trying the next model...)")
    raise RuntimeError(f"All models failed (last error: {last_error})")


# ---------------------------------------------------------------------------
# DONE FOR YOU: saves the files found in the model answer. Read it!
# The model answers with text. This script looks for blocks like:
#     ### FILE: index.html
#     ...content...
#     ### END
# SECURITY: an agent that writes files must be restricted.
#   - Path(...).name keeps only the file name, so "../../secret.html" can
#     never escape the portfolio/ folder.
#   - Only .html, .css and .js files are allowed.
#   - We never RUN anything the model wrote. We only save it.
# ---------------------------------------------------------------------------
OUTPUT_DIR = Path("portfolio")
ALLOWED_EXT = {".html", ".css", ".js"}
FILE_PATTERN = re.compile(r"###\s*FILE:\s*(.+?)\s*\n(.*?)\n###\s*END", re.DOTALL)


def strip_fences(code):
    """Models often wrap code in ``` fences. Remove them."""
    code = code.strip()
    code = re.sub(r"^```[a-zA-Z]*\n", "", code)
    code = re.sub(r"\n```$", "", code)
    return code


def save_files(text):
    OUTPUT_DIR.mkdir(exist_ok=True)
    saved = []
    for raw_path, content in FILE_PATTERN.findall(text):
        name = Path(raw_path.strip().strip("`")).name
        if Path(name).suffix.lower() not in ALLOWED_EXT:
            print(f"[skipped] {raw_path} (type not allowed)")
            continue
        target = OUTPUT_DIR / name
        target.write_text(strip_fences(content), encoding="utf-8")
        saved.append(str(target))
    return saved


def backup():
    """Save point: copy portfolio/ to portfolio_backup/ before an edit."""
    if OUTPUT_DIR.exists():
        shutil.copytree(OUTPUT_DIR, "portfolio_backup", dirs_exist_ok=True)


# ===========================================================================
# PART 1: THE ASSISTANT
# ===========================================================================

# ---------------------------------------------------------------------------
# TODO 1: the personality of your assistant (the SYSTEM prompt).
# Use CCCF (Context, Target, Constraints, Format):
#   Context     -> a friendly tutor called Study Buddy, for beginners
#   Target      -> explain concepts clearly
#   Constraints -> always answer in English with simple words, use one everyday
#                  analogy, 3 sentences maximum, say "I am not sure" instead of inventing
#   Format      -> short plain text
# ---------------------------------------------------------------------------
SYSTEM = ""


history = []  # the conversation of the assistant (so it remembers)


# ---------------------------------------------------------------------------
# TODO 2: chat(user_text): one round of conversation WITH MEMORY.
#   1. add the user message to `history`  ({"role": "user", "content": ...})
#   2. call ask_model([system message] + history)   -> returns (answer, model)
#   3. add the answer to `history`  (role "assistant") so the AI remembers
#   4. print the answer, the model used and how many requests were used (`calls`)
#   5. if ask_model raises RuntimeError: remove the last user message from
#      `history`, print a friendly error, and return
# Test: ask "What is a neuron?" then ask "Give me another analogy".
#       If the AI understands "another", your memory works.
# ---------------------------------------------------------------------------
def chat(user_text):
    print("TODO 2: chat() is not implemented yet.")


# ===========================================================================
# PART 2: THE AGENT
# ===========================================================================

# ---------------------------------------------------------------------------
# TODO 3: the system prompt of the AGENT (a web designer).
# The big new idea: save_files() above only understands this format, so your
# prompt MUST force the model to answer like this, for each file:
#     ### FILE: index.html
#     <content>
#     ### END
# This "contract" between your prompt and your code is the heart of an agent.
# Use CCCF:
#   Context     -> a web designer building a personal portfolio
#   Target      -> sections About, Skills, Projects, Contact
#   Constraints -> exactly 2 files (index.html + style.css), plain HTML and CSS,
#                  no JavaScript, no remote images, readable colors (good contrast
#                  for titles and links too), use ONLY the info given by the user
#   Format      -> the contract above, and NOTHING outside the files
# ---------------------------------------------------------------------------
SYSTEM_AGENT = ""


agent_history = []  # the conversation of the agent (so it remembers the current page)


# ---------------------------------------------------------------------------
# TODO 4: run_agent(user_text): one round of the agent (think -> act -> observe).
#   1. add the user message to `agent_history`
#   2. call ask_model([agent system message] + agent_history)
#   3. add the answer to `agent_history`
#   4. ACT: call save_files(answer). Print the saved files, the model used and `calls`
#   5. if no file was saved, print a hint
#   6. if ask_model raises RuntimeError: remove the last user message, print a friendly error
# It is almost the same as chat(). The new part is step 4: the code ACTS.
# ---------------------------------------------------------------------------
def run_agent(user_text):
    print("TODO 4: run_agent() is not implemented yet.")


HELP = "Commands: /explain <topic> | /build <about you> | /edit <change> | /quit\nAnything else is a normal chat."

if __name__ == "__main__":
    print("From Chatbot to Agent.")
    print(HELP)
    while True:
        text = input("You> ").strip()
        if not text:
            continue
        if text == "/quit":
            break
        if text.startswith("/explain "):
            chat("Explain this topic to a beginner: " + text[9:])
        # -------------------------------------------------------------------
        # TODO 5: the agent commands.
        #   /build <about you>  -> run_agent("Create the portfolio for this person: " + ...)
        #   /edit <change>      -> run_agent("Apply this change and output ALL the files
        #                          again, complete, in the same format: " + ...)
        # Why "complete"? Because save_files() overwrites the files.
        # Bonus: call backup() before each /edit (a save point, like in the slides).
        # Add your elif branches here, before the final else.
        # -------------------------------------------------------------------
        else:
            chat(text)
