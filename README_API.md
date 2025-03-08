# Twitter API Posting Agent

This project provides tools for posting to Twitter (X) using the Twitter API v2 with tweepy. It includes both a simple command-line script and a Streamlit web application that can generate tweet content using AI models (OpenAI, Anthropic, or Google Gemini) and post it to Twitter.

## Features

- Authenticate with Twitter API using API keys
- Post text tweets
- Post tweets with media attachments
- Generate tweet content using AI models
- User-friendly web interface with Streamlit
- Character count display to ensure tweets are within limits

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your environment variables in a `.env` file:
   ```
   # Twitter API credentials
   consumer_key=your_consumer_key
   consumer_secret=your_consumer_secret
   Bearer_token=your_bearer_token
   access_token=your_access_token
   access_token_secret=your_access_token_secret
   
   # AI model API keys (optional, only needed for AI tweet generation)
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Usage

### Twitter API Client

The `TwitterAPIClient` class in `twitter_api_client.py` provides methods for interacting with the Twitter API:

```python
from twitter_api_client import TwitterAPIClient

# Initialize the client
twitter = TwitterAPIClient()

# Post a tweet
tweet_id = twitter.post_tweet("Hello, Twitter!")

# Post a tweet with media
media_tweet_id = twitter.post_tweet_with_media("Check out this image!", "path/to/image.jpg")

# Get user information
user_info = twitter.get_user_info()
print(f"Authenticated as: @{user_info.username}")

# Delete a tweet
twitter.delete_tweet(tweet_id)
```

### Command-line Example

Run the `api_tweet_example.py` script to post tweets from the command line:

```
python api_tweet_example.py
```

This will post a simple text tweet and a tweet with an image (if the image file exists).

### Streamlit Web Application

Run the `api_app.py` script to launch the Streamlit web application:

```
streamlit run api_app.py
```

The web application provides a user-friendly interface for:
1. Selecting an AI model to generate tweet content
2. Entering a topic for the tweet
3. Generating tweet content
4. Posting the tweet to Twitter
5. Viewing a link to the posted tweet

## Files

- `twitter_api_client.py`: Twitter API client class
- `api_tweet_example.py`: Command-line example script
- `api_app.py`: Streamlit web application
- `requirements.txt`: Project dependencies

## Notes

- Make sure your Twitter API credentials have the necessary permissions for posting tweets.
- The Twitter API v2 requires a developer account and appropriate access levels.
- The AI tweet generation feature requires API keys for the respective AI services.
- The default image file is expected to be named `X_twitter.png` in the project directory.

## Troubleshooting

- If you encounter authentication errors, check that your API keys are correct and have the necessary permissions.
- If media uploads fail, ensure that the file exists and is in a supported format (JPG, PNG, GIF, or MP4).
- If the AI models fail to generate content, check that your API keys are valid and have sufficient quota. 