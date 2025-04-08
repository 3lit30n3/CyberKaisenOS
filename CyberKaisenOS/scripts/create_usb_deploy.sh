#!/bin/bash

# CyberKaisenOS USB Deployment Creator
# This script creates a USB deployment package for CyberKaisenOS

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check arguments
if [ "$#" -ne 1 ]; then
    echo -e "${RED}Usage: $0 [usb_path]${NC}"
    echo -e "${YELLOW}Example: $0 /media/usb${NC}"
    exit 1
fi

USB_PATH="$1"
echo -e "${PURPLE}CyberKaisenOS USB Deployment Creator${NC}"
echo -e "${BLUE}==================================${NC}"
echo -e "${YELLOW}USB Path: $USB_PATH${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: This script must be run as root${NC}"
    echo -e "${YELLOW}Please run: sudo $0 $USB_PATH${NC}"
    exit 1
fi

# Check if USB path exists
if [ ! -d "$USB_PATH" ]; then
    echo -e "${RED}Error: USB path does not exist${NC}"
    exit 1
fi

# Check if USB is writable
if [ ! -w "$USB_PATH" ]; then
    echo -e "${RED}Error: USB path is not writable${NC}"
    exit 1
fi

# Create directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p "$USB_PATH/CyberKaisenOS"
mkdir -p "$USB_PATH/CyberKaisenOS/kernel"
mkdir -p "$USB_PATH/CyberKaisenOS/service"
mkdir -p "$USB_PATH/CyberKaisenOS/scripts"

