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

# Check arguments
if [ "$#" -ne 1 ]; then
    echo -e "${RED}Usage: $0 [target_ip]${NC}"
    exit 1
fi

TARGET="$1"
echo -e "${PURPLE}CyberKaisenOS Possession${NC}"
echo -e "${BLUE}=======================${NC}"
echo -e "${YELLOW}Target: $TARGET${NC}"

# Check SSH connection
echo -e "${BLUE}Testing connection...${NC}"
ssh -o ConnectTimeout=5 -o BatchMode=yes root@$TARGET exit &>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Cannot connect to $TARGET as root${NC}"
    echo -e "${YELLOW}Make sure SSH is enabled and root login is allowed${NC}"
    exit 1
fi

# Copy files
echo -e "${BLUE}Copying files to target...${NC}"
scp -r CyberKaisenOS.py phixeo_api.py cybersecurity_kaisen.py root@$TARGET:/opt/
scp phixeo_module.c Makefile root@$TARGET:/opt/
scp install.sh root@$TARGET:/opt/

# Execute installation
echo -e "${BLUE}Executing installation on target...${NC}"
ssh root@$TARGET "cd /opt && bash install.sh"

echo -e "${GREEN}Possession complete!${NC}"
echo -e "${PURPLE}CyberKaisenOS is now integrated with $TARGET${NC}"
echo -e "${YELLOW}Always-on defense is active. Domain Expansion: Unlimited Void.${NC}"

exit 0
