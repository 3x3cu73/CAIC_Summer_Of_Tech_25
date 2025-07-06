# DevClub Cybersecurity Course – Week 4 Resources
## Web Security Fundamentals

Welcome to Week 4! This week dives deep into web application security - the most common attack surface in modern cybersecurity. You'll learn to identify, exploit, and understand web vulnerabilities that affect millions of applications worldwide.

---

## Learning Objectives
By the end of this week, you will:
- Understand HTTP protocol fundamentals and security implications
- Master the OWASP Top 10 vulnerabilities with hands-on exploitation
- Use Burp Suite for intercepting and manipulating web traffic
- Perform manual and automated web application testing
- Understand API security testing fundamentals
- Apply web security knowledge in real-world scenarios

---

## Week 4 Topics

### [HTTP Protocol & Web Fundamentals](http-fundamentals.md)
Master the foundation of web communication:
- **HTTP Methods & Status Codes** - GET, POST, PUT, DELETE and their security implications
- **Headers & Cookies** - Authentication, session management, and security headers
- **Sessions & Authentication** - How web apps track users and common flaws
- **Same-Origin Policy** - Browser security model and bypass techniques

### [OWASP Top 10 Vulnerabilities](owasp-top10.md)
Learn the most critical web application security risks:
- **Injection Attacks** - SQL injection, NoSQL injection, command injection
- **Broken Authentication** - Session hijacking, credential stuffing, weak passwords
- **Sensitive Data Exposure** - Data leakage, improper encryption, insecure storage
- **XML External Entities (XXE)** - File disclosure through XML parsing
- **Broken Access Control** - IDOR, privilege escalation, path traversal
- **Security Misconfiguration** - Default credentials, verbose errors, unnecessary services

### [Burp Suite Mastery](burp-suite.md)
Your primary web security testing tool:
- **Proxy Configuration** - Intercepting and modifying HTTP traffic
- **Repeater & Intruder** - Manual testing and automated attacks
- **Scanner Basics** - Automated vulnerability detection
- **Extensions & Workflows** - Enhancing capabilities with plugins

### [Manual Testing Techniques](manual-testing.md)
Hands-on exploitation methods:
- **Input Validation Testing** - Finding injection points and bypass techniques
- **Authentication Testing** - Brute force, session attacks, password reset flaws
- **Authorization Testing** - Horizontal and vertical privilege escalation
- **Business Logic Testing** - Finding flaws in application workflows

### [API Security Testing](api-security.md)
Modern web applications are API-driven:
- **REST API Fundamentals** - Endpoints, methods, authentication
- **API Enumeration** - Finding hidden endpoints and parameters
- **API-Specific Attacks** - Mass assignment, rate limiting bypass, JWT attacks
- **GraphQL Security** - Query complexity attacks, introspection abuse

---

## Essential Tools & Platforms

### Primary Testing Tools
- **Burp Suite Community**: https://portswigger.net/burp/communitydownload - Free web security testing platform
- **OWASP ZAP**: https://www.zaproxy.org/ - Open-source web application scanner
- **Postman**: https://www.postman.com/ - API testing and exploration tool

### Practice Platforms
- **OWASP Juice Shop**: https://owasp.org/www-project-juice-shop/ - Modern vulnerable web application
- **PortSwigger Web Security Academy**: https://portswigger.net/web-security - Free labs with guided learning
- **DVWA**: https://github.com/digininja/DVWA - Damn Vulnerable Web Application

### Online Resources
- **HackerOne Hacktivity**: https://hackerone.com/hacktivity - Real vulnerability reports
- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/ - Comprehensive methodology
- **PortSwigger Research**: https://portswigger.net/research - Latest web security research

---

## Quick Start Guide

### 🚀 New to Web Security?
1. Start with [HTTP Fundamentals](http-fundamentals.md) - understand how web apps work
2. Install Burp Suite and complete basic proxy setup
3. Try OWASP Juice Shop for hands-on practice

