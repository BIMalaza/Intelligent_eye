"""
Enhanced object detection module for the Intelligent Eye system
This module provides both static image processing and real-time detection capabilities
"""

import cv2
import numpy as np
import cvlib as cv
from PIL import Image
from cvlib.object_detection import draw_bbox
import matplotlib.pyplot as plt
import time
from config import DETECTION_CONFIG

class ObjectDetector:
    def __init__(self, model='yolov3'):
        self.model = model
        self.confidence_threshold = DETECTION_CONFIG['confidence_threshold']
        
    def detect_objects_image(self, image_path):
        """
        Detect objects in a static image
        """
        try:
            # Read image
            img = Image.open(image_path)
            img = np.array(img)
            
            # Detect objects
            bbox, label, conf = cv.detect_common_objects(
                img, 
                model=self.model,
                confidence=self.confidence_threshold
            )
            
            # Draw bounding boxes
            output_image = draw_bbox(img, bbox, label, conf)
            
            return {
                'image': output_image,
                'bboxes': bbox,
                'labels': label,
                'confidences': conf,
                'detection_count': len(label)
            }
            
        except Exception as e:
            print(f"Error in object detection: {e}")
            return None
    
    def detect_objects_frame(self, frame):
        """
        Detect objects in a video frame
        """
        try:
            # Detect objects
            bbox, label, conf = cv.detect_common_objects(
                frame, 
                model=self.model,
                confidence=self.confidence_threshold
            )
            
            # Filter for relevant classes
            filtered_results = []
            for i, (box, lbl, conf_val) in enumerate(zip(bbox, label, conf)):
                if lbl in DETECTION_CONFIG['classes_to_detect']:
                    filtered_results.append({
                        'bbox': box,
                        'label': lbl,
                        'confidence': conf_val
                    })
            
            return filtered_results
            
        except Exception as e:
            print(f"Error in frame detection: {e}")
            return []
    
    def visualize_detections(self, image, detections):
        """
        Visualize detections on image
        """
        output_image = image.copy()
        
        for detection in detections:
            bbox = detection['bbox']
            label = detection['label']
            confidence = detection['confidence']
            
            # Draw bounding box
            x1, y1, x2, y2 = bbox
            cv2.rectangle(output_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label and confidence
            text = f"{label}: {confidence:.2f}"
            cv2.putText(output_image, text, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return output_image

def demo_static_detection():
    """
    Demo function for static image detection
    """
    detector = ObjectDetector()
    
    # Detect objects in the sample image
    results = detector.detect_objects_image('my_image.jpg')
    
    if results:
        print(f"Detected {results['detection_count']} objects:")
        for i, (label, conf) in enumerate(zip(results['labels'], results['confidences'])):
            print(f"  {i+1}. {label} (confidence: {conf:.2f})")
        
        # Display results
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(results['image'], cv2.COLOR_BGR2RGB))
        plt.title("Object Detection Results")
        plt.axis('off')
        plt.show()
    else:
        print("No objects detected or error occurred")

def demo_realtime_detection():
    """
    Demo function for real-time detection
    """
    detector = ObjectDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Real-time object detection started. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect objects
        detections = detector.detect_objects_frame(frame)
        
        # Visualize detections
        output_frame = detector.visualize_detections(frame, detections)
        
        # Display frame
        cv2.imshow('Object Detection', output_frame)
        
        # Print detections
        if detections:
            print(f"Detected {len(detections)} objects:")
            for det in detections:
                print(f"  - {det['label']} (confidence: {det['confidence']:.2f})")
        
        # Break on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Object Detection Demo")
    print("1. Static image detection")
    print("2. Real-time detection")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        demo_static_detection()
    elif choice == "2":
        demo_realtime_detection()
    else:
        print("Invalid choice")