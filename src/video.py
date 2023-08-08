from src.channel import Channel

class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        video_response = Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',id=video_id).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/watch?v={video_id}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
