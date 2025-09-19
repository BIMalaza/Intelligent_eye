"""
Main Intelligent Eye for the Blind system integration
"""

import sys
import os
import time
import threading

# Check if running in virtual environment
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("WARNING: Not running in a virtual environment!")
    print("For best results, please run:")
    print("  source venv/bin/activate")
    print("  python intelligent_eye_system.py")
    print()

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("RPi.GPIO not available - running in simulation mode")
    # Create a mock GPIO module for testing
    class MockGPIO:
        BCM = 'BCM'
        OUT = 'OUT'
        IN = 'IN'
        HIGH = True
        LOW = False
        PUD_UP = 'PUD_UP'
        
        @staticmethod
        def setmode(mode):
            pass
        
        @staticmethod
        def setup(pin, mode, pull_up_down=None):
            pass
        
        @staticmethod
        def output(pin, value):
            pass
        
        @staticmethod
        def input(pin):
            return True
        
        @staticmethod
        def cleanup():
            pass
    
    GPIO = MockGPIO()
from config import SYSTEM_CONFIG, GPIO_CONFIG
from ultrasonic_sensor import UltrasonicSensor
from vision_system import VisionSystem
from audio_system import AudioSystem
from performance_monitor import PerformanceMonitor, PerformanceContext
from battery_monitor import BatteryMonitor

