"""
Voice Input Module for Maahi Robot Assistant
Handles microphone input, wake word detection, and voice-to-text conversion
"""

import speech_recognition as sr
import logging
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceInput:
    """
    Handles voice input from USB microphone
    Converts speech to text using Google's speech recognition API
    """

    def __init__(self):
        """Initialize voice recognizer"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            logger.info("Microphone calibrated for ambient noise")

    def listen_for_wake_word(self):
        """
        Listen continuously for wake word
        Returns True when wake word is detected
        """
        logger.info(f"Listening for wake word: '{WAKE_WORD}'")
        
        with self.microphone as source:
            try:
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=LISTEN_TIMEOUT)
                
                # Convert speech to text
                text = self.recognizer.recognize_google(audio, language=VOICE_LANGUAGE)
                logger.info(f"Heard: {text}")
                
                # Check if wake word is present in the text
                if WAKE_WORD.lower() in text.lower():
                    logger.info("Wake word detected!")
                    return True
                
                return False
                
            except sr.UnknownValueError:
                logger.debug("Could not understand audio")
                return False
            except sr.RequestError as e:
                logger.error(f"Error with speech recognition service: {e}")
                return False
            except Exception as e:
                logger.error(f"Error listening for wake word: {e}")
                return False

    def listen_for_command(self):
        """
        Listen for voice commands after wake word is detected
        Returns the spoken text or None if not understood
        """
        logger.info("Listening for command...")
        
        with self.microphone as source:
            try:
                # Listen for command with timeout
                audio = self.recognizer.listen(source, timeout=LISTEN_TIMEOUT)
                
                # Convert speech to text
                text = self.recognizer.recognize_google(audio, language=VOICE_LANGUAGE)
                logger.info(f"Command received: {text}")
                
                # Check if user said close word
                if CLOSE_WORD.lower() in text.lower():
                    logger.info("Close word detected - shutting down")
                    return CLOSE_WORD
                
                return text
                
            except sr.UnknownValueError:
                logger.warning("Could not understand command")
                return None
            except sr.RequestError as e:
                logger.error(f"Error with speech recognition service: {e}")
                return None
            except Exception as e:
                logger.error(f"Error listening for command: {e}")
                return None

    def listen_for_search_query(self):
        """
        Listen for search or music queries
        Returns the spoken text
        """
        logger.info("Listening for query...")
        
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(source, timeout=LISTEN_TIMEOUT)
                text = self.recognizer.recognize_google(audio, language=VOICE_LANGUAGE)
                logger.info(f"Query received: {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning("Could not understand query")
                return None
            except sr.RequestError as e:
                logger.error(f"Error with speech recognition service: {e}")
                return None
            except Exception as e:
                logger.error(f"Error listening for query: {e}")
                return None


# Simple test
if __name__ == "__main__":
    print("Voice Input Module Test")
    print("=" * 50)
    
    voice = VoiceInput()
    
    print("\nTesting wake word detection...")
    print(f"Say something with '{WAKE_WORD}' in it...")
    if voice.listen_for_wake_word():
        print("✓ Wake word detected!")
        
        print(f"\nNow say a command...")
        command = voice.listen_for_command()
        if command:
            print(f"✓ Command received: {command}")
    else:
        print("✗ Wake word not detected")
