import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from twikit import Client

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="AI Tweet Generator", layout="wide")
st.title("AI Tweet Generator")

# Initialize the client for Twitter
@st.cache_resource
def get_twitter_client():
    return Client('en-US')

client = get_twitter_client()
logged_in = False

# Function to login to Twitter
async def login_to_twitter():
    global logged_in
    if not logged_in:
        try:
            with st.spinner("Logging into Twitter..."):
                await client.login(
                    auth_info_1=os.getenv('USERNAME'),
                    auth_info_2=os.getenv('EMAIL'),
                    password=os.getenv('PASSWORD'),
                    cookies_file='cookies.json'
                )
            logged_in = True
            return True
        except Exception as e:
            st.error(f"Error logging in: {e}")
            return False
    return True

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
    prompt = f"""Create an engaging tweet about the following topic: {topic}. Make it interesting and concise.
                only return the tweet content, no other text or comments that also only one line"""
    
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
    
    return tweet_content

# Function to post tweet
async def post_tweet(tweet_content, include_image=False):
    try:
        with st.spinner("Posting tweet..."):
            await client.create_tweet(text=tweet_content)
            
            # If user wants to include an image
            if include_image:
                file_path = 'X_twitter.png'
                if os.path.exists(file_path):
                    media_ids = []
                    media_ids.append(await client.upload_media(file_path))
                    await client.create_tweet(text='Check out this image!', media_ids=media_ids)
                else:
                    st.warning(f"Image file {file_path} not found.")
        
        return True
    except Exception as e:
        st.error(f"Error creating tweet: {e}")
        return False

# Main app function
async def main():
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
    
    # Display current tweet if available
    if 'tweet_content' in st.session_state:
        st.subheader("Current Tweet:")
        st.code(st.session_state.tweet_content)
    
    # Post tweet
    if post_button and 'tweet_content' in st.session_state:
        login_success = await login_to_twitter()
        if login_success:
            post_success = await post_tweet(st.session_state.tweet_content, include_image)
            if post_success:
                st.balloons()
                st.success("Tweet posted successfully!")

# Run the app
if __name__ == "__main__":
    asyncio.run(main())
