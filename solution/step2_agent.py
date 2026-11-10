"""
FINAL VERSION: Part 1 + Part 2. The assistant becomes an AGENT.

Run from the project folder:  python solution/step2_agent.py
You can type:
    Hello                         -> chat with the assistant (it remembers)
    /explain neural network       -> a short explanation with an analogy
    /build <about you>            -> the agent writes your portfolio into portfolio/
    /edit <change>                -> the agent improves the page
    /hunt <topic>                 -> BONUS: hallucination hunter (then type: reveal)
    /quit                         -> exit
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


SYSTEM = """You are Study Buddy, a friendly AI tutor for beginners.
Rules:
- Always answer in English, with simple words.
- Explain every concept with one everyday analogy.
- Keep each answer to 3 sentences maximum.
- If you are not sure about something, say so. Never invent facts."""

SYSTEM_AGENT = """You are a web designer who builds simple personal portfolio websites.
Rules:
- Output ONLY files, using exactly this format for each file:
### FILE: <filename>
<file content>
### END
- Create exactly 2 files: index.html and style.css.
- index.html must link the stylesheet with <link rel="stylesheet" href="style.css">.
- Use plain HTML and CSS only. No JavaScript, no external libraries, no remote images.
- Sections: About, Skills, Projects, Contact. Clean, modern, responsive design.
- All text must have good contrast and be readable on its background (including titles and links).
- Use ONLY the information given by the user. Do not invent facts.
- Do not write any text outside the files."""

HUNT_PROMPT = (
    "Write 4 short numbered sentences about this topic: {topic}. "
    "EXACTLY ONE sentence must contain a believable factual error. "
    "Do not say which one. Do not explain."
)


history = []  # the conversation of the assistant (so it remembers)


def chat(user_text):
    history.append({"role": "user", "content": user_text})
    try:
        answer, model = ask_model([{"role": "system", "content": SYSTEM}] + history, max_tokens=2500)
    except RuntimeError as e:
        history.pop()  # forget the question that failed
        print(f"[error] {e}. Wait a few seconds and try again.")
        return
    history.append({"role": "assistant", "content": answer})
    print(f"\nBuddy> {answer}\n[model: {model} | requests: {calls}]\n")


agent_history = []  # the conversation of the agent (so it remembers the current page)


def run_agent(user_text):
    agent_history.append({"role": "user", "content": user_text})
    try:
        answer, model = ask_model([{"role": "system", "content": SYSTEM_AGENT}] + agent_history)
    except RuntimeError as e:
        agent_history.pop()
        print(f"[error] {e}. Wait a few seconds and try again.")
        return
    agent_history.append({"role": "assistant", "content": answer})
    saved = save_files(answer)
    if saved:
        print(f"[ok] {', '.join(saved)} | model: {model} | requests: {calls}")
        print("Open portfolio/index.html in your browser (press F5 to refresh).")
    else:
        print("[no file found] the model did not follow the format. Try again, or check SYSTEM_AGENT.")


HELP = (
    "Commands: /explain <topic> | /build <about you> | /edit <change> | /hunt <topic> | /quit\n"
    "Anything else is a normal chat with the assistant."
)

if __name__ == "__main__":
    print("From Chatbot to Agent: final version.")
    print(HELP)
    while True:
        text = input("You> ").strip()
        if not text:
            continue
        if text == "/quit":
            break
        if text.startswith("/explain "):
            chat("Explain this topic to a beginner: " + text[9:])
        elif text.startswith("/hunt "):
            chat(HUNT_PROMPT.format(topic=text[6:]))
            print("Find the sentence with the error. Type 'reveal' to see the answer.")
        elif text == "reveal":
            chat("Which sentence had the error? Quote it and give the correct fact.")
        elif text.startswith("/build "):
            run_agent("Create the portfolio for this person: " + text[7:])
        elif text.startswith("/edit "):
            backup()
            run_agent(
                "Apply this change and output ALL the files again, complete, "
                "in the same format: " + text[6:]
            )
        else:
            chat(text)
