"""
CHECKPOINT: Part 1 finished. An AI assistant (Study Buddy).

Run from the project folder:  python solution/step1_assistant.py
You can type:
    Hello                      -> a normal chat (the assistant remembers)
    /explain neural network    -> a short explanation with an analogy
    /quit                      -> exit
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


SYSTEM = """You are Study Buddy, a friendly AI tutor for beginners.
Rules:
- Always answer in English, with simple words.
- Explain every concept with one everyday analogy.
- Keep each answer to 3 sentences maximum.
- If you are not sure about something, say so. Never invent facts."""


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


if __name__ == "__main__":
    print("Study Buddy is ready. Ask anything, or: /explain <topic>   (/quit to exit)")
    while True:
        text = input("You> ").strip()
        if not text:
            continue
        if text == "/quit":
            break
        if text.startswith("/explain "):
            chat("Explain this topic to a beginner: " + text[9:])
        else:
            chat(text)
