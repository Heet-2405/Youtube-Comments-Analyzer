from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv
import warnings

warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Configure YouTube API
DEVELOPER_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def get_channel_id(video_id):
    """Fetches the channel ID for a given video."""
    try:
        response = youtube.videos().list(part='snippet', id=video_id).execute()
        if not response['items']:
            print("Error: Invalid Video ID")
            return None
        return response['items'][0]['snippet']['channelId']
    except HttpError as error:
        print(f'YouTube API Error: {error}')
        return None
    
def get_video_stats(video_id):
    """Fetches video statistics (views, likes, etc.)."""
    try:
        response = youtube.videos().list(part='statistics', id=video_id).execute()
        if not response['items']:
            print("Error: Invalid Video ID")
            return None
        return response['items'][0]['statistics']
    except HttpError as error:
        print(f'YouTube API Error: {error}')
        return None

def get_channel_info(channel_id):
    """Fetches YouTube channel details."""
    try:
        response = youtube.channels().list(
            part='snippet,statistics,brandingSettings',
            id=channel_id
        ).execute()

        if not response['items']:
            print("Error: Invalid Channel ID")
            return None

        info = response['items'][0]
        return {
            'channel_title': info['snippet']['title'],
            'video_count': info['statistics']['videoCount'],
            'channel_logo_url': info['snippet']['thumbnails']['high']['url'],
            'channel_created_date': info['snippet']['publishedAt'],
            'subscriber_count': info['statistics']['subscriberCount'],
            'channel_description': info['snippet']['description']
        }
    except HttpError as error:
        print(f'YouTube API Error: {error}')
        return None