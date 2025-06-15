# DNS & Subdomain Enumeration

## Why DNS Matters for Security

DNS (Domain Name System) is often called the "phonebook of the internet," but for security professionals, it's more like a treasure map. Organizations often reveal much more through DNS than they realize:
- **Hidden subdomains** expose internal applications
- **DNS misconfigurations** can leak entire network maps
- **Certificate transparency logs** reveal infrastructure changes
- **Historical DNS data** shows evolution of attack surface

Understanding DNS enumeration is crucial because it's often the first step in discovering an organization's true digital footprint.

---

## DNS Fundamentals

### How DNS Works

**The DNS Resolution Process - Why This Matters for Security**
When you type "google.com" in your browser, here's what actually happens:
1. **Your computer** asks a DNS resolver: "What's the IP for google.com?"
2. **Resolver queries root servers**: "Who handles .com domains?"
3. **Root server responds**: "Ask the .com name servers"
4. **Resolver queries .com servers**: "Who handles google.com?"
5. **Response**: "Ask Google's name servers"
6. **Final query to Google's servers**: Returns IP address

**Why Attackers Love DNS:**
- **Information leakage**: DNS often reveals more than organizations realize
- **Historical data**: Old DNS records show infrastructure changes
- **Misconfigurations**: Zone transfers can dump entire network maps

### Critical DNS Record Types

**A Records - The Foundation**
```bash
A      - Maps domain to IPv4 address (google.com → 142.250.184.14)
AAAA   - Maps domain to IPv6 address
```

**Pointer Records - Reverse Lookups**
```bash
PTR    - Reverse DNS (IP to domain name)
# Example: 8.8.8.8 → dns.google
```

**Service Records - Where the Gold Is**
```bash
MX     - Mail servers (shows email infrastructure)
NS     - Name servers (shows DNS infrastructure)  
CNAME  - Aliases (shows service relationships)
TXT    - Text records (often contains verification tokens, SPF records)
```

**Security Significance**: MX records reveal email servers, NS records show DNS infrastructure, TXT records often contain sensitive configuration data.

---

## Basic DNS Reconnaissance

### Essential DNS Queries
```bash
# Basic domain lookup
dig example.com

# Specific record types
dig example.com MX    # Mail servers
dig example.com NS    # Name servers  
dig example.com TXT   # Text records
dig @8.8.8.8 example.com  # Query specific DNS server

# Reverse DNS lookup
dig -x 8.8.8.8

# Short answers only
dig +short example.com
dig +short example.com MX
```

### Zone Transfer Testing

**What Are Zone Transfers?**
Zone transfers are how DNS servers replicate their databases. Think of it like one server asking another: "Give me a copy of everything you know about this domain."

**Why This Matters:**
When misconfigured, zone transfers can reveal an organization's entire DNS infrastructure - every subdomain, internal server, and service mapping.

```bash
# Step 1: Find name servers
dig example.com NS

# Step 2: Test each name server for zone transfer
dig @ns1.example.com example.com AXFR

# If successful, you'll see ALL DNS records:
# admin.example.com.    A    192.168.1.5
# mail.example.com.     A    192.168.1.10
# dev.example.com.      A    192.168.1.15
```

**Real-World Impact**: A successful zone transfer can reveal internal infrastructure, development environments, admin panels, and other assets that weren't meant to be publicly known.

---

## Subdomain Discovery

**Why Subdomains Matter**
Organizations often have dozens or hundreds of subdomains: dev.company.com, admin.company.com, api.company.com. Each one is a potential entry point, and many are forgotten or poorly secured.

### Passive Discovery (Stealthy)

**Certificate Transparency - The Hidden Goldmine**
Every SSL certificate issued is logged in public Certificate Transparency logs. This means you can find subdomains without ever touching the target's infrastructure:

```bash
# Certificate Transparency logs
curl -s "https://crt.sh/?q=%25.example.com&output=json" | jq -r '.[].name_value' | sort -u

# Using automated tools
subfinder -d example.com -silent
```

**Why This Works**: Companies get SSL certificates for internal services, development sites, and forgotten subdomains. All of these get logged publicly.

### Active Discovery (Detectable)

**Dictionary-Based Brute Force**
```bash
# Using gobuster with common subdomain names
gobuster dns -d example.com -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
```

**The Trade-off**: Active discovery finds more subdomains but generates DNS traffic that can be detected and blocked.

### Comprehensive Enumeration Script
```bash
#!/bin/bash
# dns_recon.sh - Quick DNS enumeration

DOMAIN=$1
echo "[+] DNS reconnaissance for $DOMAIN"

# Basic records
echo "=== Basic DNS Records ==="
for record in A MX NS TXT; do
    echo "--- $record ---"
    dig +short $DOMAIN $record
done

# Zone transfer test
echo "=== Testing Zone Transfers ==="
for ns in $(dig +short $DOMAIN NS); do
    echo "Testing $ns..."
    dig @$ns $DOMAIN AXFR | head -10
done

# Subdomain discovery
echo "=== Subdomain Discovery ==="
subfinder -d $DOMAIN -silent | head -20
```

---

## Advanced DNS Techniques

### DNS Cache Snooping
```bash
# Check if DNS server has cached specific records (passive)
dig @target-dns-server google.com +norecurse

# If response is authoritative, server has cached the record
```

### Wildcard Detection
Some domains use wildcards (*.example.com → same IP), which can interfere with discovery:
```bash
# Test for wildcards
dig randomstring12345.example.com
dig anotherfakestring98765.example.com

# If both resolve to same IP, wildcards are likely present
```

