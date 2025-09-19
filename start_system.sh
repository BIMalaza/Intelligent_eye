#!/bin/bash

# Intelligent Eye for the Blind - System Startup Script
# This script ensures the system runs in a virtual environment

echo "Intelligent Eye for the Blind - Starting System"
echo "=============================================="

# Check if we're in the correct directory
if [ ! -f "intelligent_eye_system.py" ]; then
    echo "Error: Please run this script from the Intelligent_eye directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Virtual environment created and packages installed"
else
    echo "Activating existing virtual environment..."
    source venv/bin/activate
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import cv2, numpy, torch, pyttsx3, RPi.GPIO" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing missing dependencies..."
    pip install -r requirements.txt
fi

# Check if YOLO model exists
if [ ! -f "models/yolov8n.pt" ]; then
    echo "Downloading YOLO model..."
    mkdir -p models
    cd models
    wget -O yolov8n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
    cd ..
fi

# Start the system
echo "Starting Intelligent Eye system..."
python3 intelligent_eye_system.py
