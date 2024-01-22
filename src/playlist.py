from src.channel import Channel
from dotenv import load_dotenv
from datetime import timedelta
import os
import isodate

load_dotenv()
api_key = os.getenv("YT_API_KEY")


class PlayList:
    youtube = Channel.get_service()

    def __init__(self, _id_):
        self.__id = _id_
        self.url = f"https://www.youtube.com/playlist?list={_id_}"
        self.playlist_videos = (self.youtube.playlistItems().
                                list(playlistId=_id_,
                                     part='contentDetails,snippet',
                                     maxResults=50,
                                     ).execute())
        video_ids = self.get_videos()
        self.response = self.youtube.videos().list(part='contentDetails,statistics',
                                                   id=','.join(video_ids)
                                                   ).execute()
        playlist_info = self.youtube.playlists().list(id=self.__id,
                                                      part='snippet',
                                                      ).execute()
        self.title = playlist_info['items'][0]['snippet']['title']

    def get_videos(self):
        """
        Получить список id видео, находящиеся в плейлисте
        """
        video_ids: list[str] = [video['contentDetails']['videoId']
                                for video in self.playlist_videos['items']]
        return video_ids

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta`
        с суммарной длительность плейлиста
        """

        total_duration = timedelta(hours=0)

        for video in self.response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное
        видео из плейлиста (по количеству лайков)
        """
        max_likes = 0
        video_id = ''
        for video in self.response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_likes:
                max_likes = like_count
                video_id = video['id']

        return f'https://youtu.be/{video_id}'
