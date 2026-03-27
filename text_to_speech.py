"""
Text-to-Speech Module for Maahi Robot Assistant
Converts text responses to Indian female voice audio and plays through speaker
"""

import logging
import os
import subprocess
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import pyttsx3
except ImportError:
    logger.warning("pyttsx3 not installed. Install: pip install pyttsx3")


class TextToSpeech:
    """
    Converts text to speech with Indian female voice
    Outputs audio through USB speaker
    """

    def __init__(self):
        """Initialize text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            
            # Set female voice
            self.set_female_voice()
            
            # Set voice properties
            self.engine.setProperty('rate', 150)  # Speech rate (words per minute)
            self.engine.setProperty('volume', SPEAKER_VOLUME / 100.0)  # Volume (0-1)
            
            logger.info("Text-to-Speech engine initialized with female voice")
            
        except Exception as e:
            logger.warning(f"pyttsx3 initialization failed: {e}")
            logger.info("Falling back to espeak/festival for TTS")
            self.engine = None

    def set_female_voice(self):
        """
        Set voice to female (preferably Indian accent if available)
        """
        try:
            voices = self.engine.getProperty('voices')
            
            # Look for female voice
            female_voice = None
            indian_female_voice = None
            
            for voice in voices:
                voice_name = voice.name.lower()
                
                # Prioritize Indian female voice
                if "indian" in voice_name and "female" in voice_name:
                    indian_female_voice = voice.id
                elif "female" in voice_name:
                    female_voice = voice.id
            
            # Use Indian female voice if available, otherwise female voice
            if indian_female_voice:
                self.engine.setProperty('voice', indian_female_voice)
                logger.info("Set voice to Indian female")
            elif female_voice:
                self.engine.setProperty('voice', female_voice)
                logger.info("Set voice to female")
            else:
                logger.warning("Female voice not available, using default")
                
        except Exception as e:
            logger.warning(f"Error setting female voice: {e}")

    def speak(self, text):
        """
        Convert text to speech and play through speaker
        
        Args:
            text (str): Text to speak
        """
        try:
            if not text:
                return
            
            logger.info(f"Speaking: {text}")
            
            if self.engine:
                # Using pyttsx3
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Fallback to espeak
                self._speak_espeak(text)
                
        except Exception as e:
            logger.error(f"Error in speak: {e}")

    def _speak_espeak(self, text):
        """
        Fallback text-to-speech using espeak command
        Requires espeak to be installed on the system
        
        Args:
            text (str): Text to speak
        """
        try:
            # Use espeak with Indian English voice if available
            cmd = [
                "espeak",
                "-v", "en-in+female3",  # Indian English female voice
                "-s", "150",  # Speed
                "-a", str(SPEAKER_VOLUME),  # Amplitude/volume
                text
            ]
            
            subprocess.run(cmd, check=True)
            logger.info("Spoke using espeak")
            
        except FileNotFoundError:
            logger.error("espeak not found. Install: sudo apt-get install espeak")
        except Exception as e:
            logger.error(f"Error with espeak: {e}")

    def speak_to_file(self, text, filename):
        """
        Save speech to audio file
        
        Args:
            text (str): Text to speak
            filename (str): Output audio file name
        """
        try:
            logger.info(f"Saving speech to file: {filename}")
            
            if self.engine:
                self.engine.save_to_file(text, filename)
                self.engine.runAndWait()
            else:
                # Use espeak to save to file
                output_path = os.path.join(TEMP_DIR, filename)
                cmd = [
                    "espeak",
                    "-v", "en-in+female3",
                    "-w", output_path,
                    text
                ]
                subprocess.run(cmd, check=True)
                
            logger.info(f"Saved to: {filename}")
            
        except Exception as e:
            logger.error(f"Error saving to file: {e}")

    def set_rate(self, rate):
        """
        Set speech rate
        
        Args:
            rate (int): Rate in words per minute (typically 50-300)
        """
        try:
            if self.engine:
                self.engine.setProperty('rate', rate)
                logger.info(f"Speech rate set to {rate} WPM")
        except Exception as e:
            logger.error(f"Error setting rate: {e}")

    def set_volume(self, volume):
        """
        Set speaker volume
        
        Args:
            volume (int): Volume level (0-100)
        """
        try:
            volume = max(0, min(100, volume))
            
            if self.engine:
                self.engine.setProperty('volume', volume / 100.0)
            
            # Also set system volume
            os.system(f"amixer set Master {volume}%")
            logger.info(f"Volume set to {volume}%")
            
        except Exception as e:
            logger.error(f"Error setting volume: {e}")

    def speak_with_emotion(self, text, emotion="neutral"):
        """
        Speak text with emotional variation
        
        Args:
            text (str): Text to speak
            emotion (str): Emotion type ("happy", "sad", "angry", "neutral")
        """
        try:
            # Adjust rate based on emotion
            emotion_rates = {
                "happy": 180,
                "sad": 120,
                "angry": 200,
                "neutral": 150
            }
            
            rate = emotion_rates.get(emotion, 150)
            self.set_rate(rate)
            self.speak(text)
            
        except Exception as e:
            logger.error(f"Error speaking with emotion: {e}")


# Test function
if __name__ == "__main__":
    print("Text-to-Speech Module Test")
    print("=" * 50)
    
    tts = TextToSpeech()
    
    # Test basic speech
    print("\n1. Testing basic speech...")
    print("Speaking: Hello! I am Maahi, your robot assistant.")
    tts.speak("Hello! I am Maahi, your robot assistant.")
    
    # Test different speeds
    print("\n2. Testing different speeds...")
    speeds = [120, 150, 180]
    for speed in speeds:
        print(f"Speaking at {speed} WPM...")
        tts.set_rate(speed)
        tts.speak("This is a test at different speeds")
        
        import time
        time.sleep(1)
    
    # Test emotions
    print("\n3. Testing different emotions...")
    tts.set_rate(150)
    emotions = ["happy", "sad", "angry", "neutral"]
    for emotion in emotions:
        print(f"Speaking with {emotion} emotion...")
        tts.speak_with_emotion("How are you today?", emotion)
        
        import time
        time.sleep(1)
    
    print("\n✓ Text-to-Speech test completed!")
