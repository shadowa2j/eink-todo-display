#!/bin/bash
# Setup script for E-Ink To-Do List Display

echo "========================================"
echo "E-Ink To-Do List Setup"
echo "========================================"
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "WARNING: This doesn't appear to be a Raspberry Pi!"
    echo "This script is designed for Raspberry Pi OS."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "Step 1: Updating system..."
sudo apt-get update

# Install required system packages
echo "Step 2: Installing system dependencies..."
sudo apt-get install -y python3-pip python3-pil python3-numpy git

# Enable SPI interface (required for e-ink display)
echo "Step 3: Enabling SPI interface..."
sudo raspi-config nonint do_spi 0

# Install Python dependencies
echo "Step 4: Installing Python packages..."
pip3 install -r requirements.txt --break-system-packages

# Download Waveshare e-Paper library
echo "Step 5: Downloading Waveshare e-Paper library..."
if [ ! -d "e-Paper" ]; then
    git clone https://github.com/waveshare/e-Paper.git
    if [ $? -eq 0 ]; then
        echo "Copying library files..."
        cp -r e-Paper/RaspberryPi_JetsonNano/python/lib .
        cp -r e-Paper/RaspberryPi_JetsonNano/python/pic .
    else
        echo "ERROR: Failed to clone e-Paper library"
        exit 1
    fi
else
    echo "e-Paper library already exists, skipping download"
fi

# Make the script executable
chmod +x todo_display.py

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "IMPORTANT: You must REBOOT your Raspberry Pi for SPI to work!"
echo ""
echo "Next steps:"
echo "1. REBOOT: sudo reboot"
echo "2. Set up Google Sheets API credentials (see SETUP_INSTRUCTIONS.md)"
echo "3. Create your Google Sheet with columns: Task | Status"
echo "4. Copy credentials.json to this folder"
echo "5. Run: python3 todo_display.py"
echo ""
