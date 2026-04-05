import requests

def run_agent_turn(script: dict, conversation_history: list, customer_message: str) -> str:
    history_text = "\n".join([f"{r['role']}: {r['message']}" for r in conversation_history])
    objections_text = json.dumps(script["objection_responses"], indent=2)

    prompt = f"""You are a professional sales agent named Alex selling {script['product']}.
Use the script responses below to handle objections. Be natural and conversational.

Your objection responses:
{objections_text}

Conversation so far:
{history_text}

Customer just said: "{customer_message}"

Respond as Alex in 2-3 sentences. Be helpful, not pushy."""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"].strip()

import json