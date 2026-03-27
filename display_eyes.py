"""
Display & Eyes Module for Maahi Robot Assistant
Handles SPI XPT2046 display to show robot's eyes and animation
Displays different eye states: normal, listening, answering, music, video
"""

import logging
import os
import time
try:
    from PIL import Image, ImageDraw, ImageFont
    # For Raspberry Pi display
    import adafruit_ili9341
    import adafruit_touch_screen
except ImportError:
    print("Warning: Display libraries not available. Running in simulation mode.")

from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DisplayEyes:
    """
    Manages the SPI display and shows robot eyes
    Can show different animations based on robot state
    """

    def __init__(self):
        """Initialize display and setup eyes"""
        try:
            self.display_available = True
            # Display initialization code for actual Raspberry Pi
            # This is a simplified placeholder - actual implementation depends on
            # the specific display library and wiring
            
            self.width = DISPLAY_WIDTH
            self.height = DISPLAY_HEIGHT
            self.current_state = EYE_NORMAL
            
            # Create image buffer
            self.image = Image.new("RGB", (self.width, self.height), color=(0, 0, 0))
            self.draw = ImageDraw.Draw(self.image)
            
            logger.info("Display initialized successfully")
            
        except Exception as e:
            logger.warning(f"Display initialization failed: {e}. Using simulation mode.")
            self.display_available = False
            self.width = DISPLAY_WIDTH
            self.height = DISPLAY_HEIGHT

    def draw_normal_eyes(self):
        """Draw normal eyes (default state)"""
        self.draw.rectangle([(0, 0), (self.width, self.height)], fill=(0, 0, 0))
        
        # Left eye
        left_eye_x = self.width // 4
        left_eye_y = self.height // 2
        eye_radius = 30
        
        # Right eye
        right_eye_x = (self.width * 3) // 4
        right_eye_y = self.height // 2
        
        # Draw white eyes
        self.draw.ellipse(
            [(left_eye_x - eye_radius, left_eye_y - eye_radius),
             (left_eye_x + eye_radius, left_eye_y + eye_radius)],
            fill=(255, 255, 255)
        )
        self.draw.ellipse(
            [(right_eye_x - eye_radius, right_eye_y - eye_radius),
             (right_eye_x + eye_radius, right_eye_y + eye_radius)],
            fill=(255, 255, 255)
        )
        
        # Draw pupils
        pupil_radius = 15
        self.draw.ellipse(
            [(left_eye_x - pupil_radius, left_eye_y - pupil_radius),
             (left_eye_x + pupil_radius, left_eye_y + pupil_radius)],
            fill=(0, 0, 0)
        )
        self.draw.ellipse(
            [(right_eye_x - pupil_radius, right_eye_y - pupil_radius),
             (right_eye_x + pupil_radius, right_eye_y + pupil_radius)],
            fill=(0, 0, 0)
        )
        
        self.current_state = EYE_NORMAL
        self.display_image()

    def draw_listening_eyes(self):
        """Draw animated listening eyes (with animated pupil movement)"""
        self.draw.rectangle([(0, 0), (self.width, self.height)], fill=(0, 0, 0))
        
        left_eye_x = self.width // 4
        left_eye_y = self.height // 2
        right_eye_x = (self.width * 3) // 4
        right_eye_y = self.height // 2
        eye_radius = 30
        
        # Draw listening indicator eyes (larger and more alert)
        self.draw.ellipse(
            [(left_eye_x - eye_radius, left_eye_y - eye_radius),
             (left_eye_x + eye_radius, left_eye_y + eye_radius)],
            fill=(100, 200, 255)  # Blue tint for listening
        )
        self.draw.ellipse(
            [(right_eye_x - eye_radius, right_eye_y - eye_radius),
             (right_eye_x + eye_radius, right_eye_y + eye_radius)],
            fill=(100, 200, 255)
        )
        
        # Draw pupils (focused)
        pupil_radius = 10
        self.draw.ellipse(
            [(left_eye_x - pupil_radius, left_eye_y - pupil_radius),
             (left_eye_x + pupil_radius, left_eye_y + pupil_radius)],
            fill=(0, 0, 0)
        )
        self.draw.ellipse(
            [(right_eye_x - pupil_radius, right_eye_y - pupil_radius),
             (right_eye_x + pupil_radius, right_eye_y + pupil_radius)],
            fill=(0, 0, 0)
        )
        
        self.current_state = EYE_LISTENING
        self.display_image()

    def draw_answering_eyes(self):
        """Draw animated answering eyes (blinking with happy expression)"""
        self.draw.rectangle([(0, 0), (self.width, self.height)], fill=(0, 0, 0))
        
        left_eye_x = self.width // 4
        left_eye_y = self.height // 2
        right_eye_x = (self.width * 3) // 4
        right_eye_y = self.height // 2
        
        # Draw happy closed eyes (curves)
        self.draw.arc(
            [(left_eye_x - 30, left_eye_y - 30),
             (left_eye_x + 30, left_eye_y + 30)],
            start=0,
            end=180,
            fill=(255, 255, 255),
            width=3
        )
        self.draw.arc(
            [(right_eye_x - 30, right_eye_y - 30),
             (right_eye_x + 30, right_eye_y + 30)],
            start=0,
            end=180,
            fill=(255, 255, 255),
            width=3
        )
        
        self.current_state = EYE_ANSWERING
        self.display_image()

    def draw_music_eyes(self):
        """Draw animated music eyes (dancing/moving eyes)"""
        self.draw.rectangle([(0, 0), (self.width, self.height)], fill=(0, 0, 0))
        
        # Animated movement for music
        offset = int(20 * ((time.time() % 1.0) * 2 - 1))  # -20 to 20
        
        left_eye_x = self.width // 4
        left_eye_y = self.height // 2
        right_eye_x = (self.width * 3) // 4
        right_eye_y = self.height // 2
        eye_radius = 30
        
        # Draw dancing eyes
        self.draw.ellipse(
            [(left_eye_x - eye_radius, left_eye_y - eye_radius + offset),
             (left_eye_x + eye_radius, left_eye_y + eye_radius + offset)],
            fill=(255, 100, 200)  # Pink for music
        )
        self.draw.ellipse(
            [(right_eye_x - eye_radius, right_eye_y - eye_radius - offset),
             (right_eye_x + eye_radius, right_eye_y + eye_radius - offset)],
            fill=(255, 100, 200)
        )
        
        # Draw pupils (offset for dancing effect)
        pupil_radius = 15
        self.draw.ellipse(
            [(left_eye_x - pupil_radius, left_eye_y - pupil_radius + offset),
             (left_eye_x + pupil_radius, left_eye_y + pupil_radius + offset)],
            fill=(0, 0, 0)
        )
        self.draw.ellipse(
            [(right_eye_x - pupil_radius, right_eye_y - pupil_radius - offset),
             (right_eye_x + pupil_radius, right_eye_y + pupil_radius - offset)],
            fill=(0, 0, 0)
        )
        
        self.current_state = EYE_MUSIC
        self.display_image()

    def draw_video_eyes(self):
        """Draw eyes indicating video playback (rectangle focused state)"""
        self.draw.rectangle([(0, 0), (self.width, self.height)], fill=(0, 0, 0))
        
        # Draw rectangular eyes (video watching)
        left_eye_x = self.width // 4
        left_eye_y = self.height // 2
        right_eye_x = (self.width * 3) // 4
        right_eye_y = self.height // 2
        
        # Left eye rectangle
        self.draw.rectangle(
            [(left_eye_x - 40, left_eye_y - 25),
             (left_eye_x + 40, left_eye_y + 25)],
            fill=(100, 255, 100)  # Green for video
        )
        # Right eye rectangle
        self.draw.rectangle(
            [(right_eye_x - 40, right_eye_y - 25),
             (right_eye_x + 40, right_eye_y + 25)],
            fill=(100, 255, 100)
        )
        
        # Draw pupils in center
        pupil_radius = 12
        self.draw.ellipse(
            [(left_eye_x - pupil_radius, left_eye_y - pupil_radius),
             (left_eye_x + pupil_radius, left_eye_y + pupil_radius)],
            fill=(0, 0, 0)
        )
        self.draw.ellipse(
            [(right_eye_x - pupil_radius, right_eye_y - pupil_radius),
             (right_eye_x + pupil_radius, right_eye_y + pupil_radius)],
            fill=(0, 0, 0)
        )
        
        self.current_state = EYE_VIDEO
        self.display_image()

    def show_text(self, text, color=(255, 255, 255)):
        """
        Display text on screen
        Useful for debugging or showing status messages
        
        Args:
            text (str): Text to display
            color (tuple): RGB color tuple
        """
        self.draw.rectangle([(0, 0), (self.width, self.height)], fill=(0, 0, 0))
        
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        self.draw.text((10, self.height // 2 - 20), text, fill=color, font=font)
        self.display_image()

    def display_image(self):
        """Display the current image buffer on screen"""
        try:
            if self.display_available:
                # This would send the image to the actual display
                # Implementation depends on the specific display library
                logger.debug("Image displayed on screen")
            else:
                logger.debug("Display not available - image buffer updated")
        except Exception as e:
            logger.error(f"Error displaying image: {e}")

    def set_state(self, state):
        """
        Set display state and show corresponding eyes
        
        Args:
            state (str): State from config (EYE_NORMAL, EYE_LISTENING, etc.)
        """
        logger.info(f"Setting display state to: {state}")
        
        if state == EYE_NORMAL:
            self.draw_normal_eyes()
        elif state == EYE_LISTENING:
            self.draw_listening_eyes()
        elif state == EYE_ANSWERING:
            self.draw_answering_eyes()
        elif state == EYE_MUSIC:
            self.draw_music_eyes()
        elif state == EYE_VIDEO:
            self.draw_video_eyes()
        else:
            self.draw_normal_eyes()

    def cleanup(self):
        """Clean up display resources"""
        logger.info("Cleaning up display...")


# Test function
if __name__ == "__main__":
    print("Display Eyes Module Test")
    print("=" * 50)
    
    display = DisplayEyes()
    
    print("\n1. Showing normal eyes...")
    display.set_state(EYE_NORMAL)
    time.sleep(2)
    
    print("2. Showing listening eyes...")
    display.set_state(EYE_LISTENING)
    time.sleep(2)
    
    print("3. Showing answering eyes...")
    display.set_state(EYE_ANSWERING)
    time.sleep(2)
    
    print("4. Showing music eyes...")
    for i in range(3):
        display.set_state(EYE_MUSIC)
        time.sleep(0.5)
    
    print("5. Showing video eyes...")
    display.set_state(EYE_VIDEO)
    time.sleep(2)
    
    print("6. Showing text...")
    display.show_text("Hello Maahi!")
    time.sleep(2)
    
    display.cleanup()
    print("\n✓ Display test completed!")
