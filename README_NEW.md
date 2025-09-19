# Intelligent Eye for the Blind

**Tshwane University of Technology**  
**Advanced Diploma in Computer Systems Engineering**  
**Student: Katlego Phalane (213642871)**  
**Course: ADYE20 - Project Design Technical Design**

A modular wearable assistive system that integrates ultrasonic obstacle detection and visual recognition with real-time audio conversion to enhance environmental awareness, autonomy, and safety for visually impaired individuals.

## System Overview

The Intelligent Eye for the Blind consists of two main components:

1. **Smart Hat**: Houses a Raspberry Pi and Pi Camera for real-time road sign and object recognition using CNNs and OCR
2. **Smart Belt**: Equipped with ultrasonic sensors for continuous obstacle detection and immediate audio warnings

## Features

- **Real-time Object Detection**: Uses YOLO for detecting pedestrians, vehicles, and other objects
- **Road Sign Recognition**: Identifies and announces road signs with distance estimation
- **Ultrasonic Obstacle Detection**: Continuous monitoring with immediate audio warnings
- **Text-to-Speech**: Converts all detections into clear audio feedback
- **Modular Design**: Hat and belt can operate independently or together
- **Offline Processing**: All computations performed locally on Raspberry Pi
- **Low Latency**: Target latency under 200ms
- **Privacy Preserving**: No cloud dependency or data transmission
- **Performance Monitoring**: Real-time metrics and validation
- **Battery Management**: Intelligent power saving and monitoring

## System Requirements

### Hardware
- Raspberry Pi 4 (4GB RAM recommended)
- Pi Camera Module v2
- HC-SR04 Ultrasonic Sensors
- USB Type-C Power Bank (4-8 hours capacity)
- MicroSD Card (32GB+)
- Speaker/Headphones for audio output

### Software
- Raspberry Pi OS
- Python 3.8+
- OpenCV
- TensorFlow/PyTorch
- YOLO (Ultralytics)

## Installation

### Quick Setup (Raspberry Pi)

1. **Clone the repository**:
   ```bash
   # Using HTTPS (recommended)
   git clone https://github.com/BIMalaza/Intelligent_eye.git
   cd Intelligent_eye
   
   # Or using SSH (if you have SSH keys set up)
   git clone git@github.com:BIMalaza/Intelligent_eye.git
   cd Intelligent_eye
   ```

2. **Run the automated installation script**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

### Manual Installation

If you prefer manual installation or the script fails:

1. **Update system packages**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install system dependencies**:
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

3. **Enable hardware interfaces**:
   ```bash
   # Enable camera interface
   sudo raspi-config nonint do_camera 0
   
   # Enable I2C and SPI
   sudo raspi-config nonint do_i2c 0
   sudo raspi-config nonint do_spi 0
   ```

4. **Set up Python environment**:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Upgrade pip
   pip install --upgrade pip
   
   # Install Python packages
   pip install -r requirements.txt
   ```

5. **Download YOLO model**:
   ```bash
   mkdir -p models
   cd models
   wget -O yolov8n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
   cd ..
   ```

6. **Set up GPIO permissions**:
   ```bash
   sudo usermod -a -G gpio $USER
   sudo usermod -a -G i2c $USER
   sudo usermod -a -G spi $USER
   
   # Reboot to apply changes
   sudo reboot
   ```

### Virtual Environment Management

The system is designed to run in a Python virtual environment for better dependency management and isolation.

**Creating Virtual Environment**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Activating Virtual Environment**:
```bash
source venv/bin/activate
```

**Deactivating Virtual Environment**:
```bash
deactivate
```

**Checking Virtual Environment Status**:
```bash
# Check if virtual environment is active
echo $VIRTUAL_ENV

# Or run this Python command
python3 -c "import sys; print('Virtual env active:', hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))"
```

**Comprehensive Setup Check**:
```bash
# Check if everything is properly configured
python3 check_setup.py
```

### Hardware Configuration

**GPIO Pin Configuration** (edit `config.py` if needed):
- Ultrasonic Trigger: GPIO 18
- Ultrasonic Echo: GPIO 24
- Status LED: GPIO 25
- Power Button: GPIO 23
- Buzzer: GPIO 12

**Hardware Connections**:
- Connect HC-SR04 ultrasonic sensor to GPIO pins 18 (trigger) and 24 (echo)
- Connect LED to GPIO pin 25 (with appropriate resistor)
- Connect push button to GPIO pin 23 (with pull-up resistor)
- Connect buzzer to GPIO pin 12
- Connect Pi Camera to camera port
- Connect speaker/headphones to audio jack

## Usage

### Basic Usage

**Option 1: Using the startup script (Recommended)**
```bash
# Run the complete system with automatic virtual environment activation
./start_system.sh
```

**Option 2: Manual virtual environment activation**
```bash
# Activate virtual environment
source venv/bin/activate

# Run the complete system
python intelligent_eye_system.py
```

### Individual Component Testing

**Option 1: Using the test runner script (Recommended)**
```bash
# Run all tests
./run_tests.sh

# Run specific test
./run_tests.sh ultrasonic
./run_tests.sh vision
./run_tests.sh audio
./run_tests.sh integrated
./run_tests.sh performance
```

**Option 2: Manual testing**
```bash
# Activate virtual environment first
source venv/bin/activate

