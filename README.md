# 🤖 MAAHI - Smart Voice Assistant Robot

A Raspberry Pi-based intelligent robot assistant that moves in any direction, answers questions using Groq AI, plays music from YouTube Music, streams YouTube videos on a display, and can be controlled via voice or web interface.

## ✨ Features

### 🎤 Voice Intelligence
- **Groq AI-Powered**: Intelligent question answering with context awareness
- **Indian Female Voice**: Natural text-to-speech output in Indian accent
- **Wake Word Activation**: Responds to "hello maahi" wake word
- **Voice Recognition**: Understands both English and Hindi commands
- **Always Listening**: Continuously monitors for wake word

### 🚗 Movement Control
- **4-Direction Movement**: Forward, backward, left turn, right turn
- **Variable Speed**: Adjustable motor speed (0-100%)
- **Obstacle Avoidance**: Ultrasonic sensor prevents collisions
- **Smooth Navigation**: PWM-controlled motors for precise movement

### 👀 Display & Eyes
- **Animated Eyes**: Shows different eye states based on activity
  - Normal eyes (idle)
  - Listening eyes (when listening for input)
  - Answering eyes (when responding)
  - Music eyes (dancing while playing music)
  - Video eyes (while watching videos)
- **SPI Display Support**: Works with 320x240 XPT2046 touch display
- **YouTube Video Playback**: Full-screen video on robot's display

### 🎵 Music & Entertainment
- **YouTube Music Integration**: Search and play any song
- **Mood-Based Suggestions**: Get music recommendations based on mood
- **USB Speaker Output**: High-quality audio through USB speaker
- **Music Control**: Play, stop, and manage playback via voice or web

### 📹 Video Streaming
- **YouTube Search**: Find and play any YouTube video
- **Offline Streaming**: Download and play videos
- **Quality Adjustment**: Adaptive quality based on connection
- **Full Control**: Start, stop, and manage playback

### 🌐 Web Interface
- **Remote Control**: Control robot from any device on the network
- **Real-Time Dashboard**: Live status updates and metrics
- **Motor Control**: Precise movement control with speed adjustment
- **Media Management**: Search and control music/video
- **Display Control**: Change eye states and display text
- **Sensor Monitoring**: Real-time distance and obstacle detection

### 🔌 Hardware Support
- **Raspberry Pi 4**: Optimal performance with 4GB RAM
- **USB Peripherals**: Microphone and speaker support
- **GPIO Integration**: Motor driver, ultrasonic sensor
- **SPI Display**: Touch-enabled display support
- **Multi-Motor Control**: 4 independent motor control

---

## 🔧 System Architecture

```
┌─────────────────────────────────────────────────────┐
│         MAAHI Voice Assistant Robot                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐      ┌──────────────┐            │
│  │ Voice Input  │      │ Groq AI      │            │
│  │ (Microphone) │─────→│ Assistant    │            │
│  └──────────────┘      └──────────────┘            │
│         ↓                        ↓                  │
│  ┌──────────────┐      ┌──────────────┐            │
│  │Text-to-Speech│     │  Display &   │            │
│  │ (Speaker)   │      │   Eyes       │            │
│  └──────────────┘      └──────────────┘            │
│         ↓                        ↓                  │
│  ┌──────────────────────────────────────┐          │
│  │  Motor Control     Obstacle Detection│          │
│  │  (4 Motors)       (Ultrasonic)      │          │
│  └──────────────────────────────────────┘          │
│         ↓                                           │
│  ┌──────────────┐      ┌──────────────┐            │
│  │Music Player  │      │Video Player  │            │
│  │(YTMusic API) │      │(YouTube)     │            │
│  └──────────────┘      └──────────────┘            │
│                                                      │
│  Web Interface (Flask) - Remote Control            │
│  http://<ip>:5000                                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 📋 File Organization

| File | Purpose |
|------|---------|
| `config.py` | Configuration & constants |
| `voice_input.py` | Microphone & voice recognition |
| `groq_assistant.py` | AI conversation engine |
| `motor_control.py` | Motor & movement control |
| `display_eyes.py` | Display & eye animations |
| `music_player.py` | YouTube Music integration |
| `youtube_player.py` | YouTube video player |
| `obstacle_detection.py` | Ultrasonic sensor |
| `text_to_speech.py` | Voice synthesis |
| `maahi_main.py` | Main robot orchestrator |
| `web_interface.py` | Flask web dashboard |

---

## 🚀 Quick Start

### 1. Hardware Setup
- Connect all components (motors, sensors, display, microphone, speaker)
- See [SETUP.md](SETUP.md) for detailed wiring diagrams

### 2. Install Dependencies
```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python3-pip portaudio19-dev espeak ffmpeg omxplayer
pip install -r requirements.txt
```

### 3. Configure
- Edit `config.py`:
  - Add your Groq API key
  - Update GPIO pin numbers if different
  - Adjust wake word and other settings

### 4. Test Modules
```bash
python3 voice_input.py      # Test microphone
python3 motor_control.py    # Test motors
python3 display_eyes.py     # Test display
python3 obstacle_detection.py # Test sensor
```

### 5. Run Robot
```bash
python3 maahi_main.py
```

---

## 🎤 Voice Commands

### Wake the Robot
Say: **"hello maahi"**

### Movement
- "move forward"
- "go backward"
- "turn left"
- "turn right"
- "stop"

### Media
- "play music [song name]"
- "play youtube video [video]"

### Information
- "what is the capital of India?"
- "tell me a joke"
- "what's the weather?"

### Close Robot
Say: **"bye"**

---

## 🕸️ Web Interface

Access the dashboard at: `http://<raspberry-pi-ip>:5000`

