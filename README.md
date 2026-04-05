# Self-Improving Call Center Agent

An AI agent that simulates sales calls, analyzes outcomes, and iteratively improves its own script. Built as part of the Binox 2026 Graduate FDE Assessment (G1).

## Why I built it this way

I chose to simulate the caller with an LLM because the main goal of the project was to show the self-improvement loop, not the voice infrastructure. Using an LLM made it faster to build, easier to test, and completely local without depending on paid APIs or extra setup. It also let me focus on the actual call quality, objection handling, and script updates.

## How the feedback loop works

The feedback loop takes the transcript from one call, analyzes what objections came up and where the agent handled them weakly, and then updates the script with a better response for the next call. So instead of repeating the same script every time, the agent learns from previous conversations and adapts its objection-handling logic. In simple terms, one call becomes training data for the next call.
```
Call #1 runs using script v1
    ↓
Transcript saved
    ↓
Analyzer identifies weak objection handling
    ↓
Script updated with better responses → script v2
    ↓
Call #2 runs using improved script v2
    ↓
Script Evolution diff printed — shows exactly what changed
```

## What the script evolution looks like

After each call, the agent prints exactly what changed in the script:
```
[Script Evolution — What Changed]
----------------------------------------
  ADDED objection handler: 'concern over investing in another solution'
    Response: Emphasize the ability to integrate CloudSync Pro...
----------------------------------------
```

This makes the self-improvement loop visible and verifiable.

## Project structure

I split it into separate files to keep each part of the system responsible for one job. The agent handles selling, the caller simulates the customer, the analyzer reviews the call, and the script manager updates the script. That made the project easier to debug, easier to extend, and much cleaner than putting everything into one large file.
```
call-center-agent/
├── main.py             # runs the full demo (2 iteration cycles)
├── agent.py            # sales agent — conducts the call using current script
├── caller.py           # simulated caller — plays the customer role
├── analyzer.py         # scores the call, identifies objections
├── script_manager.py   # loads, updates, saves script + prints diff
├── logger.py           # saves call transcripts to logs/
├── scripts/
│   └── script_v1.json  # initial sales script
├── logs/               # call transcripts saved here
├── requirements.txt
├── README.md
└── evaluation.md
```

## Setup

Requirements: Python 3.10+, [Ollama](https://ollama.com)
```bash
# 1. Install Ollama and pull the model
brew install ollama
ollama pull llama3.2
ollama serve    # run in a separate terminal tab

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python main.py
```

No API keys needed. Runs entirely locally.

## Example output
```
CALL #1 — Using script v1

Agent: Hi, this is Alex from CloudSync. We help businesses reduce 
storage costs by up to 40%. Do you have 2 minutes to hear how?

Customer: I appreciate your call, but I'm not sure we need this...

[Call Analysis]
  Outcome: success
  Score: 8/10
  Objections raised: ['price concerns', 'vendor reliability', 'setup familiarity']
  Poorly handled: ['setup familiarity']

[Script Evolution — What Changed]
  ADDED objection handler: 'concern over investing in another solution'
    Response: Emphasize integration with existing systems...

CALL #2 — Using script v2
...

Demo complete. Check logs/ for transcripts.
Check scripts/ to see how the script evolved.
```

## What I would add with more time

- Real voice input and output so the demo feels closer to a real call center workflow
- More detailed analysis tracking success metrics across multiple calls and showing trends in how the script improves over time
- A small dashboard to compare script versions, transcripts, and performance scores visually