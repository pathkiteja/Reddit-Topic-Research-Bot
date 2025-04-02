import praw
#import tweepy  # Twitter API usage commented out due to access limitations
import speech_recognition as sr
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

# Path to your service account credentials JSON file
# C:\Users\91996\Desktop\Assignment\client_secret_745508424436-fcj14vfcmsr4422e2957cjkaa6qd3lh9.apps.googleusercontent.com.json
# sixth-syntax-455615-j2-efee4870f1c0.json
SERVICE_ACCOUNT_FILE = 'sixth-syntax-455615-j2-efee4870f1c0.json'  # Replace with your credentials file path

# Define the required scope for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Your Google Sheet ID (found in the URL of your sheet)
SHEET_ID = "1trl6FWfNx9OatbnDl9yJZkpRYSOda0MjrFBi6v-4GPo"  # Replace with your actual Google Sheet ID

# Initialize Google Sheets API using OAuth2
def create_sheet_service():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)

# Function to write data to Google Sheets
def write_to_sheet(service, data):
    try:
        body = {'values': data}
        service.values().append(
            spreadsheetId=SHEET_ID,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body=body
        ).execute()
        print("✅ Data written to Google Sheets successfully!")
    except HttpError as e:
        print(f"❌ Google Sheets API error: {e}")

# Initialize Reddit API
def get_reddit_data(query):
    reddit = praw.Reddit(
        client_id='BW53DU23xz5aHtiEJaWRQw',
        client_secret='SXslOk5xpiHYn6zgT3iSrHalFc1u8Q',
        user_agent='ResearchBot/1.0'          # Replace with your Reddit user agent
    )
    posts = reddit.subreddit('all').search(query, limit=5)
    results = [["Reddit Title", "URL", "Number of Comments"]]
    
    for post in posts:
        results.append([post.title, post.url, post.num_comments])
    
    return results

# Twitter API function commented out due to access limitations
"""
def get_twitter_data(query):
    auth = tweepy.OAuth1UserHandler(
        consumer_key='your_consumer_key',
        consumer_secret='your_consumer_secret',
        access_token='your_access_token',
        access_token_secret='your_access_token_secret'
    )
    api = tweepy.API(auth)
    tweets = api.search_tweets(q=query, count=5)
    results = [["Twitter Text", "URL", "Engagement Score"]]
    
    for tweet in tweets:
        tweet_url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
        engagement = tweet.favorite_count + tweet.retweet_count
        results.append([tweet.text, tweet_url, engagement])
    
    return results
"""

# Convert speech to text (for voice input)
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for your query...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("❌ Sorry, I didn't understand that.")
        return None

# Main function
def main():
    choice = input("Enter 'T' for text input or 'V' for voice input: ").strip().upper()
    
    if choice == 'V':
        query = get_voice_input()
        if not query:
            print("🔄 Voice input failed. Switching to text input.")
            query = input("Enter your query: ")
    else:
        query = input("Enter your query: ")

    print(f"🔍 Searching for: {query}")

    reddit_data = get_reddit_data(query)
    # Twitter API usage commented out:
    # twitter_data = get_twitter_data(query)

    # Combine data from Reddit (and Twitter if enabled)
    # all_data = reddit_data + twitter_data
    all_data = reddit_data

    # Write to Google Sheets
    sheet_service = create_sheet_service().spreadsheets()
    write_to_sheet(sheet_service, all_data)

if __name__ == "__main__":
    main()