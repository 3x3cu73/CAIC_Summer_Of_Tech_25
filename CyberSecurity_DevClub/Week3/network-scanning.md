# Network Scanning & Enumeration

## What is Network Scanning?

Network scanning is like knocking on doors to see who's home. It's the process of discovering live hosts, open ports, and running services on a network. For security professionals, it's essential for:
- **Asset discovery** - Finding all devices on your network
- **Vulnerability assessment** - Identifying potential entry points
- **Network mapping** - Understanding network topology and services
- **Compliance checking** - Verifying security policies are enforced

**⚠️ Legal Notice:** Only scan networks you own or have explicit permission to test.

---

## Nmap - The Network Reconnaissance Tool

Nmap (Network Mapper) is the industry standard for network discovery. Think of it as a Swiss Army knife for network reconnaissance.

### Core Nmap Concepts

**How Nmap Works - The TCP Handshake**
Normal TCP connection: SYN → SYN-ACK → ACK
Nmap's SYN scan: SYN → SYN-ACK → RST (doesn't complete connection)
This makes it "stealthier" because it doesn't establish full connections.

**Essential Scan Types (Master These)**
```bash
# Host discovery - find live systems
nmap -sn 192.168.1.0/24

# SYN scan - fast and stealthy (requires root)
sudo nmap -sS target.com

# Service detection - identify what's running
nmap -sV target.com
```

**Why These Matter:**
- **SYN scan (-sS)**: Faster than full TCP connect, less likely to be logged
- **Service detection (-sV)**: Reveals software versions (critical for finding vulnerabilities)
- **UDP scan (-sU)**: Many forget this, but services like DNS run on UDP

### Essential Nmap Techniques

**The Power of NSE (Nmap Scripting Engine)**
NSE scripts are like specialized tools for specific tasks. Think of them as Nmap's plugin system:

```bash
# Default safe scripts - good starting point
nmap -sC target.com

# Vulnerability detection - find known security issues
nmap --script vuln target.com

# HTTP enumeration - discover web directories and files
nmap --script http-enum -p80,443 target.com
```

**Why NSE Scripts Matter:**
- **Pre-built expertise**: Scripts written by security experts
- **Automated testing**: Check for specific vulnerabilities automatically
- **Time-saving**: No need to manually test each service

**Timing and Performance - The -T Flag**
```bash
# T4 is the sweet spot for most scans
nmap -T4 target.com  # Aggressive but reasonable

# T1 for stealth (very slow)
nmap -T1 target.com

# T5 for speed (may miss results)
nmap -T5 target.com
```

---

## Practical Scanning Workflow

### 1. Host Discovery
```bash
# Find live hosts on network
nmap -sn 192.168.1.0/24

# Alternative methods if ICMP is blocked
nmap -PS22,80,443 192.168.1.0/24  # TCP SYN ping
nmap -PA80,443 192.168.1.0/24     # TCP ACK ping
```

### 2. Port Scanning
```bash
# Fast scan of common ports
nmap -F target.com

# Comprehensive scan
nmap -sS -O -sV -T4 target.com

# Save results in all formats
nmap -oA scan_results target.com
```

### 3. Service Enumeration
```bash
# HTTP services
nmap --script http-headers,http-methods -p80,443 target.com

# SSH services  
nmap --script ssh-auth-methods -p22 target.com

# SMB services (Windows)
nmap --script smb-enum-shares -p445 target.com
```

---

## Alternative Scanning Tools

### Masscan - High-Speed Scanning
```bash
# Install masscan
sudo apt install masscan

# Fast scan of common ports
sudo masscan -p80,443,22,21 192.168.1.0/24 --rate=1000

# Scan entire internet for specific port (theoretical)
sudo masscan -p443 0.0.0.0/0 --rate=10000
```

### Banner Grabbing with Netcat
```bash
# Manual banner grabbing
nc target.com 80
# Type: HEAD / HTTP/1.0 [Enter][Enter]

nc target.com 22  # SSH banner
nc target.com 25  # SMTP banner
```

---

## Vulnerability Scanning

### Nuclei - Modern Vulnerability Scanner
```bash
# Install nuclei
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Basic vulnerability scan
nuclei -u https://target.com

# Scan with specific templates
nuclei -u https://target.com -t cves/
nuclei -u https://target.com -t exposures/

# Scan multiple targets
echo "https://target1.com https://target2.com" | nuclei
```

