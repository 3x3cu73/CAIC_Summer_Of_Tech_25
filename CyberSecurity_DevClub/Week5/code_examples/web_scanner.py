#!/usr/bin/env python3
"""
Web Application Scanner - Educational web security testing tool

This scanner demonstrates:
- HTTP request automation
- Directory enumeration
- Form discovery and analysis
- Basic vulnerability detection

Usage: python web_scanner.py <target_url>
Example: python web_scanner.py http://example.com
"""

import requests
import sys
import time
import threading
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import queue

class WebScanner:
    def __init__(self, target_url, threads=10):
        self.target_url = target_url
        self.threads = threads
        self.session = requests.Session()
        self.found_urls = set()
        self.found_forms = []
        self.vulnerabilities = []
        
        # Set user agent to look legitimate
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
        # Common directories to check
        self.common_dirs = [
            'admin', 'login', 'test', 'backup', 'old', 'new', 'temp',
            'config', 'data', 'db', 'api', 'files', 'images', 'css',
            'js', 'includes', 'uploads', 'downloads', 'docs', 'help'
        ]
        
        # Common files to check
        self.common_files = [
            'index.php', 'admin.php', 'login.php', 'config.php',
            'database.php', 'connect.php', 'test.php', 'info.php',
            'robots.txt', 'sitemap.xml', '.htaccess', 'web.config',
            'readme.txt', 'changelog.txt', 'backup.sql', 'database.sql'
        ]
        
        # SQL injection test payloads
        self.sqli_payloads = [
            "'", '"', "' OR '1'='1", '" OR "1"="1',
            "' OR '1'='1' --", '" OR "1"="1" --',
            "admin'--", 'admin"--', "' UNION SELECT NULL--"
        ]
    
    def check_url(self, url):
        """
        Check if a URL exists and is accessible
        
        Args:
            url (str): URL to check
            
        Returns:
            tuple: (status_code, content_length, headers)
        """
        try:
            response = self.session.get(url, timeout=5, allow_redirects=False)
            return response.status_code, len(response.content), dict(response.headers)
        except requests.RequestException:
            return None, 0, {}
    
    def directory_enumeration(self):
        """
        Enumerate common directories and files
        """
        print("[*] Starting directory enumeration...")
        
        # Check directories
        for directory in self.common_dirs:
            url = urljoin(self.target_url, directory + '/')
            status_code, content_length, headers = self.check_url(url)
            
            if status_code and status_code == 200:
                print(f"[+] Found directory: {url} (Status: {status_code})")
                self.found_urls.add(url)
            elif status_code and status_code in [301, 302]:
                print(f"[+] Found redirect: {url} (Status: {status_code})")
                self.found_urls.add(url)
            
            time.sleep(0.1)  # Be respectful
        
        # Check files
        for filename in self.common_files:
            url = urljoin(self.target_url, filename)
            status_code, content_length, headers = self.check_url(url)
            
            if status_code and status_code == 200:
                print(f"[+] Found file: {url} (Status: {status_code}, Size: {content_length})")
                self.found_urls.add(url)
            
            time.sleep(0.1)  # Be respectful
    
    def extract_forms(self, url):
        """
        Extract forms from a webpage
        
        Args:
            url (str): URL to analyze
            
        Returns:
            list: List of form dictionaries
        """
        try:
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            forms = []
            for form in soup.find_all('form'):
                form_data = {
                    'url': url,
                    'action': form.get('action', ''),
                    'method': form.get('method', 'get').lower(),
                    'inputs': []
                }
                
                # Extract form inputs
                for input_tag in form.find_all(['input', 'textarea', 'select']):
                    input_data = {
                        'name': input_tag.get('name', ''),
                        'type': input_tag.get('type', 'text'),
                        'value': input_tag.get('value', '')
                    }
                    form_data['inputs'].append(input_data)
                
                forms.append(form_data)
            
            return forms
            
        except Exception as e:
            print(f"[!] Error extracting forms from {url}: {e}")
            return []
    
    def test_sql_injection(self, form_data):
        """
        Test form for SQL injection vulnerabilities
        
        Args:
            form_data (dict): Form information
        """
        print(f"[*] Testing {form_data['url']} for SQL injection...")
        
        for payload in self.sqli_payloads:
            # Prepare form data with payload
            data = {}
            for input_field in form_data['inputs']:
                if input_field['name'] and input_field['type'] != 'submit':
                    data[input_field['name']] = payload
            
            if not data:
                continue
            
            try:
                # Submit form with payload
                if form_data['method'] == 'post':
                    response = self.session.post(
                        urljoin(form_data['url'], form_data['action']),
                        data=data,
                        timeout=5
                    )
                else:
                    response = self.session.get(
                        urljoin(form_data['url'], form_data['action']),
                        params=data,
                        timeout=5
                    )
                
                # Check for SQL error patterns
                sql_errors = [
                    'sql syntax', 'mysql_fetch', 'ora-', 'sqlite_',
                    'postgresql', 'sql server', 'syntax error',
                    'warning: mysql', 'valid mysql result', 'error in your sql'
                ]
                
                response_text = response.text.lower()
                for error in sql_errors:
                    if error in response_text:
                        vulnerability = {
                            'type': 'SQL Injection',
                            'url': form_data['url'],
                            'parameter': list(data.keys()),
                            'payload': payload,
                            'evidence': error
                        }
                        self.vulnerabilities.append(vulnerability)
                        print(f"[!] POTENTIAL SQL INJECTION: {form_data['url']}")
                        print(f"    Payload: {payload}")
                        print(f"    Evidence: {error}")
                        break
                
            except Exception as e:
                print(f"[!] Error testing SQL injection: {e}")
            
            time.sleep(0.2)  # Be respectful
    
    def analyze_response_headers(self, url):
        """
        Analyze HTTP response headers for security issues
        
        Args:
            url (str): URL to analyze
        """
        try:
            response = self.session.get(url, timeout=5)
            headers = response.headers
            
            # Security headers to check for
            security_headers = {
                'X-Frame-Options': 'Missing clickjacking protection',
                'X-XSS-Protection': 'Missing XSS protection',
                'X-Content-Type-Options': 'Missing MIME sniffing protection',
                'Strict-Transport-Security': 'Missing HTTPS enforcement',
                'Content-Security-Policy': 'Missing CSP protection'
            }
            
            for header, description in security_headers.items():
                if header not in headers:
                    vulnerability = {
                        'type': 'Missing Security Header',
                        'url': url,
                        'header': header,
                        'description': description
                    }
                    self.vulnerabilities.append(vulnerability)
                    print(f"[!] MISSING HEADER: {header} on {url}")
            
            # Check for information disclosure
            disclosure_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version']
            for header in disclosure_headers:
                if header in headers:
                    print(f"[i] Info disclosure: {header}: {headers[header]}")
            
        except Exception as e:
            print(f"[!] Error analyzing headers for {url}: {e}")
    
    def run_scan(self):
        """
        Run the complete web application scan
        """
        print(f"Starting web application scan on {self.target_url}")
        print("-" * 60)
        
        # 1. Directory enumeration
        self.directory_enumeration()
        
        # 2. Analyze main page and found pages
        urls_to_analyze = [self.target_url] + list(self.found_urls)
        
        for url in urls_to_analyze[:10]:  # Limit to prevent overwhelming
            print(f"\n[*] Analyzing {url}")
            
            # Extract forms
            forms = self.extract_forms(url)
            self.found_forms.extend(forms)
            
            if forms:
                print(f"[+] Found {len(forms)} forms on {url}")
            
            # Analyze security headers
            self.analyze_response_headers(url)
        
        # 3. Test forms for vulnerabilities
        print(f"\n[*] Testing {len(self.found_forms)} forms for vulnerabilities...")
        for form in self.found_forms:
            self.test_sql_injection(form)
        
        # 4. Print summary
        self.print_summary()
    
    def print_summary(self):
        """
        Print scan summary
        """
        print("\n" + "=" * 60)
        print("SCAN SUMMARY")
        print("=" * 60)
        
        print(f"URLs discovered: {len(self.found_urls)}")
        for url in sorted(self.found_urls):
            print(f"  {url}")
        
        print(f"\nForms discovered: {len(self.found_forms)}")
        for form in self.found_forms:
            inputs = [inp['name'] for inp in form['inputs'] if inp['name']]
            print(f"  {form['url']} ({form['method'].upper()}) - Inputs: {inputs}")
        
        print(f"\nVulnerabilities found: {len(self.vulnerabilities)}")
        for vuln in self.vulnerabilities:
            print(f"  {vuln['type']}: {vuln['url']}")

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python web_scanner.py <target_url>")
        print("Example: python web_scanner.py http://example.com")
        sys.exit(1)
    
    target_url = sys.argv[1]
    
    # Validate URL
    parsed = urlparse(target_url)
    if not parsed.scheme or not parsed.netloc:
        print("[!] Invalid URL format. Include http:// or https://")
        sys.exit(1)
    
    # Ethical warning
    print("=" * 60)
    print("EDUCATIONAL WEB APPLICATION SCANNER")
    print("=" * 60)
    print("WARNING: Only scan applications you own or have permission to test!")
    print("Unauthorized scanning may be illegal in your jurisdiction.")
    print("=" * 60)
    
    try:
        # Create and run scanner
        scanner = WebScanner(target_url)
        scanner.run_scan()
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[!] Scan error: {e}")

if __name__ == "__main__":
    main()