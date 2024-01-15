from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("YT_API_KEY")


class Video:
    def __init__(self, video_id):
        self.id = video_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = (
            youtube.videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id
            ).execute())
        self.title = video_response["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/watch?v={video_id}"
        self.viewCount = video_response["items"][0]["statistics"]["viewCount"]
        self.likeCount = video_response["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return f"{self.title}"


class PLVideo:
    def __init__(self, video_id, playlist_id):
        self.video_id = video_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = (
            youtube.videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id
            ).execute())
        self.title = video_response["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/watch?v={video_id}"
        self.viewCount = video_response["items"][0]["statistics"]["viewCount"]
        self.likeCount = video_response["items"][0]["statistics"]["likeCount"]
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.title}"
