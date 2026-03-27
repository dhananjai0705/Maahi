"""
Obstacle Detection Module for Maahi Robot Assistant
Handles ultrasonic sensor for obstacle detection
Prevents robot from hitting objects while moving
"""

import RPi.GPIO as GPIO
import time
import logging
import threading
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ObstacleDetection:
    """
    Detects obstacles using ultrasonic sensor
    Prevents robot collision with objects
    """

    def __init__(self):
        """Initialize ultrasonic sensor pins"""
        # Set GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.trig_pin = SENSOR_TRIG_PIN
        self.echo_pin = SENSOR_ECHO_PIN
        
        # Setup pins
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        # Initial state
        GPIO.output(self.trig_pin, GPIO.LOW)
        time.sleep(0.5)  # Let sensor stabilize
        
        self.obstacle_detected = False
        self.current_distance = 0
        self.is_running = False
        
        logger.info("Obstacle Detection initialized")

    def get_distance(self):
        """
        Measure distance to nearest obstacle
        
        Returns:
            float: Distance in centimeters (or -1 if error)
        """
        try:
            # Send ultrasonic pulse
            GPIO.output(self.trig_pin, GPIO.HIGH)
            time.sleep(0.00001)  # 10 microseconds
            GPIO.output(self.trig_pin, GPIO.LOW)
            
            # Record the time when pulse starts
            start_time = time.time()
            timeout = time.time() + 1  # 1 second timeout
            
            # Wait for echo to start
            while GPIO.input(self.echo_pin) == 0:
                start_time = time.time()
                if time.time() > timeout:
                    logger.warning("Timeout waiting for echo start")
                    return -1
            
            # Wait for echo to end
            while GPIO.input(self.echo_pin) == 1:
                end_time = time.time()
                if end_time - start_time > 0.1:  # Timeout after 0.1 seconds
                    logger.warning("Timeout waiting for echo end")
                    return -1
            
            # Calculate distance
            pulse_duration = end_time - start_time
            distance = (pulse_duration * 34300) / 2  # Speed of sound = 34300 cm/s
            
            self.current_distance = distance
            return distance
            
        except Exception as e:
            logger.error(f"Error measuring distance: {e}")
            return -1

    def is_obstacle_ahead(self):
        """
        Check if there's an obstacle within threshold distance
        
        Returns:
            bool: True if obstacle detected, False otherwise
        """
        distance = self.get_distance()
        
        if distance < 0:
            return False
        
        if distance < OBSTACLE_DISTANCE_THRESHOLD:
            logger.warning(f"Obstacle detected at {distance:.2f} cm")
            self.obstacle_detected = True
            return True
        else:
            self.obstacle_detected = False
            return False

    def continuous_monitoring(self):
        """
        Continuously monitor for obstacles
        This runs in a separate thread
        """
        logger.info("Starting continuous obstacle monitoring")
        self.is_running = True
        
        while self.is_running:
            try:
                self.is_obstacle_ahead()
                time.sleep(CHECK_OBSTACLE_INTERVAL)
            except Exception as e:
                logger.error(f"Error in continuous monitoring: {e}")

    def start_monitoring_thread(self):
        """Start obstacle monitoring in a background thread"""
        monitor_thread = threading.Thread(target=self.continuous_monitoring, daemon=True)
        monitor_thread.start()
        logger.info("Obstacle monitoring thread started")
        return monitor_thread

    def stop_monitoring(self):
        """Stop continuous obstacle monitoring"""
        self.is_running = False
        logger.info("Obstacle monitoring stopped")

    def get_safe_distance(self):
        """
        Get current distance and safety status
        
        Returns:
            dict: Dictionary with distance and safety information
        """
        distance = self.get_distance()
        
        return {
            "distance": distance if distance > 0 else None,
            "is_safe": distance >= OBSTACLE_DISTANCE_THRESHOLD if distance > 0 else True,
            "obstacle_detected": self.obstacle_detected,
            "threshold": OBSTACLE_DISTANCE_THRESHOLD
        }

    def set_threshold(self, distance_cm):
        """
        Set custom obstacle detection threshold
        
        Args:
            distance_cm (float): Distance threshold in centimeters
        """
        global OBSTACLE_DISTANCE_THRESHOLD
        OBSTACLE_DISTANCE_THRESHOLD = distance_cm
        logger.info(f"Obstacle threshold set to {distance_cm} cm")

    def calibrate(self):
        """
        Calibrate sensor by averaging multiple readings
        
        Returns:
            float: Average distance reading
        """
        logger.info("Calibrating sensor...")
        readings = []
        
        for i in range(10):
            distance = self.get_distance()
            if distance > 0:
                readings.append(distance)
            time.sleep(0.1)
        
        if readings:
            average = sum(readings) / len(readings)
            logger.info(f"Calibration complete. Average distance: {average:.2f} cm")
            return average
        else:
            logger.error("Calibration failed - no valid readings")
            return -1

    def cleanup(self):
        """Clean up GPIO pins"""
        logger.info("Cleaning up obstacle detection...")
        self.stop_monitoring()
        GPIO.cleanup()


# Test function
if __name__ == "__main__":
    print("Obstacle Detection Module Test")
    print("=" * 50)
    print(f"\nThreshold distance: {OBSTACLE_DISTANCE_THRESHOLD} cm")
    print("Place your hand at different distances from the sensor\n")
    
    try:
        sensor = ObstacleDetection()
        
        # Calibrate
        print("1. Calibrating sensor...")
        sensor.calibrate()
        
        # Test single reading
        print("\n2. Testing single distance reading...")
        distance = sensor.get_distance()
        print(f"Distance: {distance:.2f} cm" if distance > 0 else "Error reading sensor")
        
        # Test obstacle detection
        print("\n3. Testing obstacle detection (10 readings)...")
        for i in range(10):
            info = sensor.get_safe_distance()
            status = "✓ SAFE" if info['is_safe'] else "✗ OBSTACLE"
            dist = f"{info['distance']:.2f}" if info['distance'] else "N/A"
            print(f"  Reading {i+1}: {dist} cm - {status}")
            time.sleep(0.5)
        
        print("\n✓ Obstacle detection test completed!")
        
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        sensor.cleanup()
