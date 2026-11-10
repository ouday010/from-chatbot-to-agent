# Troubleshooting

Find your message, then follow the fix.

| What you see | Why | Fix |
|---|---|---|
| `python is not recognized` | Python is not installed or not in PATH | Install Python from python.org and tick "Add Python to PATH". Restart the terminal. |
| `running scripts is disabled on this system` (PowerShell) | Windows blocks the venv script | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again. |
| `ModuleNotFoundError: No module named 'openai'` (or `dotenv`) | The venv is not active, or libraries are not installed | Activate the venv (you should see `(venv)` at the start of the line), then `pip install -r requirements.txt`. |
| `[X] No API key` | `.env` is missing or still has `your-key-here` | Copy `.env.example` to `.env` and paste your key after `OPENROUTER_API_KEY=`. No quotes. |
| `AuthenticationError` / `401` | Wrong or deleted key | Create a new key on openrouter.ai, update `.env`. |
| `RateLimitError` / `429` | A free model is overloaded, or you used your free quota | The program tries the next model by itself. If everything fails, wait 1 minute. If it still fails, you may have used the ~50 requests of the day: continue tomorrow, or add credits on OpenRouter. |
| `APITimeoutError` | A free model is slow or queued | Normal with free models. The program moves to the next one after `TIMEOUT` seconds. |
| `empty answer` | A reasoning model used all its tokens before answering | Normal. The program tries the next model. |
| `All models failed` | Every tried model failed | Wait a minute and retry. Run `python tools/test_models.py` to see which models work today. |
| `[no file found]` | The model did not follow the `### FILE:` format | Retry the same message. If it keeps happening, check your `SYSTEM_AGENT` (the format rule must be explicit). |
| Page text is unreadable (dark on dark) | The AI chose bad colors | Normal! Send: `/edit Make all titles and links readable on the background.` Testing with your own eyes is your job. |
| `portfolio/` is not created | Nothing was saved yet, or you ran the script from another folder | Run the command from the project folder (where `README.md` is). |
| The assistant answers in a strange language or gibberish | Small free models are weak outside English | Use English. Or move a bigger model first in `MODELS`. |
| The assistant says something false with confidence | This is a **hallucination** | Check facts in a real source. Use `/hunt` (in the final version) to practice. |

## Free quota: how to not waste it
- About **20 requests per minute** and **50 requests per day** per OpenRouter account (without credits).
- Creating more keys or accounts does not give more requests.
- Every try of every model counts as a request, so one question can cost up to `MAX_TRIES` requests when models fail.
- Do not run `tools/test_models.py` many times: it uses one request per model.
- The counter `requests: N` printed by the program counts the requests of the current run.

## Models stop working?
Free models change often.
1. `python tools/list_free_models.py --env` prints a fresh `MODELS=` line.
2. `python tools/test_models.py` shows which ones work now.
3. Put the `OK` ones first in `MODELS` in your `.env`.
