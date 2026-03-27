#!/bin/bash
# Suppress AT&T Heartbeat Noise (Ethertype 0x7373)
# and common local network bloat (UPnP/mDNS)

echo "Applying Ethernet-level noise suppression..."

# Drop AT&T proprietary heartbeats
sudo ebtables -F
sudo ebtables -A INPUT -p 0x7373 -j DROP
sudo ebtables -A FORWARD -p 0x7373 -j DROP

# Block redundant noise at UFW level
echo "Updating UFW rules for local noise..."
sudo ufw deny proto udp from any to any port 1900
sudo ufw deny proto udp from any to any port 5353

echo "Current ebtables rules:"
sudo ebtables -L
