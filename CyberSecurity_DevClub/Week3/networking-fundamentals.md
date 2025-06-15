# Networking Fundamentals

## Why Network Knowledge Matters for Security

Understanding networks is like understanding the roads in a city - you need to know how traffic flows to secure it effectively. Every security professional needs networking fundamentals because:
- **Networks are the attack surface** - Most attacks happen over networks
- **Protocols have vulnerabilities** - Each protocol has specific security implications  
- **Tools make more sense** - Understanding why Nmap works helps you use it better

---

## The TCP/IP Stack - How the Internet Works

The TCP/IP model is like a postal system with different departments handling different aspects of mail delivery. Understanding this helps you know where security issues occur and how network tools work.

**Application Layer (Layer 7) - What users interact with**
- Contains protocols like HTTP/HTTPS, SSH, FTP, DNS, SMTP
- **Security significance**: Most vulnerabilities exist here (web apps, email servers)
- **What attacks target**: Application logic, authentication, data validation

**Transport Layer (Layer 4) - How data gets delivered reliably**
- **TCP (Transmission Control Protocol)**: Reliable, connection-oriented
  - Creates a "conversation" between client and server
  - Used for: web browsing, email, file transfers (needs reliability)
- **UDP (User Datagram Protocol)**: Fast, connectionless
  - "Fire and forget" - no guarantee of delivery
  - Used for: DNS queries, video streaming, gaming (speed over reliability)
- **Ports**: Numbers (1-65535) that identify specific services running on a device

**Network Layer (Layer 3) - Addressing and routing**
- **IP addresses**: Unique identifiers for devices on networks
- **Routing**: How packets find their way across multiple networks
- **Security significance**: Source of many reconnaissance techniques

**Data Link Layer (Layer 2) - Local network communication**
- **MAC addresses**: Hardware identifiers for network interfaces
- **Switching**: Moving data within the same physical network
- **Security significance**: ARP spoofing and local network attacks occur here

### Key Concept: Ports and Services
```bash
# Common ports you'll encounter in security:
22   - SSH (secure remote access)
80   - HTTP (websites)  
443  - HTTPS (secure websites)
25   - SMTP (email sending)
53   - DNS (domain name lookup)
3389 - RDP (Windows remote desktop)
```

---

## IP Addresses and Network Ranges

**Understanding IP Address Structure**
IP addresses work like postal addresses - they have network and host portions. Think of it as "Street Name" + "House Number":
- **Network portion**: Identifies which network (like street name)
- **Host portion**: Identifies specific device (like house number)

**CIDR Notation - The /24 Mystery Explained**
The number after the slash tells you how many bits identify the network:
- `/24` = first 24 bits are network, last 8 bits are hosts (256 addresses)
- `/16` = first 16 bits are network, last 16 bits are hosts (65,536 addresses)
- `/8` = first 8 bits are network, last 24 bits are hosts (16,777,216 addresses)

**Private IP Ranges (RFC 1918) - Why They Matter for Security**
These ranges aren't routable on the internet, so they're used for internal networks:
```bash
10.0.0.0/8        # Large organizations (16.7M hosts)
172.16.0.0/12     # Medium networks (1M hosts)  
192.168.0.0/16    # Home/small office (65K hosts)
```

**Security Implication**: When you see these in scans, you know you're looking at internal infrastructure.

---

## Essential Network Tools

### Discovery and Connectivity
```bash
# Test if host is reachable
ping google.com

# Trace route to destination  
traceroute google.com

# DNS lookup
dig google.com
nslookup google.com
```

### Local Network Information
```bash
# Show network interfaces
ip addr show        # Linux
ifconfig           # Linux/Mac

# Show routing table
ip route show      # Linux
netstat -rn        # All systems

# Show active connections
netstat -tulpn     # Linux
ss -tulpn          # Modern Linux
```

### Network Monitoring
```bash
# Show listening services
netstat -ln | grep LISTEN

# Show all connections  
ss -tuln

# Monitor network traffic (requires root)
tcpdump -i eth0
```

---

## Security Implications

### Common Network Attack Vectors
- **Port scanning**: Attackers probe for open services
- **Protocol exploitation**: Each service can have vulnerabilities
- **Man-in-the-middle**: Intercepting network traffic
- **DNS poisoning**: Redirecting domain lookups

### Network Security Concepts
- **Firewalls**: Control traffic between network segments
- **NAT**: Hides internal network structure
- **VLANs**: Segment networks logically
- **Monitoring**: Detect suspicious network activity

---

## Hands-On Practice

### Exercise 1: Map Your Local Network
```bash
# Find your network range
ip route show | grep default

# Discover live hosts (replace with your network)
nmap -sn 192.168.1.0/24

# Check your own open ports
netstat -tulpn | grep LISTEN
```

### Exercise 2: Understand DNS
```bash
# See how DNS resolution works
dig +trace google.com

# Find mail servers
dig google.com MX

# Reverse DNS lookup
dig -x 8.8.8.8
```

---

## Learn More

**Essential Reading:**
- **TCP/IP Illustrated** by W. Richard Stevens (the networking bible)
- **Wireshark Network Analysis** - Learn packet analysis
- **Practical Packet Analysis** by Chris Sanders

**Online Resources:**
- **Professor Messer's Network+** (free): https://www.professormesser.com/
- **Cisco Networking Academy** (comprehensive): https://www.netacad.com/
- **Wireshark University** (packet analysis): https://wiresharktraining.com/

**Practice Labs:**
- **GNS3**: https://gns3.com/ (network simulation)
- **Packet Tracer**: https://www.netacad.com/courses/packet-tracer (Cisco simulator)
- **EVE-NG**: https://www.eve-ng.net/ (advanced network emulation)

---

## Quick Reference

### Private IP Ranges
```
10.0.0.0/8        (10.0.0.0 - 10.255.255.255)
172.16.0.0/12     (172.16.0.0 - 172.31.255.255)  
192.168.0.0/16    (192.168.0.0 - 192.168.255.255)
```

### Critical Ports for Security
```
22    SSH          Secure remote access
25    SMTP         Email (often unencrypted)
53    DNS          Domain name resolution  
80    HTTP         Web traffic (unencrypted)
135   RPC          Windows remote procedure calls
139   NetBIOS      Windows file sharing (legacy)
443   HTTPS        Secure web traffic
445   SMB          Windows file sharing
3389  RDP          Windows remote desktop
```

### Essential Commands
```bash
# Network discovery
ping <host>
traceroute <host>
nmap -sn <network>

# DNS queries  
dig <domain>
nslookup <domain>

# Local network info
ip addr show
netstat -tulpn
ss -tulpn
```

Understanding these fundamentals will make all your reconnaissance tools more effective and help you interpret their results correctly!