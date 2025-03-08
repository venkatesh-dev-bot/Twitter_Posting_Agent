import os
from twitter_api_client import TwitterAPIClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define user information
TWITTER_USERNAME = '@KVenkatesh65977'
TWITTER_EMAIL = 'kunchalavenkatesh17@gmail.com'

def main():
    # Initialize the Twitter API client
    twitter = TwitterAPIClient()
    
    # Get user information
    user_info = twitter.get_user_info()
    if user_info:
        print(f"Authenticated as: @{user_info.username}")
        print(f"Expected username: {TWITTER_USERNAME}")
    else:
        print(f"Could not authenticate. Using credentials for: {TWITTER_USERNAME} / {TWITTER_EMAIL}")
    
    # Post a simple tweet
    tweet_text = "Hello Twitter! This is a tweet posted using the Twitter API v2 with tweepy."
    tweet_id = twitter.post_tweet(tweet_text)
    
    if tweet_id:
        print(f"Tweet posted successfully! Tweet ID: {tweet_id}")
        
        # Post a tweet with media
        media_path = "X_twitter.png"  # Make sure this file exists in your project directory
        if os.path.exists(media_path):
            media_tweet_text = "Check out this image! #TwitterAPI"
            media_tweet_id = twitter.post_tweet_with_media(media_tweet_text, media_path)
            
            if media_tweet_id:
                print(f"Tweet with media posted successfully! Tweet ID: {media_tweet_id}")
            else:
                print("Failed to post tweet with media.")
        else:
            print(f"Media file {media_path} not found.")
    else:
        print("Failed to post tweet.")

if __name__ == "__main__":
    main() 