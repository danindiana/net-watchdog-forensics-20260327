import subprocess
import sys
import os

def run_test(file_path, model="qwen3.5:0.8b"):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, "r") as f:
        state_data = f.read()

    # Reuse the logic from analyze_state.py for consistency
    import analyze_state
    
    print(f"Testing {file_path} with {model}...")
    result = analyze_state.delegate_to_ollama(state_data, manual_model=model)
    return result

if __name__ == "__main__":
    # Ensure the scripts directory is in path for imports
    sys.path.append(os.path.dirname(__file__))
    
    test_cases = [
        "net-watchdog-forensics-20260327/examples/mock_incident_state.txt",
        "net-watchdog-forensics-20260327/examples/redteam_obfuscation.txt"
    ]
    
    for case in test_cases:
        print(f"\n{'='*20} STARTING TEST: {case} {'='*20}")
        print(run_test(case))
        print(f"{'='*60}\n")
