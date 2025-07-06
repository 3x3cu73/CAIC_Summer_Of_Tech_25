# API Security Testing

Modern applications are API-driven. While traditional web apps serve HTML pages, today's apps use APIs to send JSON data between frontend and backend. This shift creates new attack surfaces that require specialized testing techniques.

---

## Why API Security Matters

**APIs are everywhere** - Mobile apps, single-page applications, and microservices all rely heavily on APIs.

**APIs expose more data** - They often return raw database objects with sensitive fields that HTML pages would filter out.

**APIs assume trust** - Many APIs were designed for internal use but became exposed to the internet without proper security.

---

## API Discovery

### Finding Hidden APIs

**Common API paths:**
```bash
/api/v1/
/api/v2/
/rest/
/graphql
/swagger.json
/api-docs
```

**Documentation discovery:**
```bash
# Swagger/OpenAPI documentation
curl https://api.example.com/swagger.json
curl https://api.example.com/docs
curl https://api.example.com/api-docs

# Look for API version info
curl https://api.example.com/version
curl https://api.example.com/health
```

### Endpoint Enumeration

**Directory brute forcing:**
```bash
# Common endpoints to test
/users
/admin
/config
/health
/status
/debug
/internal
```

**Parameter discovery:**
```bash
# Try different parameter names
?id=1
?user_id=1
?userId=1
?limit=10
?page=1
?debug=true
```

---

## REST API Security Testing

### Authentication Bypass

**Missing authentication:**
```bash
# Try accessing endpoints without authentication
curl https://api.example.com/users
curl https://api.example.com/admin/config
```

**API key testing:**
```bash
# Invalid API key
curl -H "X-API-Key: invalid123" https://api.example.com/users

# Missing API key
curl https://api.example.com/users

# Try common API key names
Authorization: Bearer api_key_123
X-API-Key: secret_key
X-Auth-Token: token123
```

### IDOR in APIs (The Big One)

**Object reference testing:**
```bash
# Test different user IDs
curl https://api.example.com/users/123/profile
curl https://api.example.com/users/124/profile
curl https://api.example.com/users/999/profile

# Test with different formats
curl https://api.example.com/users/MTI0/profile (base64)
curl https://api.example.com/users/0x7c/profile (hex)
```

**Bulk data access:**
```bash
# Try to get all users
curl https://api.example.com/users?limit=999999
curl https://api.example.com/users?page=1&size=100000

# Export endpoints
curl https://api.example.com/export/users
curl https://api.example.com/admin/dump
```

### HTTP Method Testing

**Method override:**
```bash
# If DELETE is restricted
curl -X POST -H "X-HTTP-Method-Override: DELETE" \
     https://api.example.com/users/123

# Try unexpected methods
curl -X PUT https://api.example.com/users/123
curl -X PATCH https://api.example.com/users/123
```

---

## GraphQL Security Testing

### Schema Discovery (Introspection)

**Basic introspection:**
```graphql
# Get all available types
{
  __schema {
    types {
      name
    }
  }
}

# Get detailed type information  
{
  __type(name: "User") {
    fields {
      name
      type {
        name
      }
    }
  }
}
```

### GraphQL Attacks

**Field injection:**
```graphql
# Try accessing sensitive fields
{
  user(id: "1") {
    name
    email
    password    # Should not be accessible
    ssn         # Should not be accessible  
    credit_card # Should not be accessible
  }
}
```

**Query depth attack (DoS):**
```graphql
# Deeply nested query to overwhelm server
{
  user {
    posts {
      comments {
        replies {
          author {
            posts {
              comments {
                # Continue nesting...
              }
            }
          }
        }
      }
    }
  }
}
```

**Batch attack:**
```graphql
# Send many queries in one request
[
  {"query": "{ user(id: 1) { email } }"},
  {"query": "{ user(id: 2) { email } }"},
  {"query": "{ user(id: 3) { email } }"},
  # Repeat for thousands of users
]
```

---

## Modern Authentication Testing

### JWT (JSON Web Tokens)

**JWT structure:** header.payload.signature

**Common JWT vulnerabilities:**

**Algorithm confusion:**
```bash
# Change RS256 (asymmetric) to HS256 (symmetric)
# Use public key as HMAC secret
# This bypasses signature verification
```

**No signature verification:**
```bash
# Remove signature entirely
eyJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ.
# Some implementations accept unsigned tokens
```