### DNS History and Intelligence
- **SecurityTrails**: Historical DNS data and changes
- **DNSDumpster**: https://dnsdumpster.com/ (free domain research)
- **Wayback Machine**: Historical domain configurations

---

## Automation and Tooling

### Amass - Comprehensive DNS Enumeration
```bash
# Passive enumeration only
amass enum -passive -d example.com

# Active + passive enumeration
amass enum -active -d example.com

# Brute force with wordlist
amass enum -brute -d example.com -w wordlist.txt

# Use specific data sources
amass enum -d example.com -src crtsh,virustotal,threatcrowd
```

### Subfinder - Fast Passive Discovery
```bash
# Basic enumeration
subfinder -d example.com

# Multiple sources
subfinder -d example.com -all

# Output to file
subfinder -d example.com -o subdomains.txt
```

### Custom Python DNS Tool
```python
#!/usr/bin/env python3
import dns.resolver
import sys

def enumerate_dns(domain):
    print(f"[+] DNS enumeration for {domain}")
    
    record_types = ['A', 'MX', 'NS', 'TXT', 'SOA']
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            print(f"\n{record_type} Records:")
            for answer in answers:
                print(f"  {answer}")
        except:
            print(f"No {record_type} records found")

if __name__ == "__main__":
    enumerate_dns(sys.argv[1])
```

---

## Security Assessment

### DNS Security Issues to Look For
- **Zone transfers enabled** on public name servers
- **Subdomain takeover opportunities** (CNAMEs pointing to unclaimed services)
- **Information disclosure** through TXT records
- **Weak DNS configurations** allowing cache poisoning
- **Missing SPF/DMARC records** for email security

### DNS Monitoring and Defense
- **Monitor for new subdomains** that could indicate shadow IT
- **Certificate transparency monitoring** for unauthorized certificates
- **DNS query logging** to detect reconnaissance attempts
- **Rate limiting** to prevent brute force enumeration

---

## Hands-On Practice

### Exercise 1: Basic DNS Reconnaissance
```bash
# Pick a target domain (only ones you own/have permission)
DOMAIN="your-target-domain.com"

# Gather basic information
dig $DOMAIN A MX NS TXT

# Test zone transfers
for ns in $(dig +short $DOMAIN NS); do
    echo "Testing $ns"
    dig @$ns $DOMAIN AXFR
done
```

### Exercise 2: Subdomain Discovery
```bash
# Use multiple tools and compare results
subfinder -d $DOMAIN -silent > subfinder_results.txt
amass enum -passive -d $DOMAIN > amass_results.txt

# Check certificate transparency
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" | jq -r '.[].name_value' | sort -u > crt_results.txt

# Combine and deduplicate
cat *_results.txt | sort -u > all_subdomains.txt
```

### Exercise 3: Subdomain Validation
```bash
# Check which subdomains actually resolve
while read subdomain; do
    if dig +short $subdomain | grep -v '^$'; then
        echo "Active: $subdomain"
    fi
done < all_subdomains.txt
```

---

## Learning Resources

**Essential Reading:**
- **DNS and BIND** by Cricket Liu (the DNS bible)
- **Pro DNS and BIND 10** by Ron Aitchison

**Online Resources:**
- **ISC BIND Documentation**: https://bind9.readthedocs.io/
- **DNS Learning Center**: https://www.cloudflare.com/learning/dns/
- **SANS DNS Security**: https://www.sans.org/white-papers/

**Practice Platforms:**
- **DNSDumpster**: https://dnsdumpster.com/ (free domain research)
- **SecurityTrails**: https://securitytrails.com/ (DNS intelligence)
- **Shodan**: https://www.shodan.io/ (DNS server discovery)

**Advanced Tools:**
- **Fierce**: https://github.com/mschwager/fierce (domain scanner)
- **DNSRecon**: https://github.com/darkoperator/dnsrecon (enumeration tool)
- **MassDNS**: https://github.com/blechschmidt/massdns (high-performance resolver)

---

## Best Practices

### Operational Security
- **Use multiple DNS resolvers** to avoid detection patterns
- **Implement delays** between queries for large-scale enumeration  
- **Rotate source IPs** when possible for extensive reconnaissance
- **Monitor for defensive responses** (rate limiting, blocking)

### Legal and Ethical Considerations
- **Only enumerate domains you own** or have explicit permission to test
- **Respect rate limits** and don't overwhelm DNS servers
- **Follow responsible disclosure** for any security issues discovered
- **Document all activities** for accountability

---

## Quick Reference

### Essential Commands
```bash
# Basic DNS lookup
dig domain.com
dig domain.com MX NS TXT

# Zone transfer test
dig @nameserver domain.com AXFR

# Subdomain discovery
subfinder -d domain.com
amass enum -passive -d domain.com

# Certificate transparency
curl -s "https://crt.sh/?q=%25.domain.com&output=json" | jq -r '.[].name_value'

# Reverse DNS
dig -x IP_ADDRESS
```

### Useful Wordlists
```bash
# SecLists (comprehensive)
/usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt

# Common patterns
www, mail, ftp, admin, api, dev, test, staging, beta
blog, shop, portal, vpn, remote, secure, m, mobile
```

### DNS Security Checklist
- [ ] Zone transfers disabled on public name servers
- [ ] No sensitive information in TXT records  
- [ ] Subdomains properly managed and monitored
- [ ] SPF/DKIM/DMARC records configured
- [ ] DNS monitoring in place for new subdomains
- [ ] Certificate transparency monitoring enabled

DNS enumeration often provides the roadmap for further reconnaissance - master these techniques to understand how attackers map organizational infrastructure!