# Copy files
echo -e "${BLUE}Copying files...${NC}"
cp -r CyberKaisenOS/kernel/* "$USB_PATH/CyberKaisenOS/kernel/"
cp -r CyberKaisenOS/service/* "$USB_PATH/CyberKaisenOS/service/"
cp -r CyberKaisenOS/*.py "$USB_PATH/CyberKaisenOS/"

# Create summon script
echo -e "${BLUE}Creating summon script...${NC}"
cat > "$USB_PATH/summon.sh" << 'EOL'
#!/bin/bash

# CyberKaisenOS Summon Script
# This script "possesses" the host system by deploying CyberKaisenOS

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ASCII Art
echo -e "${PURPLE}"
cat << "EOF"
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗ █████╗ ██╗███████╗███████╗███╗   ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██╔══██╗██║██╔════╝██╔════╝████╗  ██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝█████╔╝ ███████║██║███████╗█████╗  ██╔██╗ ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔═██╗ ██╔══██║██║╚════██║██╔══╝  ██║╚██╗██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║  ██╗██║  ██║██║███████║███████╗██║ ╚████║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}Initiating possession ritual...${NC}"
sleep 1

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Error: This script must be run as root${NC}"
  echo -e "${YELLOW}Please run: sudo $0${NC}"
  exit 1
fi

# Detect USB drive path
USB_PATH=$(dirname "$(readlink -f "$0")")
echo -e "${BLUE}USB drive detected at: ${USB_PATH}${NC}"
sleep 1

# Check for required files
echo -e "${CYAN}Checking for required components...${NC}"
sleep 1

if [ ! -d "${USB_PATH}/CyberKaisenOS" ]; then
  echo -e "${RED}Error: Required components not found on USB drive${NC}"
  exit 1
fi

echo -e "${GREEN}All components found!${NC}"
sleep 1

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo -e "${BLUE}Creating temporary workspace at: ${TEMP_DIR}${NC}"
sleep 1

# Copy files to temporary directory
echo -e "${CYAN}Extracting components...${NC}"
cp -r "${USB_PATH}/CyberKaisenOS" "${TEMP_DIR}/"
sleep 1

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
if [ -f /etc/fedora-release ]; then
  # Fedora
  dnf -y install kernel-devel kernel-headers gcc make python3-devel python3-pip systemd-devel
elif [ -f /etc/debian_version ]; then
  # Debian/Ubuntu
  apt-get update
  apt-get -y install linux-headers-$(uname -r) gcc make python3-dev python3-pip
elif [ -f /etc/arch-release ]; then
  # Arch Linux
  pacman -Sy --noconfirm linux-headers gcc make python3 python-pip
else
  echo -e "${YELLOW}Unsupported distribution, installing minimal dependencies${NC}"
  which gcc || echo "Please install gcc"
  which make || echo "Please install make"
  which python3 || echo "Please install python3"
  which pip3 || echo "Please install pip3"
fi

# Build and install kernel module
echo -e "${YELLOW}Building Phixeo kernel module...${NC}"
cd "${TEMP_DIR}/CyberKaisenOS/kernel"
make clean && make
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to build kernel module${NC}"
  exit 1
fi

echo -e "${GREEN}Kernel module built successfully${NC}"
sleep 1

echo -e "${YELLOW}Installing Phixeo kernel module...${NC}"
make install
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to install kernel module${NC}"
  exit 1
fi

echo -e "${GREEN}Kernel module installed successfully${NC}"
sleep 1

# Create directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p /opt/cyberkaisen/phixeo
mkdir -p /etc/cyberkaisen

# Install Python package
echo -e "${YELLOW}Installing CyberKaisenOS Python package...${NC}"
cp -r "${TEMP_DIR}/CyberKaisenOS"/*.py /opt/cyberkaisen/
pip3 install -e /opt/cyberkaisen
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to install CyberKaisenOS${NC}"
  exit 1
fi

echo -e "${GREEN}CyberKaisenOS installed successfully${NC}"
sleep 1

# Install service
echo -e "${YELLOW}Installing service...${NC}"
cp "${TEMP_DIR}/CyberKaisenOS/service/cyberkaisen.service" /etc/systemd/system/
cp "${TEMP_DIR}/CyberKaisenOS/service/phixeo_service.py" /usr/local/bin/
chmod +x /usr/local/bin/phixeo_service.py

# Enable and start service
echo -e "${YELLOW}Enabling and starting CyberKaisenOS service...${NC}"
systemctl daemon-reload
systemctl enable cyberkaisen.service
systemctl start cyberkaisen.service

# Create autostart entry
echo -e "${YELLOW}Creating autostart entry...${NC}"
mkdir -p /etc/xdg/autostart/
cat > /etc/xdg/autostart/cyberkaisen.desktop << EOL
[Desktop Entry]
Type=Application
Name=CyberKaisenOS
Comment=Advanced Cybersecurity System
Exec=/usr/bin/python3 -c "from CyberKaisenOS import CyberKaisenOS; os = CyberKaisenOS(); os.unlimited_void()"
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
EOL

echo -e "${GREEN}Autostart entry created${NC}"
sleep 1

# Clean up
echo -e "${BLUE}Cleaning up...${NC}"
rm -rf "${TEMP_DIR}"
sleep 1

# Domain expansion
echo -e "${PURPLE}"
cat << "EOF"
██████╗  ██████╗ ███╗   ███╗ █████╗ ██╗███╗   ██╗    ███████╗██╗  ██╗██████╗  █████╗ ███╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗
██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██║████╗  ██║    ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║██╔═══██╗████╗  ██║
██║  ██║██║   ██║██╔████╔██║███████║██║██╔██╗ ██║    █████╗   ╚███╔╝ ██████╔╝███████║██╔██╗ ██║███████╗██║██║   ██║██╔██╗ ██║
██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║██║╚██╗██║    ██╔══╝   ██╔██╗ ██╔═══╝ ██╔══██║██║╚██╗██║╚════██║██║██║   ██║██║╚██╗██║
██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║ ╚████║    ███████╗██╔╝ ██╗██║     ██║  ██║██║ ╚████║███████║██║╚██████╔╝██║ ╚████║
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝    ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                                                              
██╗   ██╗███╗   ██╗██╗     ██╗███╗   ███╗██╗████████╗███████╗██████╗     ██╗   ██╗ ██████╗ ██╗██████╗                        
██║   ██║████╗  ██║██║     ██║████╗ ████║██║╚══██╔══╝██╔════╝██╔══██╗    ██║   ██║██╔═══██╗██║██╔══██╗                       
██║   ██║██╔██╗ ██║██║     ██║██╔████╔██║██║   ██║   █████╗  ██║  ██║    ██║   ██║██║   ██║██║██║  ██║                       
██║   ██║██║╚██╗██║██║     ██║██║╚██╔╝██║██║   ██║   ██╔══╝  ██║  ██║    ╚██╗ ██╔╝██║   ██║██║██║  ██║                       
╚██████╔╝██║ ╚████║███████╗██║██║ ╚═╝ ██║██║   ██║   ███████╗██████╔╝     ╚████╔╝ ╚██████╔╝██║██████╔╝                       
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚══════╝╚═════╝       ╚═══╝   ╚═════╝ ╚═╝╚═════╝                        
EOF
echo -e "${NC}"

echo -e "${GREEN}Possession complete! CyberKaisenOS is now integrated with this system.${NC}"
echo -e "${CYAN}Always-on defense is active. Domain Expansion: Unlimited Void.${NC}"
echo -e "${YELLOW}The system will be protected on next boot.${NC}"

exit 0
EOL

chmod +x "$USB_PATH/summon.sh"

# Create README
echo -e "${BLUE}Creating README...${NC}"
cat > "$USB_PATH/README.md" << 'EOL'
# CyberKaisenOS USB Deployment

This USB drive contains CyberKaisenOS, an advanced cybersecurity system that can "possess" any Linux-based system.

## Usage

1. Insert this USB drive into any Linux system
2. Open a terminal and navigate to the USB drive
3. Run the summon script with root privileges:

```bash
sudo ./summon.sh
```

4. The script will install CyberKaisenOS and integrate it with the host system
5. On next boot, CyberKaisenOS will be active with always-on defense

## Features

- **Always-On Defense**: Like Gojo's Infinity, CyberKaisenOS is always active
- **System Integration**: Fully integrates with the host operating system
- **Resource Optimization**: Minimizes resource consumption while maximizing effectiveness
- **Possession Capability**: Can "possess" any Linux-based system

## Requirements

- Linux-based operating system (tested on Fedora, Ubuntu, and Arch Linux)
- Root privileges
- Internet connection (for dependency installation)

## Warning

This software is powerful and should be used responsibly. Always obtain proper authorization before deploying on any system.
EOL

echo -e "${GREEN}USB deployment package created successfully!${NC}"
echo -e "${YELLOW}USB path: $USB_PATH${NC}"
echo -e "${BLUE}To deploy CyberKaisenOS on a system, insert the USB and run:${NC}"
echo -e "${PURPLE}sudo ./summon.sh${NC}"

exit 0