class IntelligentEyeSystem:
    def __init__(self):
        self.ultrasonic_sensor = None
        self.vision_system = None
        self.audio_system = None
        self.performance_monitor = None
        self.battery_monitor = None
        
        # System state
        self.is_running = False
        self.hat_enabled = True
        self.belt_enabled = True
        self.battery_level = 100
        
        # Performance monitoring
        self.start_time = None
        self.detection_count = 0
        self.latency_measurements = []
        
        # Initialize components
        self._init_components()
        
    def _init_components(self):
        """
        Initialize all system components
        """
        try:
            # Initialize GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIO_CONFIG['led_status'], GPIO.OUT)
            GPIO.setup(GPIO_CONFIG['button_power'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(GPIO_CONFIG['buzzer'], GPIO.OUT)
            
            # Initialize subsystems
            self.ultrasonic_sensor = UltrasonicSensor()
            self.vision_system = VisionSystem()
            self.audio_system = AudioSystem()
            self.performance_monitor = PerformanceMonitor()
            self.battery_monitor = BatteryMonitor()
            
            # Set up battery monitoring callbacks
            self.battery_monitor.add_callback(self._battery_callback)
            
            print("All components initialized successfully")
            
        except Exception as e:
            print(f"Error initializing components: {e}")
            raise
    
    def start_system(self):
        """
        Start the complete Intelligent Eye system
        """
        if self.is_running:
            print("System is already running")
            return
        
        try:
            self.is_running = True
            self.start_time = time.time()
            
            # Start status LED
            GPIO.output(GPIO_CONFIG['led_status'], GPIO.HIGH)
            
            # Start performance and battery monitoring
            self.performance_monitor.start_monitoring()
            self.battery_monitor.start_monitoring()
            
            # Announce system ready
            self.audio_system.system_ready()
            
            # Start ultrasonic monitoring if belt is enabled
            if self.belt_enabled:
                self.ultrasonic_sensor.start_monitoring(self._obstacle_callback)
            
            # Start vision processing if hat is enabled
            if self.hat_enabled:
                vision_thread = threading.Thread(target=self._vision_processing_loop)
                vision_thread.daemon = True
                vision_thread.start()
            
            # Start main system monitoring
            self._system_monitoring_loop()
            
        except Exception as e:
            print(f"Error starting system: {e}")
            self.stop_system()
    
    def stop_system(self):
        """
        Stop the complete system
        """
        self.is_running = False
        
        # Stop status LED
        GPIO.output(GPIO_CONFIG['led_status'], GPIO.LOW)
        
        # Stop monitoring systems
        if self.performance_monitor:
            self.performance_monitor.stop_monitoring()
        
        if self.battery_monitor:
            self.battery_monitor.stop_monitoring()
        
        # Stop subsystems
        if self.ultrasonic_sensor:
            self.ultrasonic_sensor.stop_monitoring()
        
        if self.vision_system:
            self.vision_system.stop_detection()
        
        if self.audio_system:
            self.audio_system.stop_speaking()
        
        print("System stopped")
    
    def _obstacle_callback(self, distance):
        """
        Callback for obstacle detection from ultrasonic sensor
        """
        if not self.is_running:
            return
        
        # Measure latency with performance monitoring
        with PerformanceContext(self.performance_monitor, "obstacle"):
            # Announce obstacle
            self.audio_system.announce_obstacle(distance)
            
            # Play warning beep
            self.audio_system.play_beep(frequency=800, duration=0.2)
            
            # Update statistics
            self.detection_count += 1
    
    def _vision_processing_loop(self):
        """
        Continuous vision processing loop
        """
        while self.is_running and self.hat_enabled:
            try:
                # Get power save settings based on battery level
                power_settings = self.battery_monitor.get_power_save_settings()
                
                frame = self.vision_system.capture_frame()
                if frame is not None:
                    with PerformanceContext(self.performance_monitor, "object"):
                        results = self.vision_system.process_frame(frame)
                        self._process_vision_results(results)
                
                # Use power save FPS if in power save mode
                fps = power_settings['fps']
                time.sleep(1.0 / fps)
                
            except Exception as e:
                print(f"Error in vision processing: {e}")
                time.sleep(1)
    
    def _process_vision_results(self, results):
        """
        Process vision detection results
        """
        if not self.is_running:
            return
        
        # Process road signs
        for sign in results.get('signs', []):
            self.audio_system.announce_sign(
                sign['type'], 
                sign.get('distance', None)
            )
        
        # Process objects
        for obj in results.get('objects', []):
            if obj['confidence'] > 0.7:  # High confidence objects only
                self.audio_system.announce_object(
                    obj['class'],
                    self._estimate_object_distance(obj)
                )
    
    def _estimate_object_distance(self, obj):
        """
        Estimate distance to detected object based on bounding box size
        """
        bbox = obj['bbox']
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        area = width * height
        
        # Rough distance estimation (calibrated for typical object sizes)
        if obj['class'] in ['person', 'bicycle']:
            estimated_distance = max(50, 1000 / (area ** 0.5))
        elif obj['class'] in ['car', 'truck', 'bus']:
            estimated_distance = max(100, 2000 / (area ** 0.5))
        else:
            estimated_distance = max(30, 800 / (area ** 0.5))
        
        return estimated_distance
    
    def _battery_callback(self, level_type, battery_level):
        """
        Callback for battery level changes
        """
        if level_type == 'critical':
            self.audio_system.speak("Critical battery level, shutting down")
            self.stop_system()
        elif level_type == 'low':
            self.audio_system.speak("Battery low, please recharge")
        elif level_type == 'warning':
            self.audio_system.speak("Battery warning")
        
        print(f"Battery {level_type}: {battery_level:.1f}%")
    
    def _system_monitoring_loop(self):
        """
        Main system monitoring and control loop
        """
        while self.is_running:
            try:
                # Check power button
                if GPIO.input(GPIO_CONFIG['button_power']) == GPIO.LOW:
                    print("Power button pressed - stopping system")
                    break
                
                # Update battery level from monitor
                battery_info = self.battery_monitor.get_battery_info()
                self.battery_level = battery_info['level']
                
                # Check system performance
                self._check_performance()
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("System interrupted by user")
                break
            except Exception as e:
                print(f"Error in system monitoring: {e}")
                time.sleep(1)
    
    def _check_performance(self):
        """
        Check system performance metrics
        """
        # Print performance report every 30 seconds
        if self.detection_count > 0 and self.detection_count % 30 == 0:
            self.performance_monitor.print_performance_report()
    
    def toggle_hat(self):
        """
        Toggle smart hat functionality
        """
        self.hat_enabled = not self.hat_enabled
        status = "enabled" if self.hat_enabled else "disabled"
        self.audio_system.speak(f"Smart hat {status}")
        print(f"Smart hat {status}")
    
    def toggle_belt(self):
        """
        Toggle smart belt functionality
        """
        self.belt_enabled = not self.belt_enabled
        status = "enabled" if self.belt_enabled else "disabled"
        self.audio_system.speak(f"Smart belt {status}")
        print(f"Smart belt {status}")
        
        if self.belt_enabled and self.is_running:
            self.ultrasonic_sensor.start_monitoring(self._obstacle_callback)
        elif not self.belt_enabled:
            self.ultrasonic_sensor.stop_monitoring()
    
    def get_system_status(self):
        """
        Get current system status
        """
        battery_info = self.battery_monitor.get_battery_info() if self.battery_monitor else {}
        performance_summary = self.performance_monitor.get_performance_summary() if self.performance_monitor else {}
        
        return {
            'running': self.is_running,
            'hat_enabled': self.hat_enabled,
            'belt_enabled': self.belt_enabled,
            'battery_level': self.battery_level,
            'battery_info': battery_info,
            'detection_count': self.detection_count,
            'uptime': time.time() - self.start_time if self.start_time else 0,
            'performance': performance_summary
        }
    
    def print_system_report(self):
        """
        Print comprehensive system report
        """
        print("\n" + "="*60)
        print("INTELLIGENT EYE FOR THE BLIND - SYSTEM REPORT")
        print("="*60)
        
        status = self.get_system_status()
        
        print(f"System Status: {'RUNNING' if status['running'] else 'STOPPED'}")
        print(f"Smart Hat: {'ENABLED' if status['hat_enabled'] else 'DISABLED'}")
        print(f"Smart Belt: {'ENABLED' if status['belt_enabled'] else 'DISABLED'}")
        print(f"Total Detections: {status['detection_count']}")
        print(f"Uptime: {status['uptime']:.1f} seconds")
        
        if self.battery_monitor:
            self.battery_monitor.print_battery_status()
        
        if self.performance_monitor:
            self.performance_monitor.print_performance_report()
        
        print("="*60)
    
    def save_performance_data(self, filename=None):
        """
        Save performance data to file
        """
        if self.performance_monitor:
            self.performance_monitor.save_metrics_to_file(filename)
    
    def cleanup(self):
        """
        Cleanup all system resources
        """
        self.stop_system()
        
        if self.ultrasonic_sensor:
            self.ultrasonic_sensor.cleanup()
        
        if self.vision_system:
            self.vision_system.cleanup()
        
        if self.audio_system:
            self.audio_system.cleanup()
        
        if self.performance_monitor:
            self.performance_monitor.stop_monitoring()
        
        if self.battery_monitor:
            self.battery_monitor.stop_monitoring()
        
        GPIO.cleanup()
        print("System cleanup completed")

# Main execution
if __name__ == "__main__":
    system = IntelligentEyeSystem()
    
    try:
        print("Starting Intelligent Eye for the Blind system...")
        system.start_system()
        
    except KeyboardInterrupt:
        print("System stopped by user")
    except Exception as e:
        print(f"System error: {e}")
    finally:
        system.cleanup()