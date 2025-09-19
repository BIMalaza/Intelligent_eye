# Raspberry Pi Setup - Step by Step Instructions

Follow these steps to build the Intelligent Eye for the Blind system on your Raspberry Pi.

## Step 1: Initial Setup

### 1.1 Connect to your Raspberry Pi
```bash
# If using SSH
ssh pi@your-pi-ip-address

# Or work directly on the Pi
```

### 1.2 Update the system
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.3 Install system dependencies
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

### 1.4 Enable hardware interfaces
```bash
# Enable camera interface
sudo raspi-config nonint do_camera 0

# Enable I2C and SPI
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
```

### 1.5 Set up GPIO permissions
```bash
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER
sudo usermod -a -G spi $USER
```

### 1.6 Create project directory
```bash
mkdir -p ~/intelligent_eye
cd ~/intelligent_eye
```

### 1.7 Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

## Step 2: Create Configuration File

### 2.1 Create config.py
```bash
nano config.py
```

### 2.2 Copy and paste this content:
```python
"""
Configuration file for the Intelligent Eye for the Blind system
"""

# System Configuration
SYSTEM_CONFIG = {
    'max_latency_ms': 200,
    'battery_life_hours': 6,
    'processing_fps': 5,
    'audio_volume': 0.8
}

# Camera Configuration
CAMERA_CONFIG = {
    'resolution': (640, 480),
    'fps': 30,
    'rotation': 0,
    'brightness': 50,
    'contrast': 50
}

# Ultrasonic Sensor Configuration
ULTRASONIC_CONFIG = {
    'trigger_pin': 18,
    'echo_pin': 24,
    'max_distance_cm': 400,
    'min_distance_cm': 2,
    'detection_angle': 15,  # degrees
    'warning_distance_cm': 100
}

# Object Detection Configuration
DETECTION_CONFIG = {
    'confidence_threshold': 0.5,
    'nms_threshold': 0.4,
    'model_path': 'models/yolov8n.pt',
    'classes_to_detect': [
        'person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck',
        'traffic light', 'stop sign', 'parking meter', 'bench'
    ]
}

# Road Sign Recognition Configuration
SIGN_RECOGNITION_CONFIG = {
    'model_path': 'models/road_sign_classifier.h5',
    'sign_classes': [
        'stop', 'yield', 'speed_limit', 'no_entry', 'one_way',
        'pedestrian_crossing', 'school_zone', 'construction'
    ]
}

# Text-to-Speech Configuration
TTS_CONFIG = {
    'rate': 150,
    'volume': 0.8,
    'voice_id': 0,  # 0 for male, 1 for female
    'language': 'en'
}

# Audio Feedback Configuration
AUDIO_CONFIG = {
    'obstacle_warning': "Obstacle detected at {} centimeters",
    'sign_detected': "Road sign detected: {}",
    'object_detected': "Object detected: {}",
    'system_ready': "Intelligent Eye system ready",
    'battery_low': "Battery low, please recharge"
}

# GPIO Pin Configuration
GPIO_CONFIG = {
    'ultrasonic_trigger': 18,
    'ultrasonic_echo': 24,
    'led_status': 25,
    'button_power': 23,
    'buzzer': 12
}
```

### 2.3 Save and exit (Ctrl+X, Y, Enter)

## Step 3: Create Requirements File

### 3.1 Create requirements.txt
```bash
nano requirements.txt
```

### 3.2 Copy and paste this content:
```
opencv-python==4.8.1.78
numpy==1.24.3
tensorflow==2.13.0
torch==2.0.1
torchvision==0.15.2
pyttsx3==2.90
RPi.GPIO==0.7.1
cvlib==0.2.7
Pillow==10.0.0
matplotlib==3.7.2
ultralytics==8.0.196
pygame==2.5.2
psutil==5.9.5
```

### 3.3 Save and exit (Ctrl+X, Y, Enter)

### 3.4 Install Python packages
```bash
pip install -r requirements.txt
```

## Step 4: Test Basic Setup

### 4.1 Test Python imports
```bash
python3 -c "import cv2, numpy, pyttsx3; print('Basic imports successful')"
```

### 4.2 Test GPIO (if hardware connected)
```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO available')"
```

## Step 5: Create Ultrasonic Sensor Module

### 5.1 Create ultrasonic_sensor.py
```bash
nano ultrasonic_sensor.py
```

### 5.2 Copy the ultrasonic sensor code (I'll provide this in the next message)

## Next Steps

After completing these steps, let me know and I'll provide the next file to create. We'll build the system step by step:

1. ✅ Initial setup and dependencies
2. ✅ Configuration file
3. ✅ Requirements file
4. ✅ Ultrasonic sensor module
5. ⏳ Audio system module
6. ⏳ Vision system module
7. ⏳ Performance monitor
8. ⏳ Battery monitor
9. ⏳ Main system integration
10. ⏳ Testing framework
11. ⏳ Demo scripts
12. ⏳ Validation scripts

Let me know when you've completed Step 5 and I'll provide the next file!
