# Burp Suite Mastery

Burp Suite is the industry-standard tool for web application security testing. It's like having a Swiss Army knife for finding web vulnerabilities - every security professional needs to master it.

---

## Why Burp Suite Matters

**It's the industry standard** - Used by penetration testers, bug bounty hunters, and security consultants worldwide.

**It intercepts everything** - See and modify all traffic between your browser and web applications.

**It automates tedious tasks** - Scan for vulnerabilities, brute force parameters, and replay attacks automatically.

**Download:** https://portswigger.net/burp/communitydownload (free Community Edition)

---

## Essential Setup

### Browser Proxy Configuration

**Why proxy through Burp?** To see and modify all HTTP requests before they reach the server.

**Firefox Setup (Recommended):**
1. Settings → Network Settings → Manual proxy configuration
2. HTTP Proxy: `127.0.0.1`, Port: `8080`
3. Check "Use this proxy server for all protocols"

**Install Burp's Certificate:**
1. Go to `http://burp` in your browser
2. Download "CA Certificate" 
3. Firefox: Settings → Privacy & Security → Certificates → Import
4. Check "Trust this CA to identify websites"

**Why certificate matters:** Without it, you can't intercept HTTPS traffic (most modern sites).

---

## Core Features You Must Know

### Proxy - Your Traffic Control Center

**What it does:** Shows every request your browser makes and lets you modify them.

**Essential workflow:**
1. Turn Intercept ON
2. Navigate to target website in browser
3. Request appears in Burp - modify it
4. Click Forward to send modified request

**Pro tip:** Use "Match and Replace" for automatic modifications (like changing User-Agent headers).

### Target - Mapping Your Attack Surface

**Site Map:** Automatically builds a map of all discovered URLs, parameters, and functionality.

**Scope:** Define what you're testing to avoid accidentally attacking other sites.
```
Include: example.com, *.example.com
Exclude: example.com/static/, example.com/images/
```

### Repeater - Manual Testing Powerhouse

**What it does:** Send the same request over and over with small modifications to test for vulnerabilities.

**How to use:**
1. Right-click any request → "Send to Repeater"
2. Modify parameters, headers, or body
3. Send and compare responses
4. Keep multiple tabs for A/B testing

**Perfect for:** Testing SQL injection, XSS, IDOR, and parameter manipulation.

### Intruder - Automated Attack Engine

**Attack Types:**

**Sniper (Single parameter testing):**
```
POST /login
username=admin&password=§password§
# Tests different passwords: admin, 123456, password123
```

**Pitchfork (Multiple parameters, synchronized):**
```
POST /login  
username=§user§&password=§pass§
# Tests: admin/admin123, user/user123, guest/guest123
```

**Cluster Bomb (All combinations):**
```
# Tests every username with every password
# admin/admin, admin/123456, user/admin, user/123456, etc.
```

---

## Practical Testing Workflows

### Finding SQL Injection

**Step 1:** Find injection points
```
# Add single quotes to parameters
id=1'
search=test'
username=admin'
```

**Step 2:** Confirm vulnerability in Repeater
```
# Boolean-based detection
id=1 AND 1=1  (works normally)
id=1 AND 1=2  (error or different response)
```

**Step 3:** Exploit with Intruder
```
# Use Sniper to try different SQL payloads
' OR '1'='1
'; DROP TABLE users;--
' UNION SELECT username,password FROM users--
```

### Testing for XSS

**Step 1:** Find reflection points
```
# Test in all input fields
<script>alert(1)</script>
'"><script>alert(1)</script>
```

**Step 2:** Bypass filters with Intruder
```
# If <script> is blocked, try:
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<iframe src=javascript:alert(1)>
```

### Session Analysis

**What to test:**
- Session ID predictability (increment session IDs by 1)
- Session timeout behavior
- Session fixation vulnerabilities
- Cross-site request forgery (CSRF) protection

**Use Sequencer:** Analyzes session token randomness automatically.

---

## Advanced Techniques

### Session Handling Rules

**Problem:** Many apps require authentication, but sessions expire during testing.

**Solution:** Create macros to automatically re-authenticate.

**How:**
1. Record login sequence
2. Extract session token from response  
3. Use token in subsequent requests
4. Auto-renew when session expires

### Extensions That Matter

**Logger++:** Enhanced logging with search capabilities
**Autorize:** Automated authorization testing (checks if user A can access user B's data)
**Param Miner:** Discovers hidden parameters
**Turbo Intruder:** High-speed request sending for race conditions

**Install:** Extender → BApp Store → Install with one click

---

## Common Mistakes to Avoid

### Scope Problems
- **Testing out-of-scope domains** - Could be illegal
- **Missing subdomains** - API.example.com might be more vulnerable than example.com
- **Not excluding static content** - Wastes time testing images/CSS

### Authentication Issues
- **Session timeouts during long scans** - Use session handling rules
- **Not handling CSRF tokens** - Many modern apps require these
- **Testing without proper authorization** - Some vulnerabilities only appear when logged in

### False Positives
- **Trusting automated scanner results blindly** - Always manually verify findings
- **Assuming all errors indicate vulnerabilities** - Some errors are normal application behavior

---

## Quick Reference

### Essential Hotkeys
```
Ctrl+R: Send to Repeater
Ctrl+I: Send to Intruder  
Ctrl+U: URL encode selection
Ctrl+Shift+U: URL decode selection
Ctrl+F: Search in current view
```

### Testing Checklist
- [ ] Proxy configured and certificate installed
- [ ] Target scope properly defined
- [ ] Authentication mechanism understood
- [ ] All input parameters identified
- [ ] Session management tested
- [ ] Authorization controls verified

---

## Learning Resources

### Official Resources
- **Burp Suite Documentation**: https://portswigger.net/burp/documentation - Comprehensive official docs
- **Web Security Academy**: https://portswigger.net/web-security - Free hands-on labs using Burp

### Practice Targets
- **DVWA**: http://dvwa.co.uk/ - Classic vulnerable web app
- **OWASP Juice Shop**: https://owasp.org/www-project-juice-shop/ - Modern vulnerable application
- **PortSwigger Labs**: https://portswigger.net/web-security/all-labs - Guided practice scenarios

### Advanced Learning
- **Burp Suite Certified Practitioner**: Official PortSwigger certification
- **Bug Bounty Methodology**: Learn how professionals use Burp in real assessments