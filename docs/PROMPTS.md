# Prompts for your AI helper

These prompts are for **your AI helper** (Copilot in VS Code, or a chat like ChatGPT / Claude / Gemini).
You do **not** type them in the terminal. The terminal is only for running your program.

## The loop (Plan, Small step, Test, Fix)
1. Give your AI the context.
   - AI inside VS Code: open `agent_starter.py` and say: "Read this file before answering."
   - Browser chat: copy the WHOLE file into the chat first.
2. Ask for ONE TODO only. Use a prompt below or write your own.
3. Read the answer. Put it in the right place in the file. Review it before you accept it.
4. Run the program in the terminal and test.
5. If it breaks, paste the FULL error message to your AI and ask for the smallest fix.

## CCCF: how to write a precise prompt
- **C**ontext: who you are and the situation.
- **T**arget: the exact result you want.
- **C**onstraints: rules, limits, what to avoid.
- **F**ormat: how the answer should look.

Weak prompt: `Make a chatbot.`
Strong prompt: see TODO 1 below.

---

## TODO 1: the personality of the assistant
> I am a beginner building an AI assistant in Python. In `agent_starter.py`, write the text for the
> `SYSTEM` variable. The assistant is called Study Buddy, a friendly tutor for beginners. Rules: always
> answer in English with simple words, explain every concept with one everyday analogy, maximum
> 3 sentences, and say "I am not sure" instead of inventing facts. Give me only the string to paste,
> then explain each rule in one line.

Try your own: change the personality (a pirate tutor? a strict teacher?) and see the answers change.

## TODO 2: memory
> In `agent_starter.py`, implement `chat(user_text)`. Keep the conversation in the `history` list.
> Add the user message, call `ask_model` with the system message plus `history`, add the answer to
> `history`, and print the answer, the model used and the number of requests. If `ask_model` raises
> `RuntimeError`, remove the last user message from `history`, print a friendly error and return.
> Change only this function, then explain how the memory works.

## TODO 3: the agent prompt (the contract)
> I am building an AI agent that creates a personal portfolio website. In `agent_starter.py`, write
> the text for the `SYSTEM_AGENT` variable. The model is a web designer. It must output exactly
> 2 files, `index.html` and `style.css`, each in this exact format: `### FILE: <name>` on one line,
> then the content, then `### END` on its own line, and nothing outside the files. Constraints:
> sections About, Skills, Projects, Contact; plain HTML and CSS only, no JavaScript, no remote images;
> readable colors with good contrast (titles and links too); use only the information given by the user,
> never invent facts. Give me only the string to paste, then explain each rule in one line.

## TODO 4: run_agent
> In `agent_starter.py`, implement `run_agent(user_text)`. Keep the conversation in `agent_history`.
> Call `ask_model` with the agent system message plus `agent_history`, store the answer in
> `agent_history`, call `save_files` on the answer, and print the saved files, the model used and the
> number of requests. If no file was saved, print a hint. If the call fails, remove the last user
> message and print a friendly error. Change only this function, then explain how it works.

## TODO 5: the commands
> In the loop at the bottom of `agent_starter.py`, add two commands before the final `else`.
> `/build <text>` calls `run_agent("Create the portfolio for this person: " + text)`.
> `/edit <text>` calls `run_agent` with a message asking the model to apply the change and output ALL
> the files again, complete, in the same format. Change only what is needed.

---

## What to type in the program

### Part 1 (assistant)
- `What is a neuron?`
- `Give me another analogy` (tests the memory)
- `/explain gradient descent`
- `/explain overfitting`

### Part 2 (agent): a good first description (FAKE info!)
```
/build Name: Sam Ben Ali. Role: AI student and web designer. Skills: Python, machine learning, HTML/CSS. Projects: AI Study Buddy (a terminal chatbot), Spam Detector (a small ML model). Contact: sam@example.com
```

### Example `/edit` commands (ONE change at a time)
- `/edit Add a hero section with a big title, a tagline and a button linking to Contact.`
- `/edit Use a dark theme with a purple accent. All titles and links must stay readable.`
- `/edit Make the page look good on phones.`
- `/edit Make the links readable on the dark background: use the color #d8b4fe.`
- `/edit Add a footer with the text "Built with an AI agent".`

### Bonus challenge
> Before each `/edit`, copy the folder `portfolio/` to `portfolio_backup/` (a save point).
> (Hint: the helper `backup()` already exists. Where should you call it?)

## When something breaks
> I ran the program and got this error: [paste the FULL error]. Here is the function that fails:
> [paste it]. Explain the cause in simple words, then give the smallest fix.
