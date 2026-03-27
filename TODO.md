# 📝 MAAHI ROBOT PROJECT - STEP-BY-STEP TODO LIST

## 🎯 Project Overview
You are building **MAAHI**, an intelligent voice assistant robot that can:
✓ Move in any direction with 4 motors  
✓ Answer questions using AI (Groq)  
✓ Play music from YouTube Music  
✓ Stream YouTube videos on display  
✓ Be controlled via voice or website  
✓ Show different eye animations  
✓ Detect obstacles  

---

## ⚡ PHASE 1: PREPARATION & PLANNING
### ✅ Phase 1 Checklist

- [ ] **1.1** Read the entire README.md to understand the project
- [ ] **1.2** Review SETUP.md for hardware requirements
- [ ] **1.3** Gather all hardware components:
  - [ ] Raspberry Pi 4 (4GB RAM)
  - [ ] 4 DC Motors with gearbox
  - [ ] Motor Driver (L298N)
  - [ ] USB Microphone
  - [ ] USB Speaker
  - [ ] SPI Display (320x240)
  - [ ] Ultrasonic Sensor (HC-SR04)
  - [ ] Power supply (3A+)
  - [ ] Jumper wires and breadboard
  - [ ] Chassis/frame for robot

- [ ] **1.4** Download the project files
- [ ] **1.5** Create a project notebook to track progress
- [ ] **1.6** Watch tutorial videos on:
  - Raspberry Pi GPIO basics
  - Motor control with L298N
  - SPI display setup

---

## 🔧 PHASE 2: HARDWARE ASSEMBLY & WIRING
### ⚙️ Phase 2 Checklist

- [ ] **2.1** Assemble robot frame
  - [ ] Attach motors to frame
  - [ ] Attach tyres to motor shafts
  - [ ] Mount motor driver on frame

- [ ] **2.2** Wire Motor Driver to Raspberry Pi
  ```
  Motor Driver (L298N) Connections:
  - IN1 → GPIO 17
  - IN2 → GPIO 27
  - IN3 → GPIO 22
  - IN4 → GPIO 23
  - ENA → GPIO 12
  - GND → Pi GND
  - +5V → Pi 5V
  ```
  - [ ] Double-check all connections
  - [ ] Take photos of connections

- [ ] **2.3** Wire Ultrasonic Sensor
  ```
  HC-SR04 Connections:
  - TRIG → GPIO 25
  - ECHO → GPIO 26
  - GND → Pi GND
  - VCC → Pi 5V
  ```

- [ ] **2.4** Wire Motors to Motor Driver
  - [ ] Connect 4 motors to motor driver output pins
  - [ ] Test connections with continuity tester

- [ ] **2.5** Setup Power Supply
  - [ ] Connect power to motor driver
  - [ ] Connect power to Raspberry Pi
  - [ ] Test voltage with multimeter

- [ ] **2.6** Mount Display (SPI)
  - [ ] Mount on top of robot for eyes
  - [ ] Wire SPI connections to Raspberry Pi
  - [ ] Enable SPI in Raspberry Pi settings

- [ ] **2.7** Connect USB Peripherals
  - [ ] Connect USB Microphone to Raspberry Pi
  - [ ] Connect USB Speaker to Raspberry Pi
  - [ ] Test both devices are detected

- [ ] **2.8** Final Hardware Check
  - [ ] Verify all connections are secure
  - [ ] No loose wires
  - [ ] All components powered correctly
  - [ ] Take final photos for reference

---

## 💻 PHASE 3: RASPBERRY PI SETUP
### 🐧 Phase 3 Checklist

- [ ] **3.1** Install Raspberry Pi OS
  - [ ] Download Raspberry Pi Imager
  - [ ] Write OS to SD card
  - [ ] Insert SD card into Pi
  - [ ] Power on Pi

- [ ] **3.2** Initial Raspberry Pi Configuration
  ```bash
  sudo raspi-config
  ```
  - [ ] Change password
  - [ ] Set Wi-Fi country
  - [ ] Connect to your Wi-Fi network
  - [ ] Set locale and timezone
  - [ ] Enable SSH (optional, for remote access)

