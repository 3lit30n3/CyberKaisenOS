#!/usr/bin/env python3
import os
import time
import sys
import threading
import keyboard
from CyberKaisenOS import CyberKaisenOS
from cybersecurity_kaisen import CyberKaisenAgent, Gojo, Sakuna, Toji, Maki
from phixeo_api import PhixeoAPI

class InteractiveCyberKaisen:
    def __init__(self):
        self.os = CyberKaisenOS()
        self.phixeo = PhixeoAPI()
        self.running = True
        self.current_agent = None
        self.mission_running = False
        self.mission_thread = None
        self.current_options = {}
        self.option_keys = ['e', 'f', 'd', 's', 'a', 'c']  # Left hand
        self.num_keys = ['8', '4', '5', '6', '2']  # Right hand

        # Initialize Phixeo network for dynamic mission control
        self._setup_phixeo_network()

    def _setup_phixeo_network(self):
        """Setup Phixeo network with geometric nodes for mission control."""
        # Command processing node (Tetrahedral for stability)
        self.phixeo.add_node("Tetrahedral", "process_command(input_key)")

        # Option management node (Hexagonal for connection)
        self.phixeo.add_node("Hexagonal", "update_available_options(mission_state)")

        # Agent autonomy node (Pentagonal for intelligence)
        self.phixeo.add_node("Pentagonal", "if time_since_input > 3: execute_autonomous_action()")

        # Threat assessment node (Fractal for adaptability)
        fractal_node = self.phixeo.add_fractal_node("Hexagonal", iterations=3)

        # Connect nodes to create program flow
        self.phixeo.connect_nodes(0, 1)
        self.phixeo.connect_nodes(1, 2)
        self.phixeo.connect_nodes(2, fractal_node)

        # Apply sacred geometry for optimal performance
        self.phixeo.execute_sacred_geometry("fibonacci")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print("=" * 60)
        print("        C Y B E R K A I S E N   O M N I S C I E N C E        ")
        print("=" * 60)
        print()

    def print_agent_details(self, agent_name):
        agent = self.os.agents.get(agent_name)
        if not agent:
            print(f"Agent {agent_name} not found.")
            return

        print(f"AGENT: {agent_name}")
        print(f"SPECIALTY: {agent.specialty}")
        print(f"ABILITIES:")

        if agent_name == "Gojo":
            print("  - Blue Vulnerability Magnet: Attracts and isolates vulnerabilities for analysis")
            print("  - Red Counter Pulse: Neutralizes active intrusion attempts")
            print("  - Unlimited Void (Domain Expansion): Creates impenetrable security perimeter")
        elif agent_name == "Sukuna":
            print("  - Cleave Packet Slicer: Dissects network traffic for anomalies")
            print("  - Dismantle Network Shredder: Breaks down complex threats into manageable components")
            print("  - Phantom Payload: Deploys undetectable counter-intrusion code")
            print("  - Malevolent Shrine (Domain Expansion): Aggressive counter-attack system")
        elif agent_name == "Toji":
            print("  - Silent Scout: Undetectable reconnaissance of target systems")
            print("  - Infiltration: Gains access to secured networks without triggering alerts")
        elif agent_name == "Maki":
            print("  - Exploit Disarm: Neutralizes zero-day vulnerabilities before they can be used")
            print("  - Infiltration: Gains access to secured networks without triggering alerts")

    def agent_selection_menu(self):
        self.print_header()
        print("AGENT SELECTION")
        print("-" * 60)
        print("Select an agent to operate:")
        print()

        for i, (name, agent) in enumerate(self.os.agents.items(), 1):
            print(f"{i}. {name} - {agent.specialty}")

        print()
        print("A. Add new agent")
        print("E. Edit existing agent")
        print("D. Delete agent")
        print("B. Boot CyberKaisenOS")
        print("Q. Quit")

        choice = input("\nEnter your choice: ").strip().upper()

        if choice == 'Q':
            self.running = False
        elif choice == 'A':
            self.add_agent_menu()
        elif choice == 'E':
            self.edit_agent_menu()
        elif choice == 'D':
            self.delete_agent_menu()
        elif choice == 'B':
            self.boot_system()
        elif choice.isdigit() and 1 <= int(choice) <= len(self.os.agents):
            agent_name = list(self.os.agents.keys())[int(choice) - 1]
            self.current_agent = agent_name
            self.agent_action_menu(agent_name)

    def add_agent_menu(self):
        self.print_header()
        print("ADD NEW AGENT")
        print("-" * 60)

        name = input("Enter agent name: ").strip()
        if not name:
            print("Agent name cannot be empty.")
            input("Press Enter to continue...")
            return

        if name in self.os.agents:
            print(f"Agent {name} already exists.")
            input("Press Enter to continue...")
            return

        print("\nSelect agent specialty:")
        print("1. vuln_scan - Vulnerability scanning")
        print("2. brute_force - Brute force attacks")
        print("3. osint - Open-source intelligence")

        specialty_choice = input("\nEnter specialty (1-3): ").strip()

        if specialty_choice == '1':
            specialty = "vuln_scan"
        elif specialty_choice == '2':
            specialty = "brute_force"
        elif specialty_choice == '3':
            specialty = "osint"
        else:
            print("Invalid specialty choice.")
            input("Press Enter to continue...")
            return

        self.os.agents[name] = CyberKaisenAgent(name, specialty, self.os)
        print(f"\nAgent {name} with specialty {specialty} created successfully!")
        input("Press Enter to continue...")

    def edit_agent_menu(self):
        self.print_header()
        print("EDIT AGENT")
        print("-" * 60)

        for i, name in enumerate(self.os.agents.keys(), 1):
            print(f"{i}. {name}")

        choice = input("\nSelect agent to edit (number) or 'B' to go back: ").strip()

        if choice.upper() == 'B':
            return

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(self.os.agents):
            print("Invalid choice.")
            input("Press Enter to continue...")
            return

        agent_name = list(self.os.agents.keys())[int(choice) - 1]
        agent = self.os.agents[agent_name]

        self.print_header()
        print(f"EDITING AGENT: {agent_name}")
        print("-" * 60)
        print("1. Change name")
        print("2. Change specialty")
        print("B. Back")

        edit_choice = input("\nEnter your choice: ").strip().upper()

        if edit_choice == '1':
            new_name = input("Enter new name: ").strip()
            if new_name and new_name != agent_name and new_name not in self.os.agents:
                self.os.agents[new_name] = agent
                agent.name = new_name
                del self.os.agents[agent_name]
                print(f"Agent renamed to {new_name}.")
            else:
                print("Invalid name or name already exists.")
        elif edit_choice == '2':
            print("\nSelect new specialty:")
            print("1. vuln_scan - Vulnerability scanning")
            print("2. brute_force - Brute force attacks")
            print("3. osint - Open-source intelligence")

            specialty_choice = input("\nEnter specialty (1-3): ").strip()

            if specialty_choice == '1':
                agent.specialty = "vuln_scan"
            elif specialty_choice == '2':
                agent.specialty = "brute_force"
            elif specialty_choice == '3':
                agent.specialty = "osint"
            else:
                print("Invalid specialty choice.")
                input("Press Enter to continue...")
                return

            print(f"Specialty changed to {agent.specialty}.")

        input("Press Enter to continue...")

    def delete_agent_menu(self):
        self.print_header()
        print("DELETE AGENT")
        print("-" * 60)

        for i, name in enumerate(self.os.agents.keys(), 1):
            print(f"{i}. {name}")

        choice = input("\nSelect agent to delete (number) or 'B' to go back: ").strip()

        if choice.upper() == 'B':
            return

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(self.os.agents):
            print("Invalid choice.")
            input("Press Enter to continue...")
            return

        agent_name = list(self.os.agents.keys())[int(choice) - 1]

        confirm = input(f"Are you sure you want to delete agent {agent_name}? (y/n): ").strip().lower()
        if confirm == 'y':
            del self.os.agents[agent_name]
            print(f"Agent {agent_name} deleted.")
        else:
            print("Deletion cancelled.")

        input("Press Enter to continue...")

    def agent_action_menu(self, agent_name):
        while True:
            self.print_header()
            self.print_agent_details(agent_name)
            print("\nACTIONS:")
            print("-" * 60)

            if agent_name == "Gojo":
                print("1. Scan vulnerabilities - Detect security weaknesses in the network")
                print("2. Blue vulnerability magnet - Attract and isolate vulnerabilities for analysis")
                print("3. Red counter pulse - Neutralize active intrusion attempts")
                print("4. Unlimited Void (Domain Expansion) - Create impenetrable security perimeter")
            elif agent_name == "Sukuna":
                print("1. Brute force attack - Test system resistance against repeated login attempts")
                print("2. Cleave packet slicer - Dissect network traffic for anomalies")
                print("3. Dismantle network shredder - Break down complex threats into manageable components")
                print("4. Phantom payload - Deploy undetectable counter-intrusion code")
                print("5. Malevolent Shrine (Domain Expansion) - Activate aggressive counter-attack system")
            elif agent_name == "Toji":
                print("1. Gather OSINT - Collect open-source intelligence on targets")
                print("2. Silent scout - Perform undetectable reconnaissance of target systems")
                print("3. Infiltrate target - Gain access to secured networks without triggering alerts")
            elif agent_name == "Maki":
                print("1. Gather OSINT - Collect open-source intelligence on targets")
                print("2. Exploit disarm - Neutralize zero-day vulnerabilities before they can be used")
                print("3. Infiltrate target - Gain access to secured networks without triggering alerts")
            else:
                # Generic actions for custom agents
                print("1. Execute primary function - Run agent's specialty operation")
                print("2. Analyze target - Perform detailed analysis of target systems")
                print("3. Generate report - Create comprehensive security assessment report")

            print("D. Dynamic Mission (Real-time)")
            print("\nB. Back to agent selection")

            choice = input("\nEnter your choice: ").strip().upper()

            if choice == 'B':
                break
            elif choice == 'D':
                self.dynamic_mission(agent_name)

            agent = self.os.agents[agent_name]

            if agent_name == "Gojo":
                if choice == '1':
                    agent.execute("scan")
                elif choice == '2':
                    agent.execute("blue")
                elif choice == '3':
                    agent.execute("red")
                elif choice == '4':
                    self.os.unlimited_void()
            elif agent_name == "Sukuna":
                if choice == '1':
                    agent.execute("attack")
                elif choice == '2':
                    agent.execute("cleave")
                elif choice == '3':
                    agent.execute("dismantle")
                elif choice == '4':
                    agent.execute("phantom")
                elif choice == '5':
                    self.os.malevolent_shrine()
            elif agent_name == "Toji":
                if choice == '1':
                    agent.execute("gather_osint")
                elif choice == '2':
                    agent.execute("scout")
                elif choice == '3':
                    target = input("Enter target to infiltrate: ")
                    agent.agent.infiltrate(target)
            elif agent_name == "Maki":
                if choice == '1':
                    agent.execute("gather_osint")
                elif choice == '2':
                    agent.execute("disarm")
                elif choice == '3':
                    target = input("Enter target to infiltrate: ")
                    agent.agent.infiltrate(target)
            else:
                # Generic actions for custom agents
                if choice == '1':
                    print(f"{agent_name} executing primary function...")
                    agent.execute("scan" if agent.specialty == "vuln_scan" else
                                 "attack" if agent.specialty == "brute_force" else
                                 "gather_osint")
                elif choice == '2':
                    print(f"{agent_name} analyzing target...")
                    time.sleep(1)
                    print("Analysis complete.")
                elif choice == '3':
                    print(f"{agent_name} generating report...")
                    time.sleep(1)
                    print("Report generated.")

            input("\nPress Enter to continue...")

    def boot_system(self):
        self.print_header()
        print("BOOTING CYBERKAISEN OS")
        print("-" * 60)

        self.os.boot()
        print("\nCyberKaisenOS booted successfully!")

        print("\nSelect domain expansion to execute:")
        print("1. Unlimited Void - Creates impenetrable security perimeter")
        print("2. Malevolent Shrine - Aggressive counter-attack system")
        print("3. Firewall Sanctuary - Advanced threat filtering and blocking")
        print("4. Chimera Shadow Garden - Network randomization and traffic rerouting")
        print("5. Infinite Exploit Forge - Vulnerability discovery and exploit development")
        print("6. All domain expansions - Maximum security posture")
        print("0. None")

        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            self.os.unlimited_void()
        elif choice == '2':
            self.os.malevolent_shrine()
        elif choice == '3':
            self.os.firewall_sanctuary()
        elif choice == '4':
            self.os.chimera_shadow_garden()
        elif choice == '5':
            self.os.infinite_exploit_forge()
        elif choice == '6':
            self.os.unlimited_void()
            self.os.malevolent_shrine()
            self.os.firewall_sanctuary()
            self.os.chimera_shadow_garden()
            self.os.infinite_exploit_forge()

        input("\nPress Enter to continue...")

    def dynamic_mission(self, agent_name):
        """Run a dynamic mission with real-time options using Phixeo patterns."""
        self.mission_running = True
        agent = self.os.agents[agent_name]

        # Create mission-specific Phixeo tactic
        mission_tactic = f"""
        node Tetrahedral "initialize_mission('{agent_name}')"
        node Hexagonal "for phase in mission_phases: execute_phase(phase)"
        node Pentagonal "if threat_level > 70: escalate_response()"
        connect 0 1
        connect 1 2
        """

        # Execute the Phixeo tactic
        self.os.execute_user_tactic(mission_tactic)

        # Set up keyboard listeners
        for key in self.option_keys + self.num_keys:
            keyboard.on_press_key(key, self.handle_key_press)

        try:
            mission_thread = threading.Thread(target=self._run_mission_loop, args=(agent_name, agent))
            mission_thread.daemon = True
            mission_thread.start()

            # Main thread just keeps the mission alive until ESC is pressed
            while self.mission_running:
                if keyboard.is_pressed('esc'):
                    self.mission_running = False
                time.sleep(0.1)

        finally:
            # Clean up keyboard listeners
            keyboard.unhook_all()
            print("\nMission terminated.")

    def _run_mission_loop(self, agent_name, agent):
        """The actual mission loop running in a separate thread with Phixeo patterns."""
        mission_phase = 0
        threat_level = 20
        discovered_assets = []
        vulnerabilities = []

        # Create phase-specific Phixeo nodes
        recon_node = self.phixeo.add_node("Tetrahedral", "scan_network('target_network')")
        vuln_node = self.phixeo.add_node("Hexagonal", "for asset in assets: find_vulnerabilities(asset)")
        exploit_node = self.phixeo.add_node("Pentagonal", "if vulnerability: exploit(vulnerability)")

        # Connect phase nodes
        self.phixeo.connect_nodes(recon_node, vuln_node)
        self.phixeo.connect_nodes(vuln_node, exploit_node)

        while self.mission_running:
            # Clear and redraw the screen
            self.clear_screen()
            print(f"== ACTIVE MISSION: {agent_name} ==")
            print(f"Phase: {mission_phase} | Threat Level: {threat_level}%")

            # Dynamic situation assessment using Phixeo patterns
            if mission_phase == 0:
                print("\nReconnaissance phase...")
                # Execute the reconnaissance node
                self.phixeo.nodes[recon_node]["value"] = "scan_network('target_network')"
                discovered_assets = self._simulate_discovery()
                self._update_options({
                    'e': "Scan deeper",
                    'f': "Analyze discovered assets",
                    'd': "Deploy monitoring",
                    's': "Move to infiltration",
                    'a': "Request backup",
                })
                mission_phase = 1

            elif mission_phase == 1:
                print("\nVulnerability assessment...")
                vulnerabilities = self._simulate_vulnerabilities(discovered_assets)
                threat_level = min(threat_level + 10, 100)

                self._update_options({
                    'e': "Exploit vulnerability",
                    'f': "Deploy countermeasures",
                    'd': "Document findings",
                    's': "Retreat and regroup",
                    'a': "Call for specialized support",
                })
                mission_phase = 2

            elif mission_phase == 2:
                print("\nActive engagement...")
                success = self._simulate_engagement(vulnerabilities, threat_level)
                threat_level = min(threat_level + 15, 100)

                if success:
                    self._update_options({
                        'e': "Extract data",
                        'f': "Plant backdoor",
                        'd': "Cover tracks",
                        's': "Complete mission",
                        'a': "Escalate privileges",
                    })
                else:
                    self._update_options({
                        'e': "Retry different approach",
                        'f': "Abort mission",
                        'd': "Call for backup",
                        's': "Deploy distraction",
                        'a': "Go silent",
                    })
                mission_phase = 3

            # Display current options
            self._display_options()

            # Simulate agent taking autonomous action if user doesn't respond
            time.sleep(3)
            if self.mission_running and mission_phase < 4:
                # Agent makes autonomous decision using Phixeo
                print(f"\n{agent_name} is taking initiative...")

                # Execute the appropriate Phixeo node based on phase
                if mission_phase == 1:
                    self.phixeo.nodes[vuln_node]["value"] = f"for asset in {discovered_assets}: find_vulnerabilities(asset)"
                elif mission_phase == 2:
                    self.phixeo.nodes[exploit_node]["value"] = f"if {vulnerabilities}: exploit({vulnerabilities[0]})"

                time.sleep(1)

                # Simulate changing conditions
                if mission_phase == 3:
                    # Mission completion phase
                    print(f"\n{agent_name} has completed the mission.")
                    self.mission_running = False
                else:
                    # Conditions change, options update
                    threat_level = min(threat_level + 5, 100)

                    # Options might change based on new developments
                    if threat_level > 70:
                        # Use sacred geometry for critical situations
                        self.phixeo.execute_sacred_geometry("metatron")

                        self._update_options({
                            'e': "Emergency extraction",
                            'f': "Deploy countermeasures",
                            'd': "Go dark",
                            's': "Call for backup",
                            'a': "Last resort measures",
                        })
                        print("\nALERT: Threat level critical! Options updated.")

    def _update_options(self, options):
        """Update available options."""
        self.current_options = options

    def _display_options(self):
        """Display current options to the user."""
        print("\nAVAILABLE ACTIONS:")
        for key, action in self.current_options.items():
            print(f"[{key}] {action}")
        print("\n[ESC] Abort mission")

    def handle_key_press(self, e):
        """Handle key press events during mission."""
        if not self.mission_running:
            return

        key = e.name
        if key in self.current_options:
            action = self.current_options[key]
            print(f"\nExecuting: {action}")
            # Simulate action execution
            time.sleep(1)
            print("Action completed.")

    def _simulate_discovery(self):
        """Simulate discovering network assets."""
        assets = ["Web Server", "Database", "File Storage", "Admin Console"]
        print("Discovering assets...")
        for asset in assets:
            time.sleep(0.5)
            print(f"- Found: {asset}")
        return assets

    def _simulate_vulnerabilities(self, assets):
        """Simulate finding vulnerabilities."""
        vulns = []
        for asset in assets:
            if asset == "Web Server":
                vulns.append("SQL Injection")
            elif asset == "Database":
                vulns.append("Weak Credentials")
            elif asset == "Admin Console":
                vulns.append("Session Hijacking")

        print("Scanning for vulnerabilities...")
        for vuln in vulns:
            time.sleep(0.7)
            print(f"- Vulnerability found: {vuln}")
        return vulns

    def _simulate_engagement(self, vulnerabilities, threat_level):
        """Simulate engaging with vulnerabilities."""
        success = len(vulnerabilities) > 0 and threat_level < 80

        print("Engaging target systems...")
        for vuln in vulnerabilities:
            time.sleep(0.8)
            result = "SUCCESS" if success else "FAILED"
            print(f"- Exploiting {vuln}: {result}")

        return success

    def run(self):
        while self.running:
            self.agent_selection_menu()

        print("\nShutting down CyberKaisenOS...")
        print("Goodbye!")

if __name__ == "__main__":
    try:
        interactive = InteractiveCyberKaisen()
        interactive.run()
    except KeyboardInterrupt:
        print("\n\nOperation interrupted. Shutting down CyberKaisenOS...")
        sys.exit(0)
