# HTTP Protocol & Web Fundamentals

HTTP is the foundation of web communication. Understanding how HTTP works—and how it breaks—is essential for finding web vulnerabilities. Every security flaw in web applications stems from either misunderstanding HTTP or implementing it incorrectly.

---

## Why HTTP Matters for Security

**HTTP is stateless** - Each request is independent, so applications use cookies and headers to maintain state. This creates numerous attack opportunities.

**HTTP is text-based** - All data is human-readable, making it easy to intercept and modify requests.

**HTTP trusts the client** - Servers assume clients send valid data, but attackers control all client input.

---

## HTTP Methods & Security

### The Problem with HTTP Methods

Most web applications only expect GET and POST requests, but HTTP supports many methods. Attackers can use unexpected methods to bypass security controls.

**Safe vs Unsafe Methods:**
```
GET    - Should only retrieve data (no side effects)
POST   - Can modify data on the server
PUT    - Update/replace entire resource  
DELETE - Remove resource
```

**Security Testing:**
```bash
# If POST /admin/users is blocked, try:
curl -X PUT /admin/users
curl -X DELETE /admin/users/123
curl -X PATCH /admin/users/123
```

**Method Override Attack:**
```
POST /api/users/123 HTTP/1.1
X-HTTP-Method-Override: DELETE
# Server might process this as DELETE instead of POST
```

---

## Security Headers - Your First Line of Defense

### Critical Headers Every App Should Have

**Content Security Policy (CSP):**
```
Content-Security-Policy: default-src 'self'
# Prevents XSS by controlling where scripts can load from
```

**Frame Protection:**
```
X-Frame-Options: DENY
# Prevents clickjacking attacks
```

**HTTPS Enforcement:**
```
Strict-Transport-Security: max-age=31536000
# Forces browser to use HTTPS only
```

### Headers That Leak Information

Servers often reveal too much information in headers:
```
Server: Apache/2.4.25 (Ubuntu) PHP/7.2.15
X-Powered-By: PHP/7.2.15
# Attackers now know exact versions to target
```

---

## Session Management - How Web Apps Remember You

### How Sessions Work

1. **Login:** User provides username/password
2. **Session Creation:** Server generates unique session ID
3. **Cookie Storage:** Browser stores session ID in cookie
4. **Authentication:** Browser sends cookie with each request

### Common Session Vulnerabilities

**Predictable Session IDs:**
```
Bad:  sessionid=123456789 (easily guessable)
Good: sessionid=a8f7b2c9e4d1f6h3j8k5m2n9 (random, long)
```

**Session Fixation:**
- Attacker gets session ID before victim logs in
- Tricks victim into using that same session ID
- After victim logs in, attacker uses the now-authenticated session

**Testing Session Security:**
```bash
# Try incrementing session ID
Original: sessionid=123456789
Test:     sessionid=123456790

# Check session timeout
Wait 30 minutes, try using old session
```

---

## Same-Origin Policy & CORS

### Why Same-Origin Policy Exists

Browsers enforce Same-Origin Policy to prevent malicious websites from accessing data from other sites. Without it, evil.com could read your bank account data.

**Same Origin Rules:**
```
https://example.com:443/page1
https://example.com:443/page2  ✓ Same origin
http://example.com/page1       ✗ Different protocol  
https://sub.example.com/page1  ✗ Different domain
https://example.com:8080/page1 ✗ Different port
```

### CORS - When Same-Origin Policy Gets Relaxed

CORS allows servers to specify which origins can access their resources. When misconfigured, it creates security holes.

**Dangerous CORS Configuration:**
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
# This allows ANY website to make authenticated requests!
```

**Testing CORS:**
```bash
curl -H "Origin: https://evil.com" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS https://target.com/api/data
     
# Look for Access-Control-Allow-Origin: * in response
```

---

## Quick Security Testing Checklist

### 1. Check HTTP Methods
```bash
curl -X OPTIONS /endpoint  # See which methods are allowed
curl -X PUT /endpoint      # Test unexpected methods
curl -X DELETE /endpoint   # Test dangerous methods
```

### 2. Analyze Security Headers
```bash
curl -I https://target.com
# Look for missing CSP, X-Frame-Options, HSTS
```

### 3. Test Session Management
- Try predicting session IDs
- Test session timeout
- Check if sessions invalidate on logout

### 4. Check CORS Configuration
```bash
curl -H "Origin: https://evil.com" https://target.com/api/
# Dangerous if it returns Access-Control-Allow-Origin: *
```

---

## Essential Learning Resources

### Deep Understanding
- **MDN HTTP Guide**: https://developer.mozilla.org/en-US/docs/Web/HTTP
- **OWASP Session Management**: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

### Practical Testing
- **Security Headers Scanner**: https://securityheaders.com/
- **CORS Tester**: https://cors-test.codehappy.dev/

### Browser Security
- **Same-Origin Policy**: https://web.dev/same-origin-policy/
- **CORS Explained**: https://web.dev/cross-origin-resource-sharing/