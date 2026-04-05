import requests
import json
import re

def analyze_call(transcript: list, script: dict) -> dict:
    transcript_text = "\n".join([f"{t['role']}: {t['message']}" for t in transcript])

    prompt = f"""Analyze this sales call transcript.

Transcript:
{transcript_text}

Reply with ONLY these lines, no other text:
OUTCOME: success or failure
SCORE: a number 1 to 10
OBJECTIONS: comma separated list of objections raised
POORLY_HANDLED: comma separated list of objections handled badly
IMPROVEMENT_OBJECTION: the main objection to improve
IMPROVEMENT_RESPONSE: a better response for that objection
SUMMARY: one sentence about what happened"""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    text = response.json()["response"].strip()

    def extract(label):
        match = re.search(rf"{label}:\s*(.+)", text)
        return match.group(1).strip() if match else ""

    outcome = extract("OUTCOME") or "unknown"
    score = extract("SCORE") or "5"
    objections = [o.strip() for o in extract("OBJECTIONS").split(",") if o.strip()]
    poorly = [o.strip() for o in extract("POORLY_HANDLED").split(",") if o.strip()]
    imp_obj = extract("IMPROVEMENT_OBJECTION")
    imp_res = extract("IMPROVEMENT_RESPONSE")
    summary = extract("SUMMARY")

    improvements = {}
    if imp_obj and imp_res:
        improvements[imp_obj.lower()] = imp_res

    return {
        "outcome": outcome,
        "overall_score": score,
        "objections_raised": objections,
        "objections_handled_poorly": poorly,
        "suggested_improvements": improvements,
        "summary": summary or "Call completed."
    }

def improve_script(script: dict, analysis: dict) -> dict:
    import copy
    new_script = copy.deepcopy(script)
    new_script["version"] = script["version"] + 1

    improvements = analysis.get("suggested_improvements", {})
    for objection, better_response in improvements.items():
        if objection and better_response:
            new_script["objection_responses"][objection] = better_response
            print(f"[Analyzer] Updated response for '{objection}'")

    return new_script