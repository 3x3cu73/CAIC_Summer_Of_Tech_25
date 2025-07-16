#!/usr/bin/env python3
"""
Security Automation Framework - Educational tool integration platform

This demonstrates how to build professional security testing workflows:
- Tool orchestration and result correlation
- Automated reconnaissance pipelines
- Report generation and data management
- Scalable testing across multiple targets

WARNING: Only use on systems you own or have permission to test.

Usage: python automation_framework.py <target> [options]
Example: python automation_framework.py example.com --full-scan
"""

import subprocess
import json
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
import argparse
import threading
import queue

class SecurityFramework:
    def __init__(self, target):
        self.target = target
        self.results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'tools': {},
            'vulnerabilities': [],
            'summary': {}
        }
        
        # Tool configurations
        self.tools = {
            'nmap': {
                'command': 'nmap',
                'enabled': True,
                'timeout': 300
            },
            'dirb': {
                'command': 'dirb',
                'enabled': True,
                'timeout': 600
            },
            'nikto': {
                'command': 'nikto',
                'enabled': True,
                'timeout': 900
            }
        }
        
        # Common wordlists and configurations
        self.wordlists = {
            'directories': '/usr/share/dirb/wordlists/common.txt',
            'files': '/usr/share/dirb/wordlists/extensions_common.txt'
        }
    
    def run_command(self, command, timeout=60):
        """
        Execute system command with timeout and error handling
        
        Args:
            command (str or list): Command to execute
            timeout (int): Timeout in seconds
            
        Returns:
            dict: Command result with stdout, stderr, returncode
        """
        try:
            print(f"[*] Executing: {command}")
            
            if isinstance(command, str):
                command = command.split()
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'command': ' '.join(command)
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timed out',
                'command': ' '.join(command)
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'Command not found',
                'command': ' '.join(command)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': ' '.join(command)
            }
    
    def nmap_scan(self, scan_type='quick'):
        """
        Perform network scanning with Nmap
        
        Args:
            scan_type (str): Type of scan (quick, full, stealth)
        """
        print("[*] Starting Nmap scan...")
        
        scan_options = {
            'quick': '-sS -sV --top-ports 1000',
            'full': '-sS -sV -sC -A -p-',
            'stealth': '-sS -f --scan-delay 1s',
            'udp': '-sU --top-ports 100'
        }
        
        options = scan_options.get(scan_type, scan_options['quick'])
        command = f"nmap {options} -oX - {self.target}"
        
        result = self.run_command(command, timeout=self.tools['nmap']['timeout'])
        
        if result['success']:
            # Parse XML output for structured data
            try:
                nmap_data = self.parse_nmap_xml(result['stdout'])
                self.results['tools']['nmap'] = nmap_data
                
                # Extract open ports for other tools
                open_ports = []
                for host in nmap_data.get('hosts', []):
                    for port in host.get('ports', []):
                        if port['state'] == 'open':
                            open_ports.append(port['portid'])
                
                self.results['summary']['open_ports'] = open_ports
                print(f"[+] Nmap scan completed. Found {len(open_ports)} open ports")
                
                return True
                
            except Exception as e:
                print(f"[!] Error parsing Nmap output: {e}")
                self.results['tools']['nmap'] = {'raw_output': result['stdout']}
                return False
        else:
            print(f"[!] Nmap scan failed: {result.get('error', 'Unknown error')}")
            return False
    
    def parse_nmap_xml(self, xml_output):
        """
        Parse Nmap XML output into structured data
        
        Args:
            xml_output (str): Raw XML from Nmap
            
        Returns:
            dict: Parsed scan results
        """
        try:
            root = ET.fromstring(xml_output)
            scan_data = {
                'scan_time': root.get('startstr'),
                'version': root.get('version'),
                'hosts': []
            }
            
            for host in root.findall('host'):
                host_data = {
                    'state': host.find('status').get('state'),
                    'addresses': [],
                    'hostnames': [],
                    'ports': []
                }
                
                # Extract addresses
                for address in host.findall('address'):
                    host_data['addresses'].append({
                        'addr': address.get('addr'),
                        'addrtype': address.get('addrtype')
                    })
                
                # Extract hostnames
                hostnames = host.find('hostnames')
                if hostnames is not None:
                    for hostname in hostnames.findall('hostname'):
                        host_data['hostnames'].append(hostname.get('name'))
                
                # Extract ports
                ports = host.find('ports')
                if ports is not None:
                    for port in ports.findall('port'):
                        port_data = {
                            'portid': port.get('portid'),
                            'protocol': port.get('protocol'),
                            'state': port.find('state').get('state'),
                            'service': {}
                        }
                        
                        service = port.find('service')
                        if service is not None:
                            port_data['service'] = {
                                'name': service.get('name'),
                                'product': service.get('product'),
                                'version': service.get('version'),
                                'extrainfo': service.get('extrainfo')
                            }
                        
                        host_data['ports'].append(port_data)
                
                scan_data['hosts'].append(host_data)
            
            return scan_data
            
        except ET.ParseError as e:
            print(f"[!] XML parsing error: {e}")
            return {'raw_output': xml_output}
    
    def web_directory_scan(self):
        """
        Perform web directory enumeration
        """
        print("[*] Starting directory enumeration...")
        
        # Check if web server is running
        web_ports = ['80', '443', '8080', '8443']
        open_ports = self.results['summary'].get('open_ports', [])
        
        web_detected = any(port in map(str, open_ports) for port in web_ports)
        
        if not web_detected:
            print("[!] No web servers detected, skipping directory scan")
            return False
        
        # Determine URL scheme
        if '443' in map(str, open_ports) or '8443' in map(str, open_ports):
            url = f"https://{self.target}"
        else:
            url = f"http://{self.target}"
        
        command = f"dirb {url} {self.wordlists['directories']} -r -S"
        result = self.run_command(command, timeout=self.tools['dirb']['timeout'])
        
        if result['success']:
            # Parse dirb output
            directories = self.parse_dirb_output(result['stdout'])
            self.results['tools']['dirb'] = {
                'url': url,
                'directories_found': directories,
                'raw_output': result['stdout']
            }
            
            print(f"[+] Directory scan completed. Found {len(directories)} directories")
            return True
        else:
            print(f"[!] Directory scan failed: {result.get('error', 'Unknown error')}")
            return False
    
    def parse_dirb_output(self, output):
        """
        Parse dirb output to extract found directories
        
        Args:
            output (str): Raw dirb output
            
        Returns:
            list: List of found directories
        """
        directories = []
        lines = output.split('\n')
        
        for line in lines:
            # Look for successful responses
            if '==> DIRECTORY:' in line:
                directory = line.split('DIRECTORY: ')[1].strip()
                directories.append(directory)
            elif 'CODE:200' in line and 'SIZE:' in line:
                # Extract URL from response line
                parts = line.split()
                for part in parts:
                    if part.startswith('http'):
                        directories.append(part)
                        break
        
        return list(set(directories))  # Remove duplicates
    
    def web_vulnerability_scan(self):
        """
        Perform web vulnerability scanning with Nikto
        """
        print("[*] Starting web vulnerability scan...")
        
        # Check if web server is running
        web_ports = ['80', '443', '8080', '8443']
        open_ports = self.results['summary'].get('open_ports', [])
        
        web_detected = any(port in map(str, open_ports) for port in web_ports)
        
        if not web_detected:
            print("[!] No web servers detected, skipping vulnerability scan")
            return False
        
        command = f"nikto -h {self.target} -Format txt"
        result = self.run_command(command, timeout=self.tools['nikto']['timeout'])
        
        if result['success']:
            # Parse nikto output for vulnerabilities
            vulnerabilities = self.parse_nikto_output(result['stdout'])
            self.results['tools']['nikto'] = {
                'vulnerabilities_found': len(vulnerabilities),
                'vulnerabilities': vulnerabilities,
                'raw_output': result['stdout']
            }
            
            # Add to global vulnerabilities list
            self.results['vulnerabilities'].extend(vulnerabilities)
            
            print(f"[+] Vulnerability scan completed. Found {len(vulnerabilities)} potential issues")
            return True
        else:
            print(f"[!] Vulnerability scan failed: {result.get('error', 'Unknown error')}")
            return False
    
    def parse_nikto_output(self, output):
        """
        Parse Nikto output to extract vulnerabilities
        
        Args:
            output (str): Raw Nikto output
            
        Returns:
            list: List of vulnerability dictionaries
        """
        vulnerabilities = []
        lines = output.split('\n')
        
        for line in lines:
            # Look for vulnerability indicators
            if '+ ' in line and any(keyword in line.lower() for keyword in 
                                   ['vulnerable', 'exposed', 'disclosure', 'security']):
                vuln = {
                    'tool': 'nikto',
                    'type': 'Web Vulnerability',
                    'description': line.strip(),
                    'severity': 'Medium'  # Default severity
                }
                
                # Classify severity based on keywords
                if any(keyword in line.lower() for keyword in ['critical', 'remote code']):
                    vuln['severity'] = 'Critical'
                elif any(keyword in line.lower() for keyword in ['high', 'injection']):
                    vuln['severity'] = 'High'
                elif any(keyword in line.lower() for keyword in ['low', 'information']):
                    vuln['severity'] = 'Low'
                
                vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def run_full_scan(self):
        """
        Execute complete security assessment
        """
        print(f"[*] Starting full security scan on {self.target}")
        print("-" * 60)
        
        start_time = time.time()
        
        # Phase 1: Network Discovery
        print("\n=== Phase 1: Network Discovery ===")
        self.nmap_scan('full')
        
        # Phase 2: Web Application Testing
        print("\n=== Phase 2: Web Application Testing ===")
        self.web_directory_scan()
        self.web_vulnerability_scan()
        
        # Phase 3: Analysis and Reporting
        print("\n=== Phase 3: Analysis and Reporting ===")
        self.analyze_results()
        
        end_time = time.time()
        scan_duration = end_time - start_time
        
        print(f"\n[*] Scan completed in {scan_duration:.2f} seconds")
        return True
    
    def analyze_results(self):
        """
        Analyze collected results and generate insights
        """
        summary = self.results['summary']
        
        # Count vulnerabilities by severity
        vuln_severity = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        for vuln in self.results['vulnerabilities']:
            severity = vuln.get('severity', 'Medium')
            vuln_severity[severity] += 1
        
        summary['vulnerability_count'] = len(self.results['vulnerabilities'])
        summary['vulnerability_severity'] = vuln_severity
        
        # Risk assessment
        risk_score = (vuln_severity['Critical'] * 10 + 
                     vuln_severity['High'] * 7 + 
                     vuln_severity['Medium'] * 4 + 
                     vuln_severity['Low'] * 1)
        
        if risk_score >= 20:
            risk_level = 'Critical'
        elif risk_score >= 10:
            risk_level = 'High'
        elif risk_score >= 5:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        summary['risk_score'] = risk_score
        summary['risk_level'] = risk_level
        
        print(f"[*] Risk Assessment: {risk_level} (Score: {risk_score})")
        print(f"[*] Total Vulnerabilities: {len(self.results['vulnerabilities'])}")
    
    def generate_report(self, format='json', filename=None):
        """
        Generate security assessment report
        
        Args:
            format (str): Report format (json, html, txt)
            filename (str): Output filename
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"security_report_{self.target}_{timestamp}.{format}"
        
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
        elif format == 'txt':
            self.generate_text_report(filename)
        elif format == 'html':
            self.generate_html_report(filename)
        
        print(f"[+] Report saved to {filename}")
        return filename
    
    def generate_text_report(self, filename):
        """
        Generate plain text report
        
        Args:
            filename (str): Output filename
        """
        with open(filename, 'w') as f:
            f.write(f"Security Assessment Report\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"Date: {self.results['timestamp']}\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary
            summary = self.results['summary']
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Risk Level: {summary.get('risk_level', 'Unknown')}\n")
            f.write(f"Risk Score: {summary.get('risk_score', 0)}\n")
            f.write(f"Open Ports: {len(summary.get('open_ports', []))}\n")
            f.write(f"Vulnerabilities: {summary.get('vulnerability_count', 0)}\n\n")
            
            # Detailed findings
            if self.results['vulnerabilities']:
                f.write("VULNERABILITIES\n")
                f.write("-" * 15 + "\n")
                for i, vuln in enumerate(self.results['vulnerabilities'], 1):
                    f.write(f"{i}. {vuln['type']} ({vuln['severity']})\n")
                    f.write(f"   {vuln['description']}\n\n")
            
            # Tool outputs
            f.write("TOOL OUTPUTS\n")
            f.write("-" * 12 + "\n")
            for tool, data in self.results['tools'].items():
                f.write(f"{tool.upper()}:\n")
                if 'raw_output' in data:
                    f.write(data['raw_output'][:1000] + "...\n\n")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Security Automation Framework')
    parser.add_argument('target', help='Target hostname or IP address')
    parser.add_argument('--quick', action='store_true', help='Quick scan only')
    parser.add_argument('--full-scan', action='store_true', help='Full comprehensive scan')
    parser.add_argument('--report-format', choices=['json', 'txt', 'html'], 
                       default='json', help='Report format')
    parser.add_argument('--output', help='Output filename')
    
    args = parser.parse_args()
    
    # Ethical warning
    print("=" * 60)
    print("EDUCATIONAL SECURITY AUTOMATION FRAMEWORK")
    print("=" * 60)
    print("WARNING: Only scan systems you own or have permission to test!")
    print("Unauthorized scanning may be illegal in your jurisdiction.")
    print("=" * 60)
    
    try:
        # Create framework instance
        framework = SecurityFramework(args.target)
        
        # Run appropriate scan type
        if args.full_scan:
            framework.run_full_scan()
        elif args.quick:
            framework.nmap_scan('quick')
        else:
            framework.run_full_scan()
        
        # Generate report
        report_file = framework.generate_report(
            format=args.report_format,
            filename=args.output
        )
        
        print(f"\n[*] Assessment complete. Report saved to: {report_file}")
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[!] Framework error: {e}")

if __name__ == "__main__":
    main()