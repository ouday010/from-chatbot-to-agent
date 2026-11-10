"""
Checks your setup with a tiny request (usually ONE, at most 3 if the first models fail).
Run from the project folder:  python tools/check_setup.py
"""
import os
import sys

try:
    from dotenv import load_dotenv
    from openai import OpenAI
except ImportError:
    sys.exit("[X] Libraries missing. Activate your venv, then run: pip install -r requirements.txt")

load_dotenv()

key = os.getenv("OPENROUTER_API_KEY", "")
if not key or key == "your-key-here":
    sys.exit("[X] No API key. Open your .env file and put your key after OPENROUTER_API_KEY=")
if not key.startswith("sk-or"):
    print("[!] Your key does not start with 'sk-or'. Check that you copied it from openrouter.ai.")

models = [m.strip() for m in os.getenv("MODELS", "").split(",") if m.strip()]
if not models:
    sys.exit("[X] MODELS is empty in .env. Copy the MODELS line from .env.example.")

client = OpenAI(
    base_url=os.getenv("BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=key,
    timeout=float(os.getenv("TIMEOUT", "30")),
    max_retries=0,
)

for model in models[:3]:
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with the single word: ready"}],
            max_tokens=200,
        )
        text = (r.choices[0].message.content or "").strip()
        if text:
            print(f"OK: {model} answered: {text!r}")
            print("Your setup works.")
            sys.exit(0)
        print(f"[!] {model} returned an empty answer, trying the next one...")
    except Exception as e:
        print(f"[!] {model} failed: {type(e).__name__}, trying the next one...")

sys.exit("[X] The first 3 models failed. See docs/TROUBLESHOOTING.md (wait a minute and retry, or check your key).")
