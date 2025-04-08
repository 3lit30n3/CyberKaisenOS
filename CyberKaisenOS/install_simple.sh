#!/bin/bash

# CyberKaisenOS Simple Installation Script
# This script installs CyberKaisenOS with optional possession capability

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

# Parse command line arguments
INSTALL_KERNEL=true
INSTALL_POSSESSION=false
INSTALL_SERVICE=true

function show_help {
    echo -e "${BLUE}Usage: $0 [OPTIONS]${NC}"
    echo -e ""
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  --no-kernel           Don't install kernel module (user-mode only)"
    echo -e "  --with-possession     Install system possession capability"
    echo -e "  --no-service          Don't install always-on service"
    echo -e "  -h, --help            Show this help message"
    echo -e ""
    echo -e "${YELLOW}Examples:${NC}"
    echo -e "  $0                     # Standard installation"
    echo -e "  $0 --with-possession   # Install with possession capability"
    echo -e "  $0 --no-kernel         # Install without kernel module"
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-kernel)
            INSTALL_KERNEL=false
            shift
            ;;
        --with-possession)
            INSTALL_POSSESSION=true
            shift
            ;;
        --no-service)
            INSTALL_SERVICE=false
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            ;;
    esac
done

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

# Build and install kernel module if requested
if $INSTALL_KERNEL; then
    echo -e "${BLUE}Building kernel module...${NC}"
    cd CyberKaisenOS/kernel
    make clean
    make
    make install
    echo -e "${GREEN}Kernel module installed successfully${NC}"
else
    echo -e "${YELLOW}Skipping kernel module installation${NC}"
fi

# Install Python package
echo -e "${BLUE}Installing CyberKaisenOS Python package...${NC}"
cp -r CyberKaisenOS/*.py /opt/cyberkaisen/
pip3 install -e /opt/cyberkaisen

# Install service if requested
if $INSTALL_SERVICE; then
    echo -e "${BLUE}Installing service...${NC}"
    cp CyberKaisenOS/service/cyberkaisen.service /etc/systemd/system/
    cp CyberKaisenOS/service/phixeo_service.py /usr/local/bin/
    chmod +x /usr/local/bin/phixeo_service.py
    
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
Exec=/usr/bin/cyberkaisen
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
EOL
else
    echo -e "${YELLOW}Skipping service installation${NC}"
fi

# Install possession scripts if requested
if $INSTALL_POSSESSION; then
    echo -e "${BLUE}Installing possession capability...${NC}"
    cp CyberKaisenOS/scripts/possess.sh /usr/local/bin/possess
    cp CyberKaisenOS/scripts/create_usb_deploy.sh /usr/local/bin/create-usb-deploy
    chmod +x /usr/local/bin/possess
    chmod +x /usr/local/bin/create-usb-deploy
    echo -e "${GREEN}Possession capability installed${NC}"
else
    echo -e "${YELLOW}Skipping possession capability installation${NC}"
fi

# Install simple launcher
echo -e "${BLUE}Installing CyberKaisenOS launcher...${NC}"
cp CyberKaisenOS/cyberkaisen /usr/bin/
chmod +x /usr/bin/cyberkaisen

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
echo -e "${BLUE}To run CyberKaisenOS, simply type:${NC}"
echo -e "  ${PURPLE}cyberkaisen${NC}"
echo -e ""
echo -e "${BLUE}Additional options:${NC}"
echo -e "  ${PURPLE}cyberkaisen -d shrine${NC}           # Run with Malevolent Shrine domain"
echo -e "  ${PURPLE}cyberkaisen -i${NC}                  # Run in interactive mode"

if $INSTALL_POSSESSION; then
    echo -e "  ${PURPLE}cyberkaisen -p 192.168.1.100${NC}    # Possess another system"
fi

echo -e ""
echo -e "${YELLOW}To check the status of the defense system:${NC}"
echo -e "  cat /proc/phixeo_status"

exit 0
