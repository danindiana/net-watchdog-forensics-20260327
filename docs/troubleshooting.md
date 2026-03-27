# Troubleshooting & Scenario Guide

## 1. Network Issues
### Persistent "Poor" Connections
- **Cause:** AT&T BGW320 Gateways emit proprietary heartbeats (Ethertype 0x7373) every few seconds.
- **Symptom:** Small spikes in latency reported by `netwatch` or `ndisk`.
- **Solution:** Use `suppress_noise.sh` to drop these packets at the Ethernet layer.

### Low Throughput on 10GbE NIC
- **Cause:** MTU mismatch. Many gateways only support MTU 1500.
- **Symptom:** Packet fragmentation, high CPU usage during downloads, or `speedtest` failures.
- **Solution:** Use `harden_nic.sh` to enforce MTU 1500 and double the ring buffers.

## 2. Multi-Agent VRAM Contention
### Ollama Model Swap Latency
- **Scenario:** Running multiple models with `OLLAMA_MAX_LOADED_MODELS=1`.
- **Symptom:** Each forensic check takes 30s+ due to model loading.
- **Solution:** Use the `qwen3.5:0.8b` model for routine checks. It occupies minimal VRAM (~1GB) and loads almost instantly.

### NVIDIA-SMI Resource Errors
- **Scenario:** GPUs are busy with other tasks (e.g., training, heavy inference).
- **Symptom:** `analyze_state.py` fails to find free VRAM.
- **Solution:** The script will automatically fallback to the smallest available model. You can also manually override:
  ```bash
  python3 scripts/analyze_state.py qwen3.5:0.8b
  ```

## 3. Forensic Scenarios
### Identifying "Hidden" Pings
If `tcpdump` shows ICMP traffic but `ps` doesn't show standard `ping` commands:
1. Run `analyze_state.py`.
2. Check for processes with raw sockets (`raw` type in `ss -wnp`).
3. Cross-reference with `lsof -i` to find the specific file descriptor.
