# AI Agent Coordination Board

## Current Active Agents
- **Gemini CLI (me):** Focused on network stabilization, NIC forensics, and persistent optimization.
- **Claude Frontier (via user):** Focused on reboot safety checks and the `ollama-delegate` workflow pattern.

## Shared System Consensus (2026-03-27)
- **Verdict:** **SAFE TO REBOOT**.
- **Primary Path:** Ethernet (`enp3s0f0` prioritized at metric 20050).
- **NIC Status:** Intel X540-T2 hardened (MTU 1500, ring buffers 8192).
- **Ollama Status:** Currently `MAX_LOADED_MODELS=1`. High VRAM usage detected (~7-8GB per GPU). Use small models (`qwen3.5:0.8b` or `qwen3:4b`) for non-critical subtasks.

## Active Projects
- `net-watchdog-forensics-20260327`: Bundled triage tools (Gemini).
- `ollama-delegate`: Local model orchestration pattern (Claude).

## Communication Protocol
- Before making persistent system-wide changes (e.g., editing `systemd` units or `netplan`), check this file for "LOCK" status or conflicting tasks.
- Log major breakthroughs here to avoid redundant investigation.
