# Session Documentation - 2026-03-27 (Resumed)

## Current Objective
Resolve persistent network latency ("poor" connections) and optimize routing for the Intel X540-T2 and PIA VPN.

## 1. Initial State Assessment
- **Primary NIC:** `enp3s0f0` (192.168.1.135) - Metric 100.
- **Secondary NIC:** `enp3s0f1` (192.168.1.113) - Metric 200.
- **VPN:** `wgpia0` (10.35.150.92) active.
- **Issue:** High jitter on VPN (up to 200ms) and constant outgoing traffic to Singapore (`54.179.117.50`).
- **Local Conflict:** Device `192.168.1.114` (Linksys Extender) sharing a path with the Toshiba printer (`192.168.1.50`), causing high latency.

## 2. Major Breakthroughs & Actions Taken
### **A. Identified & Suppressed "Broadcast Storm"**
- **Discovery:** Captured constant flood of Proprietary Heartbeat packets (Ethertype `0x7373`) originating from the AT&T BGW320 Gateway (`94:8f:cf:65:a2:52`).
- **Impact:** These packets were hitting the NIC at a high frequency, likely contributing to hardware-level RX drops and "poor" connection reports in latency monitors.
- **Mitigation:**
    - Implemented `ebtables` rules to drop `0x7373` at the Ethernet layer (volatile).
    - Updated `UFW` to block redundant UPnP (1900) and mDNS (5353) noise from the extender.

### **B. NIC Hardening & Stabilization**
- **Throughput Verified:** `speedtest` on `enp3s0f0` is now functional (~117 Mbps, 9ms latency) after previously failing.
- **MTU Adjustment:** Reverted MTU from 9000 back to **1500**. Confirmed that the gateway/local network does not support Jumbo Frames, which was causing significant fragmentation and drops.
- **Ring Buffers:** Doubled RX/TX buffers to **8192** on `enp3s0f0` to handle micro-bursts without dropping packets.
- **Driver Observation:** Noted `ixgbe` driver caps RX queues at 16 (on this 32-core system), which is a hardware/driver limitation but not a failure.

### **C. Singapore Ping Investigation**
- **Status:** **Resolved**.
- **Culprit:** Process `ping cgtn.cn` (PID 470664) running in `tmux` session 0, pane %3.
- **Finding:** `cgtn.cn` resolves to `54.179.117.50` (AWS Singapore). The traffic is legitimate part of the user's active monitoring.

### **D. Local Model Delegation (Ollama)**
- **Objective:** Utilize local dual-GPU resources to offload complex pattern matching and log analysis.
- **Action:** Sent filtered system state (ps, lsof, ss) to `deepseek-r1:32b`.
- **Result:** Initial attempt provided general system health assessment but failed to pinpoint the Singapore PID due to data truncation (kernel threads dominated the sample). Refined filtering is required.

## 3. Reboot Safety Assessment
- **Safe to Reboot:** Yes. 
- **Persistence:** 
    - **DNS Fixes:** (Deleted redundant overrides) are **Persistent**.
    - **MTU:** Persistently set to **1500** via NetworkManager for both 10GbE interfaces.
    - **Routing Metrics:** Persistently set to **20050 (Primary)** and **20150 (Secondary)** via NetworkManager, ensuring stable prioritization.
    - **Ring Buffers:** **Volatile** (will revert to 4096, which is safe/functional).
    - **ebtables Noise Suppression:** **Volatile** (reverts to allowing noise, but won't block access).
- **Result:** Connectivity will be maintained and stable. The "race condition" (multipath routing) is permanently resolved by the explicit metric separation.
