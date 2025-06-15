# DevClub Cybersecurity Course – Week 3 Resources
## Networking, Reconnaissance & OSINT

Welcome to Week 3! This week focuses on **reconnaissance** - the art of gathering information about targets without directly attacking them. You'll learn to map network infrastructure, discover hidden assets, and collect intelligence from public sources.

**Why Reconnaissance Matters:**
Reconnaissance is often the longest phase of any security assessment. It's where attackers (and defenders) map out the attack surface, identify potential entry points, and understand the target's digital footprint. The better your reconnaissance, the more targeted and effective your subsequent actions become.

---

## Learning Objectives
By the end of this week, you will:
- Understand network fundamentals and how to systematically map infrastructure
- Use network scanning tools to discover live hosts and running services  
- Enumerate DNS records and discover subdomains effectively
- Gather intelligence from publicly available sources (OSINT)
- Automate reconnaissance workflows for efficiency and consistency
- Understand both offensive and defensive applications of these techniques

---

## Week 3 Topics Overview

**What is Reconnaissance?** Reconnaissance (recon) is the process of gathering information about a target system, network, or organization before conducting security testing. It's like doing research before an exam - the better your intel, the more effective your approach.

**Why Learn These Skills?** Modern cybersecurity professionals need to understand how attackers gather intelligence to:
- Identify and secure exposed assets
- Understand their organization's digital footprint
- Conduct security assessments and penetration tests
- Implement effective monitoring and detection systems

### [Networking Fundamentals](networking-fundamentals.md)
**What you'll learn:** How networks actually work and communicate
- **TCP/IP Basics** - The foundation of internet communication
- **Ports & Services** - How applications talk to each other
- **Network Tools** - Essential commands every security pro should know
- **Why it matters:** You can't secure what you don't understand

### [Network Scanning & Enumeration](network-scanning.md)
**What you'll learn:** How to discover and analyze network assets
- **Nmap Mastery** - The industry-standard network scanner
- **Service Detection** - Identifying what's running on discovered systems
- **Vulnerability Scanning** - Finding potential security weaknesses
- **Why it matters:** This is how attackers map your network - learn to think like them

### [DNS & Subdomain Enumeration](dns-enumeration.md)
**What you'll learn:** How to investigate domain infrastructure
- **DNS Deep Dive** - Understanding domain name resolution
- **Subdomain Discovery** - Finding hidden parts of organizations
- **Zone Transfers** - Exploiting DNS misconfigurations
- **Why it matters:** DNS often reveals more than organizations realize

### [OSINT - Open Source Intelligence](osint-techniques.md)
**What you'll learn:** Gathering intelligence from public sources
- **Google Dorking** - Advanced search techniques for finding sensitive data
- **Social Media Intel** - What people reveal online
- **Data Breach Analysis** - Finding compromised credentials
- **Why it matters:** 80% of successful attacks start with publicly available information

### [Automation & Scripting](recon-automation.md)
**What you'll learn:** How to scale and automate your reconnaissance
- **Bash Scripting** - Automating repetitive tasks
- **Python Tools** - Building custom reconnaissance frameworks
- **Tool Integration** - Creating efficient workflows
- **Why it matters:** Manual recon doesn't scale - automation is essential for real-world security work

---

## Essential Tools & Resources

### Network Scanning Tools
- **Nmap**: https://nmap.org/ - The ultimate network discovery scanner
- **Masscan**: https://github.com/robertdavidgraham/masscan - High-speed port scanner
- **Netcat**: Built into most Linux systems - Network debugging and exploration
- **Netdiscover**: Built into Kali - ARP reconnaissance tool

### DNS & Domain Tools
- **Amass**: https://github.com/OWASP/Amass - In-depth DNS enumeration
- **Subfinder**: https://github.com/projectdiscovery/subfinder - Fast subdomain discovery
- **Whois Lookup**: https://whois.net/ - Domain registration information
- **DNS Dumpster**: https://dnsdumpster.com/ - Free domain research tool

### OSINT Platforms
- **Shodan**: https://www.shodan.io/ - Search engine for Internet-connected devices
- **Censys**: https://censys.io/ - Internet-wide scanning and analysis
- **Have I Been Pwned**: https://haveibeenpwned.com/ - Breach notification service
- **IntelTechniques**: https://inteltechniques.com/tools/ - OSINT tool collection

### Automation & Scripting
- **Recon-ng**: https://github.com/lanmaster53/recon-ng - Modular reconnaissance framework
- **TheHarvester**: Built into Kali - Email and subdomain harvester
- **SpiderFoot**: https://www.spiderfoot.net/ - Automated OSINT collection
- **Maltego**: https://www.maltego.com/ - Link analysis and data mining

