# MAAHI - Smart Voice Assistant Robot
## Complete Setup & Installation Guide

**Robot Name:** Maahi  
**Wake Word:** "hello maahi"  
**Close Word:** "bye"  
**Voice:** Indian Female Voice

---

## 📋 Table of Contents
1. [Hardware Setup](#hardware-setup)
2. [Software Dependencies](#software-dependencies)
3. [Configuration](#configuration)
4. [Installation Steps](#installation-steps)
5. [Running the Robot](#running-the-robot)
6. [Web Interface](#web-interface)
7. [Troubleshooting](#troubleshooting)

---

## 🛠️ Hardware Setup

### Components Required:
- **Raspberry Pi 4** (4GB RAM)
- **4 DC Motors** (with 4 tyres) - for movement in all directions
- **Motor Driver** (L298N or similar) - to control 4 motors
- **USB Microphone** - for voice input
- **USB Speaker** - for voice output
- **SPI XPT2046 Touch Display** (320x240 pixels) - for eyes/video display
- **Ultrasonic Sensor** (HC-SR04) - for obstacle detection
- **Power Bank/Battery** - for Raspberry Pi and motors

### Motor Driver Wiring:
```
Motor Driver Pins (L298N):
- IN1 → GPIO 17 (Left Motor Forward)
- IN2 → GPIO 27 (Left Motor Backward)
- IN3 → GPIO 22 (Right Motor Forward)
- IN4 → GPIO 23 (Right Motor Backward)
- ENA → GPIO 12 (PWM for speed control)
- GND → Raspberry Pi GND
- +5V → Raspberry Pi 5V
```

### Ultrasonic Sensor Wiring:
```
HC-SR04 Sensor:
- TRIG → GPIO 25
- ECHO → GPIO 26
- GND → Raspberry Pi GND
- VCC → Raspberry Pi 5V
```

### Display Wiring (SPI):
```
SPI XPT2046 Display:
- CS → GPIO 8 (SPI CE0)
- CLK → GPIO 11 (SPI CLK)
- MOSI → GPIO 10 (SPI MOSI)
- MISO → GPIO 9 (SPI MISO)
- TOUCH_INT → GPIO 24
- GND → Raspberry Pi GND
- VCC → Raspberry Pi 3.3V
```

---

## 📦 Software Dependencies

### System-Level Requirements:

1. **Update Raspberry Pi:**
```bash
sudo apt-get update
sudo apt-get upgrade
```

2. **Install Python and pip:**
```bash
sudo apt-get install python3 python3-pip python3-dev
```

3. **Install Audio Dependencies:**
```bash
sudo apt-get install portaudio19-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install espeak ffmpeg
```

4. **Install Video Player (for YouTube videos):**
```bash
sudo apt-get install omxplayer
# OR
sudo apt-get install vlc
```

5. **Enable SPI Interface:**
```bash
sudo raspi-config
# Navigate to: Interfacing Options → SPI → Enable
```

6. **Enable I2C Interface (if needed):**
```bash
sudo raspi-config
# Navigate to: Interfacing Options → I2C → Enable
```

---

## ⚙️ Configuration

### Step 1: Get Groq API Key
1. Visit https://console.groq.com/
2. Sign up and create an API key
3. Keep the key safe - you'll need it in the next step

### Step 2: Update config.py
Edit `config.py` and update:
```python
GROQ_API_KEY = "your_actual_groq_api_key_here"
WAKE_WORD = "hello maahi"
CLOSE_WORD = "bye"
```

### Step 3: Set up YouTube Music (Optional)
For music functionality, authenticate with YouTube Music:
```bash
pip install ytmusicapi
ytmusicapi oauth
```

---

## 🚀 Installation Steps

### Quick Start (Recommended):

1. **Clone/Download Project:**
```bash
cd /home/pi
git clone <repository-url> maahi
cd maahi
```

2. **Create Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Update GPIO Configuration:**
Edit `config.py` and verify all pin numbers match your wiring.

5. **Test Individual Modules:**
```bash
# Test voice input
python3 voice_input.py

# Test motors
python3 motor_control.py

# Test display
python3 display_eyes.py

# Test obstacle detection
python3 obstacle_detection.py

# Test text-to-speech
python3 text_to_speech.py
```

---

## ▶️ Running the Robot

### Option 1: Run Main Robot Script
```bash
cd /home/pi/maahi
source venv/bin/activate
python3 maahi_main.py
```

The robot will:
1. Initialize all components
2. Listen for the wake word: "hello maahi"
3. Once activated, listen for commands
4. Execute voice commands
5. Respond with either action or voice answer
6. Close with the word "bye"

### Option 2: Run with Web Interface
```bash
# Terminal 1 - Start robot
python3 maahi_main.py

# Terminal 2 - Start web server
python3 web_interface.py
```

Then open browser: `http://<raspberry-pi-ip>:5000`

---

## 🌐 Web Interface

### Available Controls:

**Movement:**
- Forward/Backward/Left/Right
- Adjustable speed (0-100%)

**Voice & Text:**
- Make robot speak any text
- Ask questions (uses Groq AI)

**Music:**
- Search for songs
- Play by name
- Control playback

**Video:**
- Search YouTube videos
- Play videos on display
- Stop playback

**Display:**
- Change eye states (normal, listening, answering, music, video)
- Display custom text

**Sensors:**
- Check distance readings
- View obstacle detection status

---

## 📚 File Structure

```
maahi/
├── config.py                    # All configuration settings
├── voice_input.py              # Microphone & wake word detection
├── groq_assistant.py           # AI question answering
├── motor_control.py            # Motor control (forward/backward/turn)
├── display_eyes.py             # Eyes animation & display
├── music_player.py             # YouTube Music integration
├── youtube_player.py           # YouTube video player
├── obstacle_detection.py        # Ultrasonic sensor
├── text_to_speech.py           # Text-to-speech conversion
├── maahi_main.py               # Main robot script
├── web_interface.py            # Flask web dashboard
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html              # Web interface HTML
├── static/
│   ├── css/style.css           # Web interface styling
│   └── js/script.js            # Web interface JavaScript
├── assets/
│   └── eyes/                   # Eye animation assets (optional)
├── logs/                       # Log files
└── temp/                       # Temporary files
```

---

## 🔧 Troubleshooting

### Problem: Microphone not working
```bash
# Check audio devices
arecord -l

# Test microphone
arecord -D plughw:1,0 -f cd test.wav
aplay test.wav
```

### Problem: Speaker not producing sound
```bash
# Check speaker
aplay /usr/share/sounds/alsa/Front_Center.wav

# Check volume
alsamixer
# Use arrow keys to increase volume
```

### Problem: GPIO errors
- Ensure you're running with `sudo`
- Check pin numbers in config.py
- Verify wiring connections

### Problem: Motor not moving
```bash
# Test motor control independently
python3 motor_control.py

# Check GPIO pins:
gpio readall
```

### Problem: Display not showing
- Verify SPI is enabled: `raspi-config` → Interface → SPI
- Check display connections
- Test with display library examples

### Problem: Groq API errors
- Verify API key is correct in config.py
- Check internet connection
- Verify API key has not expired

### Enable Debug Logging
Edit any Python file and change:
```python
logging.basicConfig(level=logging.DEBUG)  # More verbose output
```

---

## 📝 Voice Commands

### Movement Commands:
- "hello maahi, move forward"
- "hello maahi, go backward"
- "hello maahi, turn left"
- "hello maahi, turn right"
- "hello maahi, stop"

### Media Commands:
- "hello maahi, play music [song name]"
- "hello maahi, play youtube video [video name]"

### Information Commands:
- "hello maahi, what is the weather?"
- "hello maahi, tell me a joke"
- "hello maahi, what time is it?"

### Close Command:
- "bye" (to deactivate the robot)

---

## 🎓 Beginner Tips

1. **Start with one module at a time** - test voice, then motors, then display
2. **Use the web interface** - easier to learn than voice commands initially
3. **Check logs** - they show exactly what's happening
4. **Keep GPIO pins organized** - label your connections
5. **Backup your code** - use git to version control
6. **Update regularly** - keep packages updated: `pip install -r requirements.txt --upgrade`

---

## 📞 Support & Resources

- **Raspberry Pi Documentation:** https://www.raspberrypi.com/documentation/
- **Groq API Docs:** https://console.groq.com/docs/
- **YouTube Music API:** https://ytmusicapi.readthedocs.io/
- **Motor Driver Guide:** https://lastminuteengineers.com/l298n-dc-motor-driver-tutorial/

---

## ⚠️ Safety Notes

1. Always disconnect power before working on hardware
2. Use appropriate heat sinks for motor driver
3. Test motors at low speed first (20-30%)
4. Keep USB cables organized and away from motors
5. Use power supply rated for your components
6. Never force connections

---

## 🎉 Congratulations!

Your Maahi robot is now ready! Experiment with different commands and features. Feel free to modify the code to add your own custom features!

**Say: "Hello Maahi!"** to get started 🚀
