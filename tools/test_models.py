"""
Tests EVERY model in MODELS with one tiny request each (so it uses one request per model).
Shows which models work today: OK, EMPTY or FAIL.
Run from the project folder:  python tools/test_models.py
Then keep the OK models first in the MODELS line of your .env.
"""
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    timeout=float(os.getenv("TIMEOUT", "30")),
    max_retries=0,
)
models = [m.strip() for m in os.getenv("MODELS", "").split(",") if m.strip()]

print(f"Testing {len(models)} models (this uses {len(models)} requests)...\n")
print(f"{'STATUS':<7} {'TIME':>6}  MODEL")
for model in models:
    start = time.time()
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Explain in one short sentence what a neuron is."}],
            max_tokens=300,
        )
        text = (r.choices[0].message.content or "").strip()
        status = "OK" if text else "EMPTY"
        detail = text[:70].replace("\n", " ")
    except Exception as e:
        status = "FAIL"
        detail = type(e).__name__
    print(f"{status:<7} {time.time() - start:5.1f}s  {model}  {detail}")
