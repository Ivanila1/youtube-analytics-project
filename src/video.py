from src.channel import Channel

class WrongVideoID(Exception):
    def __init__(self):
        self.message = 'Неправильный видео id:'


class Video:
    def __init__(self, video_id):
        try:
            self.video_id = video_id
            self.video_response = Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',id=video_id).execute()
            if self.video_response['pageInfo']['totalResults'] > 0:
                self.title: str = self.video_response['items'][0]['snippet']['title']
                self.url: str = f'https://www.youtube.com/watch?v={video_id}'
                self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
                self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
            else:
                self.video_response = None
                self.title = None
                self.url = None
                self.view_count = None
                self.like_count = None
                raise WrongVideoID

        except WrongVideoID as ex:
            print(f'{ex.message} {video_id}')

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
