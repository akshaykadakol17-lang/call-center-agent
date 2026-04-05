from agent import run_agent_turn
from caller import simulate_caller
from analyzer import analyze_call, improve_script
from script_manager import load_latest_script, save_new_script, print_script_diff
from logger import save_transcript

NUM_ITERATIONS = 2
MAX_TURNS = 6

def run_call(script: dict, call_number: int) -> list:
    print(f"\n{'='*60}")
    print(f"CALL #{call_number} — Using script v{script['version']}")
    print(f"{'='*60}\n")

    transcript = []
    opening = script["opening"]
    print(f"Agent: {opening}\n")
    transcript.append({"role": "Agent", "message": opening})

    for turn in range(1, MAX_TURNS + 1):
        customer_reply = simulate_caller(transcript[-1]["message"], turn)
        print(f"Customer: {customer_reply}\n")
        transcript.append({"role": "Customer", "message": customer_reply})

        if any(word in customer_reply.lower() for word in ["goodbye", "not interested anymore", "end call", "bye"]):
            print("[Call ended by customer]\n")
            break

        agent_reply = run_agent_turn(script, transcript, customer_reply)
        print(f"Agent: {agent_reply}\n")
        transcript.append({"role": "Agent", "message": agent_reply})

    return transcript

def main():
    print("\nStarting Self-Improving Call Center Agent")
    print("==========================================\n")

    for iteration in range(1, NUM_ITERATIONS + 1):
        script = load_latest_script()

        transcript = run_call(script, iteration)

        print(f"\n[Analyzing call #{iteration}...]")
        analysis = analyze_call(transcript, script)

        print(f"\n[Call Analysis]")
        print(f"  Outcome: {analysis.get('outcome', 'unknown')}")
        print(f"  Score: {analysis.get('overall_score', '?')}/10")
        print(f"  Summary: {analysis.get('summary', '')}")
        print(f"  Objections raised: {analysis.get('objections_raised', [])}")
        print(f"  Poorly handled: {analysis.get('objections_handled_poorly', [])}")

        save_transcript(transcript, analysis, script["version"])

        if iteration < NUM_ITERATIONS:
            print(f"\n[Improving script for next call...]")
            new_script = improve_script(script, analysis)
            save_new_script(new_script)
            print(f"  Script updated from v{script['version']} to v{new_script['version']}")
            print_script_diff(script, new_script)

    print("\n==========================================")
    print("Demo complete. Check logs/ for transcripts.")
    print("Check scripts/ to see how the script evolved.")

if __name__ == "__main__":
    main()