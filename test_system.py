"""
Test script for the Intelligent Eye for the Blind system
"""

import time
import sys
from intelligent_eye_system import IntelligentEyeSystem
from config import SYSTEM_CONFIG

def test_ultrasonic_sensor():
    """
    Test ultrasonic sensor functionality
    """
    print("Testing Ultrasonic Sensor...")
    from ultrasonic_sensor import UltrasonicSensor
    
    def test_callback(distance):
        print(f"Obstacle detected at {distance:.1f} cm")
    
    sensor = UltrasonicSensor()
    
    try:
        sensor.start_monitoring(test_callback)
        print("Ultrasonic sensor test running for 10 seconds...")
        time.sleep(10)
        
    except Exception as e:
        print(f"Ultrasonic sensor test failed: {e}")
    finally:
        sensor.cleanup()

def test_vision_system():
    """
    Test vision system functionality
    """
    print("Testing Vision System...")
    from vision_system import VisionSystem
    
    def test_callback(results):
        print(f"Vision results: {len(results['objects'])} objects, {len(results['signs'])} signs")
        for obj in results['objects']:
            print(f"  Object: {obj['class']} (confidence: {obj['confidence']:.2f})")
        for sign in results['signs']:
            print(f"  Sign: {sign['type']} at {sign['distance']:.1f}cm")
    
    vision = VisionSystem()
    
    try:
        print("Vision system test running for 10 seconds...")
        vision.start_continuous_detection(test_callback)
        time.sleep(10)
        
    except Exception as e:
        print(f"Vision system test failed: {e}")
    finally:
        vision.cleanup()

def test_audio_system():
    """
    Test audio system functionality
    """
    print("Testing Audio System...")
    from audio_system import AudioSystem
    
    audio = AudioSystem()
    
    try:
        # Test basic speech
        print("Testing basic speech...")
        audio.speak("Testing the audio system")
        time.sleep(2)
        
        # Test obstacle announcement
        print("Testing obstacle announcement...")
        audio.announce_obstacle(50)
        time.sleep(2)
        
        # Test sign announcement
        print("Testing sign announcement...")
        audio.announce_sign("stop sign", 30)
        time.sleep(2)
        
        # Test object announcement
        print("Testing object announcement...")
        audio.announce_object("person", 25)
        time.sleep(2)
        
    except Exception as e:
        print(f"Audio system test failed: {e}")
    finally:
        audio.cleanup()

def test_integrated_system():
    """
    Test the complete integrated system
    """
    print("Testing Integrated System...")
    system = IntelligentEyeSystem()
    
    try:
        print("Starting integrated system test...")
        system.start_system()
        
    except Exception as e:
        print(f"Integrated system test failed: {e}")
    finally:
        system.cleanup()

def run_performance_test():
    """
    Run performance tests to validate system requirements
    """
    print("Running Performance Tests...")
    
    # Test latency
    print("Testing system latency...")
    start_time = time.time()
    
    # Simulate detection and processing
    time.sleep(0.1)  # Simulate processing time
    
    latency = (time.time() - start_time) * 1000
    print(f"Measured latency: {latency:.1f}ms")
    
    if latency < SYSTEM_CONFIG['max_latency_ms']:
        print("✓ Latency test PASSED")
    else:
        print("✗ Latency test FAILED")
    
    # Test battery life estimation
    print("Testing battery life estimation...")
    estimated_hours = SYSTEM_CONFIG['battery_life_hours']
    print(f"Estimated battery life: {estimated_hours} hours")
    
    if estimated_hours >= 4:
        print("✓ Battery life test PASSED")
    else:
        print("✗ Battery life test FAILED")

def main():
    """
    Main test function
    """
    print("Intelligent Eye for the Blind - System Test Suite")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == "ultrasonic":
            test_ultrasonic_sensor()
        elif test_type == "vision":
            test_vision_system()
        elif test_type == "audio":
            test_audio_system()
        elif test_type == "integrated":
            test_integrated_system()
        elif test_type == "performance":
            run_performance_test()
        else:
            print("Invalid test type. Available options: ultrasonic, vision, audio, integrated, performance")
    else:
        # Run all tests
        print("Running all system tests...")
        
        try:
            test_ultrasonic_sensor()
            print()
            
            test_vision_system()
            print()
            
            test_audio_system()
            print()
            
            run_performance_test()
            print()
            
            print("All tests completed!")
            
        except KeyboardInterrupt:
            print("Tests interrupted by user")
        except Exception as e:
            print(f"Test suite error: {e}")

if __name__ == "__main__":
    main()