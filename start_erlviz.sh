#!/bin/bash
# ErlViz GUI Launcher Script for Linux/macOS
# This script activates the virtual environment and starts the ErlViz GUI
#
# Copyright (c) 2025 David Leon (leondavi)
# Licensed under the MIT License - see LICENSE file for details.

set -e  # Exit on any error

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}                    ErlViz GUI Launcher                    ${NC}"
echo -e "${BLUE}============================================================${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run the setup script first:${NC}"
    echo -e "  ${BLUE}python3 setup.py${NC}"
    exit 1
fi

# Check if virtual environment activation script exists
if [ ! -f "venv/bin/activate" ]; then
    echo -e "${RED}Error: Virtual environment activation script not found!${NC}"
    echo -e "${YELLOW}Please recreate the virtual environment:${NC}"
    echo -e "  ${BLUE}python3 setup.py${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment found${NC}"

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if ErlViz is properly installed
if ! python -c "import erlviz" 2>/dev/null; then
    echo -e "${RED}Error: ErlViz not properly installed!${NC}"
    echo -e "${YELLOW}Please run the setup script:${NC}"
    echo -e "  ${BLUE}python3 setup.py${NC}"
    exit 1
fi

echo -e "${GREEN}✓ ErlViz installation verified${NC}"

# Check for system dependencies
echo -e "${BLUE}Checking system dependencies...${NC}"

# Check for Graphviz
if ! command -v dot >/dev/null 2>&1; then
    echo -e "${YELLOW}Warning: Graphviz 'dot' command not found in PATH${NC}"
    echo -e "${YELLOW}Graph generation may not work properly.${NC}"
    echo -e "${YELLOW}To install Graphviz:${NC}"
    
    # Detect OS and provide installation instructions
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "  ${BLUE}Ubuntu/Debian: sudo apt-get install graphviz${NC}"
        echo -e "  ${BLUE}CentOS/RHEL:   sudo yum install graphviz${NC}"
        echo -e "  ${BLUE}Fedora:        sudo dnf install graphviz${NC}"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "  ${BLUE}macOS:         brew install graphviz${NC}"
    fi
    echo ""
else
    echo -e "${GREEN}✓ Graphviz found: $(dot -V 2>&1)${NC}"
fi

# Launch ErlViz GUI
echo -e "${BLUE}Starting ErlViz GUI...${NC}"
echo -e "${YELLOW}Note: The GUI window may take a few seconds to appear.${NC}"
echo -e "${YELLOW}To close ErlViz, use Ctrl+C in this terminal or close the GUI window.${NC}"
echo ""

# Start the GUI
python main.py

echo -e "${GREEN}ErlViz GUI closed.${NC}"
