# Configuration file for Maahi Robot Assistant
# All settings and constants are defined here for easy modification

# ==================== ROBOT SETTINGS ====================
ROBOT_NAME = "Mahi"
WAKE_WORD = "hello Mahi"  # Wake word to activate robot
CLOSE_WORD = "bye"  # Word to deactivate robot
RESPONSE_VOICE = "female"  # Indian female voice

# ==================== GROQ API SETTINGS ====================
GROQ_API_KEY = "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"  # Replace with your actual Groq API key
GROQ_MODEL = "mixtral-8x7b-32768"  # Groq model to use
GROQ_TEMPERATURE = 0.7  # Response creativity (0-1)

# ==================== VOICE SETTINGS ====================
AUDIO_RATE = 16000  # Sample rate for audio
AUDIO_CHUNK = 1024  # Chunk size for audio processing
AUDIO_CHANNELS = 1  # Mono audio
VOICE_LANGUAGE = "en-IN"  # Indian English
LISTEN_TIMEOUT = 10  # Seconds to listen for voice command
SPEECH_THRESHOLD = 0.5  # Noise threshold

# ==================== MOTOR SETTINGS ====================
# Motor control pins (BCM GPIO pins for Raspberry Pi)
MOTOR_LEFT_FORWARD = 17
MOTOR_LEFT_BACKWARD = 27
MOTOR_RIGHT_FORWARD = 22
MOTOR_RIGHT_BACKWARD = 23
MOTOR_PWM_PIN = 12  # PWM pin for speed control
MOTOR_SPEED = 50  # Default motor speed (0-100)

# ==================== DISPLAY SETTINGS ====================
# SPI XPT2046 Touch Display settings
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED = 8000000  # 8 MHz
TOUCH_INT_PIN = 24  # Touch interrupt pin
DISPLAY_ROTATION = 0  # 0, 1, 2, 3 for different rotations

# Eye display settings
EYE_BLINK_INTERVAL = 3000  # Blink every 3 seconds (ms)
EYE_NORMAL = "normal"  # Normal eyes state
EYE_LISTENING = "listening"  # Listening state
EYE_ANSWERING = "answering"  # Answering state
EYE_MUSIC = "music"  # Playing music state
EYE_VIDEO = "video"  # Playing video state

# ==================== ULTRASONIC SENSOR SETTINGS ====================
SENSOR_TRIG_PIN = 25  # Trigger pin
SENSOR_ECHO_PIN = 26  # Echo pin
OBSTACLE_DISTANCE_THRESHOLD = 20  # Stop if obstacle within 20cm
CHECK_OBSTACLE_INTERVAL = 1  # Check every 1 second

# ==================== AUDIO OUTPUT SETTINGS ====================
# USB Speaker settings
AUDIO_OUTPUT_DEVICE = "default"  # USB speaker device name
SPEAKER_VOLUME = 80  # Default volume (0-100)

# ==================== YOUTUBE SETTINGS ====================
# YouTube Music and Video settings
SEARCH_RESULTS_LIMIT = 5  # Number of search results
VIDEO_QUALITY = "360"  # Video quality (360, 720, etc.)
MUSIC_QUALITY = "audio"  # Audio quality

# ==================== WEB INTERFACE SETTINGS ====================
FLASK_HOST = "0.0.0.0"  # Accessible from any device
FLASK_PORT = 5000  # Port number
FLASK_DEBUG = True  # Debug mode (set to False in production)

# ==================== STATE CONSTANTS ====================
STATE_IDLE = "idle"
STATE_LISTENING = "listening"
STATE_PROCESSING = "processing"
STATE_SPEAKING = "speaking"
STATE_MOVING = "moving"
STATE_PLAYING_VIDEO = "playing_video"
STATE_PLAYING_MUSIC = "playing_music"
STATE_SLEEPING = "sleeping"

# ==================== COMMANDS ====================
COMMANDS = {
    "move_forward": "move the robot forward",
    "move_backward": "move backward",
    "turn_left": "turn left",
    "turn_right": "turn right",
    "stop": "stop moving",
    "play_music": "play music",
    "play_video": "play youtube video",
    "search": "search",
}

# ==================== PATHS ====================
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EYES_ASSETS_DIR = os.path.join(BASE_DIR, "assets", "eyes")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# Create necessary directories
os.makedirs(EYES_ASSETS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
