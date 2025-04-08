#!/usr/bin/env python3
import os
import re
import json
import random
import subprocess
import datetime
from enum import Enum

class OsintSource(Enum):
    SOCIAL_MEDIA = "social_media"
    PERSONAL_INFO = "personal_info"
    COMPANY_INFO = "company_info"
    PUBLIC_RECORDS = "public_records"
    CUSTOM = "custom"

class WordlistType(Enum):
    SIMPLE = "simple"
    COMPLEX = "complex"
    TARGETED = "targeted"
    HYBRID = "hybrid"

class OsintWordlistGenerator:
    def __init__(self):
        self.target_info = {}
        self.collected_data = {}
        self.wordlist = set()
        self.output_file = None
        self.min_length = 8
        self.max_length = 16
        self.include_numbers = True
        self.include_special = True
        self.include_variations = True
        self.include_leet = True
        self.external_tools = {
            "cupp": self._check_tool_exists("cupp"),
            "crunch": self._check_tool_exists("crunch"),
            "hashcat": self._check_tool_exists("hashcat"),
            "recon-ng": self._check_tool_exists("recon-ng"),
            "spiderfoot": self._check_tool_exists("spiderfoot")
        }
    
    def _check_tool_exists(self, tool_name):
        """Check if an external tool exists in the system."""
        try:
            subprocess.run(["which", tool_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def set_target(self, target_name, target_type="person"):
        """Set the target for OSINT collection."""
        self.target_info = {
            "name": target_name,
            "type": target_type,
            "timestamp": datetime.datetime.now().isoformat()
        }
        print(f"Target set to {target_name} ({target_type})")
    
    def add_personal_info(self, **kwargs):
        """Add personal information about the target."""
        if "personal" not in self.collected_data:
            self.collected_data["personal"] = {}
            
        for key, value in kwargs.items():
            self.collected_data["personal"][key] = value
            
        print(f"Added personal information: {', '.join(kwargs.keys())}")
    
    def add_social_media(self, platform, username):
        """Add social media information."""
        if "social_media" not in self.collected_data:
            self.collected_data["social_media"] = {}
            
        self.collected_data["social_media"][platform] = username
        print(f"Added social media: {platform} - {username}")
    
    def add_company_info(self, **kwargs):
        """Add company information."""
        if "company" not in self.collected_data:
            self.collected_data["company"] = {}
            
        for key, value in kwargs.items():
            self.collected_data["company"][key] = value
            
        print(f"Added company information: {', '.join(kwargs.keys())}")
    
    def add_custom_data(self, category, **kwargs):
        """Add custom data."""
        if category not in self.collected_data:
            self.collected_data[category] = {}
            
        for key, value in kwargs.items():
            self.collected_data[category][key] = value
            
        print(f"Added {category} information: {', '.join(kwargs.keys())}")
    
    def set_output_file(self, output_file):
        """Set the output file for the wordlist."""
        self.output_file = output_file
        print(f"Output file set to {output_file}")
    
    def set_password_constraints(self, min_length=8, max_length=16, include_numbers=True, 
                                include_special=True, include_variations=True, include_leet=True):
        """Set password generation constraints."""
        self.min_length = min_length
        self.max_length = max_length
        self.include_numbers = include_numbers
        self.include_special = include_special
        self.include_variations = include_variations
        self.include_leet = include_leet
        
        print(f"Password constraints set: length {min_length}-{max_length}, " +
              f"numbers: {include_numbers}, special: {include_special}, " +
              f"variations: {include_variations}, leet: {include_leet}")
    
    def _extract_words_from_data(self):
        """Extract potential password components from collected data."""
        words = set()
        
        # Process personal information
        if "personal" in self.collected_data:
            personal = self.collected_data["personal"]
            
            # Add name variations
            if "name" in personal:
                name = personal["name"]
                words.add(name)
                words.add(name.lower())
                words.add(name.upper())
                
                # Split name into parts
                name_parts = name.split()
                for part in name_parts:
                    words.add(part)
                    words.add(part.lower())
                
            # Add birth date variations
            if "birthdate" in personal:
                birthdate = personal["birthdate"]
                if isinstance(birthdate, str):
                    # Try to parse date
                    try:
                        date = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
                        words.add(str(date.year))
                        words.add(str(date.month).zfill(2))
                        words.add(str(date.day).zfill(2))
                        words.add(f"{date.day}{date.month}{date.year}")
                        words.add(f"{date.day}{date.month}{str(date.year)[2:]}")
                    except ValueError:
                        # If parsing fails, just add the string
                        words.add(birthdate)
            
            # Add other personal info
            for key, value in personal.items():
                if key not in ["name", "birthdate"] and isinstance(value, str):
                    words.add(value)
                    words.add(value.lower())
        
        # Process social media
        if "social_media" in self.collected_data:
            for platform, username in self.collected_data["social_media"].items():
                words.add(username)
                words.add(username.lower())
                words.add(platform)
                words.add(platform.lower())
        
        # Process company info
        if "company" in self.collected_data:
            company = self.collected_data["company"]
            for key, value in company.items():
                if isinstance(value, str):
                    words.add(value)
                    words.add(value.lower())
        
        # Process any other categories
        for category, data in self.collected_data.items():
            if category not in ["personal", "social_media", "company"]:
                for key, value in data.items():
                    if isinstance(value, str):
                        words.add(value)
                        words.add(value.lower())
        
        return words
    
    def _generate_variations(self, word):
        """Generate variations of a word."""
        variations = set()
        variations.add(word)
        
        # Case variations
        variations.add(word.lower())
        variations.add(word.upper())
        variations.add(word.capitalize())
        
        # Common substitutions (leet speak)
        if self.include_leet:
            leet_map = {
                'a': '4', 'e': '3', 'i': '1', 'o': '0', 
                's': '5', 't': '7', 'b': '8', 'g': '9'
            }
            
            leet_word = word.lower()
            for char, replacement in leet_map.items():
                if char in leet_word:
                    leet_word = leet_word.replace(char, replacement)
            variations.add(leet_word)
        
        # Add common suffixes
        current_year = datetime.datetime.now().year
        for year in range(current_year - 5, current_year + 2):
            variations.add(f"{word}{year}")
            variations.add(f"{word}{str(year)[2:]}")
        
        for num in range(0, 100):
            variations.add(f"{word}{num}")
            variations.add(f"{word}_{num}")
        
        # Add common special character suffixes
        if self.include_special:
            for special in ['!', '@', '#', '$', '%', '&', '*', '?']:
                variations.add(f"{word}{special}")
                variations.add(f"{special}{word}")
                
                # Add year + special
                variations.add(f"{word}{current_year}{special}")
                variations.add(f"{word}{str(current_year)[2:]}{special}")
        
        return variations
    
    def _filter_by_length(self, words):
        """Filter words by length constraints."""
        return {word for word in words if self.min_length <= len(word) <= self.max_length}
    
    def generate_wordlist(self, wordlist_type=WordlistType.TARGETED):
        """Generate a wordlist based on collected OSINT data."""
        if not self.target_info:
            print("No target set. Please set a target first.")
            return False
            
        print(f"\n{'='*60}")
        print(f"Generating {wordlist_type.value} wordlist for {self.target_info['name']}")
        print(f"{'='*60}\n")
        
        # Extract base words from collected data
        base_words = self._extract_words_from_data()
        print(f"Extracted {len(base_words)} base words from collected data")
        
        # Generate variations
        if self.include_variations:
            all_variations = set()
            for word in base_words:
                variations = self._generate_variations(word)
                all_variations.update(variations)
            
            print(f"Generated {len(all_variations)} variations")
            self.wordlist.update(all_variations)
        else:
            self.wordlist.update(base_words)
        
        # Filter by length constraints
        self.wordlist = self._filter_by_length(self.wordlist)
        print(f"Final wordlist contains {len(self.wordlist)} entries after filtering")
        
        # Save to file if specified
        if self.output_file:
            try:
                with open(self.output_file, 'w') as f:
                    for word in sorted(self.wordlist):
                        f.write(f"{word}\n")
                print(f"Wordlist saved to {self.output_file}")
            except Exception as e:
                print(f"Error saving wordlist: {e}")
                return False
        
        return True
    
    def use_cupp(self, interactive=False):
        """Use CUPP to generate a wordlist."""
        if not self.external_tools["cupp"]:
            print("CUPP is not installed or not found in PATH")
            return False
            
        if not self.target_info:
            print("No target set. Please set a target first.")
            return False
            
        print(f"\n{'='*60}")
        print(f"Using CUPP to generate wordlist for {self.target_info['name']}")
        print(f"{'='*60}\n")
        
        try:
            if interactive:
                # Run CUPP in interactive mode
                subprocess.run(["cupp", "-i"], check=True)
            else:
                # Use collected data to generate CUPP parameters
                personal = self.collected_data.get("personal", {})
                
                first_name = personal.get("first_name", "")
                last_name = personal.get("last_name", "")
                nickname = personal.get("nickname", "")
                birthdate = personal.get("birthdate", "")
                
                # Parse birthdate if available
                birth_day = ""
                birth_month = ""
                birth_year = ""
                if birthdate:
                    try:
                        date = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
                        birth_day = str(date.day)
                        birth_month = str(date.month)
                        birth_year = str(date.year)
                    except ValueError:
                        pass
                
                # Partner info
                partner_name = personal.get("partner_name", "")
                partner_nickname = personal.get("partner_nickname", "")
                
                # Child info
                child_name = personal.get("child_name", "")
                child_nickname = personal.get("child_nickname", "")
                
                # Pet info
                pet_name = personal.get("pet_name", "")
                
                # Company info
                company = self.collected_data.get("company", {})
                company_name = company.get("name", "")
                
                # Create a temporary file with CUPP answers
                with open("cupp_answers.txt", "w") as f:
                    f.write(f"{first_name}\n")
                    f.write(f"{last_name}\n")
                    f.write(f"{nickname}\n")
                    f.write(f"{birth_day}\n")
                    f.write(f"{birth_month}\n")
                    f.write(f"{birth_year}\n")
                    f.write(f"{partner_name}\n")
                    f.write(f"{partner_nickname}\n")
                    f.write(f"{child_name}\n")
                    f.write(f"{child_nickname}\n")
                    f.write(f"{pet_name}\n")
                    f.write(f"{company_name}\n")
                
                # Run CUPP with the answers file
                output_file = f"{self.target_info['name'].replace(' ', '_')}_cupp.txt"
                subprocess.run(f"cat cupp_answers.txt | cupp -i", shell=True, check=True)
                
                # Clean up
                os.remove("cupp_answers.txt")
                
                # Load the generated wordlist
                if os.path.exists(output_file):
                    with open(output_file, 'r') as f:
                        for line in f:
                            self.wordlist.add(line.strip())
                    print(f"Added {len(self.wordlist)} words from CUPP")
                
            return True
        except Exception as e:
            print(f"Error using CUPP: {e}")
            return False
    
    def use_crunch(self, min_len=None, max_len=None, charset=None):
        """Use Crunch to generate a wordlist."""
        if not self.external_tools["crunch"]:
            print("Crunch is not installed or not found in PATH")
            return False
            
        min_len = min_len or self.min_length
        max_len = max_len or self.max_length
        
        if not charset:
            charset = "abcdefghijklmnopqrstuvwxyz"
            if self.include_numbers:
                charset += "0123456789"
            if self.include_special:
                charset += "!@#$%^&*()_+-="
        
        print(f"\n{'='*60}")
        print(f"Using Crunch to generate wordlist with length {min_len}-{max_len}")
        print(f"{'='*60}\n")
        
        try:
            output_file = "crunch_output.txt"
            subprocess.run(["crunch", str(min_len), str(max_len), charset, "-o", output_file], check=True)
            
            # Load the generated wordlist (but be careful, it could be huge)
            if os.path.exists(output_file):
                # Sample the file if it's too large
                file_size = os.path.getsize(output_file)
                if file_size > 10_000_000:  # 10MB
                    print(f"Crunch generated a large file ({file_size} bytes). Sampling...")
                    
                    # Sample random lines
                    with open(output_file, 'r') as f:
                        lines = f.readlines()
                    
                    # Take a random sample of 10,000 lines
                    sample_size = min(10000, len(lines))
                    sampled_lines = random.sample(lines, sample_size)
                    
                    for line in sampled_lines:
                        self.wordlist.add(line.strip())
                    
                    print(f"Added {sample_size} sampled words from Crunch")
                else:
                    with open(output_file, 'r') as f:
                        for line in f:
                            self.wordlist.add(line.strip())
                    print(f"Added {len(self.wordlist)} words from Crunch")
                
                # Clean up
                os.remove(output_file)
            
            return True
        except Exception as e:
            print(f"Error using Crunch: {e}")
            return False
    
    def use_recon_ng(self, module=None):
        """Use recon-ng to gather additional OSINT data."""
        if not self.external_tools["recon-ng"]:
            print("recon-ng is not installed or not found in PATH")
            return False
            
        if not self.target_info:
            print("No target set. Please set a target first.")
            return False
            
        print(f"\n{'='*60}")
        print(f"Using recon-ng to gather OSINT data for {self.target_info['name']}")
        print(f"{'='*60}\n")
        
        try:
            # Create a workspace for the target
            workspace = self.target_info['name'].replace(' ', '_').lower()
            subprocess.run(["recon-ng", "-w", workspace, "-c", "workspaces add"], check=True)
            
            # Add the target as a company or person
            if self.target_info['type'] == 'company':
                subprocess.run(["recon-ng", "-w", workspace, "-c", f"add companies {self.target_info['name']}"], check=True)
            else:
                # Assume it's a person
                personal = self.collected_data.get("personal", {})
                first_name = personal.get("first_name", "")
                last_name = personal.get("last_name", "")
                
                if first_name and last_name:
                    subprocess.run(["recon-ng", "-w", workspace, "-c", f"add contacts {first_name} {last_name}"], check=True)
            
            # Run specific module if provided
            if module:
                subprocess.run(["recon-ng", "-w", workspace, "-c", f"use {module}", "-c", "run"], check=True)
            else:
                # Run some default modules
                default_modules = [
                    "recon/domains-hosts/google_site_web",
                    "recon/domains-contacts/whois_pocs",
                    "recon/companies-contacts/linkedin_auth"
                ]
                
                for mod in default_modules:
                    try:
                        subprocess.run(["recon-ng", "-w", workspace, "-c", f"use {mod}", "-c", "run"], check=True)
                    except subprocess.CalledProcessError:
                        print(f"Error running module {mod}")
            
            # Export the results
            output_file = f"{workspace}_recon_ng.txt"
            subprocess.run(["recon-ng", "-w", workspace, "-c", f"use reporting/text", "-c", f"set filename {output_file}", "-c", "run"], check=True)
            
            # Process the results file to extract potential password components
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    content = f.read()
                
                # Extract emails, usernames, etc.
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
                for email in emails:
                    username = email.split('@')[0]
                    self.wordlist.add(username)
                    
                    # Add variations
                    if self.include_variations:
                        variations = self._generate_variations(username)
                        self.wordlist.update(variations)
                
                print(f"Extracted data from recon-ng results")
            
            return True
        except Exception as e:
            print(f"Error using recon-ng: {e}")
            return False
    
    def merge_wordlists(self, wordlist_files):
        """Merge multiple wordlist files."""
        for file_path in wordlist_files:
            if not os.path.exists(file_path):
                print(f"Wordlist file not found: {file_path}")
                continue
                
            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        word = line.strip()
                        if self.min_length <= len(word) <= self.max_length:
                            self.wordlist.add(word)
                
                print(f"Added words from {file_path}")
            except Exception as e:
                print(f"Error reading wordlist {file_path}: {e}")
        
        print(f"Total wordlist size after merging: {len(self.wordlist)}")
        return True
    
    def save_collected_data(self, output_file):
        """Save all collected OSINT data to a JSON file."""
        data = {
            "target": self.target_info,
            "data": self.collected_data,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Collected data saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving collected data: {e}")
            return False
    
    def load_collected_data(self, input_file):
        """Load collected OSINT data from a JSON file."""
        try:
            with open(input_file, 'r') as f:
                data = json.load(f)
            
            if "target" in data:
                self.target_info = data["target"]
            
            if "data" in data:
                self.collected_data = data["data"]
                
            print(f"Loaded collected data from {input_file}")
            return True
        except Exception as e:
            print(f"Error loading collected data: {e}")
            return False

# Example usage
if __name__ == "__main__":
    generator = OsintWordlistGenerator()
    
    # Set target
    generator.set_target("John Smith", "person")
    
    # Add personal information
    generator.add_personal_info(
        first_name="John",
        last_name="Smith",
        nickname="Johnny",
        birthdate="1990-05-15",
        pet_name="Buddy"
    )
    
    # Add social media
    generator.add_social_media("instagram", "johnsmith90")
    generator.add_social_media("facebook", "john.smith.1990")
    
    # Add company info
    generator.add_company_info(
        name="Acme Corp",
        position="Developer"
    )
    
    # Set output file
    generator.set_output_file("john_smith_wordlist.txt")
    
    # Generate wordlist
    generator.generate_wordlist(WordlistType.TARGETED)
    
    # Save collected data
    generator.save_collected_data("john_smith_osint.json")
