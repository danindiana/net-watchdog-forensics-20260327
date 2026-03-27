import subprocess
import sys
import os

def run_test(file_path, model="qwen3.5:0.8b"):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, "r") as f:
        state_data = f.read()

    prompt = f"Forensic Task: Identify the PID and process name responsible for anomalous ICMP traffic in this mock data. Be extremely brief. Data: {state_data}"
    
    print(f"Testing mock data with {model}...")
    cmd = ["ollama", "run", model, prompt]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    
    if process.returncode == 0:
        return stdout
    else:
        return f"Error: {stderr}"

if __name__ == "__main__":
    target_file = "net-watchdog-forensics-20260327/examples/mock_incident_state.txt"
    result = run_test(target_file)
    print("\n--- MOCK TEST RESULT ---\n")
    print(result)
