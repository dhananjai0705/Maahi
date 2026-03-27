"""
Voice Input Module for Maahi Robot Assistant
Handles microphone input, wake word detection, and voice-to-text conversion
Uses ALSA (arecord) for microphone, processes with SpeechRecognition
"""

import speech_recognition as sr
import subprocess
import logging
import os
import time
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceInput:
    """
    Handles voice input from USB microphone via ALSA
    Converts speech to text using Google's speech recognition API
    Uses arecord instead of PyAudio for microphone access
    """

    def __init__(self):
        """Initialize voice recognizer"""
        self.recognizer = sr.Recognizer()
        self.device = "hw:3,0"  # PCM2902 audio codec
        self.temp_file = "/tmp/voice_input.wav"
        logger.info("Voice input initialized (using ALSA)")

    def _record_audio(self, duration=5):
        """
        Record audio using arecord (ALSA)
        
        Args:
            duration (int): Recording duration in seconds
            
        Returns:
            str: Path to recorded WAV file, or None if recording failed
        """
        try:
            logger.info(f"Recording {duration} seconds from {self.device}...")
            cmd = [
                "arecord",
                "-D", self.device,
                "-f", "S16_LE",
                "-c", "1",
                "-r", "16000",
                "-d", str(duration),
                self.temp_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=duration + 5)
            
            if result.returncode == 0 and os.path.exists(self.temp_file):
                file_size = os.path.getsize(self.temp_file)
                logger.info(f"Audio recorded: {self.temp_file} ({file_size} bytes)")
                return self.temp_file
            else:
                logger.error(f"Recording failed: {result.stderr.decode()}")
                return None
                
        except Exception as e:
            logger.error(f"Error recording audio: {e}")
            return None

    def _recognize_from_file(self, audio_file, max_retries=3):
        """
        Recognize speech from a WAV file with retry logic
        
        Args:
            audio_file (str): Path to WAV file
            max_retries (int): Number of retry attempts
            
        Returns:
            str: Recognized text, or None if recognition failed
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Recognizing speech (attempt {attempt + 1}/{max_retries})...")
                
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
                
                text = self.recognizer.recognize_google(
                    audio, 
                    language=VOICE_LANGUAGE,
                    show_all=False
                )
                logger.info(f"Recognized: {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning(f"Could not understand audio (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    
            except sr.RequestError as e:
                logger.error(f"Speech recognition service error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Longer wait on network errors
                    
            except Exception as e:
                logger.error(f"Error recognizing speech: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
        
        logger.warning("Speech recognition failed after all retries")
        return None

    def listen_for_wake_word(self):
        """
        Listen for wake word
        Records audio and checks if wake word is present
        
        Returns:
            bool: True if wake word detected, False otherwise
        """
        logger.info(f"Listening for wake word: '{WAKE_WORD}'")
        
        # Record audio
        audio_file = self._record_audio(duration=5)
        if not audio_file:
            logger.error("Failed to record audio")
            return False
        
        # Recognize speech
        text = self._recognize_from_file(audio_file)
        if not text:
            logger.warning("Could not recognize speech")
            return False
        
        # Check for wake word (case insensitive)
        if WAKE_WORD.lower() in text.lower():
            logger.info("Wake word detected!")
            return True
        
        logger.debug(f"Wake word not found in: {text}")
        return False

    def listen_for_command(self):
        """
        Listen for voice commands
        Records and recognizes command
        
        Returns:
            str: Recognized command, or None if not understood
        """
        logger.info(f"Listening for command ({LISTEN_TIMEOUT}s)...")
        
        # Record audio
        audio_file = self._record_audio(duration=LISTEN_TIMEOUT)
        if not audio_file:
            logger.error("Failed to record audio")
            return None
        
        # Check file size
        file_size = os.path.getsize(audio_file)
        if file_size < 10000:  # Less than 10KB is likely just silence
            logger.warning(f"Audio file too small ({file_size} bytes) - might be silence")
        
        # Recognize speech
        text = self._recognize_from_file(audio_file)
        if not text:
            logger.warning("Could not recognize command")
            return None
        
        # Check for close word
        if CLOSE_WORD.lower() in text.lower():
            logger.info("Close word detected - shutting down")
            return CLOSE_WORD
        
        return text

    def listen_for_search_query(self):
        """
        Listen for search or music queries
        
        Returns:
            str: Recognized query, or None if not understood
        """
        logger.info(f"Listening for query ({LISTEN_TIMEOUT}s)...")
        
        # Record audio
        audio_file = self._record_audio(duration=LISTEN_TIMEOUT)
        if not audio_file:
            logger.error("Failed to record audio")
            return None
        
        # Recognize speech
        return self._recognize_from_file(audio_file)


# Simple test
if __name__ == "__main__":
    print("Voice Input Module Test")
    print("=" * 50)
    
    try:
        voice = VoiceInput()
        
        print("\nTesting wake word detection...")
        print(f"Say something with '{WAKE_WORD}' in it (5 seconds)...")
        if voice.listen_for_wake_word():
            print("✓ Wake word detected!")
            
            print(f"\nNow say a command ({LISTEN_TIMEOUT} seconds)...")
            print("Example commands:")
            print("  - 'What time is it?'")
            print("  - 'Move forward'")
            print("  - 'Play music'")
            
            command = voice.listen_for_command()
            if command:
                print(f"✓ Command received: {command}")
            else:
                print("✗ No command recognized")
                print("\nTroubleshooting:")
                print("  - Speak more clearly")
                print("  - Speak louder")
                print("  - Check microphone volume: alsamixer -c 3")
            
        else:
            print("✗ Wake word not detected")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
