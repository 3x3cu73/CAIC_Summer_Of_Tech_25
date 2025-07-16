#!/usr/bin/env python3
"""
Port Scanner - Educational network reconnaissance tool

This scanner demonstrates:
- TCP connection testing
- Threading for performance
- Proper error handling
- Service identification techniques

Usage: python port_scanner.py <target> [start_port] [end_port]
Example: python port_scanner.py 192.168.1.1 1 1000
"""

import socket
import sys
import threading
import time
from datetime import datetime
import queue

class PortScanner:
    def __init__(self, target, start_port=1, end_port=1000, threads=100):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.threads = threads
        self.open_ports = []
        self.port_queue = queue.Queue()
        self.results_lock = threading.Lock()
        
        # Common services for identification
        self.common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            3389: 'RDP',
            5432: 'PostgreSQL',
            3306: 'MySQL'
        }
    
    def scan_port(self, port):
        """
        Test if a single port is open
        
        Args:
            port (int): Port number to scan
            
        Returns:
            bool: True if port is open, False otherwise
        """
        try:
            # Create socket with timeout
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 1 second timeout
            
            # Attempt connection
            result = sock.connect_ex((self.target, port))
            
            sock.close()
            
            # connect_ex returns 0 if successful
            return result == 0
            
        except socket.gaierror:
            # DNS resolution failed
            return False
        except Exception:
            # Other errors
            return False
    
    def worker_thread(self):
        """
        Worker thread function for scanning ports
        """
        while True:
            try:
                # Get port from queue (timeout after 1 second)
                port = self.port_queue.get(timeout=1)
                
                # Scan the port
                if self.scan_port(port):
                    # Thread-safe addition to results
                    with self.results_lock:
                        service = self.common_ports.get(port, 'Unknown')
                        self.open_ports.append((port, service))
                        print(f"[+] Port {port}/tcp open ({service})")
                
                # Mark task as done
                self.port_queue.task_done()
                
            except queue.Empty:
                # No more ports to scan
                break
            except Exception as e:
                print(f"[!] Worker thread error: {e}")
                break
    
    def banner_grab(self, port):
        """
        Attempt to grab service banner for identification
        
        Args:
            port (int): Port to grab banner from
            
        Returns:
            str: Service banner or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target, port))
            
            # Some services send banner immediately
            banner = sock.recv(1024)
            sock.close()
            
            if banner:
                return banner.decode('utf-8', errors='ignore').strip()
            
        except:
            pass
        
        return None
    
    def run_scan(self):
        """
        Run the port scan with threading
        """
        print(f"Starting port scan on {self.target}")
        print(f"Scanning ports {self.start_port} to {self.end_port}")
        print(f"Using {self.threads} threads")
        print(f"Scan started at {datetime.now()}")
        print("-" * 50)
        
        start_time = time.time()
        
        # Add all ports to queue
        for port in range(self.start_port, self.end_port + 1):
            self.port_queue.put(port)
        
        # Create and start worker threads
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker_thread)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Wait for all ports to be scanned
        self.port_queue.join()
        
        end_time = time.time()
        
        # Print summary
        print("-" * 50)
        print(f"Scan completed in {end_time - start_time:.2f} seconds")
        print(f"Found {len(self.open_ports)} open ports")
        
        if self.open_ports:
            print("\nOpen ports summary:")
            for port, service in sorted(self.open_ports):
                print(f"  {port}/tcp\t{service}")
                
                # Try to grab banner for more info
                banner = self.banner_grab(port)
                if banner:
                    print(f"    Banner: {banner[:100]}...")
        else:
            print("No open ports found")
    
    def validate_target(self):
        """
        Validate that target is reachable
        
        Returns:
            bool: True if target is valid, False otherwise
        """
        try:
            socket.gethostbyname(self.target)
            return True
        except socket.gaierror:
            print(f"[!] Could not resolve hostname: {self.target}")
            return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python port_scanner.py <target> [start_port] [end_port]")
        print("Examples:")
        print("  python port_scanner.py 192.168.1.1")
        print("  python port_scanner.py example.com 1 100")
        print("  python port_scanner.py 10.0.0.1 80 80")
        sys.exit(1)
    
    # Parse command line arguments
    target = sys.argv[1]
    start_port = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end_port = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    
    # Validate port range
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("[!] Invalid port range. Ports must be 1-65535 and start <= end")
        sys.exit(1)
    
    # Create scanner
    scanner = PortScanner(target, start_port, end_port)
    
    # Validate target
    if not scanner.validate_target():
        sys.exit(1)
    
    # Ethical warning
    print("=" * 60)
    print("EDUCATIONAL PORT SCANNER")
    print("=" * 60)
    print("WARNING: Only scan systems you own or have permission to test!")
    print("Unauthorized scanning may be illegal in your jurisdiction.")
    print("=" * 60)
    
    try:
        # Run the scan
        scanner.run_scan()
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[!] Scan error: {e}")

if __name__ == "__main__":
    main()