- [ ] **3.3** Enable Required Interfaces
  ```bash
  sudo raspi-config
  ```
  - [ ] Enable SPI (Interfacing Options → SPI)
  - [ ] Enable I2C (Interfacing Options → I2C)
  - [ ] Enable GPIO pins

- [ ] **3.4** Update System
  ```bash
  sudo apt-get update
  sudo apt-get upgrade
  ```
  - [ ] Wait for updates to complete
  - [ ] Reboot if required

- [ ] **3.5** Install System Dependencies
  ```bash
  sudo apt-get install python3 python3-pip python3-dev
  sudo apt-get install portaudio19-dev
  sudo apt-get install libatlas-base-dev
  sudo apt-get install espeak ffmpeg
  sudo apt-get install omxplayer vlc
  ```
  - [ ] Verify all installations successful

- [ ] **3.6** Create Project Directory
  ```bash
  cd /home/pi
  mkdir maahi
  cd maahi
  ```

- [ ] **3.7** Copy Project Files
  - [ ] Copy all Python files to /home/pi/maahi/
  - [ ] Copy requirements.txt
  - [ ] Copy SETUP.md and README.md

---

## 📦 PHASE 4: PYTHON ENVIRONMENT SETUP
### 🐍 Phase 4 Checklist

- [ ] **4.1** Create Virtual Environment
  ```bash
  cd /home/pi/maahi
  python3 -m venv venv
  ```

- [ ] **4.2** Activate Virtual Environment
  ```bash
  source venv/bin/activate
  ```

- [ ] **4.3** Install Python Dependencies
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
  - [ ] Wait for all packages to install
  - [ ] Note any warnings or errors

- [ ] **4.4** Verify Installations
  ```bash
  python3 -c "import RPi.GPIO; print('GPIO OK')"
  python3 -c "import speech_recognition; print('Speech OK')"
  python3 -c "import pyttsx3; print('TTS OK')"
  ```

---

## 🔑 PHASE 5: API KEYS & AUTHENTICATION
### 🔐 Phase 5 Checklist

- [ ] **5.1** Get Groq API Key
  - [ ] Visit https://console.groq.com/
  - [ ] Sign up for account (free tier available)
  - [ ] Create an API key
  - [ ] Copy the API key

- [ ] **5.2** Update config.py with Groq API Key
  ```bash
  nano config.py
  ```
  - [ ] Find: `GROQ_API_KEY = "your_groq_api_key_here"`
  - [ ] Replace with your actual API key
  - [ ] Save file (Ctrl+O, Y, Enter)

- [ ] **5.3** Optional: Setup YouTube Music Authentication
  ```bash
  pip install ytmusicapi
  ytmusicapi oauth
  ```
  - [ ] Follow on-screen instructions
  - [ ] This generates oauth.json for YouTube Music

- [ ] **5.4** Verify API Key
  ```bash
  python3 -c "from groq import Groq; print('Groq OK')"
  ```

---

## 🧪 PHASE 6: MODULE TESTING (One by One)
### ✔️ Phase 6 Checklist

**IMPORTANT:** Test each module separately before running the main program!

- [ ] **6.1** Test Voice Input Module
  ```bash
  python3 voice_input.py
  ```
  - [ ] Say "hello maahi" when prompted
  - [ ] Verify wake word is detected ✓
  - [ ] Say a command when prompted
  - [ ] Verify command is recognized ✓

- [ ] **6.2** Test Groq AI Module
  ```bash
  python3 groq_assistant.py
  ```
  - [ ] Verify Groq initializes without errors
  - [ ] Check AI responses are generated
  - [ ] Test at least 2 different questions

- [ ] **6.3** Test Motor Control Module
  ```bash
  sudo python3 motor_control.py
  ```
  - [ ] **IMPORTANT: Place robot on safe surface (elevated or floor space)**
  - [ ] Verify forward movement ✓
  - [ ] Verify backward movement ✓
  - [ ] Verify left turn ✓
  - [ ] Verify right turn ✓
  - [ ] Motors stop smoothly ✓

