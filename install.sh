#!/bin/bash

# Intelligent Eye for the Blind - Installation Script
# This script sets up the system on a Raspberry Pi

echo "Intelligent Eye for the Blind - Installation Script"
echo "=================================================="

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    echo "Warning: This script is designed for Raspberry Pi"
    echo "Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system packages
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required system packages
echo "Installing system dependencies..."
sudo apt install -y python3-pip python3-venv python3-dev
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y espeak espeak-data libespeak1 libespeak-dev
sudo apt install -y portaudio19-dev python3-pyaudio
sudo apt install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev
sudo apt install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt install -y libjasper-dev libqt4-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev
sudo apt install -y libv4l-dev libxvidcore-dev libx264-dev
sudo apt install -y libgtk2.0-dev libtbb2 libtbb-dev
sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt install -y libatlas-base-dev gfortran
sudo apt install -y git wget unzip

# Enable camera interface
echo "Enabling camera interface..."
sudo raspi-config nonint do_camera 0

# Enable I2C and SPI
echo "Enabling I2C and SPI interfaces..."
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python packages
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating project directories..."
mkdir -p models
mkdir -p logs
mkdir -p data/images
mkdir -p data/audio

# Download YOLO model
echo "Downloading YOLO model..."
cd models
wget -O yolov8n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
cd ..

# Set up GPIO permissions
echo "Setting up GPIO permissions..."
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER
sudo usermod -a -G spi $USER

# Create systemd service (optional)
echo "Creating systemd service..."
sudo tee /etc/systemd/system/intelligent-eye.service > /dev/null <<EOF
[Unit]
Description=Intelligent Eye for the Blind
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python intelligent_eye_system.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable service (optional)
echo "Enabling systemd service..."
sudo systemctl daemon-reload
sudo systemctl enable intelligent-eye.service

# Set up audio
echo "Configuring audio settings..."
# Set default audio output to 3.5mm jack
sudo amixer cset numid=3 1

# Create desktop shortcut
echo "Creating desktop shortcut..."
cat > ~/Desktop/intelligent-eye.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Intelligent Eye
Comment=Intelligent Eye for the Blind
Exec=$(pwd)/venv/bin/python $(pwd)/intelligent_eye_system.py
Icon=$(pwd)/download.png
Terminal=true
Categories=Accessibility;Education;
EOF

chmod +x ~/Desktop/intelligent-eye.desktop

# Set up autostart (optional)
echo "Setting up autostart..."
mkdir -p ~/.config/autostart
cp ~/Desktop/intelligent-eye.desktop ~/.config/autostart/

echo ""
echo "Installation completed successfully!"
echo ""
echo "To start the system:"
echo "  source venv/bin/activate"
echo "  python intelligent_eye_system.py"
echo ""
echo "To run tests:"
echo "  python test_system.py"
echo ""
echo "To enable autostart:"
echo "  sudo systemctl start intelligent-eye"
echo ""
echo "Please reboot your Raspberry Pi to ensure all changes take effect."
echo "After reboot, the system will start automatically."