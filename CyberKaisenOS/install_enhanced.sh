#!/bin/bash

# CyberKaisenOS Enhanced Installation Script
# This script installs CyberKaisenOS with always-on defense

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

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

echo -e "${PURPLE}CyberKaisenOS Installation${NC}"
echo -e "${BLUE}=======================${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Error: This script must be run as root${NC}"
  echo -e "${YELLOW}Please run: sudo $0${NC}"
  exit 1
fi

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

# Create directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p /opt/cyberkaisen/phixeo
mkdir -p /etc/cyberkaisen

# Build and install kernel module
echo -e "${BLUE}Building kernel module...${NC}"
cd CyberKaisenOS/kernel
make clean
make
make install

# Install Python package
echo -e "${BLUE}Installing CyberKaisenOS Python package...${NC}"
cp -r CyberKaisenOS/*.py /opt/cyberkaisen/
pip3 install -e /opt/cyberkaisen

# Install service
echo -e "${BLUE}Installing service...${NC}"
cp CyberKaisenOS/service/cyberkaisen.service /etc/systemd/system/
cp CyberKaisenOS/service/phixeo_service.py /usr/local/bin/
chmod +x /usr/local/bin/phixeo_service.py

# Install scripts
echo -e "${BLUE}Installing scripts...${NC}"
cp CyberKaisenOS/scripts/possess.sh /usr/local/bin/possess
cp CyberKaisenOS/scripts/create_usb_deploy.sh /usr/local/bin/create-usb-deploy
chmod +x /usr/local/bin/possess
chmod +x /usr/local/bin/create-usb-deploy

# Enable and start service
echo -e "${BLUE}Enabling and starting CyberKaisenOS service...${NC}"
systemctl daemon-reload
systemctl enable cyberkaisen.service
systemctl start cyberkaisen.service

# Create autostart entry for GUI
echo -e "${BLUE}Creating autostart entry...${NC}"
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

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${PURPLE}CyberKaisenOS is now integrated with your system.${NC}"
echo -e "${YELLOW}Always-on defense is active. Domain Expansion: Unlimited Void.${NC}"
echo -e ""
echo -e "${BLUE}Commands available:${NC}"
echo -e "  possess [target]         - Possess another system"
echo -e "  create-usb-deploy [path] - Create USB deployment package"
echo -e ""
echo -e "${YELLOW}To check the status of the defense system:${NC}"
echo -e "  cat /proc/phixeo_status"
echo -e ""
echo -e "${YELLOW}To change defense mode:${NC}"
echo -e "  echo 'mode=quantum' > /proc/phixeo_control    # Unlimited Void"
echo -e "  echo 'mode=fractal' > /proc/phixeo_control    # Malevolent Shrine"
echo -e "  echo 'mode=geometric' > /proc/phixeo_control  # Firewall Sanctuary"

exit 0