- [ ] **6.4** Test Display Eyes Module
  ```bash
  python3 display_eyes.py
  ```
  - [ ] Display shows normal eyes ✓
  - [ ] Display shows listening eyes ✓
  - [ ] Display shows answering eyes ✓
  - [ ] Display shows music eyes ✓
  - [ ] Display shows video eyes ✓

- [ ] **6.5** Test Obstacle Detection Module
  ```bash
  sudo python3 obstacle_detection.py
  ```
  - [ ] Sensor reads distance ✓
  - [ ] Move hand closer to sensor
  - [ ] Verify distance decreases ✓
  - [ ] Move hand away
  - [ ] Verify distance increases ✓

- [ ] **6.6** Test Text-to-Speech Module
  ```bash
  python3 text_to_speech.py
  ```
  - [ ] Listen for robot voice ✓
  - [ ] Verify it's clear and intelligible ✓
  - [ ] Test different speech rates ✓

- [ ] **6.7** Test Music Player Module
  ```bash
  python3 music_player.py
  ```
  - [ ] Search functionality works ✓
  - [ ] Songs are found and displayed ✓
  - [ ] (Optional: Verify music plays if authenticated)

- [ ] **6.8** Test YouTube Video Player Module
  ```bash
  python3 youtube_player.py
  ```
  - [ ] Video search works ✓
  - [ ] Video information is retrieved ✓

**If any module fails**, check:
1. GPIO pins are correct
2. All hardware is connected
3. Dependencies are installed
4. Error messages in logs

---

## 🤖 PHASE 7: MAIN ROBOT TEST
### 🚀 Phase 7 Checklist

- [ ] **7.1** Verify All Components Working
  - [ ] All Phase 6 tests passed ✓
  - [ ] config.py is properly updated
  - [ ] No error messages in logs

- [ ] **7.2** Run Main Robot Script
  ```bash
  sudo python3 maahi_main.py
  ```
  - [ ] Robot initializes without errors ✓
  - [ ] "Waiting for wake word" message appears ✓
  - [ ] Display shows normal eyes ✓

- [ ] **7.3** Test Wake Word Activation
  - [ ] Say: "Hello Maahi"
  - [ ] RobotPT responds with "Yes, how can I help?" ✓
  - [ ] Display changes to listening eyes ✓

- [ ] **7.4** Test Voice Commands
  - [ ] Say: "move forward" → Robot moves ✓
  - [ ] Say: "turn left" → Robot turns ✓
  - [ ] Say: "stop" → Robot stops ✓
  - [ ] Say: "what is your name?" → Robot answers ✓

- [ ] **7.5** Test Obstacle Detection
  - [ ] Place obstacle in front of robot
  - [ ] Say: "move forward"
  - [ ] Robot stops before hitting obstacle ✓
  - [ ] Robot announces: "Obstacle ahead!" ✓

- [ ] **7.6** Test Music Command
  - [ ] Say: "play music bollywood"
  - [ ] Display shows music eyes ✓
  - [ ] Music plays from speaker ✓

- [ ] **7.7** Test Video Command (if display working)
  - [ ] Say: "play youtube video python tutorial"
  - [ ] Display shows video eyes ✓
  - [ ] Video plays on display ✓

- [ ] **7.8** Test Close Command
  - [ ] Say: "bye"
  - [ ] Robot says goodbye ✓
  - [ ] All components shut down cleanly ✓
  - [ ] No error messages ✓

---

## 🌐 PHASE 8: WEB INTERFACE SETUP
### 💻 Phase 8 Checklist

- [ ] **8.1** Verify Flask Installation
  ```bash
  python3 -c "import flask; print('Flask OK')"
  ```

- [ ] **8.2** Create Web Interface Directories
  ```bash
  mkdir -p templates static/css static/js
  ```
  - [ ] Verify files exist

- [ ] **8.3** Test Web Interface
  ```bash
  # Terminal 1
  python3 maahi_main.py
  
  # Terminal 2
  python3 web_interface.py
  ```
  - [ ] Flask server starts on port 5000 ✓
  - [ ] No errors in console ✓

