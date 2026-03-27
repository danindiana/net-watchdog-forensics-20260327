import subprocess
import json
import sys

def get_system_state():
    """Gathers filtered process and network state."""
    ps = subprocess.check_output(["ps", "-eo", "user,pid,ppid,comm,args", "--sort=-start_time"], text=True)
    # Filter out kernel threads for LLM clarity
    filtered_ps = "\n".join([line for line in ps.split("\n") if "[" not in line])
    
    ss = subprocess.check_output(["sudo", "ss", "-wnp"], text=True)
    lsof = subprocess.check_output(["sudo", "lsof", "-nP", "-i"], text=True)
    
    return f"PROCESSES:\n{filtered_ps[:5000]}\n\nSOCKETS:\n{ss}\n\nFILES:\n{lsof}"

def delegate_to_ollama(state_data, model="deepseek-r1:14b"):
    """Sends state data to local Ollama for forensic analysis."""
    prompt = f"Analyze this system state for anomalous ICMP or network patterns. Data: {state_data}"
    
    cmd = ["ollama", "run", model, prompt]
    print(f"Delegating analysis to {model}...")
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    
    if process.returncode == 0:
        return stdout
    else:
        return f"Error: {stderr}"

if __name__ == "__main__":
    state = get_system_state()
    analysis = delegate_to_ollama(state)
    print("\n--- FORENSIC ANALYSIS ---\n")
    print(analysis)
