import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = Channel.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['thumbnails']["default"]['url']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.views_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} {self.url}'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2,ensure_ascii=False))

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv("API_KEY_YT")
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


    def to_json(self, filename):
        list_json = {'id': self.channel_id, 'title': self.title, 'description': self.description, 'url': self.url,
                     'subscriber_count': self.subscriber_count, 'video_count': self.video_count,
                     'views_count': self.views_count}
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(list_json, indent=2,ensure_ascii=False))