- [ ] **8.4** Access Web Interface
  - [ ] Find Raspberry Pi IP: `hostname -I`
  - [ ] Open browser: `http://<pi-ip>:5000`
  - [ ] Dashboard loads ✓
  - [ ] "Connected to Maahi" notification appears ✓

- [ ] **8.5** Test Web Controls
  - [ ] Click "Forward" button → Robot moves ✓
  - [ ] Adjust speed slider → Speed changes ✓
  - [ ] Type text and click "Speak" → Robot speaks ✓
  - [ ] Search for music → Results appear ✓
  - [ ] Click to play music → Music plays ✓
  - [ ] Click eye buttons → Eyes change ✓

- [ ] **8.6** Document Web Interface
  - [ ] Screenshot the dashboard
  - [ ] Note the URL for future use
  - [ ] Save login credentials if applicable

---

## 🚗 PHASE 9: AUTONOMOUS OPERATION TEST
### 🎯 Phase 9 Checklist

- [ ] **9.1** Clear Test Area
  - [ ] Remove obstacles from robot's path
  - [ ] Create safe zone (3m x 3m minimum)
  - [ ] Place robot in center

- [ ] **9.2** Autonomy Test
  - [ ] Activate robot: "Hello Maahi"
  - [ ] Say: "move forward 10 kilometers"
  - [ ] Robot moves and avoids obstacles ✓
  - [ ] Robot responds to voice commands ✓

- [ ] **9.3** Extended Test (5 minutes)
  - [ ] Give various voice commands
  - [ ] Monitor for any errors
  - [ ] Check motor performance
  - [ ] Verify sensor readings

- [ ] **9.4** Document Performance
  - [ ] Write down any issues
  - [ ] Note response times
  - [ ] Check battery/power usage

---

## 🛠️ PHASE 10: TROUBLESHOOTING & OPTIMIZATION
### 🔧 Phase 10 Checklist

- [ ] **10.1** Check Logs
  ```bash
  ls -la logs/
  cat logs/maahi.log  # if exists
  ```
  - [ ] Review error messages
  - [ ] Fix issues one by one

- [ ] **10.2** Common Issues to Fix
  - [ ] **Motors not moving?**
    - Check GPIO pins
    - Verify power connections
    - Test motor_control.py separately
  
  - [ ] **Microphone not working?**
    ```bash
    arecord -l  # List audio devices
    ```
    - Check USB device is detected
    - Adjust recording levels
  
  - [ ] **Display not showing?**
    - Verify SPI is enabled
    - Check display connections
    - Test with display library examples
  
  - [ ] **API errors?**
    - Verify Groq API key
    - Check internet connection
    - Verify API key hasn't expired

- [ ] **10.3** Optimize Performance
  - [ ] Increase motor speed if it's too slow
  - [ ] Adjust microphone sensitivity
  - [ ] Optimize AI response time
  - [ ] Fine-tune obstacle detection threshold

- [ ] **10.4** Performance Benchmarking
  - [ ] Test voice command response time
  - [ ] Measure motor speed
  - [ ] Check API response time
  - [ ] Document results

---

## 📚 PHASE 11: CUSTOMIZATION & ENHANCEMENT
### 🎨 Phase 11 Checklist

- [ ] **11.1** Customize Robot Name
  - [ ] Edit global robot name to "MAAHI" in scripts
  - [ ] Update startup messages

- [ ] **11.2** Create Custom Commands
  - [ ] Edit `maahi_main.py`
  - [ ] Add new command handlers
  - [ ] Test new commands

- [ ] **11.3** Customize Eye Animations
  - [ ] Edit `display_eyes.py`
  - [ ] Create new eye designs
  - [ ] Add more emotions/states

- [ ] **11.4** Add Sound Effects
  - [ ] Add beep on wake word detection
  - [ ] Add error sounds
  - [ ] Add success sounds