### Available Controls:
- **Movement**: Forward, backward, left, right, stop
- **Speed**: Adjustable motor speed slider
- **Voice**: Make robot speak any text
- **Music**: Search, play, and stop music
- **Video**: Search and play YouTube videos
- **Display**: Change eye states
- **Sensors**: View distance and obstacle status
- **Status**: Real-time robot status monitoring

---

## 🔄 Workflow Example

```
User: "Hello Maahi"
├─ Robot detects wake word
├─ Display shows listening eyes
├─ Speaker says: "Yes, how can I help?"
│
User: "Play some happy music"
├─ Robot displays music eyes
├─ Searches YouTube Music for happy songs
├─ Plays selected song through speaker
│
User: "Move forward"
├─ Robot moves forward
├─ Ultrasonic sensor checks for obstacles
├─ If obstacle detected → stops and announces
│
User: "Play python tutorial"
├─ Display shows video eyes (full screen)
├─ Plays YouTube video on SPI display
│
User: "Bye"
├─ Robot powers down gracefully
└─ All components clean up
```

---

## 🛠️ Customization

### Change Wake Word
Edit `config.py`:
```python
WAKE_WORD = "your custom wake word"
```

### Change Robot Personality
Edit `maahi_main.py` - `speak()` method to add custom responses

### Add Custom Commands
In `process_command()` method:
```python
elif "your command" in command_lower:
    your_custom_function()
```

### Adjust Motor Speed
```python
MOTOR_SPEED = 50  # 0-100 in config.py
```

### Change Eye Animations
Edit `display_eyes.py` to create new eye styles

---

## 📊 Hardware Requirements

| Component | Spec |
|-----------|------|
| SBC | Raspberry Pi 4 (4GB RAM) |
| Motors | 4x DC Motors with gearbox |
| Motor Driver | L298N or similar |
| Microphone | USB Condenser Mic |
| Speaker | USB Speaker (≥5W) |
| Display | 320x240 SPI XPT2046 |
| Sensor | HC-SR04 Ultrasonic |
| Power | 3A+ Power Supply |

---

## 🐛 Troubleshooting

### Microphone not detected
```bash
arecord -l  # List devices
# Check if USB device appears
```

### Motor not moving
- Check GPIO pins in config.py
- Verify motor driver connections
- Test with motor_control.py

### Display issues
- Enable SPI: `raspi-config` → Interfaces → SPI
- Check display connections
- Verify GPIO pin numbers

### API errors
- Verify Groq API key
- Check internet connection
- Ensure API key has proper permissions

See [SETUP.md](SETUP.md) for detailed troubleshooting.

---

## 📚 Project Structure

```
maahi/
├── Python Modules (core functionality)
│   ├── config.py
│   ├── voice_input.py
│   ├── groq_assistant.py
│   ├── motor_control.py
│   ├── display_eyes.py
│   ├── music_player.py
│   ├── youtube_player.py
│   ├── obstacle_detection.py
│   ├── text_to_speech.py
│   ├── maahi_main.py
│   └── web_interface.py
├── Configuration
│   ├── requirements.txt
│   ├── SETUP.md (detailed setup guide)
│   └── README.md (this file)
├── Web Interface
│   ├── templates/index.html
│   └── static/(CSS/JS files)
├── Asset Directories
│   ├── assets/eyes/ (eye animations)
│   ├── logs/ (log files)
│   └── temp/ (temporary files)
```

---

## 🎓 Learning Resources

- **Raspberry Pi**: https://www.raspberrypi.com/
- **Voice Recognition**: https://github.com/Uberi/speech_recognition
- **Groq API**: https://console.groq.com/docs/
- **YouTube Music**: https://ytmusicapi.readthedocs.io/
- **Flask**: https://flask.palletsprojects.com/
- **GPIO Programming**: https://pypi.org/project/RPi.GPIO/

---

## 🤝 Contributing

Feel free to:
- Report bugs and issues
- Suggest new features
- Improve documentation
- Optimize performance
- Add new modules

---

## ⚖️ License

This project is open-source and available for educational use.

---

## 🙋 Support

For issues and questions:
1. Check [SETUP.md](SETUP.md) troubleshooting section
2. Review log files in `/logs/` directory
3. Test individual modules separately
4. Verify hardware connections

---

## 🎉 What's Next?

After getting Maahi working, try:
- [ ] Adding face recognition
- [ ] Implementing gesture control
- [ ] Adding scheduled reminders
- [ ] Creating smart home integration
- [ ] Building mobile app companion
- [ ] Adding emotion analysis
- [ ] Implementing visual navigation

---

## 👋 Final Notes

**Maahi is your intelligent robot companion!**

- Always keep the code updated
- Monitor logs for errors
- Back up your configuration
- Experiment safely
- Have fun! 🚀

---

**Made with ❤️ for Robotics Enthusiasts**
