# Twitter Posting Agent

## Overview
This project is a Twitter Posting Agent that allows users to post tweets dynamically using AI-generated content. The application supports multiple AI models, including ChatGPT, Gemini, and Anthropic, to create engaging tweets based on user-defined topics.

## Features
- **Dynamic Model Selection**: Users can choose between different AI models for generating tweet content.
- **Twitter Integration**: The application uses the Twikit library to interact with the Twitter API for posting tweets.
- **Session Management**: The application manages login sessions, allowing users to log in once every 24 hours.

## Requirements
- Python 3.7+
- Required libraries:
  - `twikit`
  - `crewai`
  - `langchain_openai`
  - `langchain_anthropic`
  - `langchain_google_genai`
  - `python-dotenv`

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Twitter_Posting_Agent
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   .\venv\Scripts\activate  # For Windows
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Set up your Twitter credentials in a `.env` file:
   ```
   USERNAME=your_username
   EMAIL=your_email@example.com
   PASSWORD=your_password
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Follow the prompts to select the AI model and enter the topic for the tweet.

## Example
```bash
Enter the model to use (ANTHROPIC_MODEL, GEMINI_MODEL, or CHATGPT_MODEL): ANTHROPIC_MODEL
Enter the topic for the tweet: The future of AI technology.
Generated tweet content: "AI technology is evolving rapidly, shaping the future of industries and everyday life!"
``` 

## License
This project is licensed under the MIT License.