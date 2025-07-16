#!/usr/bin/env python3
"""
Packet Sniffer - Educational network monitoring tool

This demonstrates network traffic analysis and packet inspection:
- Capturing network packets in real-time
- Protocol analysis and parsing
- Traffic pattern recognition
- Network forensics basics

WARNING: Only use on networks you own or have permission to monitor.

Usage: python packet_sniffer.py [interface] [filter]
Example: python packet_sniffer.py eth0 "tcp port 80"
"""

from scapy.all import *
import sys
import time
from collections import defaultdict
import signal

class PacketSniffer:
    def __init__(self, interface=None, packet_filter=""):
        self.interface = interface
        self.packet_filter = packet_filter
        self.packet_count = 0
        self.protocol_stats = defaultdict(int)
        self.connection_stats = defaultdict(int)
        self.suspicious_activities = []
        
        # Track connections for analysis
        self.connections = {}
        
        # Suspicious indicators
        self.suspicious_ports = [1234, 4444, 5555, 8080, 31337]
        self.scan_threshold = 10  # Port scan detection threshold
        
    def analyze_packet(self, packet):
        """
        Analyze individual packets for interesting information
        
        Args:
            packet: Scapy packet object
        """
        self.packet_count += 1
        
        # Basic packet information
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto
            
            # Update protocol statistics
            if packet.haslayer(TCP):
                self.protocol_stats['TCP'] += 1
                self.analyze_tcp_packet(packet, timestamp)
            elif packet.haslayer(UDP):
                self.protocol_stats['UDP'] += 1
                self.analyze_udp_packet(packet, timestamp)
            elif packet.haslayer(ICMP):
                self.protocol_stats['ICMP'] += 1
                self.analyze_icmp_packet(packet, timestamp)
            
            # Check for suspicious activities
            self.check_suspicious_activity(packet, timestamp)
        
        elif packet.haslayer(ARP):
            self.protocol_stats['ARP'] += 1
            self.analyze_arp_packet(packet, timestamp)
        
        # Print packet summary every 10 packets
        if self.packet_count % 10 == 0:
            self.print_statistics()
    
    def analyze_tcp_packet(self, packet, timestamp):
        """
        Analyze TCP packets for connections and suspicious activity
        
        Args:
            packet: TCP packet
            timestamp: Packet timestamp
        """
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        flags = packet[TCP].flags
        
        # Connection tracking
        connection_key = f"{src_ip}:{src_port} -> {dst_ip}:{dst_port}"
        
        print(f"[{timestamp}] TCP: {connection_key} (Flags: {flags})")
        
        # Check for SYN packets (potential port scanning)
        if flags == 2:  # SYN flag
            scan_key = f"{src_ip}_to_{dst_ip}"
            self.connection_stats[scan_key] += 1
            
            # Detect potential port scanning
            if self.connection_stats[scan_key] > self.scan_threshold:
                self.suspicious_activities.append({
                    'type': 'Port Scan',
                    'timestamp': timestamp,
                    'source': src_ip,
                    'target': dst_ip,
                    'details': f'Multiple SYN packets detected ({self.connection_stats[scan_key]})'
                })
        
        # Check for suspicious ports
        if dst_port in self.suspicious_ports:
            print(f"    [!] SUSPICIOUS: Connection to known backdoor port {dst_port}")
            self.suspicious_activities.append({
                'type': 'Suspicious Port',
                'timestamp': timestamp,
                'source': src_ip,
                'destination': f"{dst_ip}:{dst_port}",
                'details': f'Connection to suspicious port {dst_port}'
            })
        
        # Check for potential data exfiltration (large outbound packets)
        if packet.haslayer(Raw) and len(packet[Raw].load) > 1000:
            print(f"    [!] LARGE DATA: {len(packet[Raw].load)} bytes")
    
    def analyze_udp_packet(self, packet, timestamp):
        """
        Analyze UDP packets
        
        Args:
            packet: UDP packet
            timestamp: Packet timestamp
        """
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        
        print(f"[{timestamp}] UDP: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
        
        # DNS traffic analysis
        if dst_port == 53 or src_port == 53:
            if packet.haslayer(DNSQR):
                query = packet[DNSQR].qname.decode('utf-8')
                print(f"    DNS Query: {query}")
                
                # Check for suspicious DNS queries
                if any(suspicious in query.lower() for suspicious in ['tunnel', 'exfil', 'backdoor']):
                    self.suspicious_activities.append({
                        'type': 'Suspicious DNS',
                        'timestamp': timestamp,
                        'source': src_ip,
                        'details': f'Suspicious DNS query: {query}'
                    })
        
        # DHCP traffic
        elif dst_port == 67 or dst_port == 68:
            print(f"    DHCP Traffic")
    
    def analyze_icmp_packet(self, packet, timestamp):
        """
        Analyze ICMP packets
        
        Args:
            packet: ICMP packet
            timestamp: Packet timestamp
        """
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        icmp_type = packet[ICMP].type
        icmp_code = packet[ICMP].code
        
        icmp_types = {
            0: 'Echo Reply',
            3: 'Destination Unreachable',
            8: 'Echo Request',
            11: 'Time Exceeded'
        }
        
        icmp_name = icmp_types.get(icmp_type, f'Type {icmp_type}')
        print(f"[{timestamp}] ICMP: {src_ip} -> {dst_ip} ({icmp_name})")
        
        # Check for ICMP tunneling (data in ICMP packets)
        if packet.haslayer(Raw) and len(packet[Raw].load) > 64:
            print(f"    [!] SUSPICIOUS: Large ICMP packet ({len(packet[Raw].load)} bytes)")
            self.suspicious_activities.append({
                'type': 'ICMP Tunneling',
                'timestamp': timestamp,
                'source': src_ip,
                'destination': dst_ip,
                'details': f'Large ICMP packet: {len(packet[Raw].load)} bytes'
            })
    
    def analyze_arp_packet(self, packet, timestamp):
        """
        Analyze ARP packets for potential spoofing
        
        Args:
            packet: ARP packet
            timestamp: Packet timestamp
        """
        if packet[ARP].op == 1:  # ARP Request
            print(f"[{timestamp}] ARP Request: Who has {packet[ARP].pdst}? Tell {packet[ARP].psrc}")
        elif packet[ARP].op == 2:  # ARP Reply
            print(f"[{timestamp}] ARP Reply: {packet[ARP].psrc} is at {packet[ARP].hwsrc}")
            
            # Simple ARP spoofing detection (same IP, different MAC)
            arp_key = packet[ARP].psrc
            if arp_key in self.connections:
                if self.connections[arp_key] != packet[ARP].hwsrc:
                    print(f"    [!] POTENTIAL ARP SPOOFING: {arp_key} changed MAC")
                    self.suspicious_activities.append({
                        'type': 'ARP Spoofing',
                        'timestamp': timestamp,
                        'details': f'IP {arp_key} associated with multiple MACs'
                    })
            else:
                self.connections[arp_key] = packet[ARP].hwsrc
    
    def check_suspicious_activity(self, packet, timestamp):
        """
        General suspicious activity checks
        
        Args:
            packet: Network packet
            timestamp: Packet timestamp
        """
        # Check for non-standard packet sizes
        if len(packet) > 1500:  # Larger than standard MTU
            print(f"    [!] LARGE PACKET: {len(packet)} bytes")
        
        # Check for packets with unusual TTL values
        if packet.haslayer(IP) and packet[IP].ttl < 10:
            print(f"    [!] LOW TTL: {packet[IP].ttl}")
    
    def print_statistics(self):
        """
        Print current capture statistics
        """
        print(f"\n--- Statistics (Packets: {self.packet_count}) ---")
        for protocol, count in self.protocol_stats.items():
            print(f"{protocol}: {count}")
        
        if self.suspicious_activities:
            print(f"Suspicious Activities: {len(self.suspicious_activities)}")
        print("-" * 40)
    
    def print_final_report(self):
        """
        Print final analysis report
        """
        print("\n" + "=" * 60)
        print("PACKET CAPTURE ANALYSIS REPORT")
        print("=" * 60)
        
        print(f"Total Packets Captured: {self.packet_count}")
        print(f"Capture Duration: {time.strftime('%H:%M:%S')}")
        
        print("\nProtocol Statistics:")
        for protocol, count in sorted(self.protocol_stats.items()):
            percentage = (count / self.packet_count) * 100 if self.packet_count > 0 else 0
            print(f"  {protocol}: {count} ({percentage:.1f}%)")
        
        if self.suspicious_activities:
            print(f"\nSuspicious Activities Found: {len(self.suspicious_activities)}")
            for i, activity in enumerate(self.suspicious_activities, 1):
                print(f"\n{i}. {activity['type']} at {activity['timestamp']}")
                print(f"   Details: {activity['details']}")
                if 'source' in activity:
                    print(f"   Source: {activity['source']}")
                if 'destination' in activity:
                    print(f"   Destination: {activity['destination']}")
        else:
            print("\nNo suspicious activities detected.")
    
    def start_capture(self, count=0):
        """
        Start packet capture
        
        Args:
            count (int): Number of packets to capture (0 = infinite)
        """
        print(f"Starting packet capture on interface: {self.interface or 'default'}")
        if self.packet_filter:
            print(f"Using filter: {self.packet_filter}")
        print("Press Ctrl+C to stop capture\n")
        
        try:
            sniff(
                iface=self.interface,
                filter=self.packet_filter,
                prn=self.analyze_packet,
                count=count,
                store=0  # Don't store packets in memory
            )
        except KeyboardInterrupt:
            print("\n[!] Capture stopped by user")
        except Exception as e:
            print(f"[!] Capture error: {e}")
        finally:
            self.print_final_report()

def list_interfaces():
    """
    List available network interfaces
    """
    print("Available network interfaces:")
    try:
        interfaces = get_if_list()
        for i, iface in enumerate(interfaces):
            print(f"  {i}: {iface}")
    except:
        print("  Could not enumerate interfaces")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("Usage: python packet_sniffer.py [interface] [filter]")
        print("\nExamples:")
        print("  python packet_sniffer.py                    # Capture on default interface")
        print("  python packet_sniffer.py eth0               # Capture on eth0")
        print("  python packet_sniffer.py eth0 'tcp port 80' # Capture HTTP traffic on eth0")
        print("  python packet_sniffer.py wlan0 'icmp'       # Capture ICMP on wireless")
        print("\nCommon filters:")
        print("  'tcp'                    # TCP traffic only")
        print("  'udp port 53'            # DNS traffic")
        print("  'host 192.168.1.1'       # Traffic to/from specific host")
        print("  'tcp port 22 or tcp port 80' # SSH and HTTP traffic")
        print("\nList interfaces:")
        list_interfaces()
        sys.exit(0)
    
    # Parse command line arguments
    interface = sys.argv[1] if len(sys.argv) > 1 else None
    packet_filter = sys.argv[2] if len(sys.argv) > 2 else ""
    
    # Check if running as root (required for packet capture)
    if os.geteuid() != 0:
        print("[!] This script requires root privileges for packet capture")
        print("    Run with: sudo python packet_sniffer.py ...")
        sys.exit(1)
    
    # Ethical warning
    print("=" * 60)
    print("EDUCATIONAL PACKET SNIFFER")
    print("=" * 60)
    print("WARNING: Only monitor networks you own or have permission to analyze!")
    print("Unauthorized packet capture may be illegal in your jurisdiction.")
    print("=" * 60)
    
    try:
        # Create and start sniffer
        sniffer = PacketSniffer(interface, packet_filter)
        sniffer.start_capture()
        
    except KeyboardInterrupt:
        print("\n[!] Sniffer stopped by user")
    except Exception as e:
        print(f"[!] Sniffer error: {e}")

if __name__ == "__main__":
    main()