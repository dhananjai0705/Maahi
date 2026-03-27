"""
Motor Control Module for Maahi Robot Assistant
Handles movement control - forward, backward, left turn, right turn, stop
Works with 4-wheel motor setup and motor driver
"""

import RPi.GPIO as GPIO
import time
import logging
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MotorControl:
    """
    Controls the 4 motors for the robot's movement
    Uses GPIO pins and PWM for speed control
    """

    def __init__(self):
        """Initialize GPIO pins and motor setup"""
        # Set GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Define motor pins
        self.left_forward = MOTOR_LEFT_FORWARD
        self.left_backward = MOTOR_LEFT_BACKWARD
        self.right_forward = MOTOR_RIGHT_FORWARD
        self.right_backward = MOTOR_RIGHT_BACKWARD
        self.pwm_pin = MOTOR_PWM_PIN
        
        # Setup all pins as outputs
        pins = [
            self.left_forward,
            self.left_backward,
            self.right_forward,
            self.right_backward,
            self.pwm_pin
        ]
        
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        
        # Setup PWM for speed control (50 Hz frequency)
        self.pwm = GPIO.PWM(self.pwm_pin, 50)
        self.pwm.start(0)
        
        self.current_speed = MOTOR_SPEED
        self.is_moving = False
        
        logger.info("Motor Control initialized")

    def set_speed(self, speed):
        """
        Set motor speed (0-100)
        
        Args:
            speed (int): Speed percentage (0-100)
        """
        speed = max(0, min(100, speed))  # Clamp between 0-100
        self.current_speed = speed
        self.pwm.ChangeDutyCycle(speed)
        logger.info(f"Motor speed set to {speed}%")

    def move_forward(self, duration=None):
        """
        Move robot forward
        
        Args:
            duration (float): Optional duration in seconds
        """
        logger.info("Moving forward...")
        GPIO.output(self.left_forward, GPIO.HIGH)
        GPIO.output(self.left_backward, GPIO.LOW)
        GPIO.output(self.right_forward, GPIO.HIGH)
        GPIO.output(self.right_backward, GPIO.LOW)
        
        self.is_moving = True
        
        if duration:
            time.sleep(duration)
            self.stop()

    def move_backward(self, duration=None):
        """
        Move robot backward
        
        Args:
            duration (float): Optional duration in seconds
        """
        logger.info("Moving backward...")
        GPIO.output(self.left_forward, GPIO.LOW)
        GPIO.output(self.left_backward, GPIO.HIGH)
        GPIO.output(self.right_forward, GPIO.LOW)
        GPIO.output(self.right_backward, GPIO.HIGH)
        
        self.is_moving = True
        
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_left(self, duration=None):
        """
        Turn robot left (rotate in place)
        
        Args:
            duration (float): Optional duration in seconds
        """
        logger.info("Turning left...")
        GPIO.output(self.left_forward, GPIO.LOW)
        GPIO.output(self.left_backward, GPIO.HIGH)
        GPIO.output(self.right_forward, GPIO.HIGH)
        GPIO.output(self.right_backward, GPIO.LOW)
        
        self.is_moving = True
        
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_right(self, duration=None):
        """
        Turn robot right (rotate in place)
        
        Args:
            duration (float): Optional duration in seconds
        """
        logger.info("Turning right...")
        GPIO.output(self.left_forward, GPIO.HIGH)
        GPIO.output(self.left_backward, GPIO.LOW)
        GPIO.output(self.right_forward, GPIO.LOW)
        GPIO.output(self.right_backward, GPIO.HIGH)
        
        self.is_moving = True
        
        if duration:
            time.sleep(duration)
            self.stop()

    def move_diagonally_left(self, duration=None):
        """
        Move diagonally left (forward-left)
        
        Args:
            duration (float): Optional duration in seconds
        """
        logger.info("Moving diagonally left...")
        GPIO.output(self.left_forward, GPIO.LOW)
        GPIO.output(self.left_backward, GPIO.LOW)
        GPIO.output(self.right_forward, GPIO.HIGH)
        GPIO.output(self.right_backward, GPIO.LOW)
        
        self.is_moving = True
        
        if duration:
            time.sleep(duration)
            self.stop()

    def move_diagonally_right(self, duration=None):
        """
        Move diagonally right (forward-right)
        
        Args:
            duration (float): Optional duration in seconds
        """
        logger.info("Moving diagonally right...")
        GPIO.output(self.left_forward, GPIO.HIGH)
        GPIO.output(self.left_backward, GPIO.LOW)
        GPIO.output(self.right_forward, GPIO.LOW)
        GPIO.output(self.right_backward, GPIO.LOW)
        
        self.is_moving = True
        
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        """Stop all motor movement"""
        logger.info("Stopping...")
        GPIO.output(self.left_forward, GPIO.LOW)
        GPIO.output(self.left_backward, GPIO.LOW)
        GPIO.output(self.right_forward, GPIO.LOW)
        GPIO.output(self.right_backward, GPIO.LOW)
        
        self.is_moving = False

    def cleanup(self):
        """Clean up GPIO pins"""
        logger.info("Cleaning up motor control...")
        self.stop()
        self.pwm.stop()
        GPIO.cleanup()


# Test function
if __name__ == "__main__":
    print("Motor Control Module Test")
    print("=" * 50)
    print("\nWARNING: This will move your robot!")
    print("Make sure the robot is on a safe surface.")
    
    try:
        input("Press Enter to start motor test...")
        
        motor = MotorControl()
        motor.set_speed(50)  # Set to 50% speed
        
        # Test forward
        print("\n1. Moving forward for 2 seconds...")
        motor.move_forward(2)
        time.sleep(1)
        
        # Test backward
        print("2. Moving backward for 2 seconds...")
        motor.move_backward(2)
        time.sleep(1)
        
        # Test left turn
        print("3. Turning left for 2 seconds...")
        motor.turn_left(2)
        time.sleep(1)
        
        # Test right turn
        print("4. Turning right for 2 seconds...")
        motor.turn_right(2)
        time.sleep(1)
        
        print("\n✓ Motor test completed!")
        
    except Exception as e:
        print(f"Error during motor test: {e}")
    finally:
        motor.cleanup()
