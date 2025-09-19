# Raspberry Pi Setup Guide - Step by Step

This guide will help you build the Intelligent Eye for the Blind system file by file on your Raspberry Pi.

## Prerequisites

Make sure your Raspberry Pi is set up with:
- Raspberry Pi OS (latest version)
- Internet connection
- SSH access (if working remotely)

## Step 1: Initial Setup and Dependencies

### 1.1 Update the system
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Install system dependencies
```bash
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
```

### 1.3 Enable hardware interfaces
```bash
# Enable camera interface
sudo raspi-config nonint do_camera 0

# Enable I2C and SPI
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
```

### 1.4 Set up GPIO permissions
```bash
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER
sudo usermod -a -G spi $USER
```

### 1.5 Create project directory
```bash
mkdir -p ~/intelligent_eye
cd ~/intelligent_eye
```

### 1.6 Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

## Step 2: Create Configuration File

Create `config.py`:
```bash
nano config.py
```

Copy and paste the configuration content (I'll provide this in the next step).

## Step 3: Create Core System Files

We'll create each file one by one:

1. `config.py` - System configuration
2. `ultrasonic_sensor.py` - Ultrasonic sensor module
3. `audio_system.py` - Text-to-speech system
4. `vision_system.py` - Computer vision module
5. `performance_monitor.py` - Performance tracking
6. `battery_monitor.py` - Battery management
7. `intelligent_eye_system.py` - Main system integration
8. `test_system.py` - Testing framework
9. `demo_presentation.py` - Demonstration scripts
10. `proposal_validation.py` - Requirements validation

## Step 4: Install Python Dependencies

Create `requirements.txt` and install packages:
```bash
pip install -r requirements.txt
```

## Step 5: Download YOLO Model

```bash
mkdir -p models
cd models
wget -O yolov8n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
cd ..
```

## Step 6: Test Each Component

Test each component individually to ensure everything works.

## Step 7: Run the Complete System

Once all components are working, run the integrated system.

---

Let's start with Step 2. Would you like me to provide the content for `config.py` first?
