import asyncio
from twikit import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define your Twitter credentials
USERNAME = os.getenv('USERNAME', '@KVenkatesh65977')
EMAIL = os.getenv('EMAIL', 'kunchalavenkatesh17@gmail.com')
PASSWORD = os.getenv('PASSWORD', '@Kvenkatesh1209')

# Initialize the client
client = Client('en-US')

async def main():
    # Log in to your Twitter account
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'  # Optional: to save cookies for future sessions
    )

    # Create a tweet
    await client.create_tweet(text='Hello Twitter! This is a tweet from twikit!')

    # If you want to post media
    media_ids = [
        await client.upload_media('X_twitter.png')
    ]
    await client.create_tweet(text='Check out this image!', media_ids=media_ids)

# Run the main function
asyncio.run(main())