- [ ] **11.5** Improve Voice Quality
  - [ ] Import high-quality voice model
  - [ ] Adjust speech rate
  - [ ] Test different voice options

---

## 🌟 PHASE 12: DEPLOYMENT & DOCUMENTATION
### 📖 Phase 12 Checklist

- [ ] **12.1** Create Project Documentation
  - [ ] Document all GPIO pin assignments
  - [ ] Take photos of hardware setup
  - [ ] Create wiring diagram
  - [ ] Write troubleshooting guide

- [ ] **12.2** Backup Project Files
  ```bash
  tar -czf maahi_backup.tar.gz maahi/
  ```
  - [ ] Create backup on external drive
  - [ ] Test backup restoration

- [ ] **12.3** Version Control (Optional)
  ```bash
  cd /home/pi/maahi
  git init
  git add .
  git commit -m "Initial Maahi robot project"
  ```

- [ ] **12.4** Create User Manual
  - [ ] List all voice commands
  - [ ] Explain web interface controls
  - [ ] Provide troubleshooting steps
  - [ ] Include safety warnings

- [ ] **12.5** Create Video Demonstration
  - [ ] Film robot in action
  - [ ] Demonstrate voice commands
  - [ ] Show web interface
  - [ ] Share online (optional)

- [ ] **12.6** Final System Test
  - [ ] Run all tests one more time
  - [ ] Verify all components working
  - [ ] Check for any console errors
  - [ ] Document final state

---

## 🎉 FINAL CHECKLIST
### ✅ Project Completion

- [ ] **All hardware working** ✓
- [ ] **All modules tested individually** ✓
- [ ] **Main robot script runs smoothly** ✓
- [ ] **Web interface accessible** ✓
- [ ] **Voice control working** ✓
- [ ] **Obstacle detection active** ✓
- [ ] **Music playing correctly** ✓
- [ ] **Videos playing on display** ✓
- [ ] **Documentation complete** ✓
- [ ] **Backup created** ✓

---

## 🚀 NEXT STEPS (ADVANCED)
### 🎓 After Completion

After successfully completing all phases, you can enhance your robot with:

1. **Face Recognition** - Recognize users
2. **Gesture Control** - Control with hand gestures
3. **Smart Home Integration** - Control lights, fans, etc.
4. **Object Detection** - Identify objects in video
5. **Path Planning** - Autonomous navigation
6. **Machine Learning** - Train custom voice model
7. **Mobile App** - Control from phone
8. **Weather Integration** - Get weather updates
9. **Email Notifications** - Alert on email
10. **Multi-language Support** - Support more languages

---

## 📞 TROUBLESHOOTING QUICK REFERENCE

**Issue** → **Solution**
- **GPIO errors** → Run with `sudo python3`
- **Module not found** → Install: `pip install module_name`
- **No microphone** → Check USB or test with `arecord -l`
- **No display** → Enable SPI and check connections
- **API errors** → Verify API key in config.py
- **Slow response** → Check RAM usage with `free -h`
- **Motor not moving** → Check power and GPIO pins

---

## 🎯 ESTIMATED TIME
- **Phase 1-2:** 2-3 hours (Hardware)
- **Phase 3-5:** 1-2 hours (Setup)
- **Phase 6:** 2-3 hours (Testing)
- **Phase 7-8:** 1-2 hours (Main Testing)
- **Phase 9-12:** 2-4 hours (Optimization & Documentation)

**Total: ~11-17 hours** ⏱️

---

## 🏆 SUCCESS CRITERIA

Your project is complete when:
1. ✅ Robot responds to wake word
2. ✅ Voice commands move the robot
3. ✅ Obstacle detection prevents collision
4. ✅ Eyes animate correctly
5. ✅ Music plays from speaker
6. ✅ Videos play on display
7. ✅ Web interface controls robot
8. ✅ No error messages appear
9. ✅ All components respond within 2 seconds
10. ✅ Robot shuts down cleanly

---

**Good Luck! 🚀 Your Maahi Robot will be Amazing! 🤖**

---

*Last Updated: 2024*  
*For support, refer to README.md and SETUP.md*
