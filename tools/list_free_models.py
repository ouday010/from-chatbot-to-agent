"""
Lists the free models available on OpenRouter right now (no API key needed).

  python tools/list_free_models.py          -> readable list
  python tools/list_free_models.py --env    -> a ready-to-paste MODELS= line for your .env
"""
import json
import sys
import urllib.request

URL = "https://openrouter.ai/api/v1/models"

with urllib.request.urlopen(URL, timeout=30) as response:
    data = json.load(response)["data"]

free = sorted(m["id"] for m in data if m["id"].endswith(":free"))

if "--env" in sys.argv:
    print("MODELS=" + ",".join(free))
else:
    print(f"{len(free)} free models:")
    for model_id in free:
        print(" -", model_id)
    print("\nTip: run with --env to get a MODELS= line for your .env file.")
