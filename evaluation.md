# Evaluation: Architecture Trade-offs

## Why simulate the caller with an LLM

The main goal of this project was to demonstrate the self-improvement loop, not the voice infrastructure. Using an LLM to simulate the customer made it faster to build, easier to test, and completely local without depending on paid APIs or extra setup. It also kept the focus on call quality, objection handling, and script updates — which is what the brief actually asks for.

In a production deployment, the simulated caller would be replaced with real STT/TTS (e.g. ElevenLabs for voice output, Whisper for transcription). The rest of the architecture stays identical.

## Why separate files instead of one script

| File | Responsibility |
|---|---|
| `agent.py` | Sales agent — conducts the call using the current script |
| `caller.py` | Simulates the customer — generates realistic objections |
| `analyzer.py` | Reviews the transcript, scores the call, suggests improvements |
| `script_manager.py` | Loads, saves, and diffs script versions |
| `logger.py` | Persists transcripts for review |

Each file has one job. This made the project easier to debug, easier to extend, and much cleaner than a single large file. If the analyzer breaks, it doesn't affect the caller. If the script format changes, only `script_manager.py` needs updating.

## How the feedback loop works

After each call, the analyzer reads the full transcript and identifies which objections were raised and which were handled poorly. It then suggests a better response for the weakest objection. The script manager applies that improvement and saves a new versioned script file. The next call loads the latest script automatically.

This means one call literally becomes training data for the next call — without any manual intervention.

## Alternatives considered

| Approach | Why I didn't use it |
|---|---|
| Real voice (ElevenLabs) | Paid API, adds setup friction, not needed to demonstrate the core loop |
| n8n for orchestration | Adds visual complexity without improving the logic — Python is more transparent |
| Single script file | Harder to debug, harder to extend, all concerns mixed together |
| GPT-4 / Claude API | Paid, quota-limited — Ollama is free and fully reproducible |

## What I would improve with more time

- Add real voice input and output so the demo feels closer to a real call center workflow
- Track success metrics across multiple calls and show trends in how the script improves over time
- Build a small dashboard to compare script versions, transcripts, and performance scores visually
- Add a confidence score to each objection response so the agent knows when a handler is well-tested vs newly added

## Business relevance

Real call center agents repeat the same mistakes indefinitely unless a manager reviews recordings and manually updates scripts. This agent automates that review cycle — every call produces a transcript, every transcript produces an analysis, every analysis improves the script. At scale, this compresses weeks of script iteration into hours of automated runs.