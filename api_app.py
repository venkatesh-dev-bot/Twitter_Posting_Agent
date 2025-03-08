import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from twitter_api_client import TwitterAPIClient

# Load environment variables
load_dotenv()

# User information
TWITTER_USERNAME = os.getenv('USERNAME', '@KVenkatesh65977')
TWITTER_EMAIL = os.getenv('EMAIL', 'kunchalavenkatesh17@gmail.com')

# Set page configuration
st.set_page_config(page_title="Twitter API Posting Agent", layout="wide")
st.title("Twitter API Posting Agent")
st.caption(f"Connected to Twitter account: {TWITTER_USERNAME}")

# Initialize the Twitter API client
@st.cache_resource
def get_twitter_client():
    return TwitterAPIClient()

twitter_client = get_twitter_client()

# Function to generate tweet content
async def generate_tweet_content(topic, model_name):
    # Initialize the selected AI model
    if model_name == 'ANTHROPIC_MODEL':
        llm = ChatAnthropic(model="claude-3-7-sonnet-20250219", api_key=os.getenv('ANTHROPIC_API_KEY'), temperature=0)
    elif model_name == 'GEMINI_MODEL':
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.getenv('GEMINI_API_KEY'), temperature=0)
    else:  # Default to OpenAI
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv('OPENAI_API_KEY'), temperature=0)
    
    # Create a structured prompt for generating tweet content
    prompt = f"""Create an engaging tweet about the following topic: {topic}. 
                Make it interesting and concise (under 280 characters).
                Only return the tweet content, no other text or comments."""
    
    # Use the AI model to generate tweet content
    with st.spinner(f"Generating tweet using {model_name}..."):
        if model_name == 'GEMINI_MODEL':
            # Format the input for Google Generative AI
            messages = [{"role": "user", "content": prompt}]
            response = await llm.ainvoke(messages)
            tweet_content = response.content
        else:
            response = await llm.ainvoke(prompt)
            tweet_content = response.content
    
    return tweet_content.strip()

# Function to post tweet
def post_tweet(tweet_content, include_image=False):
    try:
        with st.spinner("Posting tweet..."):
            if include_image and os.path.exists('X_twitter.png'):
                tweet_id = twitter_client.post_tweet_with_media(tweet_content, 'X_twitter.png')
            else:
                tweet_id = twitter_client.post_tweet(tweet_content)
            
            if tweet_id:
                return True, tweet_id
            else:
                return False, None
    except Exception as e:
        st.error(f"Error creating tweet: {e}")
        return False, None

# Main app function
async def main():
    # Display user info
    user_info = twitter_client.get_user_info()
    if user_info:
        st.sidebar.success(f"Authenticated as: @{user_info.username}")
    else:
        st.sidebar.warning(f"Using credentials for: {TWITTER_USERNAME}")
        st.sidebar.info("Note: Authentication status will be confirmed when posting a tweet")
    
    # Sidebar for model selection
    st.sidebar.header("Settings")
    model_options = {
        'ANTHROPIC_MODEL': 'Claude (Anthropic)',
        'GEMINI_MODEL': 'Gemini (Google)',
        'CHATGPT_MODEL': 'GPT (OpenAI)'
    }
    selected_model = st.sidebar.selectbox(
        "Select AI Model",
        list(model_options.keys()),
        format_func=lambda x: model_options[x]
    )
    
    include_image = st.sidebar.checkbox("Include default image (X_twitter.png)")
    
    # Main content area
    topic = st.text_input("Enter a topic for your tweet:")
    
    col1, col2 = st.columns(2)
    generate_button = col1.button("Generate Tweet")
    post_button = col2.button("Post Tweet", disabled=not 'tweet_content' in st.session_state)
    
    # Generate tweet
    if generate_button and topic:
        tweet_content = await generate_tweet_content(topic, selected_model)
        st.session_state.tweet_content = tweet_content
        st.success("Tweet generated successfully!")
        st.code(tweet_content)
        
        # Character count
        char_count = len(tweet_content)
        st.info(f"Character count: {char_count}/280")
    
    # Display current tweet if available
    if 'tweet_content' in st.session_state:
        st.subheader("Current Tweet:")
        st.code(st.session_state.tweet_content)
        
        # Character count
        char_count = len(st.session_state.tweet_content)
        st.info(f"Character count: {char_count}/280")
    
    # Post tweet
    if post_button and 'tweet_content' in st.session_state:
        success, tweet_id = post_tweet(st.session_state.tweet_content, include_image)
        if success:
            st.balloons()
            st.success(f"Tweet posted successfully! Tweet ID: {tweet_id}")
            
            # Add a link to the tweet
            if user_info:
                tweet_url = f"https://twitter.com/{user_info.username}/status/{tweet_id}"
                st.markdown(f"[View your tweet]({tweet_url})")
            else:
                tweet_url = f"https://twitter.com/{TWITTER_USERNAME.replace('@', '')}/status/{tweet_id}"
                st.markdown(f"[View your tweet]({tweet_url})")

# Run the app
if __name__ == "__main__":
    asyncio.run(main()) 