# Then run tests
python test_system.py ultrasonic
python test_system.py vision
python test_system.py audio
python test_system.py integrated
python test_system.py performance
```

### Proposal Validation

**Option 1: Using the demo runner script (Recommended)**
```bash
# Run validation
./run_demo.sh validation
```

**Option 2: Manual validation**
```bash
# Activate virtual environment first
source venv/bin/activate

# Then run validation
python proposal_validation.py
```

### Demonstration Scripts

**Option 1: Using the demo runner script (Recommended)**
```bash
# Run full demonstration
./run_demo.sh

# Run specific demo components
./run_demo.sh architecture
./run_demo.sh components
./run_demo.sh integrated
./run_demo.sh modular
./run_demo.sh performance
./run_demo.sh battery
```

**Option 2: Manual demo**
```bash
# Activate virtual environment first
source venv/bin/activate

# Then run demos
python demo_presentation.py
python demo_presentation.py architecture
python demo_presentation.py components
python demo_presentation.py integrated
python demo_presentation.py modular
python demo_presentation.py performance
python demo_presentation.py battery
```

### Modular Operation

The system supports modular operation:

- **Hat only**: Disable belt for vision-only mode
- **Belt only**: Disable hat for obstacle detection only
- **Combined**: Full system operation

## Configuration

Edit `config.py` to customize:

- Camera settings (resolution, FPS, brightness)
- Ultrasonic sensor parameters (detection range, warning distance)
- Object detection confidence thresholds
- Audio feedback settings
- GPIO pin assignments

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Smart Hat     │    │   Smart Belt    │
│                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Pi Camera   │ │    │ │ Ultrasonic  │ │
│ │ (Vision)    │ │    │ │ Sensors     │ │
│ └─────────────┘ │    │ └─────────────┘ │
│                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Raspberry   │ │    │ │ Raspberry   │ │
│ │ Pi (CNN)    │ │    │ │ Pi (GPIO)   │ │
│ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
            ┌─────────────────┐
            │  Audio System   │
            │  (Text-to-      │
            │   Speech)       │
            └─────────────────┘
```

## Performance Metrics

- **Obstacle Detection Accuracy**: >90% (validated)
- **System Latency**: <200ms (validated)
- **Battery Life**: 4-8 hours (validated)
- **Detection Range**: 2-400cm (ultrasonic)
- **Processing FPS**: 5-30 (configurable)
- **Power Save Mode**: Automatic activation at low battery
- **Offline Processing**: 100% local processing, no cloud dependency

## New Features & Enhancements

### Performance Monitoring
- Real-time latency tracking (<200ms target)
- Accuracy metrics collection (>90% target)
- System resource monitoring (CPU, memory, battery)
- Comprehensive performance reporting
- JSON export for analysis

### Battery Management
- Real-time battery level monitoring
- Power save mode activation
- Battery life estimation
- Low battery warnings and auto-shutdown
- USB Type-C charging support

### Validation & Testing
- Proposal requirements validation
- Comprehensive test suite
- Performance benchmarking
- Demo scripts for presentation
- Automated validation reporting

### Enhanced Modularity
- Independent hat/belt operation
- Runtime module toggling
- Power save mode per module
- Flexible configuration options

## Troubleshooting

### Common Issues

1. **Camera not detected**:
   - Enable camera interface: `sudo raspi-config`
   - Check camera connection
   - Verify camera permissions

2. **Ultrasonic sensor not working**:
   - Check GPIO connections
   - Verify sensor power supply
   - Test with multimeter

3. **Audio not playing**:
   - Check speaker/headphone connection
   - Verify audio output settings
   - Test with `aplay` command

4. **High latency**:
   - Reduce camera resolution
   - Lower processing FPS
   - Close unnecessary processes

5. **Permission denied errors**:
   - Ensure user is in GPIO group: `sudo usermod -a -G gpio $USER`
   - Reboot after adding to groups
   - Check file permissions

6. **Import errors**:
   - Activate virtual environment: `source venv/bin/activate`
   - Install missing packages: `pip install -r requirements.txt`
   - Check Python version: `python3 --version`

7. **Virtual environment issues**:
   - Not in virtual environment: Run `source venv/bin/activate`
   - Virtual environment not found: Run `python3 -m venv venv`
   - Packages not found: Run `pip install -r requirements.txt`
   - Wrong Python version: Use `python3` instead of `python`

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

If the system is running slowly:
1. Check CPU usage: `htop`
2. Monitor memory: `free -h`
3. Reduce camera resolution in `config.py`
4. Enable power save mode
5. Close unnecessary applications

## Future Enhancements

- [ ] Machine learning model optimization
- [ ] Additional sensor integration (IMU, GPS)
- [ ] Mobile app companion
- [ ] Voice command interface
- [ ] Cloud backup and analytics
- [ ] Multi-language support
- [ ] Advanced obstacle classification
- [ ] Predictive navigation assistance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- World Health Organization for vision impairment statistics
- OpenCV community for computer vision tools
- Ultralytics for YOLO implementation
- Raspberry Pi Foundation for hardware platform

## Contact

For questions, suggestions, or support, please contact:
- Project Lead: Katlego Phalane
- Student ID: 213642871
- Institution: Tshwane University of Technology
- Course: ADYE20 - Project Design Technical Design

---

**Note**: This system is designed for research and educational purposes. For commercial use or medical applications, please ensure compliance with relevant regulations and standards.
