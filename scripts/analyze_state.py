import subprocess
import json
import sys
import re

def get_system_state():
    """Gathers filtered process and network state."""
    ps = subprocess.check_output(["ps", "-eo", "user,pid,ppid,comm,args", "--sort=-start_time"], text=True)
    filtered_ps = "\n".join([line for line in ps.split("\n") if "[" not in line])
    ss = subprocess.check_output(["sudo", "ss", "-wnp"], text=True)
    lsof = subprocess.check_output(["sudo", "lsof", "-nP", "-i"], text=True)
    return f"PROCESSES:\n{filtered_ps[:5000]}\n\nSOCKETS:\n{ss}\n\nFILES:\n{lsof}"

def get_free_vram():
    """Returns the maximum free VRAM (MB) available on any single GPU."""
    try:
        res = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"], text=True)
        free_mem = [int(x) for x in res.strip().split("\n")]
        return max(free_mem)
    except:
        return 0

def get_optimal_model(free_vram_mb):
    """Selects the best fitting model based on size and free VRAM."""
    try:
        res = subprocess.check_output(["ollama", "list"], text=True)
        lines = res.strip().split("\n")[1:] # Skip header
        models = []
        for line in lines:
            parts = re.split(r'\s{2,}', line)
            name = parts[0]
            size_str = parts[2]
            
            val = float(re.search(r'([0-9.]+)', size_str).group(1))
            if 'GB' in size_str: val *= 1024
            
            models.append({'name': name, 'size_mb': val})
        
        target_vram = free_vram_mb - 500
        fit_models = [m for m in models if m['size_mb'] < target_vram]
        
        if not fit_models:
            return min(models, key=lambda x: x['size_mb'])['name']
        
        return max(fit_models, key=lambda x: x['size_mb'])['name']
    except:
        return "qwen3.5:0.8b" 

def delegate_to_ollama(state_data):
    """Sends state data to local Ollama using dynamic model selection or manual override."""
    # Priority: Command line argument -> Optimal VRAM selection -> Fallback
    if len(sys.argv) > 1:
        model = sys.argv[1]
        print(f"Using manual model override: {model}")
    else:
        free_vram = get_free_vram()
        model = get_optimal_model(free_vram)
        print(f"System Free VRAM: {free_vram}MB. Selected Model: {model}")
    
    prompt = f"Analyze this system state for anomalous network patterns. Be concise. Data: {state_data}"
    print(f"Delegating analysis to {model}...")
    
    # Use -s for silent mode if possible, but ollama run is interactive. 
    # For scripts, the API is better, but keeping 'ollama run' as requested for now.
    cmd = ["ollama", "run", model, prompt]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    
    if process.returncode == 0:
        return stdout
    else:
        return f"Error: {stderr}"

if __name__ == "__main__":
    state = get_system_state()
    analysis = delegate_to_ollama(state)
    print("\n--- DYNAMIC FORENSIC ANALYSIS ---\n")
    print(analysis)
