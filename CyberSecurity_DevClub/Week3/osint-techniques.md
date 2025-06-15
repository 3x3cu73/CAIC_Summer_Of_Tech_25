# OSINT - Open Source Intelligence

## What is OSINT and Why It Matters

OSINT (Open Source Intelligence) is the practice of collecting and analyzing publicly available information. Think of it as detective work using only legal, public sources. For cybersecurity professionals, OSINT is crucial because:
- **80% of cyber attacks** start with publicly available information
- **Social engineering** relies heavily on OSINT research
- **Threat intelligence** uses OSINT to track adversaries
- **Digital footprint analysis** helps organizations understand their exposure

**Key principle:** If it's publicly available, it's fair game for collection and analysis.

---

## Google Dorking - Advanced Search Mastery

**What Makes Google Dorking Powerful**
Google indexes billions of pages, including many that contain sensitive information not meant to be public. By using advanced search operators, you can find specific types of content that normal users would never discover.

**The Psychology Behind It**: Organizations often forget that search engines index their content. Development sites, configuration files, employee directories, and error pages all become searchable.

### Essential Google Operators

**Site-Specific Intelligence Gathering**
```bash
# Find all pages on a specific domain
site:example.com

# Find employee information
site:linkedin.com "works at Company Name"

# Find exposed credentials and configs  
site:github.com "password" "username"
site:pastebin.com "@company.com" "password"
```

**File Type Discovery**
```bash
# Find specific document types
filetype:pdf site:example.com       # Company PDFs
filetype:xlsx "budget"              # Excel files with financial data
filetype:env "DB_PASSWORD"          # Environment files with secrets
```

**Why This Works**: 
- **PDFs** often contain organizational charts, technical documentation, contact lists
- **Excel files** may have employee data, financial information, technical inventories
- **Config files** accidentally committed to public repositories contain credentials

### High-Value Google Dorks

**Infrastructure Discovery**
```bash
# Find admin panels and management interfaces
site:company.com inurl:admin
site:company.com "server-status"
intitle:"Welcome to nginx" site:company.com
```

**Employee and Contact Intelligence**
```bash
# Employee discovery across platforms
"@company.com" -site:company.com
site:company.com filetype:pdf "employee" OR "directory"
```

### Google Dorks for Security Research
- **Google Hacking Database**: https://www.exploit-db.com/google-hacking-database
- **DorkSearch**: https://dorksearch.com/ (automated dorking)
- **GHDB Categories**: SQL injection, sensitive files, error messages, network data

---

## Social Media Intelligence (SOCMINT)

**Why Social Media Is a Security Goldmine**
People share far more than they realize on social platforms. Employees post about work projects, check in at company locations, share technical frustrations, and reveal organizational relationships. This creates a detailed map of an organization's human infrastructure.

### LinkedIn Reconnaissance

**The Professional Intelligence Hub**
LinkedIn is particularly valuable because people actively share professional information:

```bash
# Employee discovery patterns
site:linkedin.com "Target Company" "Security Engineer"
site:linkedin.com "works at Target Company"
site:linkedin.com "former Target Company employee"
```

**What LinkedIn Reveals:**
- **Organizational hierarchy**: Who reports to whom
- **Technology stack**: People mention tools they use
- **Recent changes**: New hires, departures, promotions  
- **Professional relationships**: Connections between employees
- **Conference attendance**: Industry events and expertise areas

**Security Implications**: Attackers use this to map organizational structure, identify key personnel for social engineering, and understand technology environments.

### Twitter/X Intelligence

**Real-Time Organizational Insights**
```bash
# Company monitoring
site:twitter.com "Target Company"
site:twitter.com from:@companyhandle

# Employee sentiment analysis
site:twitter.com "works at Target Company"
```

**What Twitter Reveals:**
- **Company announcements**: Product launches, security incidents
- **Employee satisfaction**: Complaints or praise about workplace
- **Technical discussions**: Architecture decisions, tool preferences
- **Crisis management**: How companies respond to issues

### Automated Social Media Recon
- **Sherlock**: https://github.com/sherlock-project/sherlock (username hunting)
- **Social Mapper**: https://github.com/Greenwolf/social_mapper (facial recognition)
- **theHarvester**: Built-in social media sources

---

## Email and Username Investigation

**Understanding Email Patterns - The Key to Organizational Mapping**
Most organizations follow predictable email patterns. Once you identify the pattern, you can predict email addresses for any employee.

### Email Pattern Discovery
```bash
# Common corporate email patterns
firstname.lastname@company.com    # Most common
firstname@company.com             # Smaller organizations
f.lastname@company.com           # Space-conscious orgs
flastname@company.com            # Very common
```

**How to Identify Patterns:**
1. Find a few confirmed email addresses (from contact pages, LinkedIn, etc.)
2. Analyze the structure to identify the pattern
3. Apply the pattern to generate potential email addresses
4. Validate using tools like theHarvester

### Username Enumeration Across Platforms

**Why Username Hunting Matters**
People tend to reuse usernames across platforms. Finding someone's username on one platform often leads to discovering their accounts on others, revealing personal interests, connections, and additional contact information.