---

## Quick Start Guide

### 🌐 New to Networking?
1. Start with [Networking Fundamentals](networking-fundamentals.md) - learn TCP/IP basics
2. Practice with built-in tools like ping, traceroute, and netstat
3. Move to [Network Scanning](network-scanning.md) for active reconnaissance

### 🔍 Want to Find Hidden Assets?
1. Jump to [DNS Enumeration](dns-enumeration.md) - discover subdomains and services
2. Practice with online tools using example domains
3. Learn automation techniques for large-scale discovery

### 🕵️ Interested in Intelligence Gathering?
1. Explore [OSINT Techniques](osint-techniques.md) - start with Google dorking
2. Practice social media and public record investigation
3. Learn to correlate information from multiple sources

---

## Week 3 CTF Challenge (Weekend)

**Challenge Categories:**
1. **Network Scanning**
2. **Service Enumeration**
3. **DNS Investigation**
4. **OSINT Collection**
5. **Automation Scripting**

---

## Real-World Applications

### 🛡️ How These Skills Protect Organizations

**Asset Discovery:**
- Security teams use reconnaissance to inventory all organizational assets
- Penetration testers identify attack surfaces during security assessments
- Compliance auditors verify that all systems are properly documented

**Threat Intelligence:**
- OSINT analysts track threat actors and their infrastructure
- Incident response teams investigate attack origins and methods
- Law enforcement uses digital intelligence for criminal investigations

**Defensive Applications:**
- Network monitoring systems detect unauthorized scanning attempts
- DNS monitoring identifies suspicious domain registrations
- Social media monitoring protects against targeted attacks

---

## Practice Platforms & Resources

### Recommended Online Practice

**TryHackMe Rooms**
- **Google Dorking**: https://tryhackme.com/room/googledorking
- **Passive Reconnaissance**: https://tryhackme.com/room/passiverecon
- **Active Reconnaissance**: https://tryhackme.com/room/activerecon
- **Nmap**: https://tryhackme.com/room/furthernmap

**HackTheBox Academy**
- **Information Gathering**: Comprehensive reconnaissance modules
- **Footprinting**: Advanced enumeration techniques
- **Network Enumeration**: Professional-grade scanning methods

**OSINT Training Platforms**
- **OSINT Exercise**: https://www.osintexercise.com/ - Practice scenarios
- **Trace Labs**: https://www.tracelabs.org/ - Crowdsourced OSINT for good
- **Bellingcat**: https://www.bellingcat.com/ - Professional OSINT techniques

### Legal Practice Targets
- **Metasploitable**: Vulnerable Linux distribution for testing
- **DVWA**: Damn Vulnerable Web Application
- **HackTheBox Retired Machines**: With VIP subscription
- **Your Own Lab**: Set up isolated networks for testing

---

## Week 3 Checklist

- [ ] Read all five topic-specific guides
- [ ] Practiced network scanning with Nmap on legal targets
- [ ] Completed DNS enumeration exercises
- [ ] Performed OSINT investigation on provided scenarios
- [ ] Built basic automation scripts for reconnaissance tasks
- [ ] Understood ethical and legal considerations
- [ ] Ready for Week 3 CTF challenge

---

## Ethical Considerations & Legal Notice

### ⚖️ Legal and Ethical Guidelines

**Always Remember:**
- Only scan networks and systems you own or have explicit permission to test
- Respect rate limits and don't overwhelm target systems
- Follow responsible disclosure for any vulnerabilities discovered
- Understand local laws regarding network scanning and data collection

**Professional Ethics:**
- Document all activities for accountability
- Maintain confidentiality of discovered information
- Use findings constructively to improve security
- Respect privacy and avoid unnecessary intrusion

---

## Getting Help & Community

### 🆘 Common Issues & Solutions

**"Nmap scans are too slow"**
→ Use timing templates (-T4), scan specific ports, use parallel scanning

**"Can't find subdomains"**
→ Try multiple tools, use different wordlists, check certificate transparency logs

**"OSINT searches return no results"**
→ Try different search engines, use various search operators, check archived content

### 📚 Community Resources
- **r/netsec** - Network security discussions and tools
- **r/OSINT** - Open source intelligence community
- **r/AskNetsec** - Questions about network security
- **Penetration Testing Discord servers** - Real-time collaboration

---

## Next Week Preview

**Week 4: Web Security Fundamentals**
Dive into web application security, learn to find and exploit common web vulnerabilities using professional tools like Burp Suite!