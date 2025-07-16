#!/usr/bin/env python3
"""
TCP Client Example - Connect to a web server and fetch a page

This demonstrates the basics of network programming:
1. Creating a socket connection
2. Sending HTTP requests
3. Receiving and processing responses
4. Proper connection cleanup

Usage: python tcp_client.py
"""

import socket
import sys

def tcp_client(host, port):
    """
    Connect to a web server and send an HTTP request
    
    Args:
        host (str): Target hostname or IP address
        port (int): Target port number
    """
    try:
        # Create TCP socket
        # AF_INET = IPv4, SOCK_STREAM = TCP
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"Connecting to {host}:{port}")
        
        # Connect to the target
        client.connect((host, port))
        
        # Send HTTP GET request
        http_request = f"GET / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Python-Client\r\n\r\n"
        client.send(http_request.encode())
        
        # Receive response (up to 4096 bytes)
        response = client.recv(4096)
        
        print("Response received:")
        print("-" * 50)
        print(response.decode('utf-8', errors='ignore'))
        
    except socket.gaierror as e:
        print(f"DNS resolution failed: {e}")
    except socket.error as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Always close the connection
        try:
            client.close()
            print("Connection closed")
        except:
            pass

def banner_grab(host, port):
    """
    Simple banner grabbing - useful for service identification
    
    Args:
        host (str): Target hostname or IP
        port (int): Target port
    """
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)  # 5 second timeout
        
        client.connect((host, port))
        
        # Some services send banner immediately
        banner = client.recv(1024)
        
        if banner:
            print(f"Banner from {host}:{port}")
            print(banner.decode('utf-8', errors='ignore').strip())
        else:
            print(f"No banner received from {host}:{port}")
            
        client.close()
        
    except Exception as e:
        print(f"Banner grab failed for {host}:{port} - {e}")

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
        tcp_client(host, port)
    else:
        # Default examples
        print("=== HTTP Request Example ===")
        tcp_client("httpbin.org", 80)
        
        print("\n=== Banner Grabbing Examples ===")
        banner_grab("httpbin.org", 80)