```bash
# Sherlock - find usernames across platforms
git clone https://github.com/sherlock-project/sherlock
python3 sherlock.py target_username
```

**What Username Discovery Reveals:**
- **Personal interests**: Hobbies, political views, lifestyle choices
- **Professional networks**: Industry connections and expertise
- **Communication channels**: Alternative contact methods
- **Behavioral patterns**: Activity times, communication styles

### Email Breach Analysis

**The Power of Breach Database Analysis**
Data breaches expose not just passwords, but also reveal:
- **Password patterns**: How people construct passwords
- **Account relationships**: Same passwords across multiple services
- **Personal information**: Names, addresses, security questions
- **Timeline data**: When accounts were created, last used

---

## Document and Metadata Analysis

**The Hidden Information in Files**
Every digital document contains metadata - information about the document that's invisible to casual users but reveals significant intelligence about the organization that created it.

### Metadata Extraction
```bash
# Using exiftool
exiftool document.pdf        # Extract all metadata
exiftool *.pdf > metadata.txt   # Batch processing
exiftool -Author -GPS* image.jpg  # Specific fields
```

**What Metadata Typically Reveals:**
- **Author information**: Real names, usernames, email addresses
- **Software versions**: What tools the organization uses
- **Creation timestamps**: When documents were created/modified
- **File paths**: Internal directory structures and server names
- **GPS coordinates**: For images, reveals physical locations
- **Network information**: Printers used, internal IP addresses

**Real-World Example**: A PDF from a company website shows:
- Author: "john.smith@company.com"
- Creator: "Microsoft Word 2019"
- Creation date: Shows working hours
- File path: "C:\Users\john.smith\Documents\Projects\Secret_Project\"

This one file reveals an employee name, email pattern, software versions, and internal project names.

### Intelligence Gathering from Documents
```bash
# Find organization documents
site:company.com filetype:pdf
site:company.com filetype:doc "internal" OR "confidential"
site:company.com filetype:xlsx "budget" OR "financial"
```

**Document Intelligence Workflow:**
1. **Discover documents** using Google dorking
2. **Download documents** from target website  
3. **Extract metadata** with exiftool
4. **Analyze patterns** (authors, software, paths)
5. **Create profiles** of employees and technology stack

---

## Infrastructure and Technical Intelligence

### Domain and IP Intelligence
```bash
# WHOIS information
whois example.com
whois 192.168.1.1

# Historical domain data
# - DomainTools (paid)
# - SecurityTrails (freemium)
# - WhoisHistory.com
```

### Shodan - The Internet Scanner
```bash
# Install and setup
pip install shodan
shodan init YOUR_API_KEY

# Basic searches
shodan search "apache"
shodan search "org:Target Company"
shodan search "hostname:target.com"

# Advanced queries
shodan search "country:US city:Austin port:22"
shodan search "product:MySQL version:5.7"
shodan search "vuln:CVE-2017-0144"
```

### Certificate Intelligence
```bash
# Certificate transparency logs
curl -s "https://crt.sh/?q=%25.company.com&output=json" | \
    jq -r '.[].name_value' | sort -u

# What certificates reveal:
# - Subdomains and internal hostnames
# - Infrastructure changes over time
# - Technology stack indicators
# - Organizational validation details
```

---

## Practical OSINT Workflows

### Basic Company Reconnaissance
```bash
#!/bin/bash
# basic_osint.sh - Quick company intelligence gathering

COMPANY=$1
DOMAIN=$2

echo "[+] Basic OSINT for $COMPANY ($DOMAIN)"

# Step 1: Domain information
echo "=== Domain Intelligence ==="
whois $DOMAIN
dig $DOMAIN MX NS TXT

# Step 2: Subdomain discovery
echo "=== Subdomain Discovery ==="
subfinder -d $DOMAIN -silent | head -10

# Step 3: Email harvesting
echo "=== Email Discovery ==="
theHarvester -d $DOMAIN -b google,bing -l 100

# Step 4: Employee discovery
echo "=== Employee Discovery ==="
echo "Manual: Search 'site:linkedin.com \"$COMPANY\"'"

# Step 5: Document analysis
echo "=== Document Discovery ==="
echo "Manual: Search 'site:$DOMAIN filetype:pdf'"
```

### Social Engineering Preparation
```bash
# Target employee research workflow:
# 1. LinkedIn profile analysis
# 2. Social media presence (Twitter, Facebook, Instagram)
# 3. Professional interests and hobbies
# 4. Recent activities and posts
# 5. Personal relationships and connections
# 6. Technology preferences and expertise
```

---

## Automation and Frameworks

### Recon-ng Framework
```bash
# Install and setup
git clone https://github.com/lanmaster53/recon-ng
cd recon-ng
pip3 install -r REQUIREMENTS

# Basic usage
./recon-ng
workspaces create company_recon
modules install all
modules load recon/domains-hosts/google_site_web
options set SOURCE example.com
run
```