**Claims manipulation:**
```json
# Decode payload and modify
{
  "user_id": 123,      # Change to different user
  "role": "admin",     # Escalate privileges
  "exp": 9999999999    # Extend expiration
}
```

### OAuth 2.0 Testing

**Authorization flow manipulation:**
```bash
# Redirect URI manipulation
https://auth.example.com/oauth?redirect_uri=https://attacker.com

# State parameter missing (CSRF vulnerability)
# Scope elevation
scope=read -> scope=admin

# Client secret exposure (mobile apps)
```

---

## Advanced API Attacks

### Mass Assignment

**Parameter pollution:**
```json
# Original request
{
  "name": "John",
  "email": "john@example.com"
}

# Add unexpected parameters
{
  "name": "John", 
  "email": "john@example.com",
  "role": "admin",
  "is_verified": true,
  "account_balance": 999999
}
```

### Rate Limiting Bypass

**Header manipulation:**
```bash
# Try different IP headers
curl -H "X-Forwarded-For: 1.2.3.4" /api/endpoint
curl -H "X-Real-IP: 5.6.7.8" /api/endpoint
curl -H "X-Originating-IP: 9.10.11.12" /api/endpoint

# User-Agent rotation
curl -H "User-Agent: Mobile-App/1.0" /api/endpoint
```

**Endpoint variations:**
```bash
# Case sensitivity bypass
/API/users vs /api/users vs /Api/Users

# HTTP version
# Some rate limiters only check HTTP/1.1
```

### API Versioning Issues

**Version testing:**
```bash
# Test different versions for vulnerabilities
curl /api/v1/users/123
curl /api/v2/users/123
curl /api/beta/users/123
curl /api/legacy/users/123

# Old versions might lack security controls
```

---

## API Testing Tools

### Command Line

**cURL (Essential for API testing):**
```bash
# GET with authentication
curl -H "Authorization: Bearer token123" \
     https://api.example.com/users

# POST JSON data
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"name":"test","role":"admin"}' \
     https://api.example.com/users

# File upload testing
curl -X POST \
     -F "file=@malicious.php" \
     https://api.example.com/upload
```

**HTTPie (User-friendly cURL alternative):**
```bash
# Install: pip install httpie
http GET api.example.com/users Authorization:"Bearer token"
http POST api.example.com/users name=test role=admin
```

### Automated Testing

**Postman:**
- GUI-based API testing
- Environment variables for different configs
- Basic security testing features

**Custom scripts:**
```python
import requests

# API enumeration
endpoints = ["users", "admin", "config", "health"]
for endpoint in endpoints:
    r = requests.get(f"https://api.example.com/{endpoint}")
    print(f"{endpoint}: {r.status_code}")
    if r.status_code == 200:
        print(f"Content: {r.json()}")
```

---

## Quick Testing Checklist

### 1. Discovery
- [ ] Find API endpoints (/api, /graphql, /swagger.json)
- [ ] Enumerate available endpoints
- [ ] Check for API documentation
- [ ] Identify authentication mechanisms

### 2. Authentication Testing
- [ ] Test without authentication
- [ ] Try invalid/expired tokens
- [ ] Test token manipulation (JWT claims, etc.)
- [ ] Check for rate limiting

### 3. Authorization Testing  
- [ ] Test IDOR (access other users' data)
- [ ] Test privilege escalation (user → admin)
- [ ] Test bulk data access
- [ ] Check function-level access controls

### 4. Input Validation
- [ ] Test for injection vulnerabilities
- [ ] Try mass assignment attacks
- [ ] Test file upload endpoints
- [ ] Check for XXE in XML APIs

### 5. Business Logic
- [ ] Test API version differences
- [ ] Look for race conditions
- [ ] Test unusual parameter combinations
- [ ] Check for logical flaws in workflows

---

## Learning Resources

### API Security Standards
- **OWASP API Security Top 10**: https://owasp.org/www-project-api-security/ - API-specific vulnerability guide
- **API Security in Action**: Book covering modern API security practices

### Practice Platforms
- **VAmPI**: https://github.com/erev0s/VAmPI - Vulnerable REST API for practice
- **DVGA**: https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application - GraphQL security testing
- **crAPI**: https://github.com/OWASP/crAPI - OWASP vulnerable API

### Tools & Resources
- **Burp Suite**: Has excellent API testing capabilities
- **OWASP ZAP**: Free alternative with API scanning features
- **GraphQL Voyager**: https://github.com/APIs-guru/graphql-voyager - Schema visualization