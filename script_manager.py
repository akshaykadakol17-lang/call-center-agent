import json
import os

SCRIPTS_DIR = "scripts"

def load_latest_script():
    files = sorted([f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".json")])
    latest = os.path.join(SCRIPTS_DIR, files[-1])
    with open(latest) as f:
        return json.load(f)

def save_new_script(script: dict):
    version = script["version"]
    path = os.path.join(SCRIPTS_DIR, f"script_v{version}.json")
    with open(path, "w") as f:
        json.dump(script, f, indent=2)
    print(f"[Script Manager] Saved new script: script_v{version}.json")
    return path

def print_script_diff(old_script: dict, new_script: dict):
    print("\n[Script Evolution — What Changed]")
    print("-" * 40)

    old_responses = old_script.get("objection_responses", {})
    new_responses = new_script.get("objection_responses", {})

    changed = False

    for key, new_val in new_responses.items():
        if key not in old_responses:
            print(f"  ADDED objection handler: '{key}'")
            print(f"    Response: {new_val[:100]}...")
            changed = True
        elif old_responses[key] != new_val:
            print(f"  UPDATED: '{key}'")
            print(f"    Before: {old_responses[key][:80]}...")
            print(f"    After:  {new_val[:80]}...")
            changed = True

    if not changed:
        print("  No changes made to script this iteration.")

    print("-" * 40)