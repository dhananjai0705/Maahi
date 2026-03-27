"""
YouTube Video Player Module for Maahi Robot Assistant
Handles YouTube video searches and playback on SPI XPT2046 display
"""

import logging
import os
import subprocess
import time
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from yt_dlp import YoutubeDL
except ImportError:
    logger.warning("yt-dlp not installed. Install: pip install yt-dlp")


class YouTubeVideoPlayer:
    """
    Handles YouTube video search and playback
    Plays videos on the SPI display
    """

    def __init__(self):
        """Initialize YouTube video player"""
        self.is_playing = False
        self.current_video = None
        self.current_title = None
        
        # yt-dlp options for video download
        self.ydl_options = {
            "quiet": True,
            "no_warnings": True,
            "format": "best[height<=360]",  # Use 360p or lower for Raspberry Pi
            "no_playlist": True,
        }
        
        logger.info("YouTube Video Player initialized")

    def search_videos(self, query, limit=SEARCH_RESULTS_LIMIT):
        """
        Search for YouTube videos
        
        Args:
            query (str): Video search query
            limit (int): Number of results to return
            
        Returns:
            list: List of video results with metadata
        """
        try:
            logger.info(f"Searching YouTube for: {query}")
            
            search_url = f"ytsearch{limit}:{query}"
            
            ydl_options = self.ydl_options.copy()
            ydl_options["quiet"] = False
            ydl_options["extract_flat"] = "in_playlist"
            
            videos = []
            
            try:
                from yt_dlp import YoutubeDL
                with YoutubeDL(ydl_options) as ydl:
                    results = ydl.extract_info(search_url, download=False)
                    
                    if "entries" in results:
                        for entry in results["entries"][:limit]:
                            video_info = {
                                "title": entry.get("title", "Unknown"),
                                "video_id": entry.get("id", ""),
                                "url": f"https://www.youtube.com/watch?v={entry.get('id', '')}",
                                "duration": entry.get("duration", 0),
                                "thumbnail": entry.get("thumbnail", "")
                            }
                            videos.append(video_info)
                            logger.info(f"  - {video_info['title']}")
            except ImportError:
                logger.error("yt-dlp not available. Install: pip install yt-dlp")
                return []
            
            return videos
            
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            return []

    def get_video_info(self, video_url):
        """
        Get detailed information about a video
        
        Args:
            video_url (str): URL of the YouTube video
            
        Returns:
            dict: Video metadata
        """
        try:
            logger.info(f"Getting info for: {video_url}")
            
            try:
                from yt_dlp import YoutubeDL
                with YoutubeDL(self.ydl_options) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    
                    video_info = {
                        "title": info.get("title", "Unknown"),
                        "duration": info.get("duration", 0),
                        "thumbnail": info.get("thumbnail", ""),
                        "description": info.get("description", ""),
                        "view_count": info.get("view_count", 0),
                        "url": video_url
                    }
                    
                    return video_info
            except ImportError:
                return {}
                
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return {}

    def play_video(self, video_url, title=""):
        """
        Play a YouTube video on the SPI display
        
        Args:
            video_url (str): URL of YouTube video
            title (str): Video title for logging
            
        Returns:
            bool: True if playback started, False otherwise
        """
        try:
            if not video_url:
                logger.error("No video URL provided")
                return False
            
            self.current_video = video_url
            self.current_title = title
            
            logger.info(f"Playing video: {title}")
            logger.info(f"URL: {video_url}")
            
            # Use omxplayer (best for Raspberry Pi) or vlc
            # First, try omxplayer (default on Raspberry Pi)
            try:
                subprocess.Popen([
                    "omxplayer",
                    "--orientation", "0",
                    video_url
                ])
                self.is_playing = True
                logger.info("Video playback started with omxplayer")
                return True
            except FileNotFoundError:
                logger.info("omxplayer not found, trying vlc...")
                
                try:
                    subprocess.Popen([
                        "vlc",
                        "-f",  # Fullscreen
                        "--play-and-exit",
                        video_url
                    ])
                    self.is_playing = True
                    logger.info("Video playback started with vlc")
                    return True
                except FileNotFoundError:
                    logger.error("Neither omxplayer nor vlc found")
                    logger.info("Install: sudo apt-get install omxplayer or vlc")
                    return False
            
        except Exception as e:
            logger.error(f"Error playing video: {e}")
            return False

    def play_video_by_search(self, search_query, title=""):
        """
        Search for a video and play the first result
        
        Args:
            search_query (str): Video search query
            title (str): Optional title for logging
            
        Returns:
            bool: True if playback started, False otherwise
        """
        try:
            videos = self.search_videos(search_query, limit=1)
            
            if videos:
                video = videos[0]
                if not title:
                    title = video["title"]
                
                return self.play_video(video["url"], title)
            else:
                logger.warning(f"No videos found for: {search_query}")
                return False
                
        except Exception as e:
            logger.error(f"Error playing video by search: {e}")
            return False

    def stop_playback(self):
        """Stop video playback"""
        try:
            logger.info("Stopping video playback")
            # Kill omxplayer or vlc processes
            os.system("pkill -f omxplayer")
            os.system("pkill -f vlc")
            self.is_playing = False
            self.current_video = None
            self.current_title = None
        except Exception as e:
            logger.error(f"Error stopping video: {e}")

    def get_video_stream_url(self, video_url):
        """
        Get direct streaming URL for a video
        Useful for custom video player implementation
        
        Args:
            video_url (str): YouTube video URL
            
        Returns:
            str: Direct stream URL or empty string if failed
        """
        try:
            try:
                from yt_dlp import YoutubeDL
                ydl_options = self.ydl_options.copy()
                ydl_options["quiet"] = True
                
                with YoutubeDL(ydl_options) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    
                    # Get best format with video
                    formats = info.get("formats", [])
                    for fmt in formats:
                        if fmt.get("vcodec") != "none" and fmt.get("acodec") != "none":
                            stream_url = fmt.get("url", "")
                            if stream_url:
                                logger.info("Stream URL extracted")
                                return stream_url
                    
                    return ""
            except ImportError:
                return ""
                
        except Exception as e:
            logger.error(f"Error getting stream URL: {e}")
            return ""

    def download_video(self, video_url, output_path=None):
        """
        Download a YouTube video for offline playback
        
        Args:
            video_url (str): YouTube video URL
            output_path (str): Where to save the video
            
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            if not output_path:
                output_path = os.path.join(TEMP_DIR, "%(title)s.%(ext)s")
            
            logger.info(f"Downloading video to: {output_path}")
            
            try:
                from yt_dlp import YoutubeDL
                ydl_options = self.ydl_options.copy()
                ydl_options["outtmpl"] = output_path
                ydl_options["quiet"] = False
                ydl_options["progress_hooks"] = [self._progress_hook]
                
                with YoutubeDL(ydl_options) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    logger.info(f"Downloaded: {info.get('title', 'video')}")
                    return True
            except ImportError:
                logger.error("yt-dlp not available")
                return False
                
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return False

    def _progress_hook(self, d):
        """Progress hook for video downloads"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            logger.info(f"Downloading: {percent} at {speed} ETA: {eta}")
        elif d['status'] == 'finished':
            logger.info("Download finished")


# Test function
if __name__ == "__main__":
    print("YouTube Video Player Module Test")
    print("=" * 50)
    
    player = YouTubeVideoPlayer()
    
    # Test search
    print("\n1. Testing video search...")
    videos = player.search_videos("Python tutorial", limit=3)
    if videos:
        print(f"Found {len(videos)} videos:")
        for video in videos:
            print(f"  - {video['title']} ({video['duration']}s)")
    
    # Test getting video info
    if videos:
        print("\n2. Testing video info retrieval...")
        info = player.get_video_info(videos[0]['url'])
        if info:
            print(f"Title: {info['title']}")
            print(f"Duration: {info['duration']} seconds")
            print(f"Views: {info['view_count']}")
    
    # Note: Video playback requires:
    # - omxplayer or vlc installed
    # - YouTube video accessible
    # - Display properly configured
    
    print("\n✓ Video player test completed!")
    print("Note: For video playback, ensure omxplayer is installed")
    print("Install: sudo apt-get install omxplayer")
