import json
import os
from datetime import datetime

LOGS_DIR = "logs"

def save_transcript(transcript: list, analysis: dict, version: int):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(LOGS_DIR, f"call_v{version}_{timestamp}.json")
    with open(filename, "w") as f:
        json.dump({"transcript": transcript, "analysis": analysis}, f, indent=2)
    print(f"[Logger] Saved transcript: {filename}")