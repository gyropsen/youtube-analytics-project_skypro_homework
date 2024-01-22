from src.video import Video
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
        playlist_videos = (self.youtube.playlistItems().
                           list(playlistId=_id_,
                                part='contentDetails,snippet',
                                maxResults=50,
                                ).execute())
        self.title = playlist_videos["items"][0]["snippet"]["title"]

    def get_videos(self):
        """
        Получить список id видео, находящиеся в плейлисте
        """
        playlist_videos = (self.youtube.playlistItems().
                           list(playlistId=self.__id,
                                part='contentDetails',
                                maxResults=50,
                                ).execute())
        video_ids: list[str] = [video['contentDetails']['videoId']
                                for video in playlist_videos['items']]
        return video_ids

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta`
        с суммарной длительность плейлиста
        """
        video_ids = self.get_videos()

        response = self.youtube.videos().list(part='contentDetails,statistics',
                                              id=','.join(video_ids)
                                              ).execute()

        total_duration = timedelta(hours=0)

        for video in response['items']:
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
        video_ids = self.get_videos()

        max_video_ids = max([video.likeCount, video.id]
                            for video in [Video(video) for video in video_ids])
        return f"https://youtu.be/{max_video_ids[1]}"