### 🔍 Want to Find Web Vulnerabilities?
1. Jump to [OWASP Top 10](owasp-top10.md) - learn the most common flaws
2. Practice with PortSwigger Web Security Academy labs
3. Master [Burp Suite](burp-suite.md) for professional testing

### 🛠️ Focus on Tools & Automation?
1. Explore [Burp Suite Mastery](burp-suite.md) - advanced features and workflows
2. Learn about [API Security Testing](api-security.md) - modern attack surfaces
3. Practice with automated scanners and custom scripts

---

## Week 4 CTF Challenge (Weekend)

**Challenge Categories:**
1. **SQL Injection**
2. **Cross-Site Scripting (XSS)**
3. **Authentication Bypass**
4. **API Security**
5. **Web Application Logic Flaws**

---

## Real-World Applications

### 🛡️ How Web Security Protects Organizations

**Vulnerability Assessment:**
- Security teams scan applications for OWASP Top 10 vulnerabilities
- Automated tools integrate into CI/CD pipelines for continuous security
- Manual testing uncovers complex business logic flaws

**Incident Response:**
- Web security knowledge helps investigate data breaches
- Understanding attack vectors enables proper remediation
- Log analysis reveals attack patterns and IOCs

**Compliance & Auditing:**
- PCI DSS, SOX, and GDPR require secure web applications
- Security auditors verify proper controls and testing procedures
- Penetration testers validate real-world security posture

---

## Practice Platforms & Learning Resources

### Hands-On Learning

**PortSwigger Web Security Academy** - https://portswigger.net/web-security
- Free comprehensive labs covering all major vulnerabilities
- Progressive difficulty with detailed explanations
- Covers advanced topics like DOM-based attacks and prototype pollution

**OWASP WebGoat** - https://owasp.org/www-project-webgoat/
- Interactive learning environment with lessons and challenges
- Covers secure coding practices alongside vulnerability exploitation
- Good for understanding both attack and defense perspectives

**PentesterLab** - https://pentesterlab.com/
- Hands-on exercises with real vulnerable applications
- Advanced topics like code review and white-box testing
- Professional-grade exercises used by security teams

### Bug Bounty Practice
- **HackerOne**: https://hackerone.com/ - Real bug bounty programs and disclosed reports
- **Bugcrowd**: https://bugcrowd.com/ - Crowdsourced security testing platform
- **Intigriti**: https://www.intigriti.com/ - European bug bounty platform

### Advanced Learning
- **SANS Web Application Penetration Testing**: Professional certification track
- **eLearnSecurity Web Application Penetration Tester**: Practical certification
- **Offensive Security Web Expert (OSWE)**: Advanced exploitation techniques

---

## Week 4 Checklist

- [ ] Read all five topic-specific guides
- [ ] Installed and configured Burp Suite Community Edition
- [ ] Completed at least 5 PortSwigger Web Security Academy labs
- [ ] Practiced with OWASP Juice Shop or similar vulnerable application
- [ ] Understood HTTP fundamentals and browser security model
- [ ] Learned manual testing techniques for major vulnerability classes
- [ ] Ready for Week 4 CTF challenge

---

## Getting Help & Community

### 🆘 Common Issues & Solutions

**"Burp Suite proxy isn't working"**
→ Check browser proxy settings, ensure certificate is installed, verify target scope

**"Can't find SQL injection"**
→ Try different payloads, check error messages, use time-based techniques for blind SQLi

**"XSS payload not executing"**
→ Check input filtering, try different contexts (HTML, JavaScript, CSS), use encoding bypasses

### 📚 Community Resources
- **r/netsec** - Latest security research and discussions
- **OWASP Slack** - Active community for web application security
- **Bug Bounty Discord servers** - Real-time collaboration and tips
- **InfoSec Twitter** - Follow researchers and get latest vulnerability news

---

## Next Week Preview

**Week 5: Privilege Escalation, Post-Exploitation & Final CTF**
Learn advanced attack techniques and prepare for the comprehensive final challenge!