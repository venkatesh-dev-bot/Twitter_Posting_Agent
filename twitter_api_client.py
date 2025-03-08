import os
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TwitterAPIClient:
    def __init__(self):
        # Load Twitter API credentials from environment variables
        self.consumer_key = os.getenv('consumer_key')
        self.consumer_secret = os.getenv('consumer_secret')
        self.access_token = os.getenv('access_token')
        self.access_token_secret = os.getenv('access_token_secret')
        self.bearer_token = os.getenv('Bearer_token')
        
        # Initialize the API client
        self.client = None
        self.api = None
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize the Twitter API client using credentials"""
        try:
            # Initialize v2 client
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            
            # Initialize v1.1 API for media uploads
            auth = tweepy.OAuth1UserHandler(
                self.consumer_key,
                self.consumer_secret,
                self.access_token,
                self.access_token_secret
            )
            self.api = tweepy.API(auth)
            
            return True
        except Exception as e:
            print(f"Error initializing Twitter API client: {e}")
            return False
    
    def post_tweet(self, text):
        """Post a tweet with text content"""
        try:
            response = self.client.create_tweet(text=text)
            return response.data['id']
        except Exception as e:
            print(f"Error posting tweet: {e}")
            return None
    
    def post_tweet_with_media(self, text, media_path):
        """Post a tweet with media attachment"""
        try:
            # Upload media using v1.1 API
            media = self.api.media_upload(filename=media_path)
            media_id = media.media_id
            
            # Post tweet with media using v2 API
            response = self.client.create_tweet(
                text=text,
                media_ids=[media_id]
            )
            return response.data['id']
        except Exception as e:
            print(f"Error posting tweet with media: {e}")
            return None
    
    def delete_tweet(self, tweet_id):
        """Delete a tweet by ID"""
        try:
            self.client.delete_tweet(id=tweet_id)
            return True
        except Exception as e:
            print(f"Error deleting tweet: {e}")
            return False
    
    def get_user_info(self):
        """Get information about the authenticated user"""
        try:
            response = self.client.get_me(user_fields=['name', 'username', 'description', 'profile_image_url'])
            return response.data
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None 