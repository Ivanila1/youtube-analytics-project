import datetime
import isodate
from src.channel import Channel


class PlayList:

    def __init__(self, playlist_id):
        __get_service = Channel.get_service()
        playlist = __get_service.playlists().list(part="snippet,contentDetails", id=playlist_id).execute()
        self.playlist_videos = __get_service.playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResults=50, ).execute()
        self._video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self._video_response = __get_service.videos().list(part='contentDetails,statistics', id=','.join(self._video_ids)).execute()
        self.title: str = playlist['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/playlist?list={playlist_id}'

    @property
    def total_duration(self):
        duration = datetime.timedelta()
        for video in self._video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        url = None
        most_liked = 0
        for i in range(len(self._video_response['items'])):
            if most_liked < int(self._video_response['items'][i]['statistics']['likeCount']):
                most_liked = int(self._video_response['items'][i]['statistics']['likeCount'])
                url = f"https://youtu.be/{self._video_response['items'][i]['id']}"
        return url
