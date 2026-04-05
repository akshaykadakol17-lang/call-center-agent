import requests

OBJECTION_POOL = [
    "too expensive",
    "not interested",
    "already have a solution",
    "no time"
]

def simulate_caller(agent_message: str, turn: int) -> str:
    prompt = f"""You are a busy business owner receiving a cold sales call. 
You are skeptical but polite. React naturally to what the sales agent says.
Use one of these objections naturally if it fits: {OBJECTION_POOL}
After 4-5 turns, decide to either agree to a demo or end the call.

Sales agent just said: "{agent_message}"
Turn number: {turn}

Respond as the customer in 1-2 sentences only."""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"].strip()