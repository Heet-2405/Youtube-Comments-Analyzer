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