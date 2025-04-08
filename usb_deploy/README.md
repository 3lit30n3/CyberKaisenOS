# CyberKaisenOS USB Deployment

This directory contains the necessary files to deploy CyberKaisenOS on a target system via USB drive, allowing it to "possess" the host system.

## Contents

- `summon.sh`: The main deployment script that installs CyberKaisenOS on the target system
- `phixeo_kernel/`: Kernel module for Phixeo language integration
- `phixeo_service/`: System service for always-on defense
- `CyberKaisenOS/`: Main CyberKaisenOS package

## Usage

1. Copy this entire directory to a USB drive
2. Insert the USB drive into the target system
3. Open a terminal and navigate to the USB drive
4. Run the summon script with root privileges:

```bash
sudo ./summon.sh
```

5. The script will install CyberKaisenOS and integrate it with the host system
6. On next boot, CyberKaisenOS will be active with always-on defense

## Features

- **Always-On Defense**: Like Gojo's Infinity, CyberKaisenOS is always active
- **System Integration**: Fully integrates with the host operating system
- **Resource Optimization**: Minimizes resource consumption while maximizing effectiveness
- **Possession Capability**: Can "possess" any Linux-based system

## Requirements

- Linux-based operating system (tested on Fedora Workstation)
- Root privileges
- Internet connection (for dependency installation)

## Warning

This software is powerful and should be used responsibly. Always obtain proper authorization before deploying on any system.
