"""
Ultrasonic sensor module for obstacle detection in the smart belt
"""

import RPi.GPIO as GPIO
import time
import threading
from config import ULTRASONIC_CONFIG, GPIO_CONFIG

class UltrasonicSensor:
    def __init__(self):
        self.trigger_pin = GPIO_CONFIG['ultrasonic_trigger']
        self.echo_pin = GPIO_CONFIG['ultrasonic_echo']
        self.max_distance = ULTRASONIC_CONFIG['max_distance_cm']
        self.min_distance = ULTRASONIC_CONFIG['min_distance_cm']
        self.warning_distance = ULTRASONIC_CONFIG['warning_distance_cm']
        self.detection_angle = ULTRASONIC_CONFIG['detection_angle']
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        # Sensor state
        self.is_running = False
        self.current_distance = None
        self.obstacle_detected = False
        self.callback = None
        
        # Threading for continuous monitoring
        self.monitor_thread = None
        
    def measure_distance(self):
        """
        Measure distance using ultrasonic sensor
        Returns distance in centimeters
        """
        try:
            # Send trigger pulse
            GPIO.output(self.trigger_pin, False)
            time.sleep(0.000002)
            GPIO.output(self.trigger_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, False)
            
            # Measure echo pulse duration
            start_time = time.time()
            timeout = time.time() + 0.1  # 100ms timeout
            
            while GPIO.input(self.echo_pin) == 0 and time.time() < timeout:
                start_time = time.time()
                
            if time.time() >= timeout:
                return None
                
            stop_time = time.time()
            timeout = time.time() + 0.1
            
            while GPIO.input(self.echo_pin) == 1 and time.time() < timeout:
                stop_time = time.time()
                
            if time.time() >= timeout:
                return None
            
            # Calculate distance
            duration = stop_time - start_time
            distance = (duration * 34300) / 2  # Speed of sound = 343 m/s
            
            # Validate distance
            if self.min_distance <= distance <= self.max_distance:
                return distance
            else:
                return None
                
        except Exception as e:
            print(f"Error measuring distance: {e}")
            return None
    
    def start_monitoring(self, callback=None):
        """
        Start continuous monitoring of obstacles
        """
        self.callback = callback
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print("Ultrasonic sensor monitoring started")
    
    def stop_monitoring(self):
        """
        Stop continuous monitoring
        """
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("Ultrasonic sensor monitoring stopped")
    
    def _monitor_loop(self):
        """
        Continuous monitoring loop
        """
        while self.is_running:
            distance = self.measure_distance()
            
            if distance is not None:
                self.current_distance = distance
                self.obstacle_detected = distance <= self.warning_distance
                
                # Call callback if obstacle detected
                if self.obstacle_detected and self.callback:
                    self.callback(distance)
            else:
                self.obstacle_detected = False
            
            time.sleep(0.1)  # 100ms interval
    
    def get_distance(self):
        """
        Get current measured distance
        """
        return self.current_distance
    
    def is_obstacle_detected(self):
        """
        Check if obstacle is detected within warning distance
        """
        return self.obstacle_detected
    
    def cleanup(self):
        """
        Cleanup GPIO resources
        """
        self.stop_monitoring()
        GPIO.cleanup()
        print("Ultrasonic sensor cleaned up")

# Test function
if __name__ == "__main__":
    def obstacle_callback(distance):
        print(f"Obstacle detected at {distance:.1f} cm")
    
    sensor = UltrasonicSensor()
    
    try:
        sensor.start_monitoring(obstacle_callback)
        
        # Run for 10 seconds
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("Stopping ultrasonic sensor test")
    finally:
        sensor.cleanup()