### OpenVAS (Enterprise Vulnerability Management)
- **Installation:** Complex, use official documentation
- **Web Interface:** Comprehensive vulnerability management
- **Use Case:** Enterprise-grade vulnerability assessments
- **Learning Resource:** https://www.openvas.org/

---

## Interpreting Scan Results

### Understanding Port States
- **Open**: Service accepting connections
- **Closed**: Port accessible but no service
- **Filtered**: Firewall blocking access
- **Open|Filtered**: Cannot determine state

### Example Nmap Output Analysis
```bash
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 7.4 (protocol 2.0)
80/tcp  open  http     Apache httpd 2.4.6 ((CentOS))
443/tcp open  ssl/http Apache httpd 2.4.6 ((CentOS))
3306/tcp closed mysql
```

**What this tells us:**
- SSH is running (potential remote access)
- Web server is Apache on CentOS (research CVEs for this version)
- HTTPS is available (check certificate details)
- MySQL port is closed (but MySQL might be running on non-standard port)

---

## Scanning Best Practices

### Legal and Ethical Guidelines
- **Only scan what you own** or have explicit permission
- **Follow responsible disclosure** for vulnerabilities found
- **Respect rate limits** to avoid overwhelming systems
- **Document everything** for accountability

### Technical Best Practices
- **Start with host discovery** before port scanning
- **Use appropriate timing** based on network conditions
- **Combine multiple tools** for comprehensive coverage
- **Save results** in multiple formats for analysis

### Detection Avoidance
```bash
# Slow and stealthy
nmap -T1 -sS target.com

# Use random decoys
nmap -D RND:5 target.com

# Source port spoofing
nmap --source-port 53 target.com
```

---

## Hands-On Exercises

### Exercise 1: Local Network Discovery
```bash
# Step 1: Find your network range
ip route show | grep default

# Step 2: Discover live hosts
nmap -sn YOUR_NETWORK/24

# Step 3: Scan interesting hosts
nmap -sV -T4 HOST_IP
```

### Exercise 2: Service Enumeration
```bash
# Scan for web services
nmap -p 80,443,8080,8443 --script http-headers target.com

# Check for common vulnerabilities
nmap --script vuln target.com
```

### Exercise 3: Stealth Scanning
```bash
# Compare normal vs stealth scan results
nmap -sS target.com
nmap -sS -T1 -f target.com
```

---

## Advanced Learning Resources

**Official Documentation:**
- **Nmap Book**: https://nmap.org/book/ (free online)
- **Nmap NSE Scripts**: https://nmap.org/nsedoc/

**Practice Platforms:**
- **Metasploitable**: Intentionally vulnerable Linux
- **DVWA**: Damn Vulnerable Web Application  
- **HackTheBox**: Retired machines (with VIP)

**Advanced Courses:**
- **SANS SEC560**: Network Penetration Testing
- **eLearnSecurity ePTX**: Penetration Testing eXtreme
- **Cybrary**: Free network security courses

**Books:**
- **"Nmap Network Scanning"** by Gordon Lyon (Nmap creator)
- **"The Network Security Test Lab"** by Michael Gregg

---

## Quick Reference

### Essential Nmap Commands
```bash
# Host discovery
nmap -sn 192.168.1.0/24

# Basic port scan
nmap target.com

# Service detection
nmap -sV target.com  

# Vulnerability scanning
nmap --script vuln target.com

# Comprehensive scan
nmap -sS -O -sV -sC -T4 target.com

# Save all formats
nmap -oA results target.com
```

### Common Port Numbers
```
22    - SSH (secure shell)
25    - SMTP (email)
53    - DNS (domain names)
80    - HTTP (web)
135   - Windows RPC
139   - NetBIOS (Windows)
443   - HTTPS (secure web)
445   - SMB (Windows file sharing)
993   - IMAPS (secure email)
3389  - RDP (Windows remote desktop)
```

### Quick Vulnerability Checks
```bash
# Check for eternal blue (Windows)
nmap --script smb-vuln-ms17-010 target.com

# Check for heartbleed (OpenSSL)
nmap --script ssl-heartbleed -p 443 target.com

# Check for weak SSH
nmap --script ssh-auth-methods -p 22 target.com
```

Remember: Scanning is just the beginning. The real security work happens when you analyze and act on the results!