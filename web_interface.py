"""
Web Interface for Maahi Robot Assistant
Flask-based web dashboard for remote control of robot functions
"""

from flask import Flask, render_template, request, jsonify
import logging
from config import *
import threading
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global robot instance (will be passed from main script)
robot_instance = None


def set_robot_instance(robot):
    """Set the robot instance for web control"""
    global robot_instance
    robot_instance = robot


# ==================== WEB ROUTES ====================

@app.route('/')
def index():
    """Serve main dashboard"""
    return render_template('index.html', robot_name=ROBOT_NAME)


@app.route('/api/status')
def get_status():
    """Get current robot status"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    status = {
        "robot_name": ROBOT_NAME,
        "state": robot_instance.current_state,
        "is_active": robot_instance.is_active,
        "motor_speed": robot_instance.motor.current_speed,
        "distance": robot_instance.obstacle_sensor.current_distance,
        "music_playing": robot_instance.music_player.is_playing,
        "video_playing": robot_instance.video_player.is_playing,
    }
    
    return jsonify(status)


# ==================== MOTOR CONTROL ROUTES ====================

@app.route('/api/motor/forward', methods=['POST'])
def motor_forward():
    """Move robot forward"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        duration = request.json.get('duration', None)
        robot_instance.handle_move_forward(duration)
        return jsonify({"status": "success", "action": "moving forward"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/motor/backward', methods=['POST'])
def motor_backward():
    """Move robot backward"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        duration = request.json.get('duration', None)
        robot_instance.handle_move_backward(duration)
        return jsonify({"status": "success", "action": "moving backward"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/motor/left', methods=['POST'])
def motor_left():
    """Turn robot left"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        duration = request.json.get('duration', None)
        robot_instance.handle_turn_left(duration)
        return jsonify({"status": "success", "action": "turning left"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/motor/right', methods=['POST'])
def motor_right():
    """Turn robot right"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        duration = request.json.get('duration', None)
        robot_instance.handle_turn_right(duration)
        return jsonify({"status": "success", "action": "turning right"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/motor/stop', methods=['POST'])
def motor_stop():
    """Stop robot movement"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        robot_instance.handle_stop()
        return jsonify({"status": "success", "action": "stopped"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/motor/speed', methods=['POST'])
def set_motor_speed():
    """Set motor speed"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        speed = request.json.get('speed', MOTOR_SPEED)
        robot_instance.motor.set_speed(speed)
        return jsonify({"status": "success", "speed": speed})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


# ==================== VOICE & TEXT ROUTES ====================

@app.route('/api/speak', methods=['POST'])
def speak():
    """Make robot speak"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Run in thread to not block HTTP response
        thread = threading.Thread(target=robot_instance.speak, args=(text, True))
        thread.daemon = True
        thread.start()
        
        return jsonify({"status": "success", "text": text})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


# ==================== MUSIC ROUTES ====================

@app.route('/api/music/search', methods=['POST'])
def search_music():
    """Search for music"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        query = request.json.get('query', '')
        if not query:
            return jsonify({"error": "No search query provided"}), 400
        
        songs = robot_instance.music_player.search_songs(query, limit=5)
        
        return jsonify({
            "status": "success",
            "query": query,
            "songs": songs
        })
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/music/play', methods=['POST'])
def play_music():
    """Play music"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        song_name = request.json.get('song_name', '')
        artist_name = request.json.get('artist_name', '')
        
        if not song_name:
            return jsonify({"error": "No song name provided"}), 400
        
        # Run in thread
        thread = threading.Thread(
            target=robot_instance.music_player.play_song_by_name,
            args=(song_name, artist_name)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "status": "success",
            "song": song_name,
            "artist": artist_name
        })
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/music/stop', methods=['POST'])
def stop_music():
    """Stop music playback"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        robot_instance.music_player.stop_playback()
        return jsonify({"status": "success", "action": "music stopped"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


# ==================== VIDEO ROUTES ====================

@app.route('/api/video/search', methods=['POST'])
def search_video():
    """Search for YouTube videos"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        query = request.json.get('query', '')
        if not query:
            return jsonify({"error": "No search query provided"}), 400
        
        videos = robot_instance.video_player.search_videos(query, limit=5)
        
        return jsonify({
            "status": "success",
            "query": query,
            "videos": videos
        })
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/play', methods=['POST'])
def play_video():
    """Play YouTube video"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        video_url = request.json.get('url', '')
        title = request.json.get('title', '')
        
        if not video_url:
            return jsonify({"error": "No video URL provided"}), 400
        
        # Run in thread
        thread = threading.Thread(
            target=robot_instance.video_player.play_video,
            args=(video_url, title)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "status": "success",
            "video": title,
            "url": video_url
        })
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/stop', methods=['POST'])
def stop_video():
    """Stop video playback"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        robot_instance.video_player.stop_playback()
        return jsonify({"status": "success", "action": "video stopped"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


# ==================== SENSOR ROUTES ====================

@app.route('/api/sensor/distance', methods=['GET'])
def get_distance():
    """Get current distance reading"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        info = robot_instance.obstacle_sensor.get_safe_distance()
        return jsonify(info)
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


# ==================== DISPLAY ROUTES ====================

@app.route('/api/display/eyes', methods=['POST'])
def set_display_eyes():
    """Set display eyes state"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        state = request.json.get('state', EYE_NORMAL)
        robot_instance.display.set_state(state)
        return jsonify({"status": "success", "state": state})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/display/text', methods=['POST'])
def display_text():
    """Display text on screen"""
    if not robot_instance:
        return jsonify({"error": "Robot not initialized"}), 500
    
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        robot_instance.display.show_text(text)
        return jsonify({"status": "success", "text": text})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


def start_web_server():
    """Start Flask web server"""
    logger.info(f"Starting web server on {FLASK_HOST}:{FLASK_PORT}")
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG,
        threaded=True
    )


if __name__ == "__main__":
    start_web_server()
