"""
Music Player Module for Maahi Robot Assistant
Handles music playback from YouTube Music using ytmusicapi
Plays audio through USB speaker
"""

import logging
import os
import subprocess
import time
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from ytmusicapi import YTMusic
except ImportError:
    logger.warning("ytmusicapi not installed. Please install: pip install ytmusicapi")


class MusicPlayer:
    """
    Handles music playback from YouTube Music
    Downloads and plays songs through USB speaker
    """

    def __init__(self):
        """Initialize YouTube Music API"""
        try:
            self.ytmusic = YTMusic("oauth.json")  # Requires authentication setup
            self.is_playing = False
            self.current_song = None
            self.current_artist = None
            
            logger.info("YouTube Music API initialized")
            
        except Exception as e:
            logger.warning(f"YouTube Music API initialization failed: {e}")
            logger.info("Note: You need to set up authentication. Run: ytmusicapi oauth")
            self.ytmusic = None

    def search_songs(self, query, limit=SEARCH_RESULTS_LIMIT):
        """
        Search for songs on YouTube Music
        
        Args:
            query (str): Song or artist name to search
            limit (int): Number of results to return
            
        Returns:
            list: List of song results with metadata
        """
        try:
            if not self.ytmusic:
                logger.error("YouTube Music API not initialized")
                return []
            
            logger.info(f"Searching for: {query}")
            
            results = self.ytmusic.search(query, filter="songs", limit=limit)
            
            songs = []
            for result in results:
                song_info = {
                    "title": result.get("title", "Unknown"),
                    "artist": result.get("artists", [{}])[0].get("name", "Unknown") if result.get("artists") else "Unknown",
                    "video_id": result.get("videoId", ""),
                    "duration": result.get("duration", 0)
                }
                songs.append(song_info)
                logger.info(f"  - {song_info['title']} by {song_info['artist']}")
            
            return songs
            
        except Exception as e:
            logger.error(f"Error searching songs: {e}")
            return []

    def search_by_mood(self, mood, limit=SEARCH_RESULTS_LIMIT):
        """
        Search for songs based on mood
        
        Args:
            mood (str): Mood or genre (e.g., "happy", "sad", "energetic")
            limit (int): Number of results to return
            
        Returns:
            list: List of song results
        """
        # Create a search query based on mood
        mood_queries = {
            "happy": "happy songs",
            "sad": "sad songs",
            "energetic": "energetic music",
            "relaxing": "relaxing music",
            "workout": "workout music",
            "party": "party songs",
            "love": "love songs",
            "instrumental": "instrumental music"
        }
        
        search_term = mood_queries.get(mood.lower(), f"{mood} music")
        return self.search_songs(search_term, limit)

    def play_song_by_video_id(self, video_id, title="", artist=""):
        """
        Play a song using YouTube video ID
        Uses yt-dlp to stream and play audio
        
        Args:
            video_id (str): YouTube video ID
            title (str): Song title for logging
            artist (str): Artist name for logging
        """
        try:
            if not video_id:
                logger.error("No video ID provided")
                return False
            
            self.current_song = title
            self.current_artist = artist
            
            logger.info(f"Playing: {title} by {artist}")
            
            # Use yt-dlp to stream and play music
            # You may need to adjust based on your audio output setup
            cmd = [
                "yt-dlp",
                "-q",
                "-f", "bestaudio",
                "-o", "-",
                f"https://www.youtube.com/watch?v={video_id}",
                "|",
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-"
            ]
            
            # Alternative using subprocess with pipe
            process = subprocess.Popen(
                [
                    "yt-dlp",
                    "-f", "bestaudio",
                    "-o", "-",
                    f"https://www.youtube.com/watch?v={video_id}"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            
            subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-"],
                stdin=process.stdout
            )
            
            process.stdout.close()
            
            self.is_playing = True
            logger.info("Music playback started")
            
            return True
            
        except FileNotFoundError:
            logger.error("yt-dlp or ffplay not found. Install: pip install yt-dlp and apt-get install ffmpeg")
            return False
        except Exception as e:
            logger.error(f"Error playing song: {e}")
            return False

    def play_song_by_name(self, song_name, artist_name=""):
        """
        Search and play a song by name
        
        Args:
            song_name (str): Song name to search
            artist_name (str): Optional artist name for better search
            
        Returns:
            bool: True if playback started, False otherwise
        """
        try:
            search_query = f"{song_name} {artist_name}".strip()
            songs = self.search_songs(search_query, limit=1)
            
            if songs:
                song = songs[0]
                return self.play_song_by_video_id(
                    song["video_id"],
                    song["title"],
                    song["artist"]
                )
            else:
                logger.warning(f"No songs found for: {search_query}")
                return False
                
        except Exception as e:
            logger.error(f"Error playing song by name: {e}")
            return False

    def stop_playback(self):
        """Stop current music playback"""
        try:
            logger.info("Stopping music playback")
            # Kill any active playback processes
            os.system("pkill -f ffplay")
            self.is_playing = False
            self.current_song = None
            self.current_artist = None
        except Exception as e:
            logger.error(f"Error stopping playback: {e}")

    def get_playlist(self, playlist_id):
        """
        Get songs from a playlist
        
        Args:
            playlist_id (str): YouTube Music playlist ID
            
        Returns:
            list: List of songs in the playlist
        """
        try:
            if not self.ytmusic:
                return []
            
            playlist = self.ytmusic.get_playlist(playlist_id)
            logger.info(f"Loaded playlist: {playlist.get('header', {}).get('title', 'Unknown')}")
            
            songs = []
            for track in playlist.get("contents", []):
                song_info = {
                    "title": track.get("title", "Unknown"),
                    "artist": track.get("artists", [{}])[0].get("name", "Unknown") if track.get("artists") else "Unknown",
                    "video_id": track.get("videoId", "")
                }
                songs.append(song_info)
            
            return songs
            
        except Exception as e:
            logger.error(f"Error getting playlist: {e}")
            return []

    def set_volume(self, volume):
        """
        Set system volume
        
        Args:
            volume (int): Volume level (0-100)
        """
        try:
            volume = max(0, min(100, volume))
            # Use amixer for volume control on Raspberry Pi
            os.system(f"amixer set Master {volume}%")
            logger.info(f"Volume set to {volume}%")
        except Exception as e:
            logger.error(f"Error setting volume: {e}")


# Test function
if __name__ == "__main__":
    print("Music Player Module Test")
    print("=" * 50)
    
    player = MusicPlayer()
    
    # Test search
    print("\n1. Testing song search...")
    songs = player.search_songs("Bollywood", limit=3)
    if songs:
        print(f"Found {len(songs)} songs")
        for song in songs:
            print(f"  - {song['title']} by {song['artist']}")
    
    # Test mood-based search
    print("\n2. Testing mood-based search...")
    happy_songs = player.search_by_mood("happy", limit=2)
    if happy_songs:
        print(f"Happy songs found:")
        for song in happy_songs:
            print(f"  - {song['title']}")
    
    # Note: Actual playback requires:
    # - YouTube Music authentication setup
    # - yt-dlp and ffmpeg installed
    # - USB speaker connected
    
    print("\n✓ Music player test completed!")
    print("Note: For full functionality, set up YouTube Music authentication")
    print("Run: ytmusicapi oauth")
