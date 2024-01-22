import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv("YT_API_KEY")


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel = youtube.channels().list(id=self.__channel_id,
                                                 part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = (
            self.channel)['items'][0]['snippet']['description']
        self.url = \
            f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"
        self.subscriberCount = (
            self.channel)['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self):
        print(self.channel)

    def __str__(self):
        return f"{self.title} ({self.url})"

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        with open(filename, 'w') as fp:
            json.dump(dict(channel_id=self.__channel_id,
                           title=self.title,
                           description=self.description,
                           url=self.url,
                           subscriberCount=self.subscriberCount,
                           video_count=self.video_count,
                           viewCount=self.viewCount), fp, ensure_ascii=False)

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        return self.subscriberCount > other.subscriberCount

    def __ge__(self, other):
        return self.subscriberCount >= other.subscriberCount

    def __lt__(self, other):
        return self.subscriberCount < other.subscriberCount

    def __le__(self, other):
        return self.subscriberCount <= other.subscriberCount

    def __eq__(self, other):
        return self.subscriberCount == other.subscriberCount
