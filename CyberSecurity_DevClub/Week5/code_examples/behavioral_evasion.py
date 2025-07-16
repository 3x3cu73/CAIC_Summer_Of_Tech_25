#!/usr/bin/env python3
"""
Behavioral Evasion Techniques - Educational demonstration of human behavior simulation

This script demonstrates techniques to evade behavioral analysis systems:
- Human timing simulation
- Activity pattern mimicry
- Process masquerading
- Living off the land techniques

WARNING: Only use on systems you own or have permission to test.

Usage: python behavioral_evasion.py [options]
"""

import os
import sys
import time
import random
import psutil
import subprocess
import argparse
from datetime import datetime, timedelta

class BehavioralEvasionToolkit:
    def __init__(self):
        self.business_hours = (9, 17)  # 9 AM to 5 PM
        self.business_days = [0, 1, 2, 3, 4]  # Monday to Friday (0=Monday)
        
        # Legitimate-looking process names
        self.legitimate_process_names = [
            "systemd-networkd",
            "NetworkManager", 
            "systemd-resolved",
            "gnome-session",
            "pulseaudio",
            "dbus-daemon",
            "update-notifier",
            "gvfs-daemon",
            "evolution-data-server"
        ]
        
        # Human-like activity patterns
        self.human_activities = [
            ("web_browsing", 120, 300),      # 2-5 minutes
            ("email_check", 30, 120),        # 30 seconds - 2 minutes  
            ("document_editing", 300, 1800), # 5-30 minutes
            ("break_time", 600, 3600),       # 10-60 minutes
            ("meeting_time", 1800, 3600),    # 30-60 minutes
            ("idle_time", 60, 300)           # 1-5 minutes
        ]
    
    def is_business_time(self):
        """
        Check if current time is during typical business hours
        
        Returns:
            bool: True if within business hours
        """
        now = datetime.now()
        return (now.weekday() in self.business_days and 
                self.business_hours[0] <= now.hour <= self.business_hours[1])
    
    def wait_for_business_hours(self):
        """
        Wait until business hours to blend with normal activity
        """
        while not self.is_business_time():
            now = datetime.now()
            print(f"[*] Currently {now.strftime('%A %H:%M')} - waiting for business hours...")
            
            # Calculate time until next business day
            if now.weekday() >= 4:  # Friday or later
                days_until_monday = 7 - now.weekday()
                next_business = now.replace(hour=9, minute=0, second=0, microsecond=0)
                next_business += timedelta(days=days_until_monday)
            else:
                if now.hour >= 17:  # After business hours
                    next_business = now.replace(hour=9, minute=0, second=0, microsecond=0)
                    next_business += timedelta(days=1)
                else:  # Before business hours
                    next_business = now.replace(hour=9, minute=0, second=0, microsecond=0)
            
            wait_seconds = (next_business - now).total_seconds()
            print(f"[*] Sleeping for {wait_seconds:.0f} seconds until business hours")
            time.sleep(min(wait_seconds, 3600))  # Sleep max 1 hour at a time
    
    def human_timing_delay(self, min_delay=5, max_delay=60):
        """
        Add human-like delays with natural variation
        
        Args:
            min_delay (int): Minimum delay in seconds
            max_delay (int): Maximum delay in seconds
        """
        # Add some randomness to make it more human-like
        base_delay = random.randint(min_delay, max_delay)
        
        # Add occasional longer pauses (simulating distractions)
        if random.random() < 0.1:  # 10% chance of longer pause
            base_delay *= random.randint(2, 5)
            print(f"[*] Taking a longer break ({base_delay}s) - simulating distraction")
        
        print(f"[*] Human-like delay: {base_delay} seconds")
        time.sleep(base_delay)
    
    def simulate_typing_delays(self, text, base_wpm=40):
        """
        Simulate human typing with realistic delays and errors
        
        Args:
            text (str): Text to "type"
            base_wpm (int): Base words per minute (human average)
        """
        print(f"[*] Simulating typing: '{text}'")
        
        # Calculate base delay between characters
        chars_per_second = (base_wpm * 5) / 60  # Assuming 5 chars per word
        base_delay = 1.0 / chars_per_second
        
        typed_text = ""
        for i, char in enumerate(text):
            # Add variation to typing speed
            char_delay = base_delay * random.uniform(0.5, 2.0)
            
            # Simulate occasional typos and corrections
            if random.random() < 0.05:  # 5% chance of typo
                print(".", end="", flush=True)  # Visual indicator of typo
                time.sleep(char_delay)
                # Backspace and correct
                time.sleep(char_delay * 2)
                print("\b", end="", flush=True)
            
            # Longer pauses for punctuation and spaces
            if char in ".,!?;: ":
                char_delay *= random.uniform(1.5, 3.0)
            
            typed_text += char
            print(char, end="", flush=True)
            time.sleep(char_delay)
        
        print()  # New line after typing
        return typed_text
    
    def mimic_user_activity_pattern(self, duration_hours=8):
        """
        Simulate realistic user activity patterns during work day
        
        Args:
            duration_hours (int): How long to simulate activity
        """
        start_time = time.time()
        end_time = start_time + (duration_hours * 3600)
        
        print(f"[*] Simulating {duration_hours} hours of user activity patterns")
        
        while time.time() < end_time:
            # Choose random activity
            activity_name, min_duration, max_duration = random.choice(self.human_activities)
            duration = random.randint(min_duration, max_duration)
            
            print(f"[*] Simulating '{activity_name}' for {duration} seconds")
            
            # Simulate different activity types
            if activity_name == "web_browsing":
                self.simulate_web_browsing(duration)
            elif activity_name == "email_check":
                self.simulate_email_activity(duration)
            elif activity_name == "document_editing":
                self.simulate_document_work(duration)
            elif activity_name in ["break_time", "meeting_time", "idle_time"]:
                print(f"[*] Idle period - {activity_name}")
                time.sleep(duration)
            
            # Short pause between activities
            time.sleep(random.randint(5, 30))
    
    def simulate_web_browsing(self, duration):
        """Simulate web browsing behavior"""
        pages_to_visit = duration // 30  # Visit a page every 30 seconds
        
        for i in range(pages_to_visit):
            print(f"[*] Simulating page {i+1} browsing...")
            # Simulate loading time
            time.sleep(random.randint(2, 8))
            # Simulate reading/scrolling
            time.sleep(random.randint(15, 45))
    
    def simulate_email_activity(self, duration):
        """Simulate email checking behavior"""
        emails_to_check = duration // 20  # 20 seconds per email
        
        for i in range(emails_to_check):
            print(f"[*] Reading email {i+1}...")
            time.sleep(random.randint(10, 30))
    
    def simulate_document_work(self, duration):
        """Simulate document editing work"""
        print(f"[*] Working on document...")
        
        # Simulate typing bursts with pauses
        typing_sessions = duration // 120  # 2-minute sessions
        
        for session in range(typing_sessions):
            typing_duration = random.randint(30, 90)
            print(f"[*] Typing session {session+1} for {typing_duration}s")
            time.sleep(typing_duration)
            
            # Break between typing sessions
            break_duration = random.randint(10, 60)
            print(f"[*] Taking {break_duration}s break from typing")
            time.sleep(break_duration)
    
    def process_masquerading(self, command, disguise_name=None):
        """
        Execute command with legitimate-looking process name
        
        Args:
            command (str): Command to execute
            disguise_name (str): Process name to masquerade as
        """
        if not disguise_name:
            disguise_name = random.choice(self.legitimate_process_names)
        
        print(f"[*] Executing '{command}' disguised as '{disguise_name}'")
        
        try:
            # Create script that changes its process name
            script_content = f'''#!/bin/bash
# Change process name
exec -a "{disguise_name}" {command}
'''
            script_path = f"/tmp/.{disguise_name}"
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            os.chmod(script_path, 0o755)
            
            # Execute with disguised name
            process = subprocess.Popen([script_path], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            print(f"[+] Process started with PID {process.pid} as '{disguise_name}'")
            return process
            
        except Exception as e:
            print(f"[-] Error with process masquerading: {e}")
            return None
    
    def living_off_the_land_examples(self):
        """
        Demonstrate living off the land techniques using built-in tools
        """
        print("[*] Demonstrating Living Off The Land (LOLBins) techniques:")
        print()
        
        # File operations using built-in tools
        print("1. File operations with built-in tools:")
        lol_commands = [
            ("Reading files", "cat /etc/passwd | head -5"),
            ("Finding files", "find /tmp -name '*.log' -type f"),
            ("Network testing", "ping -c 3 google.com"),
            ("Process listing", "ps aux | head -10"),
            ("System info", "uname -a"),
            ("Network connections", "ss -tulpn | head -5")
        ]
        
        for description, command in lol_commands:
            print(f"   {description}: {command}")
            
            # Add human-like delay before execution
            self.human_timing_delay(2, 10)
            
            try:
                result = subprocess.run(command, shell=True, 
                                      capture_output=True, text=True, timeout=10)
                if result.stdout:
                    print(f"   Output preview: {result.stdout[:100]}...")
                print()
            except Exception as e:
                print(f"   Error: {e}")
                print()
    
    def evade_behavioral_monitoring(self):
        """
        Comprehensive behavioral evasion demonstration
        """
        print("=== Behavioral Evasion Demonstration ===")
        print()
        
        # Check if we're in business hours
        if not self.is_business_time():
            print("[*] Outside business hours - demonstrating wait behavior")
            print("    (In real scenario, would wait for business hours)")
            # For demo, we'll continue instead of actually waiting
        
        # Simulate normal user login behavior
        print("[*] Phase 1: Simulating normal user login pattern")
        self.human_timing_delay(5, 15)
        
        # Simulate initial system checks (what users typically do)
        print("[*] Phase 2: Normal post-login activities")
        self.simulate_typing_delays("whoami", 35)
        time.sleep(2)
        self.simulate_typing_delays("pwd", 35)
        time.sleep(3)
        
        # Mix legitimate activities with reconnaissance
        print("[*] Phase 3: Mixing legitimate and reconnaissance activities")
        
        # Legitimate activity
        print("[*] Checking emails (legitimate)")
        self.simulate_email_activity(60)
        
        # Reconnaissance disguised as normal admin tasks
        print("[*] System administration (reconnaissance)")
        self.living_off_the_land_examples()
        
        # More legitimate activity
        print("[*] Document work (legitimate)")
        self.simulate_document_work(120)
        
        print()
        print("[+] Behavioral evasion demonstration completed")
        print("    Key principles demonstrated:")
        print("    - Human-like timing and delays")
        print("    - Mixed legitimate and malicious activities")
        print("    - Use of built-in tools (LOLBins)")
        print("    - Process name masquerading")
        print("    - Business hours awareness")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Educational Behavioral Evasion Toolkit')
    parser.add_argument('--demo', action='store_true',
                       help='Run full behavioral evasion demonstration')
    parser.add_argument('--wait-business', action='store_true',
                       help='Wait for business hours before proceeding')
    parser.add_argument('--simulate-activity', type=int, default=1,
                       help='Simulate user activity for N hours')
    parser.add_argument('--masquerade', type=str,
                       help='Command to execute with process masquerading')
    parser.add_argument('--disguise-as', type=str,
                       help='Process name to masquerade as')
    parser.add_argument('--lolbins', action='store_true',
                       help='Demonstrate living off the land techniques')
    
    args = parser.parse_args()
    
    # Ethical warning
    print("=" * 60)
    print("EDUCATIONAL BEHAVIORAL EVASION TOOLKIT")
    print("=" * 60)
    print("WARNING: Only use on systems you own or have permission to test!")
    print("Unauthorized system access may be illegal in your jurisdiction.")
    print()
    print("This tool is for educational purposes and authorized security testing only.")
    print("=" * 60)
    print()
    
    toolkit = BehavioralEvasionToolkit()
    
    if args.demo:
        toolkit.evade_behavioral_monitoring()
    
    elif args.wait_business:
        toolkit.wait_for_business_hours()
        print("[+] Now in business hours - proceed with operations")
    
    elif args.simulate_activity:
        toolkit.mimic_user_activity_pattern(args.simulate_activity)
    
    elif args.masquerade:
        disguise = args.disguise_as or random.choice(toolkit.legitimate_process_names)
        process = toolkit.process_masquerading(args.masquerade, disguise)
        if process:
            print(f"[*] Process running - PID: {process.pid}")
            print("[*] Press Ctrl+C to terminate")
            try:
                process.wait()
            except KeyboardInterrupt:
                process.terminate()
                print("\n[*] Process terminated")
    
    elif args.lolbins:
        toolkit.living_off_the_land_examples()
    
    else:
        parser.print_help()
        print()
        print("Educational Examples:")
        print("  --demo                                    # Full demonstration")
        print("  --simulate-activity 2                    # Simulate 2 hours of activity")
        print("  --masquerade 'bash' --disguise-as 'systemd-networkd'")
        print("  --lolbins                                # Show LOLBins techniques")

if __name__ == "__main__":
    main()