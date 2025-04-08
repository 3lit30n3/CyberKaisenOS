#!/bin/bash

# CyberKaisenOS Possession Script
# This script "possesses" a target system with CyberKaisenOS

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

# Check arguments
if [ "$#" -ne 1 ]; then
    echo -e "${RED}Usage: $0 [target_ip]${NC}"
    exit 1
fi

TARGET="$1"
echo -e "${PURPLE}System Possession${NC}"
echo -e "${BLUE}=======================${NC}"
echo -e "${YELLOW}Target: $TARGET${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: This script must be run as root${NC}"
    echo -e "${YELLOW}Please run: sudo $0 $TARGET${NC}"
    exit 1
fi

# Check SSH connection
echo -e "${BLUE}Testing connection...${NC}"
ssh -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no root@$TARGET exit &>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Cannot connect to $TARGET as root${NC}"
    echo -e "${YELLOW}Make sure SSH is enabled and root login is allowed${NC}"
    exit 1
fi

# Create temporary package
echo -e "${BLUE}Creating possession package...${NC}"
TEMP_DIR=$(mktemp -d)
mkdir -p $TEMP_DIR/CyberKaisenOS/{kernel,service,scripts}

# Copy files
cp -r CyberKaisenOS/kernel/* $TEMP_DIR/CyberKaisenOS/kernel/
cp -r CyberKaisenOS/service/* $TEMP_DIR/CyberKaisenOS/service/
cp -r CyberKaisenOS/*.py $TEMP_DIR/CyberKaisenOS/

# Create install script
cat > $TEMP_DIR/install.sh << 'EOL'
#!/bin/bash

# CyberKaisenOS Installation Script
# This script installs CyberKaisenOS with always-on defense

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${PURPLE}CyberKaisenOS Installation${NC}"
echo -e "${BLUE}=======================${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${YELLOW}This script must be run as root${NC}"
  echo -e "Please run: sudo $0"
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

# Enable and start service
echo -e "${BLUE}Enabling and starting CyberKaisenOS service...${NC}"
systemctl daemon-reload
systemctl enable cyberkaisen.service
systemctl start cyberkaisen.service

# Create autostart entry for GUI
echo -e "${BLUE}Creating autostart entry...${NC}"
mkdir -p /etc/xdg/autostart/
cat > /etc/xdg/autostart/cyberkaisen.desktop << EOF
[Desktop Entry]
Type=Application
Name=CyberKaisenOS
Comment=Advanced Cybersecurity System
Exec=/usr/bin/python3 -c "from CyberKaisenOS import CyberKaisenOS; os = CyberKaisenOS(); os.unlimited_void()"
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
EOF

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${PURPLE}CyberKaisenOS is now integrated with your system.${NC}"
echo -e "${YELLOW}Always-on defense is active. Domain Expansion: Unlimited Void.${NC}"

exit 0
EOL

chmod +x $TEMP_DIR/install.sh

# Copy files to target
echo -e "${BLUE}Copying files to target...${NC}"
scp -r $TEMP_DIR/* root@$TARGET:/tmp/

# Execute installation
echo -e "${BLUE}Executing installation on target...${NC}"
ssh -o StrictHostKeyChecking=no root@$TARGET "cd /tmp && bash install.sh"

# Clean up
echo -e "${BLUE}Cleaning up...${NC}"
rm -rf $TEMP_DIR

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

echo -e "${GREEN}Possession complete! CyberKaisenOS is now integrated with $TARGET.${NC}"
echo -e "${CYAN}Always-on defense is active. Domain Expansion: Unlimited Void.${NC}"

exit 0
