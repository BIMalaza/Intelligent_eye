"""
Vision system module for road sign and object recognition in the smart hat
"""

import cv2
import numpy as np
import torch
from ultralytics import YOLO
import time
from config import CAMERA_CONFIG, DETECTION_CONFIG, SIGN_RECOGNITION_CONFIG

class VisionSystem:
    def __init__(self):
        self.camera = None
        self.model = None
        self.sign_model = None
        self.is_running = False
        
        # Initialize camera
        self._init_camera()
        
        # Load models
        self._load_models()
        
    def _init_camera(self):
        """
        Initialize Pi Camera
        """
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['resolution'][0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['resolution'][1])
            self.camera.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
            self.camera.set(cv2.CAP_PROP_BRIGHTNESS, CAMERA_CONFIG['brightness'])
            self.camera.set(cv2.CAP_PROP_CONTRAST, CAMERA_CONFIG['contrast'])
            
            if not self.camera.isOpened():
                raise Exception("Could not open camera")
                
            print("Camera initialized successfully")
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            self.camera = None
    
    def _load_models(self):
        """
        Load YOLO and road sign recognition models
        """
        try:
            # Load YOLO model for general object detection
            self.model = YOLO(DETECTION_CONFIG['model_path'])
            print("YOLO model loaded successfully")
            
            # Load road sign classification model (if available)
            try:
                import tensorflow as tf
                self.sign_model = tf.keras.models.load_model(SIGN_RECOGNITION_CONFIG['model_path'])
                print("Road sign model loaded successfully")
            except:
                print("Road sign model not available, using YOLO for sign detection")
                self.sign_model = None
                
        except Exception as e:
            print(f"Error loading models: {e}")
            self.model = None
            self.sign_model = None
    
    def capture_frame(self):
        """
        Capture a frame from the camera
        """
        if self.camera is None:
            return None
            
        ret, frame = self.camera.read()
        if ret:
            # Rotate frame if needed
            if CAMERA_CONFIG['rotation'] != 0:
                frame = cv2.rotate(frame, CAMERA_CONFIG['rotation'])
            return frame
        return None
    
    def detect_objects(self, frame):
        """
        Detect objects in the frame using YOLO
        """
        if self.model is None or frame is None:
            return []
        
        try:
            # Run YOLO detection
            results = self.model(frame, conf=DETECTION_CONFIG['confidence_threshold'])
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get bounding box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        
                        # Get class and confidence
                        class_id = int(box.cls[0].cpu().numpy())
                        confidence = float(box.conf[0].cpu().numpy())
                        
                        # Get class name
                        class_name = self.model.names[class_id]
                        
                        # Filter for relevant classes
                        if class_name in DETECTION_CONFIG['classes_to_detect']:
                            detections.append({
                                'class': class_name,
                                'confidence': confidence,
                                'bbox': (int(x1), int(y1), int(x2), int(y2)),
                                'center': (int((x1 + x2) / 2), int((y1 + y2) / 2))
                            })
            
            return detections
            
        except Exception as e:
            print(f"Error in object detection: {e}")
            return []
    
    def detect_road_signs(self, frame):
        """
        Detect and classify road signs
        """
        if frame is None:
            return []
        
        # First detect objects that might be signs
        objects = self.detect_objects(frame)
        signs = []
        
        for obj in objects:
            if obj['class'] in ['stop sign', 'traffic light']:
                # Calculate distance estimation based on bounding box size
                bbox = obj['bbox']
                width = bbox[2] - bbox[0]
                height = bbox[3] - bbox[1]
                area = width * height
                
                # Rough distance estimation (calibrated for typical sign sizes)
                if obj['class'] == 'stop sign':
                    estimated_distance = max(50, 2000 / (area ** 0.5))
                else:
                    estimated_distance = max(30, 1500 / (area ** 0.5))
                
                signs.append({
                    'type': obj['class'],
                    'confidence': obj['confidence'],
                    'distance': estimated_distance,
                    'bbox': obj['bbox'],
                    'center': obj['center']
                })
        
        return signs
    
    def process_frame(self, frame):
        """
        Process a single frame for both object and sign detection
        """
        if frame is None:
            return {'objects': [], 'signs': []}
        
        # Detect objects
        objects = self.detect_objects(frame)
        
        # Detect road signs
        signs = self.detect_road_signs(frame)
        
        return {
            'objects': objects,
            'signs': signs,
            'timestamp': time.time()
        }
    
    def start_continuous_detection(self, callback=None):
        """
        Start continuous detection
        """
        self.is_running = True
        
        while self.is_running:
            frame = self.capture_frame()
            if frame is not None:
                results = self.process_frame(frame)
                if callback:
                    callback(results)
            
            time.sleep(1.0 / CAMERA_CONFIG['fps'])
    
    def stop_detection(self):
        """
        Stop continuous detection
        """
        self.is_running = False
    
    def cleanup(self):
        """
        Cleanup camera resources
        """
        self.stop_detection()
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        print("Vision system cleaned up")

# Test function
if __name__ == "__main__":
    def detection_callback(results):
        print(f"Detected {len(results['objects'])} objects and {len(results['signs'])} signs")
        for obj in results['objects']:
            print(f"  Object: {obj['class']} (confidence: {obj['confidence']:.2f})")
        for sign in results['signs']:
            print(f"  Sign: {sign['type']} at {sign['distance']:.1f}cm")
    
    vision = VisionSystem()
    
    try:
        vision.start_continuous_detection(detection_callback)
    except KeyboardInterrupt:
        print("Stopping vision system test")
    finally:
        vision.cleanup()