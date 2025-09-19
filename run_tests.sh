#!/bin/bash

# Intelligent Eye for the Blind - Test Runner Script
# This script runs tests in a virtual environment

echo "Intelligent Eye for the Blind - Running Tests"
echo "============================================"

# Check if we're in the correct directory
if [ ! -f "test_system.py" ]; then
    echo "Error: Please run this script from the Intelligent_eye directory"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run install.sh first"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import cv2, numpy, torch, pyttsx3" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing missing dependencies..."
    pip install -r requirements.txt
fi

# Run tests based on argument
if [ $# -eq 0 ]; then
    echo "Running all tests..."
    python3 test_system.py
else
    echo "Running $1 test..."
    python3 test_system.py $1
fi
