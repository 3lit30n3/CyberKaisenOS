# CyberKaisenOS Documentation

CyberKaisenOS is an advanced cybersecurity system that combines offensive and defensive capabilities to provide comprehensive security solutions. Inspired by the anime "Jujutsu Kaisen," the system uses domain expansions and cursed techniques as metaphors for powerful cybersecurity tools and techniques.

## Table of Contents

1. [Installation](#installation)
2. [System Integration](#system-integration)
3. [Always-On Defense](#always-on-defense)
4. [System Possession](#system-possession)
5. [Domain Expansions](#domain-expansions)
6. [Phixeo Language](#phixeo-language)
7. [Agents](#agents)
8. [Command Reference](#command-reference)
9. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Linux-based operating system (tested on Fedora, Ubuntu, and Arch Linux)
- Root privileges
- Internet connection (for dependency installation)

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/elite/cyberkaisen.git
cd cyberkaisen

# Run the installation script
sudo ./install_enhanced.sh
```

### USB Installation

If you have a USB deployment package:

1. Insert the USB drive into your system
2. Navigate to the USB drive
3. Run the summon script:

```bash
sudo ./summon.sh
```

## System Integration

CyberKaisenOS integrates with your operating system at multiple levels:

1. **Kernel Level**: The Phixeo kernel module provides low-level system integration for always-on protection
2. **Service Level**: The systemd service ensures CyberKaisenOS is always running
3. **User Level**: The autostart entry launches the GUI interface at login

## Always-On Defense

Like Gojo's Infinity technique in Jujutsu Kaisen, CyberKaisenOS provides always-on defense that is active even when the interactive interface is not running.

### Defense Modes

CyberKaisenOS supports three defense modes:

1. **Quantum Mode** (Unlimited Void): Probabilistic packet inspection with quantum-inspired algorithms
2. **Fractal Mode** (Malevolent Shrine): Recursive pattern matching for threat detection
3. **Geometric Mode** (Firewall Sanctuary): Structural packet analysis based on sacred geometry

### Defense Levels

Five defense levels are available:

1. **Low**: Minimal protection, just logging
2. **Medium**: Standard protection, blocks repeated threats
3. **High**: Enhanced protection, blocks all suspicious activity
4. **Maximum**: Maximum protection, aggressive blocking and counter-measures
5. **Adaptive**: Self-adjusting protection based on threat activity

### Checking Defense Status

```bash
cat /proc/phixeo_status
```

### Changing Defense Mode

```bash
# Unlimited Void (quantum mode)
echo 'mode=quantum' > /proc/phixeo_control

# Malevolent Shrine (fractal mode)
echo 'mode=fractal' > /proc/phixeo_control

# Firewall Sanctuary (geometric mode)
echo 'mode=geometric' > /proc/phixeo_control
```

### Changing Defense Level

```bash
# Set to low level
echo 'defense=low' > /proc/phixeo_control

# Set to medium level
echo 'defense=medium' > /proc/phixeo_control

# Set to high level
echo 'defense=high' > /proc/phixeo_control

# Set to maximum level
echo 'defense=maximum' > /proc/phixeo_control

# Set to adaptive level
echo 'defense=adaptive' > /proc/phixeo_control
```

## System Possession

Like Sukuna's ability to possess vessels in Jujutsu Kaisen, CyberKaisenOS can "possess" other systems.

### Possessing a System via SSH

```bash
possess target_ip
```

This will deploy CyberKaisenOS on the target system and activate always-on defense.

### Creating a USB Deployment Package

```bash
create-usb-deploy /path/to/usb
```

This creates a USB deployment package that can be used to possess any Linux-based system.

## Domain Expansions

Domain Expansions are powerful security techniques that transform the digital environment.

### Unlimited Void

```bash
python -c "from CyberKaisenOS import CyberKaisenOS; os = CyberKaisenOS(); os.unlimited_void()"
```

Creates an impenetrable security perimeter with quantum-inspired defense.

### Malevolent Shrine

```bash
python -c "from CyberKaisenOS import CyberKaisenOS; os = CyberKaisenOS(); os.malevolent_shrine()"
```

Deploys aggressive counter-attack capabilities with fractal pattern matching.

### Firewall Sanctuary

```bash
python -c "from CyberKaisenOS import CyberKaisenOS; os = CyberKaisenOS(); os.firewall_sanctuary()"
```

Establishes advanced threat filtering with geometric defense structures.

## Phixeo Language

Phixeo is a multi-paradigm computational framework that transcends traditional programming approaches. It combines quantum computing principles, fractal mathematics, and sacred geometry to create security structures that are fundamentally superior to conventional systems.

### Execution Modes

- **Quantum Mode**: Security states that exist in superposition, making them impossible to observe without detection
- **Fractal Mode**: Recursive vulnerability discovery that scales with complexity
- **Geometric Mode**: Multi-dimensional security layers based on sacred geometry

### Technical Details

The Phixeo Language operates across multiple execution modes, each with unique security implications:

#### Quantum Mode
- Implements quantum circuit principles for security operations
- Creates entangled security states that cannot be observed without detection
- Uses superposition to maintain multiple security configurations simultaneously
- Example: `Unlimited Void` domain expansion uses quantum entanglement to create impenetrable security perimeters

#### Fractal Mode
- Employs recursive patterns for vulnerability discovery and exploit development
- Scales attack and defense patterns across different complexity levels
- Self-similar structures that adapt to threat complexity
- Example: `Malevolent Shrine` uses fractal attack patterns that scale with threat intensity

#### Geometric Mode
- Utilizes sacred geometry patterns for optimal defense structures
- Creates multi-dimensional security layers with cross-dimensional mapping
- Implements non-orientable topologies (Klein bottle, tesseract) for advanced packet inspection
- Example: `Firewall Sanctuary` uses sacred geometry to optimize defense coverage

#### Dimensional Layers
- Creates n-dimensional security zones with configurable properties
- Maps between dimensions to protect across multiple attack vectors
- Enables cross-dimensional security operations
- Example: `Chimera Shadow Garden` uses dimensional mapping for traffic redirection

## Agents

CyberKaisenOS includes specialized agents with unique capabilities:

### Gojo

Specializes in vulnerability scanning and defense.

```bash
python cyberkaisen_cli.py agent gojo scan
```

### Sukuna

Specializes in brute force attacks and offensive capabilities.

```bash
python cyberkaisen_cli.py agent sukuna social_brute_force --username target_user --platform instagram --wordlist wordlist.txt
```

### Toji

Specializes in OSINT and stealth operations.

```bash
python cyberkaisen_cli.py agent toji gather_osint --target-name "John Smith" --generate-wordlist
```

### Maki

Specializes in exploit disarming and defense.

```bash
python cyberkaisen_cli.py agent maki disarm
```

## Command Reference

### CLI Commands

```bash
# Boot the system
python cyberkaisen_cli.py boot

# Execute a domain expansion
python cyberkaisen_cli.py domain void

# Use an agent
python cyberkaisen_cli.py agent gojo scan

# Social media brute force
python cyberkaisen_cli.py agent sukuna social_brute_force --username target_user --platform instagram --wordlist wordlist.txt

# OSINT gathering
python cyberkaisen_cli.py agent toji gather_osint --target-name "John Smith" --generate-wordlist
```

### System Commands

```bash
# Possess another system
possess target_ip

# Create USB deployment package
create-usb-deploy /path/to/usb

# Check defense status
cat /proc/phixeo_status

# Change defense mode
echo 'mode=quantum' > /proc/phixeo_control

# Change defense level
echo 'defense=maximum' > /proc/phixeo_control

# Clear suspicious IP list
echo 'clear_suspicious' > /proc/phixeo_control
```

## Troubleshooting

### Kernel Module Issues

If the kernel module fails to load:

```bash
# Check if module is loaded
lsmod | grep phixeo

# Try to load the module manually
sudo modprobe phixeo_module

# Check kernel logs for errors
dmesg | grep phixeo
```

### Service Issues

If the service fails to start:

```bash
# Check service status
systemctl status cyberkaisen

# View service logs
journalctl -u cyberkaisen

# Restart the service
systemctl restart cyberkaisen
```

### Permission Issues

If you encounter permission issues:

```bash
# Make sure you're running as root
sudo -i

# Check file permissions
ls -la /usr/local/bin/possess
ls -la /usr/local/bin/create-usb-deploy

# Fix permissions if needed
chmod +x /usr/local/bin/possess
chmod +x /usr/local/bin/create-usb-deploy
```

## Co-Developers

CyberKaisenOS was developed by:
- Elite (Lead Developer)
- Claude (AI Assistant)

## License

This project is for educational and research purposes only. Use responsibly.
