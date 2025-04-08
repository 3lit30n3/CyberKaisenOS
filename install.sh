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
dnf -y install kernel-devel kernel-headers gcc make python3-devel python3-pip systemd-devel

# Create directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p /opt/cyberkaisen/phixeo
mkdir -p /etc/cyberkaisen

# Install Python package
echo -e "${BLUE}Installing CyberKaisenOS Python package...${NC}"
pip install -e .

# Create systemd service
echo -e "${BLUE}Creating systemd service...${NC}"
cat > /etc/systemd/system/cyberkaisen.service << EOL
[Unit]
Description=CyberKaisenOS Always-On Defense
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/usr/bin/python3 -c "from CyberKaisenOS import CyberKaisenOS; os = CyberKaisenOS(); os.unlimited_void()"

[Install]
WantedBy=multi-user.target
EOL

# Create possession script
echo -e "${BLUE}Creating possession script...${NC}"
cat > /usr/local/bin/possess << EOL
#!/bin/bash
# CyberKaisenOS Possession Script
# Usage: possess [target]

if [ "\$#" -ne 1 ]; then
    echo "Usage: possess [target]"
    exit 1
fi

TARGET="\$1"
echo "Initiating possession of \$TARGET..."

# Copy necessary files
scp -r /opt/cyberkaisen root@\$TARGET:/opt/
scp /etc/systemd/system/cyberkaisen.service root@\$TARGET:/etc/systemd/system/

# Execute remote commands
ssh root@\$TARGET "systemctl daemon-reload && systemctl enable cyberkaisen.service && systemctl start cyberkaisen.service"

echo "Possession complete. CyberKaisenOS is now active on \$TARGET."
EOL

chmod +x /usr/local/bin/possess

# Create USB deployment script
echo -e "${BLUE}Creating USB deployment script...${NC}"
cat > /usr/local/bin/create-usb-deploy << EOL
#!/bin/bash
# Create USB deployment package
# Usage: create-usb-deploy [usb_path]

if [ "\$#" -ne 1 ]; then
    echo "Usage: create-usb-deploy [usb_path]"
    exit 1
fi

USB_PATH="\$1"
echo "Creating deployment package on \$USB_PATH..."

# Create directories
mkdir -p "\$USB_PATH/cyberkaisen"

# Copy files
cp -r /opt/cyberkaisen "\$USB_PATH/"
cp /etc/systemd/system/cyberkaisen.service "\$USB_PATH/cyberkaisen/"
cp /usr/local/bin/possess "\$USB_PATH/cyberkaisen/summon.sh"
chmod +x "\$USB_PATH/cyberkaisen/summon.sh"

echo "USB deployment package created. Insert this USB into any Linux system and run summon.sh to possess it."
EOL

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

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${PURPLE}CyberKaisenOS is now integrated with your system.${NC}"
echo -e "${YELLOW}Always-on defense is active. Domain Expansion: Unlimited Void.${NC}"
echo -e ""
echo -e "${BLUE}Commands available:${NC}"
echo -e "  possess [target]         - Possess another system"
echo -e "  create-usb-deploy [path] - Create USB deployment package"

exit 0
