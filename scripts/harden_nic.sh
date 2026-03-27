#!/bin/bash
# NIC Hardening Script for Intel X540-T2
# Optimized for 1 Gbps link on 10GbE hardware

INTERFACE=${1:-enp3s0f0}

echo "Hardening interface: $INTERFACE"

# 1. Doubling Ring Buffers to handle micro-bursts
echo "Setting RX/TX ring buffers to 8192..."
sudo ethtool -G "$INTERFACE" rx 8192 tx 8192

# 2. Setting Interrupt Coalescing
echo "Optimizing interrupt coalescing (96us)..."
sudo ethtool -C "$INTERFACE" rx-usecs 96 tx-usecs 96

# 3. Ensuring MTU 1500 (Gateway Compatibility)
echo "Ensuring MTU 1500..."
sudo ip link set dev "$INTERFACE" mtu 1500

# 4. Verifying Settings
ethtool -g "$INTERFACE" | grep -A 5 "Current"
ethtool -c "$INTERFACE" | grep "rx-usecs"
ip link show "$INTERFACE" | grep "mtu"
