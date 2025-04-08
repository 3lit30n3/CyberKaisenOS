#!/usr/bin/env python3
import random
import time
import json
import os
import hashlib
import threading
from math import pi, sqrt
from enum import Enum

class DefenseLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"
    ADAPTIVE = "adaptive"

class ThreatResponse(Enum):
    MONITOR = "monitor"
    BLOCK = "block"
    REDIRECT = "redirect"
    HONEYPOT = "honeypot"
    COUNTERATTACK = "counterattack"

class HoneypotType(Enum):
    BASIC = "basic"
    INTERACTIVE = "interactive"
    DECEPTIVE = "deceptive"
    ADVANCED = "advanced"

class DefenseSystem:
    def __init__(self):
        self.active_defenses = {}
        self.threat_database = {}
        self.honeypots = {}
        self.deception_networks = {}
        self.intrusion_logs = []
        self.defense_level = DefenseLevel.MEDIUM
        self.auto_response = True
        self.learning_mode = True
        self.phi = (1 + sqrt(5)) / 2  # Golden ratio for defense calculations
        self.monitoring_threads = []
        
    def set_defense_level(self, level):
        """Set the overall defense level."""
        if isinstance(level, str):
            try:
                level = DefenseLevel(level.lower())
            except ValueError:
                print(f"Invalid defense level: {level}")
                return False
                
        if isinstance(level, DefenseLevel):
            self.defense_level = level
            print(f"Defense level set to {level.value}")
            
            # Adjust all active defenses to the new level
            for defense_id in self.active_defenses:
                self.active_defenses[defense_id]["level"] = level
                
            return True
        else:
            print("Invalid defense level type")
            return False
            
    def deploy_firewall(self, name, rules=None, level=None):
        """Deploy a firewall with specified rules."""
        defense_id = f"firewall_{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
        if not rules:
            rules = self._generate_default_rules()
            
        level = level or self.defense_level
        
        firewall = {
            "id": defense_id,
            "name": name,
            "type": "firewall",
            "rules": rules,
            "level": level,
            "status": "active",
            "created": time.time(),
            "blocked_attempts": 0,
            "effectiveness": self._calculate_effectiveness(rules, level)
        }
        
        self.active_defenses[defense_id] = firewall
        print(f"Deployed firewall '{name}' with {len(rules)} rules at {level.value} level")
        return defense_id
        
    def deploy_ids(self, name, signatures=None, level=None, response=ThreatResponse.MONITOR):
        """Deploy an Intrusion Detection System."""
        defense_id = f"ids_{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
        if not signatures:
            signatures = self._generate_default_signatures()
            
        level = level or self.defense_level
        
        if isinstance(response, str):
            try:
                response = ThreatResponse(response.lower())
            except ValueError:
                response = ThreatResponse.MONITOR
        
        ids = {
            "id": defense_id,
            "name": name,
            "type": "ids",
            "signatures": signatures,
            "level": level,
            "response": response,
            "status": "active",
            "created": time.time(),
            "detected_threats": 0,
            "effectiveness": self._calculate_effectiveness(signatures, level)
        }
        
        self.active_defenses[defense_id] = ids
        print(f"Deployed IDS '{name}' with {len(signatures)} signatures at {level.value} level")
        return defense_id
        
    def deploy_honeypot(self, name, target_service, honeypot_type=HoneypotType.INTERACTIVE, level=None):
        """Deploy a honeypot to attract and analyze attacks."""
        honeypot_id = f"honeypot_{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
        if isinstance(honeypot_type, str):
            try:
                honeypot_type = HoneypotType(honeypot_type.lower())
            except ValueError:
                honeypot_type = HoneypotType.BASIC
                
        level = level or self.defense_level
        
        honeypot = {
            "id": honeypot_id,
            "name": name,
            "type": "honeypot",
            "service": target_service,
            "honeypot_type": honeypot_type,
            "level": level,
            "status": "active",
            "created": time.time(),
            "interactions": 0,
            "captured_payloads": [],
            "attacker_ips": set(),
            "effectiveness": self._calculate_honeypot_effectiveness(honeypot_type, level)
        }
        
        self.honeypots[honeypot_id] = honeypot
        print(f"Deployed {honeypot_type.value} honeypot '{name}' emulating {target_service}")
        return honeypot_id
        
    def create_deception_network(self, name, size=10, services=None, level=None):
        """Create a deception network with fake systems and services."""
        network_id = f"deception_{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
        if not services:
            services = ["http", "ssh", "ftp", "smb", "database"]
            
        level = level or self.defense_level
        
        # Generate fake systems
        systems = []
        for i in range(size):
            service = random.choice(services)
            system = {
                "id": f"system_{i}",
                "name": f"{name}_sys_{i}",
                "service": service,
                "ip": f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
                "os": random.choice(["Windows", "Linux", "FreeBSD"]),
                "interactions": 0,
                "status": "online"
            }
            systems.append(system)
            
        network = {
            "id": network_id,
            "name": name,
            "type": "deception_network",
            "systems": systems,
            "level": level,
            "status": "active",
            "created": time.time(),
            "total_interactions": 0,
            "effectiveness": self._calculate_deception_effectiveness(size, level)
        }
        
        self.deception_networks[network_id] = network
        print(f"Created deception network '{name}' with {size} fake systems")
        return network_id
        
    def deploy_adaptive_defense(self, name, learning_rate=0.05, adaptation_interval=300):
        """Deploy an adaptive defense system that learns from attacks."""
        defense_id = f"adaptive_{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
        adaptive = {
            "id": defense_id,
            "name": name,
            "type": "adaptive",
            "learning_rate": learning_rate,
            "adaptation_interval": adaptation_interval,
            "level": DefenseLevel.ADAPTIVE,
            "status": "active",
            "created": time.time(),
            "adaptations": 0,
            "learned_patterns": [],
            "effectiveness": 0.7  # Initial effectiveness
        }
        
        self.active_defenses[defense_id] = adaptive
        
        # Start adaptation thread
        thread = threading.Thread(target=self._adaptation_loop, args=(defense_id, adaptation_interval))
        thread.daemon = True
        thread.start()
        self.monitoring_threads.append(thread)
        
        print(f"Deployed adaptive defense '{name}' with {adaptation_interval}s adaptation interval")
        return defense_id
        
    def _adaptation_loop(self, defense_id, interval):
        """Background thread for adaptive defense learning."""
        while defense_id in self.active_defenses and self.active_defenses[defense_id]["status"] == "active":
            time.sleep(interval)
            
            # Analyze recent threats and adapt
            if self.intrusion_logs:
                recent_logs = [log for log in self.intrusion_logs if time.time() - log["timestamp"] < interval]
                if recent_logs:
                    # Extract patterns and adapt
                    patterns = self._extract_attack_patterns(recent_logs)
                    if patterns:
                        self.active_defenses[defense_id]["learned_patterns"].extend(patterns)
                        self.active_defenses[defense_id]["adaptations"] += 1
                        self.active_defenses[defense_id]["effectiveness"] = min(
                            0.95, 
                            self.active_defenses[defense_id]["effectiveness"] + 
                            self.active_defenses[defense_id]["learning_rate"]
                        )
                        print(f"Adaptive defense '{self.active_defenses[defense_id]['name']}' learned {len(patterns)} new patterns")
                        
    def _extract_attack_patterns(self, logs):
        """Extract attack patterns from logs for adaptive learning."""
        # This would be a complex ML algorithm in a real system
        # Here we'll simulate it with a simple pattern extraction
        patterns = []
        
        # Group by source
        sources = {}
        for log in logs:
            if "source" in log:
                if log["source"] not in sources:
                    sources[log["source"]] = []
                sources[log["source"]].append(log)
                
        # Look for repeated patterns
        for source, source_logs in sources.items():
            if len(source_logs) > 3:  # If same source has multiple attempts
                pattern = {
                    "source": source,
                    "frequency": len(source_logs),
                    "techniques": list(set([log.get("technique", "unknown") for log in source_logs])),
                    "targets": list(set([log.get("target", "unknown") for log in source_logs]))
                }
                patterns.append(pattern)
                
        return patterns
        
    def log_intrusion(self, details):
        """Log an intrusion attempt."""
        if not isinstance(details, dict):
            print("Intrusion details must be a dictionary")
            return False
            
        log_entry = {
            "id": f"intrusion_{len(self.intrusion_logs)}",
            "timestamp": time.time(),
            **details
        }
        
        self.intrusion_logs.append(log_entry)
        
        # Auto-respond if enabled
        if self.auto_response:
            self._auto_respond_to_intrusion(log_entry)
            
        return log_entry["id"]
        
    def _auto_respond_to_intrusion(self, intrusion):
        """Automatically respond to an intrusion based on defense level."""
        response = None
        
        if self.defense_level == DefenseLevel.LOW:
            response = ThreatResponse.MONITOR
        elif self.defense_level == DefenseLevel.MEDIUM:
            response = ThreatResponse.BLOCK
        elif self.defense_level == DefenseLevel.HIGH:
            response = ThreatResponse.REDIRECT
        elif self.defense_level == DefenseLevel.MAXIMUM:
            response = ThreatResponse.COUNTERATTACK
        elif self.defense_level == DefenseLevel.ADAPTIVE:
            # Choose response based on threat assessment
            threat_level = intrusion.get("threat_level", 0)
            if threat_level < 30:
                response = ThreatResponse.MONITOR
            elif threat_level < 60:
                response = ThreatResponse.BLOCK
            elif threat_level < 80:
                response = ThreatResponse.REDIRECT
            else:
                response = ThreatResponse.COUNTERATTACK
                
        # Execute the response
        if response == ThreatResponse.MONITOR:
            print(f"Monitoring intrusion from {intrusion.get('source', 'unknown')}")
        elif response == ThreatResponse.BLOCK:
            print(f"Blocking intrusion from {intrusion.get('source', 'unknown')}")
            # Add to blocked list
            if "source" in intrusion:
                self._add_to_blocklist(intrusion["source"])
        elif response == ThreatResponse.REDIRECT:
            print(f"Redirecting intrusion from {intrusion.get('source', 'unknown')} to honeypot")
            # Find a suitable honeypot
            honeypot = self._find_suitable_honeypot(intrusion)
            if honeypot:
                print(f"Redirected to honeypot: {honeypot['name']}")
        elif response == ThreatResponse.COUNTERATTACK:
            print(f"Launching counterattack against {intrusion.get('source', 'unknown')}")
            # This would be the offensive capability in a real system
            
        return response
        
    def _find_suitable_honeypot(self, intrusion):
        """Find a suitable honeypot for redirecting an intrusion."""
        if not self.honeypots:
            return None
            
        target_service = intrusion.get("target_service", "unknown")
        
        # Try to find a matching service honeypot
        matching_honeypots = [h for h in self.honeypots.values() 
                             if h["service"] == target_service and h["status"] == "active"]
        
        if matching_honeypots:
            return random.choice(matching_honeypots)
            
        # Otherwise return any active honeypot
        active_honeypots = [h for h in self.honeypots.values() if h["status"] == "active"]
        if active_honeypots:
            return random.choice(active_honeypots)
            
        return None
        
    def _add_to_blocklist(self, source):
        """Add a source to the blocklist."""
        # In a real system, this would update firewall rules
        for defense_id, defense in self.active_defenses.items():
            if defense["type"] == "firewall" and defense["status"] == "active":
                if "blocklist" not in defense:
                    defense["blocklist"] = []
                if source not in defense["blocklist"]:
                    defense["blocklist"].append(source)
                    defense["blocked_attempts"] += 1
                    print(f"Added {source} to {defense['name']} blocklist")
                    
    def _generate_default_rules(self):
        """Generate default firewall rules."""
        return [
            {"action": "allow", "protocol": "tcp", "port": 80, "description": "HTTP"},
            {"action": "allow", "protocol": "tcp", "port": 443, "description": "HTTPS"},
            {"action": "allow", "protocol": "tcp", "port": 22, "description": "SSH"},
            {"action": "deny", "protocol": "tcp", "port": "1-21", "description": "Block low ports"},
            {"action": "deny", "protocol": "tcp", "port": "23-79", "description": "Block dangerous services"},
            {"action": "deny", "protocol": "tcp", "port": "81-442", "description": "Block unneeded services"},
            {"action": "deny", "protocol": "tcp", "port": "444-65535", "description": "Block high ports"},
            {"action": "deny", "protocol": "udp", "port": "1-65535", "description": "Block all UDP"},
            {"action": "deny", "protocol": "icmp", "description": "Block ICMP"}
        ]
        
    def _generate_default_signatures(self):
        """Generate default IDS signatures."""
        return [
            {"name": "SQL Injection", "pattern": "SELECT.*FROM", "severity": "high"},
            {"name": "XSS Attack", "pattern": "<script>", "severity": "high"},
            {"name": "Command Injection", "pattern": ";&|`", "severity": "critical"},
            {"name": "Directory Traversal", "pattern": "\\.\\./", "severity": "medium"},
            {"name": "Port Scan", "pattern": "multiple ports in short time", "severity": "medium"},
            {"name": "Brute Force", "pattern": "multiple auth failures", "severity": "high"},
            {"name": "Malware Download", "pattern": "\\.exe|\\.dll|\\.sh", "severity": "high"},
            {"name": "Data Exfiltration", "pattern": "large outbound transfer", "severity": "critical"}
        ]
        
    def _calculate_effectiveness(self, rules, level):
        """Calculate the effectiveness of a defense based on rules and level."""
        base_effectiveness = 0.5
        rules_factor = min(1.0, len(rules) / 10)  # More rules = more effective, up to a point
        
        level_multiplier = 1.0
        if level == DefenseLevel.LOW:
            level_multiplier = 0.7
        elif level == DefenseLevel.MEDIUM:
            level_multiplier = 1.0
        elif level == DefenseLevel.HIGH:
            level_multiplier = 1.3
        elif level == DefenseLevel.MAXIMUM:
            level_multiplier = 1.5
        elif level == DefenseLevel.ADAPTIVE:
            level_multiplier = 1.2
            
        effectiveness = base_effectiveness + (rules_factor * 0.5)
        effectiveness *= level_multiplier
        
        # Apply golden ratio for balance
        effectiveness = min(0.95, effectiveness * self.phi / 2)
        
        return effectiveness
        
    def _calculate_honeypot_effectiveness(self, honeypot_type, level):
        """Calculate the effectiveness of a honeypot."""
        base_effectiveness = 0.4
        
        type_multiplier = 1.0
        if honeypot_type == HoneypotType.BASIC:
            type_multiplier = 0.7
        elif honeypot_type == HoneypotType.INTERACTIVE:
            type_multiplier = 1.0
        elif honeypot_type == HoneypotType.DECEPTIVE:
            type_multiplier = 1.3
        elif honeypot_type == HoneypotType.ADVANCED:
            type_multiplier = 1.6
            
        level_multiplier = 1.0
        if level == DefenseLevel.LOW:
            level_multiplier = 0.7
        elif level == DefenseLevel.MEDIUM:
            level_multiplier = 1.0
        elif level == DefenseLevel.HIGH:
            level_multiplier = 1.3
        elif level == DefenseLevel.MAXIMUM:
            level_multiplier = 1.5
        elif level == DefenseLevel.ADAPTIVE:
            level_multiplier = 1.2
            
        effectiveness = base_effectiveness * type_multiplier * level_multiplier
        
        # Apply golden ratio for balance
        effectiveness = min(0.95, effectiveness * self.phi / 2)
        
        return effectiveness
        
    def _calculate_deception_effectiveness(self, size, level):
        """Calculate the effectiveness of a deception network."""
        base_effectiveness = 0.3
        size_factor = min(1.0, size / 20)  # More systems = more effective, up to a point
        
        level_multiplier = 1.0
        if level == DefenseLevel.LOW:
            level_multiplier = 0.7
        elif level == DefenseLevel.MEDIUM:
            level_multiplier = 1.0
        elif level == DefenseLevel.HIGH:
            level_multiplier = 1.3
        elif level == DefenseLevel.MAXIMUM:
            level_multiplier = 1.5
        elif level == DefenseLevel.ADAPTIVE:
            level_multiplier = 1.2
            
        effectiveness = base_effectiveness + (size_factor * 0.6)
        effectiveness *= level_multiplier
        
        # Apply golden ratio for balance
        effectiveness = min(0.95, effectiveness * self.phi / 2)
        
        return effectiveness
        
    def get_defense_status(self, defense_id=None):
        """Get the status of a specific defense or all defenses."""
        if defense_id:
            if defense_id in self.active_defenses:
                return self.active_defenses[defense_id]
            elif defense_id in self.honeypots:
                return self.honeypots[defense_id]
            elif defense_id in self.deception_networks:
                return self.deception_networks[defense_id]
            else:
                print(f"Defense {defense_id} not found")
                return None
        else:
            # Return summary of all defenses
            return {
                "defense_level": self.defense_level.value,
                "active_defenses": len(self.active_defenses),
                "honeypots": len(self.honeypots),
                "deception_networks": len(self.deception_networks),
                "intrusion_logs": len(self.intrusion_logs),
                "auto_response": self.auto_response,
                "learning_mode": self.learning_mode
            }
            
    def disable_defense(self, defense_id):
        """Disable a specific defense."""
        if defense_id in self.active_defenses:
            self.active_defenses[defense_id]["status"] = "disabled"
            print(f"Disabled defense: {self.active_defenses[defense_id]['name']}")
            return True
        elif defense_id in self.honeypots:
            self.honeypots[defense_id]["status"] = "disabled"
            print(f"Disabled honeypot: {self.honeypots[defense_id]['name']}")
            return True
        elif defense_id in self.deception_networks:
            self.deception_networks[defense_id]["status"] = "disabled"
            print(f"Disabled deception network: {self.deception_networks[defense_id]['name']}")
            return True
        else:
            print(f"Defense {defense_id} not found")
            return False
            
    def enable_defense(self, defense_id):
        """Enable a specific defense."""
        if defense_id in self.active_defenses:
            self.active_defenses[defense_id]["status"] = "active"
            print(f"Enabled defense: {self.active_defenses[defense_id]['name']}")
            return True
        elif defense_id in self.honeypots:
            self.honeypots[defense_id]["status"] = "active"
            print(f"Enabled honeypot: {self.honeypots[defense_id]['name']}")
            return True
        elif defense_id in self.deception_networks:
            self.deception_networks[defense_id]["status"] = "active"
            print(f"Enabled deception network: {self.deception_networks[defense_id]['name']}")
            return True
        else:
            print(f"Defense {defense_id} not found")
            return False
            
    def save_defense_config(self, filename):
        """Save the current defense configuration to a file."""
        config = {
            "defense_level": self.defense_level.value,
            "auto_response": self.auto_response,
            "learning_mode": self.learning_mode,
            "active_defenses": self.active_defenses,
            "honeypots": self.honeypots,
            "deception_networks": self.deception_networks
        }
        
        # Convert sets to lists for JSON serialization
        for honeypot_id in config["honeypots"]:
            if "attacker_ips" in config["honeypots"][honeypot_id]:
                config["honeypots"][honeypot_id]["attacker_ips"] = list(config["honeypots"][honeypot_id]["attacker_ips"])
        
        try:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"Defense configuration saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving defense configuration: {e}")
            return False
            
    def load_defense_config(self, filename):
        """Load a defense configuration from a file."""
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
                
            # Convert defense level string to enum
            if "defense_level" in config:
                try:
                    self.defense_level = DefenseLevel(config["defense_level"])
                except ValueError:
                    self.defense_level = DefenseLevel.MEDIUM
                    
            if "auto_response" in config:
                self.auto_response = config["auto_response"]
                
            if "learning_mode" in config:
                self.learning_mode = config["learning_mode"]
                
            if "active_defenses" in config:
                self.active_defenses = config["active_defenses"]
                
            if "honeypots" in config:
                self.honeypots = config["honeypots"]
                # Convert attacker_ips lists back to sets
                for honeypot_id in self.honeypots:
                    if "attacker_ips" in self.honeypots[honeypot_id]:
                        self.honeypots[honeypot_id]["attacker_ips"] = set(self.honeypots[honeypot_id]["attacker_ips"])
                
            if "deception_networks" in config:
                self.deception_networks = config["deception_networks"]
                
            print(f"Defense configuration loaded from {filename}")
            return True
        except Exception as e:
            print(f"Error loading defense configuration: {e}")
            return False
            
    def simulate_attack(self, attack_type, source="192.168.1.100", target="web_server", intensity=5):
        """Simulate an attack to test defenses."""
        print(f"Simulating {attack_type} attack from {source} against {target} with intensity {intensity}")
        
        # Log the simulated attack
        intrusion = {
            "source": source,
            "target": target,
            "technique": attack_type,
            "intensity": intensity,
            "threat_level": min(100, intensity * 10),
            "simulated": True
        }
        
        intrusion_id = self.log_intrusion(intrusion)
        
        # Check if any defenses detected/blocked it
        detected = False
        blocked = False
        
        for defense_id, defense in self.active_defenses.items():
            if defense["status"] != "active":
                continue
                
            if defense["type"] == "ids":
                # Check if any signature matches
                for sig in defense["signatures"]:
                    if attack_type.lower() in sig["name"].lower():
                        detected = True
                        defense["detected_threats"] += 1
                        print(f"Attack detected by {defense['name']} using signature: {sig['name']}")
                        break
                        
            elif defense["type"] == "firewall":
                # Check if source is in blocklist
                if "blocklist" in defense and source in defense["blocklist"]:
                    blocked = True
                    defense["blocked_attempts"] += 1
                    print(f"Attack blocked by {defense['name']} - source {source} is in blocklist")
                    break
                    
        # Check honeypots
        for honeypot_id, honeypot in self.honeypots.items():
            if honeypot["status"] != "active":
                continue
                
            if honeypot["service"] in target:
                honeypot["interactions"] += 1
                honeypot["attacker_ips"].add(source)
                if random.random() < 0.7:  # 70% chance to capture payload
                    honeypot["captured_payloads"].append({
                        "type": attack_type,
                        "source": source,
                        "timestamp": time.time()
                    })
                    print(f"Attack payload captured by honeypot {honeypot['name']}")
                    
        # Check deception networks
        for network_id, network in self.deception_networks.items():
            if network["status"] != "active":
                continue
                
            # Check if any system in the network was targeted
            for system in network["systems"]:
                if system["service"] in target or random.random() < 0.3:  # 30% chance of random targeting
                    system["interactions"] += 1
                    network["total_interactions"] += 1
                    print(f"Deception network {network['name']} system {system['name']} interacted with attack")
                    
        result = {
            "intrusion_id": intrusion_id,
            "detected": detected,
            "blocked": blocked,
            "attack_type": attack_type,
            "source": source,
            "target": target,
            "intensity": intensity
        }
        
        return result

# Example usage
if __name__ == "__main__":
    defense = DefenseSystem()
    
    # Deploy various defenses
    firewall_id = defense.deploy_firewall("Main Firewall")
    ids_id = defense.deploy_ids("Network IDS")
    honeypot_id = defense.deploy_honeypot("SSH Honeypot", "ssh", HoneypotType.INTERACTIVE)
    deception_id = defense.create_deception_network("Fake DMZ", size=5)
    adaptive_id = defense.deploy_adaptive_defense("Adaptive Defense")
    
    # Set to maximum defense level
    defense.set_defense_level(DefenseLevel.MAXIMUM)
    
    # Simulate some attacks
    defense.simulate_attack("SQL Injection", target="web_application")
    defense.simulate_attack("Brute Force", target="ssh_server", intensity=8)
    defense.simulate_attack("Port Scan", intensity=3)
    
    # Get defense status
    status = defense.get_defense_status()
    print(f"Defense status: {status}")
    
    # Save configuration
    defense.save_defense_config("defense_config.json")
