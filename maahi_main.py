"""
Main Voice Assistant Script for Maahi Robot
Orchestrates all components: voice input, AI responses, motor control, display, and music/video
"""

import logging
import time
import threading
from config import *
from voice_input import VoiceInput
from groq_assistant import GroqAssistant
from motor_control import MotorControl
from display_eyes import DisplayEyes
from music_player import MusicPlayer
from youtube_player import YouTubeVideoPlayer
from obstacle_detection import ObstacleDetection
from text_to_speech import TextToSpeech

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MaahiRobotAssistant:
    """
    Main robot assistant combining all functionalities
    Handles voice interactions, movement, display, and media
    """

    def __init__(self):
        """Initialize all robot components"""
        logger.info("=" * 60)
        logger.info(f"Initializing {ROBOT_NAME} Robot Assistant")
        logger.info("=" * 60)
        
        try:
            # Initialize components
            self.voice_input = VoiceInput()
            self.groq = GroqAssistant()
            self.motor = MotorControl()
            self.display = DisplayEyes()
            self.music_player = MusicPlayer()
            self.video_player = YouTubeVideoPlayer()
            self.obstacle_sensor = ObstacleDetection()
            self.tts = TextToSpeech()
            
            # State management
            self.current_state = STATE_IDLE
            self.is_active = False
            self.should_exit = False
            
            # Start obstacle monitoring
            self.obstacle_sensor.start_monitoring_thread()
            
            logger.info(f"✓ {ROBOT_NAME} initialized successfully!")
            logger.info(f"Wake word: '{WAKE_WORD}'")
            logger.info(f"Close word: '{CLOSE_WORD}'")
            
        except Exception as e:
            logger.error(f"Error initializing robot: {e}")
            raise

    def speak(self, text, show_eyes=True):
        """
        Make robot speak using text-to-speech
        
        Args:
            text (str): Text to speak
            show_eyes (bool): Whether to show answering eyes animation
        """
        try:
            if show_eyes:
                self.display.set_state(EYE_ANSWERING)
            
            logger.info(f"Speaking: {text}")
            self.tts.speak(text)
            
        except Exception as e:
            logger.error(f"Error speaking: {e}")

    def process_command(self, command):
        """
        Process voice command and execute corresponding action
        
        Args:
            command (str): User's voice command
        """
        try:
            command_lower = command.lower()
            
            logger.info(f"Processing command: {command}")
            
            # Movement commands
            if "forward" in command_lower or "आगे" in command:
                self.handle_move_forward()
            elif "backward" in command_lower or "पीछे" in command:
                self.handle_move_backward()
            elif "left" in command_lower or "बाएं" in command:
                self.handle_turn_left()
            elif "right" in command_lower or "दाएं" in command:
                self.handle_turn_right()
            elif "stop" in command_lower or "रुको" in command:
                self.handle_stop()
            
            # Media commands
            elif "play music" in command_lower or "संगीत बजाएं" in command:
                self.handle_play_music(command)
            elif "youtube" in command_lower or "वीडियो" in command:
                self.handle_play_video(command)
            
            # Question/help command
            else:
                self.handle_ask_question(command)
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")

    def handle_move_forward(self, duration=None):
        """Handle forward movement command"""
        try:
            logger.info("Moving forward...")
            self.current_state = STATE_MOVING
            
            if self.obstacle_sensor.is_obstacle_ahead():
                self.speak("Obstacle ahead! Stopping.")
                self.motor.stop()
            else:
                self.motor.move_forward()
                if duration:
                    time.sleep(duration)
                    self.motor.stop()
                    
        except Exception as e:
            logger.error(f"Error moving forward: {e}")

    def handle_move_backward(self, duration=None):
        """Handle backward movement command"""
        try:
            logger.info("Moving backward...")
            self.current_state = STATE_MOVING
            self.motor.move_backward()
            
            if duration:
                time.sleep(duration)
                self.motor.stop()
                
        except Exception as e:
            logger.error(f"Error moving backward: {e}")

    def handle_turn_left(self, duration=None):
        """Handle left turn command"""
        try:
            logger.info("Turning left...")
            self.current_state = STATE_MOVING
            self.motor.turn_left()
            
            if duration:
                time.sleep(duration)
                self.motor.stop()
                
        except Exception as e:
            logger.error(f"Error turning left: {e}")

    def handle_turn_right(self, duration=None):
        """Handle right turn command"""
        try:
            logger.info("Turning right...")
            self.current_state = STATE_MOVING
            self.motor.turn_right()
            
            if duration:
                time.sleep(duration)
                self.motor.stop()
                
        except Exception as e:
            logger.error(f"Error turning right: {e}")

    def handle_stop(self):
        """Handle stop command"""
        try:
            logger.info("Stop command received")
            self.motor.stop()
            self.music_player.stop_playback()
            self.video_player.stop_playback()
            self.current_state = STATE_IDLE
            self.display.set_state(EYE_NORMAL)
            
        except Exception as e:
            logger.error(f"Error stopping: {e}")

    def handle_play_music(self, command):
        """
        Handle music playback command
        
        Args:
            command (str): User's music request
        """
        try:
            self.display.set_state(EYE_MUSIC)
            self.speak("Let me search for music")
            
            # Extract search query
            search_query = command.replace("play music", "").replace("संगीत बजाएं", "").strip()
            
            if not search_query:
                self.speak("What music would you like to listen to?")
                search_query = self.voice_input.listen_for_search_query()
            
            if search_query:
                logger.info(f"Searching for music: {search_query}")
                self.music_player.play_song_by_name(search_query)
                self.current_state = STATE_PLAYING_MUSIC
                
                # Keep showing music eyes while playing
                while self.music_player.is_playing and not self.should_exit:
                    self.display.set_state(EYE_MUSIC)
                    time.sleep(1)
            else:
                self.speak("Could not understand music request")
                
        except Exception as e:
            logger.error(f"Error playing music: {e}")
            self.speak("Sorry, I couldn't play the music")

    def handle_play_video(self, command):
        """
        Handle YouTube video playback command
        
        Args:
            command (str): User's video request
        """
        try:
            self.display.set_state(EYE_VIDEO)
            self.speak("Let me search for the video")
            
            # Extract search query
            search_query = command.replace("youtube", "").replace("वीडियो", "").replace("play", "").strip()
            
            if not search_query:
                self.speak("What video would you like to watch?")
                search_query = self.voice_input.listen_for_search_query()
            
            if search_query:
                logger.info(f"Searching for video: {search_query}")
                self.video_player.play_video_by_search(search_query)
                self.current_state = STATE_PLAYING_VIDEO
                
                # Wait for video to finish
                while self.video_player.is_playing and not self.should_exit:
                    self.display.set_state(EYE_VIDEO)
                    time.sleep(1)
                
                # Return to normal state after video
                self.current_state = STATE_IDLE
                self.display.set_state(EYE_NORMAL)
                
            else:
                self.speak("Could not understand video request")
                
        except Exception as e:
            logger.error(f"Error playing video: {e}")
            self.speak("Sorry, I couldn't play the video")

    def handle_ask_question(self, question):
        """
        Handle general question answering using Groq API
        
        Args:
            question (str): User's question
        """
        try:
            logger.info(f"Processing question: {question}")
            self.current_state = STATE_PROCESSING
            
            # Get answer from Groq
            answer = self.groq.get_response(question)
            
            # Speak the answer
            self.speak(answer)
            
            self.current_state = STATE_IDLE
            self.display.set_state(EYE_NORMAL)
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            self.speak("I'm sorry, I couldn't process that question")

    def listen_and_respond(self):
        """
        Main listening loop - waits for wake word, then processes commands
        """
        logger.info(f"Waiting for wake word: '{WAKE_WORD}'...")
        
        try:
            while not self.should_exit:
                # Listen for wake word
                if self.voice_input.listen_for_wake_word():
                    logger.info("!" * 50)
                    logger.info("WAKE WORD DETECTED!")
                    logger.info("!" * 50)
                    
                    self.is_active = True
                    self.display.set_state(EYE_LISTENING)
                    self.speak("Yes, how can I help?")
                    
                    # Listen for command
                    while self.is_active and not self.should_exit:
                        self.display.set_state(EYE_LISTENING)
                        command = self.voice_input.listen_for_command()
                        
                        if command:
                            # Check for close word
                            if CLOSE_WORD.lower() in command.lower():
                                logger.info("Close word detected - shutting down")
                                self.speak(f"Goodbye! Turning off now.")
                                self.is_active = False
                                self.should_exit = True
                                break
                            
                            # Process the command
                            self.process_command(command)
                            
                            # Ask if user needs anything else
                            self.display.set_state(EYE_LISTENING)
                            self.speak("Anything else?")
                        else:
                            logger.warning("No command heard - waiting for new wake word")
                            self.is_active = False
                            self.display.set_state(EYE_NORMAL)
                
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt - shutting down")
            self.should_exit = True
        except Exception as e:
            logger.error(f"Error in listen loop: {e}")

    def shutdown(self):
        """Clean up and shut down the robot"""
        logger.info("=" * 60)
        logger.info(f"Shutting down {ROBOT_NAME} Robot Assistant")
        logger.info("=" * 60)
        
        try:
            self.motor.cleanup()
            self.display.cleanup()
            self.obstacle_sensor.cleanup()
            self.music_player.stop_playback()
            self.video_player.stop_playback()
            
            logger.info("✓ Robot shut down successfully")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

    def run(self):
        """Start the main robot loop"""
        try:
            self.listen_and_respond()
        finally:
            self.shutdown()


# Main execution
if __name__ == "__main__":
    try:
        robot = MaahiRobotAssistant()
        robot.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
