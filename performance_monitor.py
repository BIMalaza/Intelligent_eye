"""
Performance monitoring module for the Intelligent Eye system
Tracks latency, accuracy, and system metrics as specified in the project proposal
"""

import time
import threading
import json
import os
from datetime import datetime
from collections import deque
import psutil
import numpy as np
from config import SYSTEM_CONFIG

class PerformanceMonitor:
    def __init__(self, max_samples=1000):
        self.max_samples = max_samples
        
        # Latency tracking
        self.detection_latencies = deque(maxlen=max_samples)
        self.processing_latencies = deque(maxlen=max_samples)
        self.audio_latencies = deque(maxlen=max_samples)
        
        # Accuracy tracking
        self.obstacle_detections = deque(maxlen=max_samples)
        self.object_detections = deque(maxlen=max_samples)
        self.sign_detections = deque(maxlen=max_samples)
        
        # System metrics
        self.cpu_usage = deque(maxlen=100)
        self.memory_usage = deque(maxlen=100)
        self.battery_level = 100  # Will be updated by battery monitor
        
        # Performance thresholds from proposal
        self.max_latency_ms = SYSTEM_CONFIG['max_latency_ms']
        self.target_accuracy = 0.90  # 90% as specified in proposal
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread = None
        self.start_time = None
        
        # Statistics
        self.total_detections = 0
        self.false_positives = 0
        self.false_negatives = 0
        
    def start_monitoring(self):
        """Start performance monitoring"""
        self.is_monitoring = True
        self.start_time = time.time()
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Monitor system resources
                self.cpu_usage.append(psutil.cpu_percent())
                self.memory_usage.append(psutil.virtual_memory().percent)
                
                # Check performance thresholds
                self._check_performance_thresholds()
                
                time.sleep(1)  # Monitor every second
                
            except Exception as e:
                print(f"Error in performance monitoring: {e}")
                time.sleep(1)
    
    def record_detection_latency(self, start_time, end_time, detection_type="general"):
        """Record detection latency"""
        latency_ms = (end_time - start_time) * 1000
        self.detection_latencies.append(latency_ms)
        
        if detection_type == "obstacle":
            self.obstacle_detections.append({
                'timestamp': time.time(),
                'latency_ms': latency_ms,
                'type': 'obstacle'
            })
        elif detection_type == "object":
            self.object_detections.append({
                'timestamp': time.time(),
                'latency_ms': latency_ms,
                'type': 'object'
            })
        elif detection_type == "sign":
            self.sign_detections.append({
                'timestamp': time.time(),
                'latency_ms': latency_ms,
                'type': 'sign'
            })
        
        self.total_detections += 1
        return latency_ms
    
    def record_processing_latency(self, start_time, end_time):
        """Record processing latency"""
        latency_ms = (end_time - start_time) * 1000
        self.processing_latencies.append(latency_ms)
        return latency_ms
    
    def record_audio_latency(self, start_time, end_time):
        """Record audio synthesis latency"""
        latency_ms = (end_time - start_time) * 1000
        self.audio_latencies.append(latency_ms)
        return latency_ms
    
    def record_false_positive(self, detection_type="general"):
        """Record a false positive detection"""
        self.false_positives += 1
        print(f"False positive recorded for {detection_type}")
    
    def record_false_negative(self, detection_type="general"):
        """Record a false negative detection"""
        self.false_negatives += 1
        print(f"False negative recorded for {detection_type}")
    
    def update_battery_level(self, level):
        """Update battery level"""
        self.battery_level = level
    
    def _check_performance_thresholds(self):
        """Check if system meets performance thresholds"""
        if len(self.detection_latencies) > 10:
            avg_latency = np.mean(list(self.detection_latencies)[-10:])
            if avg_latency > self.max_latency_ms:
                print(f"WARNING: Average latency {avg_latency:.1f}ms exceeds threshold {self.max_latency_ms}ms")
        
        if len(self.cpu_usage) > 5:
            avg_cpu = np.mean(list(self.cpu_usage)[-5:])
            if avg_cpu > 80:
                print(f"WARNING: High CPU usage {avg_cpu:.1f}%")
        
        if len(self.memory_usage) > 5:
            avg_memory = np.mean(list(self.memory_usage)[-5:])
            if avg_memory > 85:
                print(f"WARNING: High memory usage {avg_memory:.1f}%")
    
    def get_accuracy_metrics(self):
        """Calculate accuracy metrics"""
        if self.total_detections == 0:
            return {
                'accuracy': 0.0,
                'precision': 0.0,
                'recall': 0.0,
                'f1_score': 0.0
            }
        
        true_positives = self.total_detections - self.false_positives
        precision = true_positives / (true_positives + self.false_positives) if (true_positives + self.false_positives) > 0 else 0
        recall = true_positives / (true_positives + self.false_negatives) if (true_positives + self.false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = true_positives / self.total_detections
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'total_detections': self.total_detections,
            'false_positives': self.false_positives,
            'false_negatives': self.false_negatives
        }
    
    def get_latency_metrics(self):
        """Get latency statistics"""
        metrics = {}
        
        if self.detection_latencies:
            metrics['detection'] = {
                'avg_ms': np.mean(self.detection_latencies),
                'min_ms': np.min(self.detection_latencies),
                'max_ms': np.max(self.detection_latencies),
                'p95_ms': np.percentile(self.detection_latencies, 95),
                'samples': len(self.detection_latencies)
            }
        
        if self.processing_latencies:
            metrics['processing'] = {
                'avg_ms': np.mean(self.processing_latencies),
                'min_ms': np.min(self.processing_latencies),
                'max_ms': np.max(self.processing_latencies),
                'p95_ms': np.percentile(self.processing_latencies, 95),
                'samples': len(self.processing_latencies)
            }
        
        if self.audio_latencies:
            metrics['audio'] = {
                'avg_ms': np.mean(self.audio_latencies),
                'min_ms': np.min(self.audio_latencies),
                'max_ms': np.max(self.audio_latencies),
                'p95_ms': np.percentile(self.audio_latencies, 95),
                'samples': len(self.audio_latencies)
            }
        
        return metrics
    
    def get_system_metrics(self):
        """Get system resource metrics"""
        return {
            'cpu_usage': {
                'current': psutil.cpu_percent(),
                'avg': np.mean(self.cpu_usage) if self.cpu_usage else 0,
                'max': np.max(self.cpu_usage) if self.cpu_usage else 0
            },
            'memory_usage': {
                'current': psutil.virtual_memory().percent,
                'avg': np.mean(self.memory_usage) if self.memory_usage else 0,
                'max': np.max(self.memory_usage) if self.memory_usage else 0
            },
            'battery_level': self.battery_level,
            'uptime_seconds': time.time() - self.start_time if self.start_time else 0
        }
    
    def get_performance_summary(self):
        """Get comprehensive performance summary"""
        accuracy_metrics = self.get_accuracy_metrics()
        latency_metrics = self.get_latency_metrics()
        system_metrics = self.get_system_metrics()
        
        # Check if system meets proposal requirements
        meets_latency = True
        meets_accuracy = True
        
        if latency_metrics.get('detection', {}).get('avg_ms', 0) > self.max_latency_ms:
            meets_latency = False
        
        if accuracy_metrics['accuracy'] < self.target_accuracy:
            meets_accuracy = False
        
        return {
            'accuracy_metrics': accuracy_metrics,
            'latency_metrics': latency_metrics,
            'system_metrics': system_metrics,
            'requirements_met': {
                'latency_under_200ms': meets_latency,
                'accuracy_above_90_percent': meets_accuracy,
                'overall': meets_latency and meets_accuracy
            },
            'proposal_targets': {
                'max_latency_ms': self.max_latency_ms,
                'target_accuracy': self.target_accuracy
            }
        }
    
    def save_metrics_to_file(self, filename=None):
        """Save metrics to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_metrics_{timestamp}.json"
        
        metrics = self.get_performance_summary()
        
        # Add raw data for analysis
        metrics['raw_data'] = {
            'detection_latencies': list(self.detection_latencies),
            'processing_latencies': list(self.processing_latencies),
            'audio_latencies': list(self.audio_latencies),
            'obstacle_detections': list(self.obstacle_detections),
            'object_detections': list(self.object_detections),
            'sign_detections': list(self.sign_detections)
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(metrics, f, indent=2)
            print(f"Performance metrics saved to {filename}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def print_performance_report(self):
        """Print a formatted performance report"""
        summary = self.get_performance_summary()
        
        print("\n" + "="*60)
        print("INTELLIGENT EYE - PERFORMANCE REPORT")
        print("="*60)
        
        # Accuracy metrics
        acc = summary['accuracy_metrics']
        print(f"\nACCURACY METRICS:")
        print(f"  Overall Accuracy: {acc['accuracy']:.2%}")
        print(f"  Precision: {acc['precision']:.2%}")
        print(f"  Recall: {acc['recall']:.2%}")
        print(f"  F1-Score: {acc['f1_score']:.2%}")
        print(f"  Total Detections: {acc['total_detections']}")
        print(f"  False Positives: {acc['false_positives']}")
        print(f"  False Negatives: {acc['false_negatives']}")
        
        # Latency metrics
        lat = summary['latency_metrics']
        print(f"\nLATENCY METRICS:")
        if 'detection' in lat:
            d = lat['detection']
            print(f"  Detection Latency: {d['avg_ms']:.1f}ms avg, {d['p95_ms']:.1f}ms p95")
        if 'processing' in lat:
            p = lat['processing']
            print(f"  Processing Latency: {p['avg_ms']:.1f}ms avg, {p['p95_ms']:.1f}ms p95")
        if 'audio' in lat:
            a = lat['audio']
            print(f"  Audio Latency: {a['avg_ms']:.1f}ms avg, {a['p95_ms']:.1f}ms p95")
        
        # System metrics
        sys = summary['system_metrics']
        print(f"\nSYSTEM METRICS:")
        print(f"  CPU Usage: {sys['cpu_usage']['current']:.1f}% (avg: {sys['cpu_usage']['avg']:.1f}%)")
        print(f"  Memory Usage: {sys['memory_usage']['current']:.1f}% (avg: {sys['memory_usage']['avg']:.1f}%)")
        print(f"  Battery Level: {sys['battery_level']:.1f}%")
        print(f"  Uptime: {sys['uptime_seconds']:.1f} seconds")
        
        # Requirements check
        req = summary['requirements_met']
        print(f"\nPROPOSAL REQUIREMENTS:")
        print(f"  Latency < 200ms: {'✓ PASS' if req['latency_under_200ms'] else '✗ FAIL'}")
        print(f"  Accuracy > 90%: {'✓ PASS' if req['accuracy_above_90_percent'] else '✗ FAIL'}")
        print(f"  Overall: {'✓ PASS' if req['overall'] else '✗ FAIL'}")
        
        print("="*60)

# Context manager for easy performance monitoring
class PerformanceContext:
    def __init__(self, monitor, operation_type="general"):
        self.monitor = monitor
        self.operation_type = operation_type
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            end_time = time.time()
            self.monitor.record_detection_latency(
                self.start_time, end_time, self.operation_type
            )

# Test function
if __name__ == "__main__":
    monitor = PerformanceMonitor()
    
    try:
        monitor.start_monitoring()
        
        # Simulate some detections
        for i in range(10):
            with PerformanceContext(monitor, "obstacle"):
                time.sleep(0.05)  # Simulate processing
            
            with PerformanceContext(monitor, "object"):
                time.sleep(0.08)  # Simulate processing
            
            time.sleep(0.5)
        
        # Print report
        monitor.print_performance_report()
        
    except KeyboardInterrupt:
        print("Stopping performance monitor test")
    finally:
        monitor.stop_monitoring()
        monitor.save_metrics_to_file()
