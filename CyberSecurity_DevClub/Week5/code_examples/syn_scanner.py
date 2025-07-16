#!/usr/bin/env python3
"""
SYN Scanner using Scapy - Educational stealth scanning tool

This demonstrates advanced packet crafting and network reconnaissance:
- Custom packet creation with Scapy
- Stealth scanning techniques
- Network protocol understanding

WARNING: Only use on networks you own or have permission to test.

Usage: python syn_scanner.py <target> <ports>
Example: python syn_scanner.py 192.168.1.1 22,80,443
"""

from scapy.all import *
import sys
import random
import time

class SYNScanner:
    def __init__(self, target, interface=None):
        self.target = target
        self.interface = interface
        self.open_ports = []
        
        # Generate random source port for each scan
        self.src_port = random.randint(1024, 65535)
        
    def syn_scan_port(self, port):
        """
        Perform SYN scan on a single port
        
        How SYN scanning works:
        1. Send SYN packet (connection request)
        2. Wait for response:
           - SYN-ACK = port open
           - RST = port closed
           - No response = filtered/dropped
        3. Send RST to close connection (stealth)
        
        Args:
            port (int): Target port to scan
            
        Returns:
            str: 'open', 'closed', or 'filtered'
        """
        try:
            # Create IP layer
            ip_layer = IP(dst=self.target)
            
            # Create TCP layer with SYN flag
            tcp_layer = TCP(
                sport=self.src_port,  # Random source port
                dport=port,           # Target port
                flags="S"             # SYN flag
            )
            
            # Combine layers into packet
            packet = ip_layer / tcp_layer
            
            print(f"[*] Scanning port {port}...")
            
            # Send packet and wait for response
            response = sr1(
                packet,
                timeout=2,      # 2 second timeout
                verbose=0       # Suppress Scapy output
            )
            
            if response:
                # Check TCP flags in response
                if response.haslayer(TCP):
                    tcp_flags = response[TCP].flags
                    
                    # SYN-ACK response (flags = 18)
                    if tcp_flags == 18:
                        print(f"[+] Port {port}: OPEN")
                        
                        # Send RST to close connection (stealth)
                        rst_packet = IP(dst=self.target) / TCP(
                            sport=self.src_port,
                            dport=port,
                            flags="R"
                        )
                        send(rst_packet, verbose=0)
                        
                        return 'open'
                    
                    # RST response (flags = 4)
                    elif tcp_flags == 4:
                        print(f"[-] Port {port}: CLOSED")
                        return 'closed'
                
                # ICMP response (port unreachable, etc.)
                elif response.haslayer(ICMP):
                    print(f"[!] Port {port}: FILTERED (ICMP response)")
                    return 'filtered'
            
            else:
                # No response - likely filtered
                print(f"[!] Port {port}: FILTERED (no response)")
                return 'filtered'
                
        except Exception as e:
            print(f"[!] Error scanning port {port}: {e}")
            return 'error'
    
    def scan_ports(self, ports):
        """
        Scan multiple ports
        
        Args:
            ports (list): List of ports to scan
        """
        print(f"Starting SYN scan on {self.target}")
        print(f"Scanning {len(ports)} ports...")
        print("-" * 50)
        
        results = {'open': [], 'closed': [], 'filtered': []}
        
        for port in ports:
            result = self.syn_scan_port(port)
            
            if result in results:
                results[result].append(port)
            
            # Small delay between scans to be respectful
            time.sleep(0.1)
        
        # Print summary
        print("\n" + "=" * 50)
        print("SCAN SUMMARY")
        print("=" * 50)
        
        if results['open']:
            print(f"Open ports ({len(results['open'])}): {', '.join(map(str, results['open']))}")
        
        if results['closed']:
            print(f"Closed ports ({len(results['closed'])}): {', '.join(map(str, results['closed']))}")
        
        if results['filtered']:
            print(f"Filtered ports ({len(results['filtered'])}): {', '.join(map(str, results['filtered']))}")
        
        return results
    
    def stealth_scan(self, ports, delay_range=(0.5, 2.0)):
        """
        Perform stealth scan with random delays
        
        Args:
            ports (list): Ports to scan
            delay_range (tuple): Min and max delay between scans
        """
        print(f"Starting STEALTH SYN scan on {self.target}")
        print(f"Using random delays between {delay_range[0]} and {delay_range[1]} seconds")
        print("-" * 60)
        
        results = {'open': [], 'closed': [], 'filtered': []}
        
        # Randomize port order to avoid detection
        random.shuffle(ports)
        
        for port in ports:
            result = self.syn_scan_port(port)
            
            if result in results:
                results[result].append(port)
            
            # Random delay to avoid pattern detection
            delay = random.uniform(delay_range[0], delay_range[1])
            time.sleep(delay)
        
        return results

def parse_ports(port_string):
    """
    Parse port specification string
    
    Supports:
    - Single ports: "80"
    - Ranges: "1-1000"
    - Lists: "22,80,443"
    - Mixed: "22,80-90,443"
    
    Args:
        port_string (str): Port specification
        
    Returns:
        list: List of port numbers
    """
    ports = []
    
    for part in port_string.split(','):
        if '-' in part:
            # Handle ranges
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            # Handle single ports
            ports.append(int(part))
    
    return sorted(list(set(ports)))  # Remove duplicates and sort

def main():
    """Main function"""
    if len(sys.argv) < 3:
        print("Usage: python syn_scanner.py <target> <ports> [stealth]")
        print("\nPort specification examples:")
        print("  Single port: 80")
        print("  Multiple ports: 22,80,443")
        print("  Port range: 1-1000")
        print("  Mixed: 22,80-90,443,8080")
        print("\nExamples:")
        print("  python syn_scanner.py 192.168.1.1 22,80,443")
        print("  python syn_scanner.py example.com 1-1000")
        print("  python syn_scanner.py 10.0.0.1 80 stealth")
        sys.exit(1)
    
    target = sys.argv[1]
    port_spec = sys.argv[2]
    stealth_mode = len(sys.argv) > 3 and sys.argv[3].lower() == 'stealth'
    
    # Parse ports
    try:
        ports = parse_ports(port_spec)
        if not ports:
            raise ValueError("No valid ports specified")
    except ValueError as e:
        print(f"[!] Invalid port specification: {e}")
        sys.exit(1)
    
    # Validate port ranges
    for port in ports:
        if not (1 <= port <= 65535):
            print(f"[!] Invalid port: {port}. Ports must be 1-65535")
            sys.exit(1)
    
    # Check if running as root (required for raw sockets)
    if os.geteuid() != 0:
        print("[!] This script requires root privileges for raw socket access")
        print("    Run with: sudo python syn_scanner.py ...")
        sys.exit(1)
    
    # Ethical warning
    print("=" * 60)
    print("EDUCATIONAL SYN SCANNER")
    print("=" * 60)
    print("WARNING: Only scan systems you own or have permission to test!")
    print("Unauthorized scanning may be illegal in your jurisdiction.")
    print("=" * 60)
    
    try:
        # Create scanner
        scanner = SYNScanner(target)
        
        # Run appropriate scan type
        if stealth_mode:
            results = scanner.stealth_scan(ports)
        else:
            results = scanner.scan_ports(ports)
        
        # Additional information
        print(f"\nScan completed. Scanned {len(ports)} ports on {target}")
        if results['open']:
            print("Consider running service detection on open ports:")
            print(f"nmap -sV -p {','.join(map(str, results['open']))} {target}")
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[!] Scan error: {e}")

if __name__ == "__main__":
    main()