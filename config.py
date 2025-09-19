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