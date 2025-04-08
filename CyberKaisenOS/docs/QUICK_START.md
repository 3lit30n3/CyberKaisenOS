# CyberKaisenOS Quick Start Guide

This guide will help you get started with CyberKaisenOS quickly.

## Installation

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/elite/cyberkaisen.git
cd cyberkaisen

# Run the installation script
sudo ./install_simple.sh
```

### Installation Options

```bash
# Install with possession capability
sudo ./install_simple.sh --with-possession

# Install without kernel module (user-mode only)
sudo ./install_simple.sh --no-kernel

# Install without always-on service
sudo ./install_simple.sh --no-service
```

### USB Installation

If you have a USB deployment package:

1. Insert the USB drive into your system
2. Navigate to the USB drive
3. Run the summon script:

```bash
sudo ./summon.sh
```

## Basic Usage

### Run CyberKaisenOS

```bash
# Run with default settings (Unlimited Void domain)
cyberkaisen

# Run with Malevolent Shrine domain
cyberkaisen -d shrine

# Run with Firewall Sanctuary domain
cyberkaisen -d sanctuary

# Run in interactive mode
cyberkaisen -i

# Possess another system (if installed with --with-possession)
cyberkaisen -p 192.168.1.100
```

### Check Defense Status

```bash
cat /proc/phixeo_status
```

### Change Defense Mode

```bash
# Unlimited Void (quantum mode)
echo 'mode=quantum' > /proc/phixeo_control

# Malevolent Shrine (fractal mode)
echo 'mode=fractal' > /proc/phixeo_control

# Firewall Sanctuary (geometric mode)
echo 'mode=geometric' > /proc/phixeo_control
```

## Agent Commands

### Gojo (Vulnerability Scanning)

```bash
python cyberkaisen_cli.py agent gojo scan
```

### Sukuna (Brute Force)

```bash
python cyberkaisen_cli.py agent sukuna social_brute_force --username target_user --platform instagram --wordlist wordlist.txt
```

### Toji (OSINT)

```bash
python cyberkaisen_cli.py agent toji gather_osint --target-name "John Smith" --generate-wordlist
```

### Maki (Exploit Disarming)

```bash
python cyberkaisen_cli.py agent maki disarm
```

## Interactive Mode

```bash
python interactive_cyberkaisen.py
```

## For More Information

See the full documentation in the `docs` directory.
