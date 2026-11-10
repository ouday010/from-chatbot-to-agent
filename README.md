<div align="center">

# 🤖➡️🧑‍💻 FROM CHATBOT TO AGENT

### Build an AI that builds your portfolio

**Start with a simple AI assistant. End with an AI agent that writes a real website into a folder on your computer.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![OpenRouter](https://img.shields.io/badge/API-OpenRouter-8A2BE2)
![Cost](https://img.shields.io/badge/Cost-FREE-brightgreen)
![Level](https://img.shields.io/badge/Level-Beginner-orange)
![Time](https://img.shields.io/badge/Time-30--40%20min-lightgrey)

*A hands-on practice for the workshop **"The Architecture of AI: From Neurons to Vibe Coding"***

</div>

---

## 📖 Table of contents
1. [What you will build](#-what-you-will-build)
2. [The big idea: assistant vs agent](#-the-big-idea-assistant-vs-agent)
3. [Your roadmap](#-your-roadmap)
4. [Before the workshop (do it the day before)](#-before-the-workshop-do-it-the-day-before)
5. [Part 1: build the assistant](#-part-1-build-the-assistant)
6. [Part 2: turn it into an agent](#-part-2-turn-it-into-an-agent)
7. [Bonus](#-bonus)
8. [Level up ideas](#-level-up-ideas)
9. [Troubleshooting](#-troubleshooting)
10. [Safety rules](#-safety-rules)
11. [Repository map](#-repository-map)

---

## 🎯 What you will build

You will build **one program in two steps**.

**Step 1: an AI assistant (Study Buddy).** You talk, it answers with text.

```text
You> What is a neuron?
Buddy> A neuron is like a tiny voting machine: it receives many small signals, adds them up,
and "fires" only if the total is strong enough. A network is millions of them working together.
[model: cohere/north-mini-code:free | requests: 1]

You> Give me another analogy
Buddy> Think of a neuron as a doorbell: many people can push it a little, but it only rings
when the pushes add up to something big enough.
```

**Step 2: an AI agent.** You describe yourself, and the program **creates files**.

```text
You> /build Name: Sam Ben Ali. Role: AI student and web designer. Skills: Python, machine learning, HTML/CSS. Projects: AI Study Buddy, Spam Detector. Contact: sam@example.com
[ok] portfolio/index.html, portfolio/style.css | model: cohere/north-mini-code:free | requests: 3
Open portfolio/index.html in your browser (press F5 to refresh).

You> /edit Use a dark theme with a purple accent. All titles and links must stay readable.
[ok] portfolio/index.html, portfolio/style.css | model: cohere/north-mini-code:free | requests: 4
```

You open `portfolio/index.html` in your browser: **your own website, written by your own AI agent.**

> The AI answers are different every time. Your output will not be identical to the examples above. That is normal.

You will use **vibe coding**: you do not write all the code yourself. You write precise prompts, an AI helper writes the code, and **you test, read and fix**.

---

## 💡 The big idea: assistant vs agent

| | AI assistant | AI agent |
|---|---|---|
| What it returns | Text for a human | Text that **our code turns into actions** |
| Who acts? | You (copy, paste, click) | The program (saves files by itself) |
| Loop | Question → answer | Think → **Act** → Observe → Repeat |
| In this project | `chat()` | `run_agent()` + `save_files()` |

The model never touches your computer. It only writes text. **Our code** reads that text and saves files.
That is why the agent needs a **contract**: the prompt forces the model to answer in a fixed format,
and the code understands that format.

```text
### FILE: index.html
<html>...</html>
### END
```

```text
        you describe yourself
                 │
                 ▼
     ┌───────────────────────┐
     │  LLM (free model via  │
     │      OpenRouter)      │
     └───────────┬───────────┘
                 │ text in the "### FILE" format
                 ▼
     ┌───────────────────────┐
     │  save_files()  (code) │──► portfolio/index.html, style.css
     └───────────────────────┘
                 ▲                              │
                 └── you look, then /edit ◄─────┘
```

---

## 🗺️ Your roadmap

You get a file with **5 TODOs**. Each TODO is a small mission.

| # | Part | TODO | You write (with your AI helper) | Test with | Time |
|---|---|---|---|---|---|
| 1 | Assistant | `SYSTEM` | The personality and rules of the assistant | `What is a neuron?` | ~5 min |
| 2 | Assistant | `chat()` | A function with **memory** | `Give me another analogy` | ~7 min |
| 3 | Agent | `SYSTEM_AGENT` | The **contract**: output files in a fixed format | (tested in TODO 5) | ~7 min |
| 4 | Agent | `run_agent()` | One round of the agent: think → act | (tested in TODO 5) | ~7 min |
| 5 | Agent | commands | `/build` and `/edit` | `/build ...` then open the page | ~8 min |

Stuck? Look at the finished versions in `solution/` (but try first!).

---

## 🧰 Before the workshop (do it the day before)

About 20 minutes. **Do not skip it**: the workshop time is for building, not for installing.

### Step 1. Check Python
Open a terminal and run:
```bash
python --version
```
You need **3.9 or newer**. On Mac/Linux, if `python` does not work, try `python3 --version`.
If it fails: install Python from [python.org](https://www.python.org/downloads/) (on Windows, tick **"Add Python to PATH"**).

### Step 2. Get the project
Choose one:
- **With git:** `git clone https://github.com/ouday010/from-chatbot-to-agent.git` then `cd` into the folder.
- **Without git:** click the green **Code** button on GitHub, then **Download ZIP**, then extract it.

Open the folder in **VS Code**: *File → Open Folder*. Open the terminal inside VS Code: *Terminal → New Terminal*.

### Step 3. Create a virtual environment and install the libraries
A virtual environment (venv) is a private box for this project's libraries.

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
You should see `(venv)` at the beginning of the terminal line. This means it is active.
If you open a new terminal later, activate it again.

> PowerShell says *"running scripts is disabled"*? Run once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again.

### Step 4. Get your OpenRouter API key
1. Create an account on [openrouter.ai](https://openrouter.ai).
2. Open the **Keys** page and click **Create Key**. Give it any name.
3. **Copy the key now.** It starts with `sk-or-`.

**What is OpenRouter?** One website, one key, many AI models from many companies. You choose the model in each request.
Models whose id ends with `:free` cost nothing. Free limits (without credits): about **20 requests per minute** and **50 requests per day**.
A key is like a password: never share it, never write it in the code, never upload it.

### Step 5. Create your `.env` file
The `.env` file stores your secret settings outside the code.

1. In the project, copy `.env.example` and name the copy `.env`.
   (VS Code: right click `.env.example` → Copy, then Paste, then Rename.)
2. Open `.env`. Replace `your-key-here` with your key. **No quotes, no spaces.**

```text
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
```
3. Leave the other lines as they are. The `MODELS=` line already contains all free models we know.
   The file `.gitignore` keeps `.env` out of GitHub.

### Step 6. Check your setup
```bash
python tools/check_setup.py
```
Expected:
```text
OK: cohere/north-mini-code:free answered: 'ready'
Your setup works.
```
It uses 1 request (up to 3 if the first models fail). **Run it once, then stop experimenting**: the free plan allows only ~50 requests per day for everything you run.
If you see an error, open [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md).

### Step 7. Choose your AI helper (the one that writes code for you)
Choose ONE, and test it before the workshop:
- **AI inside VS Code** (for example GitHub Copilot Chat): sign in and check that you can use it. It can read and edit your files. Ask it to explain its plan first and **review its changes before you accept them**.
- **A chat in your browser** (ChatGPT, Claude, Gemini...): works everywhere. You copy your file into the chat, then copy the answer back.

If the AI inside VS Code does not work for you, the browser chat is fine.

✅ **Checklist:** Python OK · `(venv)` active · libraries installed · `.env` created · `check_setup.py` says OK · AI helper ready.

---

## 🧠 Part 1: build the assistant

Open **`agent_starter.py`**. Read the comment at the top. Find the sections marked `TODO`.
The functions `ask_model` and `save_files` are already written for you.

### How to work (the vibe coding loop)
1. **Give context** to your AI helper (open the file in VS Code, or paste the whole file in a browser chat).
2. **Ask for ONE TODO** with a precise prompt. Use CCCF: **C**ontext, **T**arget, **C**onstraints, **F**ormat.
3. **Read** the answer. Put it in the right place.
4. **Run** the program and **test**.
5. If it breaks: paste the **full error** to your AI.

The prompts are NOT typed in the terminal. They go to your AI helper. The terminal is only for running the program.
Ready-made prompts are in [`docs/PROMPTS.md`](docs/PROMPTS.md). Try writing your own first.

---

### ✏️ TODO 1: the personality of the assistant (`SYSTEM`)

**Goal:** tell the AI who it is and how to answer. This is the *system prompt*.

**Example prompt for your AI helper:**
> I am a beginner building an AI assistant in Python. In `agent_starter.py`, write the text for the `SYSTEM` variable. The assistant is called Study Buddy, a friendly tutor for beginners. Rules: always answer in English with simple words, explain every concept with one everyday analogy, maximum 3 sentences, and say "I am not sure" instead of inventing facts. Give me only the string to paste.

**Expected result in the file:**
```python
SYSTEM = """You are Study Buddy, a friendly AI tutor for beginners.
Rules:
- Always answer in English, with simple words.
- Explain every concept with one everyday analogy.
- Keep each answer to 3 sentences maximum.
- If you are not sure about something, say so. Never invent facts."""
```

**Can I test it now?** Not yet: `chat()` is TODO 2. Go on.

**What you can change:** make the tutor a pirate, a strict teacher, or a football coach. Different system prompt = different behavior.

**Common mistakes:** forgetting the triple quotes `"""` · writing the prompt in Arabic or French (small free models answer badly outside English).

---

### ✏️ TODO 2: memory (`chat()`)

**Goal:** a function that sends your message to the model **and remembers the conversation**.
A model has no memory. Each request is new. The memory is the `history` list that **we** send every time.

**Example prompt for your AI helper:**
> In `agent_starter.py`, implement `chat(user_text)`. Keep the conversation in the `history` list. Add the user message, call `ask_model` with the system message plus `history`, add the answer to `history`, and print the answer, the model used and the number of requests. If `ask_model` raises `RuntimeError`, remove the last user message from `history`, print a friendly error and return. Change only this function, then explain how the memory works.

**Run it:**
```bash
python agent_starter.py
```

**What you can type:**

| Type | What happens |
|---|---|
| `What is a neuron?` | Normal chat |
| `Give me another analogy` | **Memory test.** If the answer talks about neurons, your memory works. |
| `/explain gradient descent` | A short explanation with an analogy (already in the main loop) |
| `/explain overfitting` | Same, other topic |
| `/quit` | Exit |

**Expected output (the text will differ):**
```text
You> What is a neuron?
Buddy> A neuron is like a tiny voting machine ... 
[model: cohere/north-mini-code:free | requests: 1]
```
If a model fails, you see lines like `(google/gemma-4-31b-it:free failed: RateLimitError. Trying the next model...)`. That is the fallback working.

**Common errors:**
- `TODO 2: chat() is not implemented yet.` → you did not replace the function yet.
- `All models failed` → wait a minute, retry. See [Troubleshooting](#-troubleshooting).
- The AI forgets the previous message → your function does not add the answer to `history`.

> ✅ **Checkpoint:** you have a working assistant. The finished version is `solution/step1_assistant.py`.

**Hallucination moment (optional):** ask something very recent or niche, for example `/explain vibe coding`.
Small models often answer with confidence and **get it wrong**. Always verify facts.

---

## 🤖 Part 2: turn it into an agent

Now the key idea. The assistant only talks. The agent **acts**: it writes files.
Before coding, read the function `save_files` in the file. It searches the answer for blocks like:

```text
### FILE: index.html
...content...
### END
```
and saves them in `portfolio/`. It is **restricted for safety**: only the file name is kept (no `../`), only `.html .css .js` are allowed, and we never run what the model wrote.

---

### ✏️ TODO 3: the contract (`SYSTEM_AGENT`)

**Goal:** a new system prompt that turns the model into a **web designer** and **forces the format** that `save_files` understands.
If the model does not follow the format, nothing is saved. This contract is the heart of an agent.

**Example prompt for your AI helper:**
> I am building an AI agent that creates a personal portfolio website. In `agent_starter.py`, write the text for the `SYSTEM_AGENT` variable. The model is a web designer. It must output exactly 2 files, `index.html` and `style.css`, each in this exact format: `### FILE: <name>` on one line, then the content, then `### END` on its own line, and nothing outside the files. Constraints: sections About, Skills, Projects, Contact; plain HTML and CSS only, no JavaScript, no remote images; readable colors with good contrast (titles and links too); use only the information given by the user, never invent facts. Give me only the string to paste.

**Expected result in the file:**
```python
SYSTEM_AGENT = """You are a web designer who builds simple personal portfolio websites.
Rules:
- Output ONLY files, using exactly this format for each file:
### FILE: <filename>
<file content>
### END
- Create exactly 2 files: index.html and style.css.
- ...
- Do not write any text outside the files."""
```

**Why each rule exists:**

| Rule | Why |
|---|---|
| Exact `### FILE` / `### END` format | So our code can find the files |
| Exactly 2 files | Predictable result |
| Plain HTML/CSS, no JavaScript, no remote images | Safe and works offline |
| Good contrast | Without it, AI often writes dark text on a dark background |
| Only the user's info | Prevents invented facts (hallucination) |
| Nothing outside the files | Extra text would break the parsing |

**Can I test it now?** Not yet: you need `run_agent()` (TODO 4).

---

### ✏️ TODO 4: one round of the agent (`run_agent()`)

**Goal:** the same idea as `chat()`, plus **one new thing: the code acts** (it saves the files).

**Example prompt for your AI helper:**
> In `agent_starter.py`, implement `run_agent(user_text)`. Keep the conversation in `agent_history`. Call `ask_model` with the agent system message plus `agent_history`, store the answer in `agent_history`, call `save_files` on the answer, and print the saved files, the model used and the number of requests. If no file was saved, print a hint. If the call fails, remove the last user message and print a friendly error. Change only this function, then explain how it works.

**Think → Act → Observe:**
1. *Think:* the model writes the files as text.
2. *Act:* `save_files(answer)` writes them to disk.
3. *Observe:* **you** open the page and look. Then you ask for a change.

**Can I test it now?** Not yet: nothing calls `run_agent()` until TODO 5.

---

### ✏️ TODO 5: the commands (`/build` and `/edit`)

**Goal:** connect the agent to the main loop at the bottom of the file.

**Example prompt for your AI helper:**
> In the loop at the bottom of `agent_starter.py`, add two commands before the final `else`. `/build <text>` calls `run_agent("Create the portfolio for this person: " + text)`. `/edit <text>` calls `run_agent` with a message asking the model to apply the change and output ALL the files again, complete, in the same format. Change only what is needed.

**Why "ALL the files again, complete"?** Because `save_files` overwrites the files. A partial answer would erase your page.

**Run it:**
```bash
python agent_starter.py
```

**What you can type (use FAKE info!):**
```text
/build Name: Sam Ben Ali. Role: AI student and web designer. Skills: Python, machine learning, HTML/CSS. Projects: AI Study Buddy (a terminal chatbot), Spam Detector (a small ML model). Contact: sam@example.com
```
Then **open `portfolio/index.html`** in your browser (double click it, or right click → *Open with browser*; or in VS Code right click → *Reveal in File Explorer*).

Now improve it, **one change at a time**, then press **F5** in the browser:

| Type | What to expect |
|---|---|
| `/edit Add a hero section with a big title, a tagline and a button linking to Contact.` | A big top section |
| `/edit Use a dark theme with a purple accent. All titles and links must stay readable.` | Dark page |
| `/edit Make the page look good on phones.` | Responsive layout |
| `/edit Make the links readable on the dark background: use the color #d8b4fe.` | Fix a color problem |
| `/edit Add a footer with the text "Built with an AI agent".` | A footer |

**Expected output:**
```text
[ok] portfolio/index.html, portfolio/style.css | model: cohere/north-mini-code:free | requests: 5
Open portfolio/index.html in your browser (press F5 to refresh).
```

**Lessons you will see with your own eyes:**
- A vague description gives a plain page. A precise description gives a better page.
- The AI makes mistakes (for example dark titles on a dark background). **You** must look and catch them. This is the *Test → Fix* part of the iteration engine.
- Small steps work better than one huge request.

**Common errors:**
- `[no file found]` → the model did not follow the contract. Retry. If it repeats, make your `SYSTEM_AGENT` stricter.
- `/build` behaves like a normal chat → you did not add the branch before the `else`.
- The page is empty or broken → send `/edit` asking to fix the specific problem you see.

> ✅ **Done!** You built an assistant, then turned it into an agent. The finished version is `solution/step2_agent.py`.

---

## 🎁 Bonus

**1. Save point.** Call `backup()` before each `/edit`. It copies `portfolio/` to `portfolio_backup/`, so you can go back if the AI breaks your page.

**2. Hallucination hunter** (in `solution/step2_agent.py`). Type `/hunt Roman history`: the AI writes 4 sentences and **one** contains a believable error. Can you find it? Type `reveal` to see the answer. Small models also make mistakes in the *hunt* itself, so check the facts yourself.

**3. Run the finished version:**
```bash
python solution/step2_agent.py
```

---

## 🚀 Level up ideas
- Add a **dark / light** mode in your page with a `/edit`.
- Let the user choose **colors and fonts** at the start (ask questions with `input()`).
- Add a command `/undo` that restores `portfolio_backup/`.
- Allow a third file type or an `images/` folder (think about the security first!).
- Publish your page for free with **GitHub Pages**.
- Make the agent **loop by itself**: it checks its own page and fixes problems (that is closer to real coding agents).

---

## 🛠️ Troubleshooting

Short version (full table in [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)):

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Activate the venv, then `pip install -r requirements.txt` |
| `No API key` | Check `.env`: `OPENROUTER_API_KEY=...` with no quotes |
| `429` / `RateLimitError` | A free model is busy. The program tries the next one. Wait a minute if all fail. |
| `APITimeoutError` | A free model is slow. Normal. It moves to the next one. |
| `empty answer` | A reasoning model ran out of tokens. Normal. It moves to the next one. |
| Nothing works anymore today | You may have used the ~50 free requests of the day. Try tomorrow. |
| Free models changed | `python tools/list_free_models.py --env`, then `python tools/test_models.py` |

**About the quota:** every try counts as a request. One question can use up to `MAX_TRIES` requests (default 6) when models fail. More keys or accounts do not give more requests.

---

## 🔐 Safety rules
- **Never** put your API key in the code, in a prompt, or on GitHub. It lives in `.env` only.
- Use **fake or minimal** personal info in prompts. Free models may log what you send.
- **Read** the code your AI writes before you run it.
- An agent that writes files must be **restricted** (see `save_files`). Never run what a model wrote without understanding it.
- The AI can be confidently wrong. **Verify.**

---

## 🗂️ Repository map

```text
.
├── README.md                  ← you are here
├── agent_starter.py           ← YOUR MISSION: finish the 5 TODOs
├── solution/
│   ├── step1_assistant.py     ← checkpoint: Part 1 (assistant)
│   └── step2_agent.py         ← final version: assistant + agent + bonus
├── tools/
│   ├── check_setup.py         ← tests your setup (1 tiny request)
│   ├── list_free_models.py    ← lists today's free models (--env for a MODELS line)
│   └── test_models.py         ← tests every model: OK / EMPTY / FAIL
├── docs/
│   ├── PROMPTS.md             ← how to prompt + example prompts + things to type
│   └── TROUBLESHOOTING.md     ← errors and fixes
├── .env.example               ← copy to .env and add your key
├── requirements.txt           ← openai, python-dotenv
└── .gitignore                 ← keeps .env and generated files out of GitHub
```

---

<div align="center">

**Golden rules:** one small step at a time · test after each step · paste the full error · never share your key · understand before you trust.

⭐ Built for the workshop *"The Architecture of AI: From Neurons to Vibe Coding"*

</div>
