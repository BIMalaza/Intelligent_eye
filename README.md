# Intelligent Eye for the Blind

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

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd intelligent-eye-blind
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download YOLO model**:
   ```bash
   wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
   mkdir models
   mv yolov8n.pt models/
   ```

4. **Configure GPIO pins** (edit `config.py` if needed):
   - Ultrasonic Trigger: GPIO 18
   - Ultrasonic Echo: GPIO 24
   - Status LED: GPIO 25
   - Power Button: GPIO 23
   - Buzzer: GPIO 12

## Usage

### Basic Usage

Run the complete system:
```bash
python intelligent_eye_system.py
```

### Individual Component Testing

Test ultrasonic sensor:
```bash
python test_system.py ultrasonic
```

Test vision system:
```bash
python test_system.py vision
```

Test audio system:
```bash
python test_system.py audio
```

Test integrated system:
```bash
python test_system.py integrated
```

Run performance tests:
```bash
python test_system.py performance
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

- **Obstacle Detection Accuracy**: >90%
- **System Latency**: <200ms
- **Battery Life**: 4-8 hours
- **Detection Range**: 2-400cm (ultrasonic)
- **Processing FPS**: 5-30 (configurable)

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

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- [ ] Machine learning model optimization
- [ ] Additional sensor integration (IMU, GPS)
- [ ] Mobile app companion
- [ ] Voice command interface
- [ ] Cloud backup and analytics
- [ ] Multi-language support

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
- Project Lead: [Your Name]
- Email: [your.email@example.com]
- GitHub: [your-github-username]

---

**Note**: This system is designed for research and educational purposes. For commercial use or medical applications, please ensure compliance with relevant regulations and standards.