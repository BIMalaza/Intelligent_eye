#!/usr/bin/env python3
"""
Setup checker for Intelligent Eye for the Blind system
Checks if virtual environment and dependencies are properly configured
"""

import sys
import os
import subprocess

def check_virtual_environment():
    """Check if running in virtual environment"""
    print("Checking virtual environment...")
    
    in_venv = (hasattr(sys, 'real_prefix') or 
               (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    
    if in_venv:
        print("✓ Running in virtual environment")
        print(f"  Python executable: {sys.executable}")
        print(f"  Virtual env path: {os.environ.get('VIRTUAL_ENV', 'Unknown')}")
    else:
        print("✗ NOT running in virtual environment")
        print("  Please run: source venv/bin/activate")
    
    return in_venv

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\nChecking dependencies...")
    
    required_packages = [
        'cv2', 'numpy', 'torch', 'torchvision', 'pyttsx3', 
        'PIL', 'matplotlib', 'ultralytics', 'pygame', 'psutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
                print(f"✓ OpenCV: {cv2.__version__}")
            elif package == 'PIL':
                from PIL import Image
                print(f"✓ Pillow: {Image.__version__}")
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'Unknown')
                print(f"✓ {package}: {version}")
        except ImportError:
            print(f"✗ {package}: Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All required packages are installed")
        return True

def check_yolo_model():
    """Check if YOLO model is downloaded"""
    print("\nChecking YOLO model...")
    
    model_path = "models/yolov8n.pt"
    if os.path.exists(model_path):
        size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        print(f"✓ YOLO model found: {model_path} ({size:.1f} MB)")
        return True
    else:
        print(f"✗ YOLO model not found: {model_path}")
        print("Run: mkdir -p models && cd models && wget -O yolov8n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt")
        return False

def check_gpio():
    """Check GPIO availability"""
    print("\nChecking GPIO...")
    
    try:
        import RPi.GPIO as GPIO
        print("✓ RPi.GPIO available (Raspberry Pi mode)")
        return True
    except ImportError:
        print("⚠ RPi.GPIO not available (simulation mode)")
        print("  This is normal if not running on Raspberry Pi")
        return False

def check_camera():
    """Check camera availability"""
    print("\nChecking camera...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera available")
            cap.release()
            return True
        else:
            print("✗ Camera not available")
            return False
    except Exception as e:
        print(f"✗ Camera check failed: {e}")
        return False

def check_file_structure():
    """Check if all required files are present"""
    print("\nChecking file structure...")
    
    required_files = [
        'intelligent_eye_system.py',
        'vision_system.py',
        'ultrasonic_sensor.py',
        'audio_system.py',
        'performance_monitor.py',
        'battery_monitor.py',
        'config.py',
        'test_system.py',
        'demo_presentation.py',
        'proposal_validation.py',
        'requirements.txt'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✓ All required files present")
        return True

def main():
    """Main setup checker"""
    print("Intelligent Eye for the Blind - Setup Checker")
    print("=" * 50)
    
    checks = [
        check_virtual_environment(),
        check_dependencies(),
        check_yolo_model(),
        check_gpio(),
        check_camera(),
        check_file_structure()
    ]
    
    print("\n" + "=" * 50)
    print("SETUP SUMMARY")
    print("=" * 50)
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"Checks passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 Setup is complete! You can run the system.")
        print("\nTo start the system:")
        print("  ./start_system.sh")
        print("  # or")
        print("  source venv/bin/activate")
        print("  python intelligent_eye_system.py")
    else:
        print("⚠ Setup incomplete. Please fix the issues above.")
        print("\nQuick setup:")
        print("  ./install.sh")
        print("  source venv/bin/activate")
        print("  python check_setup.py")

if __name__ == "__main__":
    main()
