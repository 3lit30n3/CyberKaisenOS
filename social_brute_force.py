#!/usr/bin/env python3
import random
import time
import json
import os
from math import pi, sqrt
from enum import Enum

class Platform(Enum):
    GMAIL = "gmail"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    SNAPCHAT = "snapchat"
    ONLYFANS = "onlyfans"
    CUSTOM = "custom"

class ProxyType(Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"

class CaptchaHandler:
    def __init__(self):
        self.service_api_key = None
        self.service_type = "2captcha"  # Default service
        self.success_rate = 0.85  # Simulated success rate
    
    def set_service(self, service_type, api_key):
        """Set the captcha solving service and API key."""
        self.service_type = service_type
        self.service_api_key = api_key
        print(f"Captcha service set to {service_type} with API key: {api_key[:5]}...")
    
    def solve_captcha(self, captcha_type="recaptcha"):
        """Simulate solving a captcha."""
        if not self.service_api_key:
            print("No captcha service API key set. Captcha solving will fail.")
            return False
            
        print(f"Attempting to solve {captcha_type} using {self.service_type}...")
        # Simulate captcha solving with success probability
        success = random.random() < self.success_rate
        
        if success:
            print(f"Successfully solved {captcha_type}")
            return "simulated_captcha_token"
        else:
            print(f"Failed to solve {captcha_type}")
            return False

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_proxy_index = 0
        self.rotation_interval = 5  # Default rotation every 5 requests
        self.request_count = 0
    
    def add_proxy(self, ip, port, proxy_type=ProxyType.HTTP, username=None, password=None):
        """Add a proxy to the proxy list."""
        proxy = {
            "ip": ip,
            "port": port,
            "type": proxy_type,
            "username": username,
            "password": password
        }
        self.proxies.append(proxy)
        print(f"Added {proxy_type.value} proxy: {ip}:{port}")
    
    def load_proxies_from_file(self, file_path):
        """Load proxies from a file."""
        try:
            if not os.path.exists(file_path):
                print(f"Proxy file not found: {file_path}")
                return False
                
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                parts = line.split(':')
                if len(parts) >= 2:
                    ip = parts[0]
                    port = parts[1]
                    proxy_type = ProxyType.HTTP  # Default
                    
                    if len(parts) >= 3:
                        try:
                            proxy_type = ProxyType(parts[2].lower())
                        except ValueError:
                            proxy_type = ProxyType.HTTP
                    
                    username = None
                    password = None
                    if len(parts) >= 5:
                        username = parts[3]
                        password = parts[4]
                        
                    self.add_proxy(ip, port, proxy_type, username, password)
            
            print(f"Loaded {len(self.proxies)} proxies from {file_path}")
            return True
        except Exception as e:
            print(f"Error loading proxies: {e}")
            return False
    
    def get_current_proxy(self):
        """Get the current proxy."""
        if not self.proxies:
            return None
            
        proxy = self.proxies[self.current_proxy_index]
        self.request_count += 1
        
        # Check if we need to rotate
        if self.request_count >= self.rotation_interval:
            self.rotate_proxy()
            self.request_count = 0
            
        return proxy
    
    def rotate_proxy(self):
        """Rotate to the next proxy."""
        if not self.proxies:
            return None
            
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        proxy = self.proxies[self.current_proxy_index]
        print(f"Rotated to proxy: {proxy['ip']}:{proxy['port']}")
        return proxy
    
    def set_rotation_interval(self, interval):
        """Set the proxy rotation interval."""
        self.rotation_interval = interval
        print(f"Proxy rotation interval set to {interval} requests")

class SocialBruteForce:
    def __init__(self):
        self.target_username = None
        self.platform = None
        self.wordlist_path = None
        self.custom_url = None
        self.delay = 1.0  # Default delay between attempts
        self.max_attempts = 1000  # Default max attempts
        self.success = False
        self.attempts = 0
        self.found_password = None
        self.proxy_manager = ProxyManager()
        self.captcha_handler = CaptchaHandler()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        
        # Simulated success rate for demonstration
        self.simulation_success_rate = 0.001  # 0.1% chance of success per attempt
        
        # Geometric strength factor (for CyberKaisen theme)
        self.strength_factor = pi + (5 * sqrt(3) / 4)
    
    def set_target(self, username, platform=Platform.GMAIL):
        """Set the target username and platform."""
        self.target_username = username
        self.platform = platform
        print(f"Target set to {username} on {platform.value}")
    
    def set_custom_target(self, url, username):
        """Set a custom target URL and username."""
        self.custom_url = url
        self.target_username = username
        self.platform = Platform.CUSTOM
        print(f"Custom target set to {username} on {url}")
    
    def set_wordlist(self, wordlist_path):
        """Set the wordlist file path."""
        if not os.path.exists(wordlist_path):
            print(f"Wordlist file not found: {wordlist_path}")
            return False
            
        self.wordlist_path = wordlist_path
        print(f"Wordlist set to {wordlist_path}")
        return True
    
    def set_delay(self, delay):
        """Set the delay between attempts."""
        self.delay = delay
        print(f"Delay between attempts set to {delay} seconds")
    
    def set_max_attempts(self, max_attempts):
        """Set the maximum number of attempts."""
        self.max_attempts = max_attempts
        print(f"Maximum attempts set to {max_attempts}")
    
    def set_user_agent(self, user_agent):
        """Set the user agent string."""
        self.user_agent = user_agent
        print(f"User agent set to: {user_agent}")
    
    def _simulate_login_attempt(self, username, password):
        """Simulate a login attempt."""
        # Get current proxy if available
        proxy = self.proxy_manager.get_current_proxy()
        proxy_str = f" via {proxy['ip']}:{proxy['port']}" if proxy else ""
        
        print(f"Attempting login for {username} with password: {password[:3]}***{proxy_str}")
        
        # Simulate captcha challenge (20% chance)
        if random.random() < 0.2:
            print("Captcha challenge detected!")
            captcha_result = self.captcha_handler.solve_captcha()
            if not captcha_result:
                print("Failed to solve captcha, skipping this attempt")
                return False
        
        # Simulate login attempt
        time.sleep(self.delay)  # Respect the delay
        
        # Apply geometric strength factor to increase success chance
        adjusted_success_rate = min(0.999, self.simulation_success_rate * self.strength_factor)
        
        # Simulate success/failure
        success = random.random() < adjusted_success_rate
        
        if success:
            print(f"SUCCESS! Password found: {password}")
            self.success = True
            self.found_password = password
            return True
        else:
            return False
    
    def attack(self):
        """Execute the brute force attack."""
        if not self.target_username:
            print("No target username set")
            return False
            
        if not self.wordlist_path:
            print("No wordlist set")
            return False
            
        print(f"\n{'='*60}")
        print(f"Starting brute force attack on {self.platform.value}")
        print(f"Target: {self.target_username}")
        print(f"Wordlist: {self.wordlist_path}")
        print(f"{'='*60}\n")
        
        try:
            with open(self.wordlist_path, 'r') as f:
                for password in f:
                    password = password.strip()
                    if not password:
                        continue
                        
                    self.attempts += 1
                    
                    if self._simulate_login_attempt(self.target_username, password):
                        return True
                        
                    if self.attempts >= self.max_attempts:
                        print(f"Reached maximum attempts ({self.max_attempts})")
                        break
                        
            if not self.success:
                print(f"\nAttack completed. Password not found after {self.attempts} attempts.")
                return False
            else:
                return True
                
        except Exception as e:
            print(f"Error during attack: {e}")
            return False
    
    def get_results(self):
        """Get the results of the attack."""
        return {
            "success": self.success,
            "attempts": self.attempts,
            "password": self.found_password if self.success else None,
            "platform": self.platform.value,
            "target": self.target_username
        }
    
    def save_results(self, output_file):
        """Save the results to a file."""
        results = self.get_results()
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
            print(f"Results saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving results: {e}")
            return False

# Example usage
if __name__ == "__main__":
    brute_forcer = SocialBruteForce()
    brute_forcer.set_target("test_user", Platform.INSTAGRAM)
    brute_forcer.set_wordlist("wordlist.txt")
    brute_forcer.set_delay(0.5)
    brute_forcer.set_max_attempts(100)
    
    # Set up proxies
    brute_forcer.proxy_manager.add_proxy("192.168.1.1", "8080", ProxyType.HTTP)
    brute_forcer.proxy_manager.add_proxy("192.168.1.2", "8080", ProxyType.SOCKS5)
    brute_forcer.proxy_manager.set_rotation_interval(10)
    
    # Set up captcha handler
    brute_forcer.captcha_handler.set_service("2captcha", "your_api_key_here")
    
    # Run the attack
    brute_forcer.attack()
    
    # Get and save results
    results = brute_forcer.get_results()
    print(results)
    brute_forcer.save_results("attack_results.json")
