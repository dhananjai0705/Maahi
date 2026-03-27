"""
Groq API Integration Module for Maahi Robot Assistant
Handles AI-powered responses to user questions using Groq's API
"""

from groq import Groq
import logging
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqAssistant:
    """
    Interacts with Groq API for intelligent responses
    Provides context-aware answers to user queries
    """

    def __init__(self, api_key=GROQ_API_KEY):
        """Initialize Groq client with API key"""
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY not set in config.py. "
                "Please add your Groq API key from https://console.groq.com/keys"
            )
        
        self.client = Groq(api_key=api_key)
        self.model = GROQ_MODEL
        self.temperature = GROQ_TEMPERATURE
        self.conversation_history = []
        
        logger.info(f"Groq Assistant initialized with model: {self.model}")

    def get_response(self, user_message):
        """
        Get AI response from Groq for user message
        Maintains conversation context
        
        Args:
            user_message (str): User's question or command
            
        Returns:
            str: AI-generated response
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            logger.info(f"Sending to Groq: {user_message}")
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=self.conversation_history,
                model=self.model,
                temperature=self.temperature,
                max_tokens=1024,
            )
            
            # Extract response
            response_text = chat_completion.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            logger.info(f"Groq response: {response_text}")
            
            # Keep conversation history manageable (last 10 messages)
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error getting response from Groq: {e}")
            return "Sorry, I couldn't process your request. Please try again."

    def get_simple_response(self, user_message):
        """
        Get response without maintaining conversation history
        Useful for simple queries
        
        Args:
            user_message (str): User's question
            
        Returns:
            str: AI-generated response
        """
        try:
            logger.info(f"Simple query to Groq: {user_message}")
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": user_message}
                ],
                model=self.model,
                temperature=self.temperature,
                max_tokens=512,
            )
            
            response_text = chat_completion.choices[0].message.content
            logger.info(f"Groq response: {response_text}")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error getting simple response: {e}")
            return "I couldn't understand that. Can you please repeat?"

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    def get_music_recommendation(self, mood_or_genre):
        """
        Get music recommendation based on mood or genre
        
        Args:
            mood_or_genre (str): User's mood or desired genre
            
        Returns:
            str: Song or artist recommendation
        """
        prompt = f"I want to listen to music. My mood is: {mood_or_genre}. Suggest a popular song or artist that matches this mood. Just give me 1-2 songs with artist names."
        
        return self.get_simple_response(prompt)

    def process_video_search_query(self, query):
        """
        Process and refine video search query
        
        Args:
            query (str): User's video search query
            
        Returns:
            str: Refined search query
        """
        prompt = f"User wants to search YouTube video with this query: '{query}'. Provide a clean, searchable version of this query (just 2-4 key words)."
        
        return self.get_simple_response(prompt)


# Test function
if __name__ == "__main__":
    print("Groq Assistant Module Test")
    print("=" * 50)
    
    try:
        assistant = GroqAssistant()
        
        # Test simple response
        print("\n1. Testing simple response...")
        response = assistant.get_simple_response("What is the capital of India?")
        print(f"Question: What is the capital of India?")
        print(f"Answer: {response}\n")
        
        # Test music recommendation
        print("2. Testing music recommendation...")
        recommendation = assistant.get_music_recommendation("happy and energetic")
        print(f"Mood: happy and energetic")
        print(f"Recommendation: {recommendation}\n")
        
        # Test conversation history
        print("3. Testing conversation context...")
        response1 = assistant.get_response("My name is Alice")
        print(f"Message 1: My name is Alice")
        print(f"Response: {response1}\n")
        
        response2 = assistant.get_response("What is my name?")
        print(f"Message 2: What is my name?")
        print(f"Response: {response2}\n")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        print("\nMake sure you have set GROQ_API_KEY in config.py")
