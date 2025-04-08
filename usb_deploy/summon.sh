#!/bin/bash

# CyberKaisenOS - Summon Script
# This script "possesses" a host system by deploying CyberKaisenOS

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

if [ ! -d "${USB_PATH}/phixeo_kernel" ] || [ ! -d "${USB_PATH}/phixeo_service" ]; then
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
cp -r "${USB_PATH}/phixeo_kernel" "${TEMP_DIR}/"
cp -r "${USB_PATH}/phixeo_service" "${TEMP_DIR}/"
cp -r "${USB_PATH}/CyberKaisenOS" "${TEMP_DIR}/"
sleep 1

# Build and install kernel module
echo -e "${YELLOW}Building Phixeo kernel module...${NC}"
cd "${TEMP_DIR}/phixeo_kernel"
make clean && make
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to build kernel module${NC}"
  exit 1
fi

echo -e "${GREEN}Kernel module built successfully${NC}"
sleep 1

echo -e "${YELLOW}Installing Phixeo kernel module...${NC}"
insmod phixeo_module.ko
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to install kernel module${NC}"
  exit 1
fi

echo -e "${GREEN}Kernel module installed successfully${NC}"
sleep 1

# Build and install service
echo -e "${YELLOW}Building Phixeo service...${NC}"
cd "${TEMP_DIR}/phixeo_service"
make clean && make
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to build service${NC}"
  exit 1
fi

echo -e "${GREEN}Service built successfully${NC}"
sleep 1

echo -e "${YELLOW}Installing Phixeo service...${NC}"
make install
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to install service${NC}"
  exit 1
fi

echo -e "${GREEN}Service installed successfully${NC}"
sleep 1

# Install CyberKaisenOS
echo -e "${YELLOW}Installing CyberKaisenOS...${NC}"
cd "${TEMP_DIR}/CyberKaisenOS"
pip install -e .
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to install CyberKaisenOS${NC}"
  exit 1
fi

echo -e "${GREEN}CyberKaisenOS installed successfully${NC}"
sleep 1

# Create autostart entry
echo -e "${YELLOW}Creating autostart entry...${NC}"
mkdir -p /etc/xdg/autostart/
cat > /etc/xdg/autostart/cyberkaisen.desktop << EOL
[Desktop Entry]
Type=Application
Name=CyberKaisenOS
Comment=Advanced Cybersecurity System
Exec=python -c "from CyberKaisenOS import CyberKaisenOS; os = CyberKaisenOS(); os.unlimited_void()"
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
