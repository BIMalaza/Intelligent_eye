"""
Battery monitoring module for the Intelligent Eye system
Implements real battery level monitoring and power management
"""

import time
import threading
import subprocess
import os
from config import SYSTEM_CONFIG

class BatteryMonitor:
    def __init__(self):
        self.battery_level = 100
        self.is_charging = False
        self.voltage = 0.0
        self.current = 0.0
        self.temperature = 0.0
        
        # Power management settings
        self.critical_level = 10
        self.low_level = 20
        self.warning_level = 30
        
        # Battery life estimation
        self.battery_capacity_mah = 5000  # Typical power bank capacity
        self.current_draw_ma = 500  # Estimated current draw
        self.estimated_hours = self.battery_capacity_mah / self.current_draw_ma
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread = None
        self.callbacks = []
        
        # Power saving modes
        self.power_save_mode = False
        self.reduced_fps = 2  # Reduced FPS in power save mode
        self.reduced_processing = True
        
    def add_callback(self, callback):
        """Add battery level change callback"""
        self.callbacks.append(callback)
    
    def start_monitoring(self):
        """Start battery monitoring"""
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print("Battery monitoring started")
    
    def stop_monitoring(self):
        """Stop battery monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("Battery monitoring stopped")
    
    def _monitor_loop(self):
        """Main battery monitoring loop"""
        while self.is_monitoring:
            try:
                # Read battery information
                self._read_battery_info()
                
                # Check battery level and trigger callbacks
                self._check_battery_level()
                
                # Update power save mode based on battery level
                self._update_power_save_mode()
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                print(f"Error in battery monitoring: {e}")
                time.sleep(5)
    
    def _read_battery_info(self):
        """Read battery information from system"""
        try:
            # Try to read from /sys/class/power_supply (Linux)
            if os.path.exists('/sys/class/power_supply'):
                self._read_linux_battery_info()
            else:
                # Fallback to simulated battery monitoring
                self._simulate_battery_info()
                
        except Exception as e:
            print(f"Error reading battery info: {e}")
            self._simulate_battery_info()
    
    def _read_linux_battery_info(self):
        """Read battery info from Linux power supply interface"""
        try:
            # Look for battery in power supply directory
            power_supply_dir = '/sys/class/power_supply'
            battery_dirs = [d for d in os.listdir(power_supply_dir) 
                          if d.startswith('BAT') or 'battery' in d.lower()]
            
            if battery_dirs:
                battery_dir = os.path.join(power_supply_dir, battery_dirs[0])
                
                # Read capacity
                capacity_file = os.path.join(battery_dir, 'capacity')
                if os.path.exists(capacity_file):
                    with open(capacity_file, 'r') as f:
                        self.battery_level = int(f.read().strip())
                
                # Read charging status
                status_file = os.path.join(battery_dir, 'status')
                if os.path.exists(status_file):
                    with open(status_file, 'r') as f:
                        status = f.read().strip().lower()
                        self.is_charging = 'charging' in status or 'full' in status
                
                # Read voltage
                voltage_file = os.path.join(battery_dir, 'voltage_now')
                if os.path.exists(voltage_file):
                    with open(voltage_file, 'r') as f:
                        voltage_uv = int(f.read().strip())
                        self.voltage = voltage_uv / 1000000  # Convert to volts
                
                # Read current
                current_file = os.path.join(battery_dir, 'current_now')
                if os.path.exists(current_file):
                    with open(current_file, 'r') as f:
                        current_ua = int(f.read().strip())
                        self.current = current_ua / 1000000  # Convert to amps
                
                # Read temperature
                temp_file = os.path.join(battery_dir, 'temp')
                if os.path.exists(temp_file):
                    with open(temp_file, 'r') as f:
                        temp_deci_c = int(f.read().strip())
                        self.temperature = temp_deci_c / 10  # Convert to celsius
            else:
                self._simulate_battery_info()
                
        except Exception as e:
            print(f"Error reading Linux battery info: {e}")
            self._simulate_battery_info()
    
    def _simulate_battery_info(self):
        """Simulate battery information for testing/demo purposes"""
        # Simulate gradual battery drain
        if not self.is_charging and self.battery_level > 0:
            # Drain 1% every 5 minutes (simulated)
            self.battery_level = max(0, self.battery_level - 0.1)
        
        # Simulate charging
        if self.is_charging and self.battery_level < 100:
            self.battery_level = min(100, self.battery_level + 0.5)
        
        # Simulate voltage (3.7V typical for Li-ion)
        self.voltage = 3.7 + (self.battery_level - 50) * 0.01
        
        # Simulate current draw
        if self.is_charging:
            self.current = 1.0  # 1A charging current
        else:
            self.current = -0.5  # 500mA discharge current
        
        # Simulate temperature
        self.temperature = 25 + (100 - self.battery_level) * 0.1
    
    def _check_battery_level(self):
        """Check battery level and trigger appropriate callbacks"""
        for callback in self.callbacks:
            try:
                if self.battery_level <= self.critical_level:
                    callback('critical', self.battery_level)
                elif self.battery_level <= self.low_level:
                    callback('low', self.battery_level)
                elif self.battery_level <= self.warning_level:
                    callback('warning', self.battery_level)
            except Exception as e:
                print(f"Error in battery callback: {e}")
    
    def _update_power_save_mode(self):
        """Update power save mode based on battery level"""
        if self.battery_level <= self.warning_level and not self.power_save_mode:
            self.power_save_mode = True
            print("Power save mode activated")
        elif self.battery_level > self.warning_level + 10 and self.power_save_mode:
            self.power_save_mode = False
            print("Power save mode deactivated")
    
    def get_battery_info(self):
        """Get current battery information"""
        return {
            'level': self.battery_level,
            'is_charging': self.is_charging,
            'voltage': self.voltage,
            'current': self.current,
            'temperature': self.temperature,
            'power_save_mode': self.power_save_mode,
            'estimated_hours_remaining': self._calculate_remaining_hours()
        }
    
    def _calculate_remaining_hours(self):
        """Calculate estimated hours remaining"""
        if self.is_charging:
            return None  # Can't estimate while charging
        
        if self.current_draw_ma <= 0:
            return None
        
        remaining_capacity = (self.battery_level / 100) * self.battery_capacity_mah
        hours_remaining = remaining_capacity / self.current_draw_ma
        return max(0, hours_remaining)
    
    def set_charging_state(self, is_charging):
        """Manually set charging state (for testing)"""
        self.is_charging = is_charging
        print(f"Charging state set to: {is_charging}")
    
    def set_battery_level(self, level):
        """Manually set battery level (for testing)"""
        self.battery_level = max(0, min(100, level))
        print(f"Battery level set to: {self.battery_level}%")
    
    def get_power_save_settings(self):
        """Get power save mode settings"""
        if self.power_save_mode:
            return {
                'fps': self.reduced_fps,
                'reduced_processing': self.reduced_processing,
                'ultrasonic_interval': 0.2,  # Slower ultrasonic readings
                'vision_skip_frames': 2  # Skip every other frame
            }
        else:
            return {
                'fps': SYSTEM_CONFIG['processing_fps'],
                'reduced_processing': False,
                'ultrasonic_interval': 0.1,
                'vision_skip_frames': 1
            }
    
    def print_battery_status(self):
        """Print current battery status"""
        info = self.get_battery_info()
        
        print("\n" + "="*40)
        print("BATTERY STATUS")
        print("="*40)
        print(f"Level: {info['level']:.1f}%")
        print(f"Charging: {'Yes' if info['is_charging'] else 'No'}")
        print(f"Voltage: {info['voltage']:.2f}V")
        print(f"Current: {info['current']:.3f}A")
        print(f"Temperature: {info['temperature']:.1f}°C")
        print(f"Power Save Mode: {'On' if info['power_save_mode'] else 'Off'}")
        
        if info['estimated_hours_remaining'] is not None:
            print(f"Estimated Time Remaining: {info['estimated_hours_remaining']:.1f} hours")
        
        # Status indicators
        if info['level'] <= self.critical_level:
            print("⚠️  CRITICAL BATTERY LEVEL")
        elif info['level'] <= self.low_level:
            print("🔋 LOW BATTERY")
        elif info['level'] <= self.warning_level:
            print("⚡ BATTERY WARNING")
        else:
            print("✅ Battery OK")
        
        print("="*40)

# Test function
if __name__ == "__main__":
    def battery_callback(level_type, battery_level):
        print(f"Battery {level_type}: {battery_level:.1f}%")
    
    monitor = BatteryMonitor()
    monitor.add_callback(battery_callback)
    
    try:
        monitor.start_monitoring()
        
        # Simulate battery drain
        for i in range(20):
            monitor.set_battery_level(100 - i * 5)
            monitor.print_battery_status()
            time.sleep(2)
        
    except KeyboardInterrupt:
        print("Stopping battery monitor test")
    finally:
        monitor.stop_monitoring()