### theHarvester - Email and Subdomain Discovery
```bash
# Comprehensive harvesting
theHarvester -d company.com -b all -f results.html

# Specific sources
theHarvester -d company.com -b google,bing,linkedin,twitter

# Output formats
theHarvester -d company.com -b all -f results.xml
```

### SpiderFoot - Automated OSINT
```bash
# Installation
git clone https://github.com/smicallef/spiderfoot
cd spiderfoot
pip3 install -r requirements.txt

# Web interface
python3 sf.py -l 127.0.0.1:5001

# Command line
python3 sf.py -s example.com -t IP_ADDRESS -m sfp_dnsresolve
```

---

## Advanced OSINT Techniques

### Dark Web and Breach Monitoring
- **Have I Been Pwned**: https://haveibeenpwned.com/
- **DeHashed**: https://dehashed.com/ (paid breach database)
- **IntelX**: https://intelx.io/ (darknet monitoring)

### Geolocation Intelligence
```bash
# IP geolocation
curl "http://ip-api.com/json/8.8.8.8"

# Image geolocation
# - Reverse image search (Google Images, TinEye)
# - EXIF GPS data extraction
# - Visual landmark identification
```

### Cryptocurrency Intelligence
- **Blockchain explorers** for transaction analysis
- **Chainalysis** for professional investigation
- **OSINT framework** for crypto addresses

---

## OSINT Tools and Resources

### Essential OSINT Tools
```bash
# Information gathering
theHarvester          # Email and subdomain harvesting
sherlock              # Username hunting across platforms
recon-ng              # Modular reconnaissance framework
spiderfoot            # Automated OSINT collection

# Social media analysis
twint                 # Twitter intelligence tool
InstagramOSINT        # Instagram analysis
LinkedInt             # LinkedIn intelligence

# Metadata analysis
exiftool              # File metadata extraction
FOCA                  # Document metadata analysis (Windows)
```

### Online OSINT Resources
- **OSINT Framework**: https://osintframework.com/ (comprehensive tool list)
- **IntelTechniques**: https://inteltechniques.com/ (methodologies and tools)
- **Bellingcat**: https://www.bellingcat.com/ (investigative techniques)
- **SANS OSINT**: https://www.sans.org/white-papers/osint/

---

## Hands-On Practice

### Exercise 1: Company Intelligence Gathering
```bash
# Choose a public company for practice
COMPANY="Microsoft"
DOMAIN="microsoft.com"

# Step 1: Basic domain reconnaissance
whois $DOMAIN
dig $DOMAIN MX NS TXT

# Step 2: Employee discovery
# Search: site:linkedin.com "Microsoft" "Security Engineer"

# Step 3: Document analysis  
# Search: site:microsoft.com filetype:pdf

# Step 4: Technology stack research
# Search: site:microsoft.com "powered by" OR "built with"
```

### Exercise 2: Personal Digital Footprint
```bash
# Analyze your own digital footprint (ethical practice)
# 1. Google your full name in quotes
# 2. Search for your email addresses
# 3. Check username availability across platforms
# 4. Review your social media privacy settings
# 5. Search for documents with your metadata
```

### Exercise 3: Breach Analysis
```bash
# Check for compromised credentials (your own only)
# 1. Use Have I Been Pwned to check email addresses
# 2. Review password reuse across services
# 3. Analyze timeline of security incidents
# 4. Implement better security practices based on findings
```

---

## Legal and Ethical Considerations

### What's Legal in OSINT
- **Public websites and databases**
- **Social media posts (public)**
- **Government records and filings**
- **News articles and publications**
- **Academic research and papers**

### Ethical Guidelines
- **Respect privacy** even when information is public
- **Don't overwhelm services** with automated requests
- **Maintain confidentiality** of discovered information
- **Use information constructively** for legitimate security purposes
- **Follow responsible disclosure** for vulnerabilities

### Legal Boundaries
- **No unauthorized access** to systems or accounts
- **Respect terms of service** for websites and APIs
- **Be aware of local laws** regarding data collection
- **Document sources and methods** for accountability

---

## Quick Reference

### Google Dork Cheat Sheet
```bash
# Basic operators
site:domain.com           # Specific site
filetype:pdf             # Specific file type
inurl:admin              # URL contains term
intitle:"index of"       # Title contains phrase
intext:password          # Page contains text

# Advanced combinations
site:company.com filetype:pdf "confidential"
site:linkedin.com "works at Company" "security"
"@company.com" -site:company.com
```

### Essential OSINT Commands
```bash
# Domain intelligence
whois domain.com
dig domain.com MX NS TXT
subfinder -d domain.com

# Email harvesting
theHarvester -d domain.com -b all

# Username hunting
sherlock target_username

# Metadata extraction
exiftool document.pdf
exiftool *.jpg
```

### OSINT Verification Checklist
- [ ] Cross-verify information from multiple sources
- [ ] Check publication dates and relevance
- [ ] Validate accuracy through additional research
- [ ] Document sources and collection methods
- [ ] Assess confidence level of findings
- [ ] Consider potential disinformation

Remember: OSINT is about pattern recognition and correlation. The real intelligence comes from analyzing and connecting information from multiple sources, not just collecting data!