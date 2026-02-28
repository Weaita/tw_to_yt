import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

CLIENT_ID = os.environ['YOUTUBE_CLIENT_ID']
CLIENT_SECRET = os.environ['YOUTUBE_CLIENT_SECRET']
REFRESH_TOKEN = os.environ['YOUTUBE_REFRESH_TOKEN']
TWITCH_URL = os.environ['TWITCH_URL']
VIDEO_TITLE = os.environ['VIDEO_TITLE']

def get_authenticated_service():
    creds = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build('youtube', 'v3', credentials=creds)

def upload_latest_video():
    files = [f for f in os.listdir('.') if f.endswith('.mp4')]
    if not files:
        print("No MP4 files found.")
        return

    files.sort(key=os.path.getmtime)
    video_file = files[-1]
    print(f"Video found: {video_file}")

    try:
        youtube = get_authenticated_service()
        body = {
            'snippet': {
                'title': VIDEO_TITLE,
                'description': f'Auto re-upload from {TWITCH_URL}',
                'tags': ['twitch', 'vod'],
                'categoryId': '20'
            },
            'status': {
                'privacyStatus': 'private',
                'selfDeclaredMadeForKids': False
            }
        }
        ## print(f"Uploading video: {VIDEO_TITLE}")
        media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Progress: {int(status.progress() * 100)}%")
        print(f"Upload complete.")
    except Exception as e:
        print(f"Error: {e}")

upload_latest_video()