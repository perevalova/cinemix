"""get trailer from YouTube Data API"""

import requests
from django.core.management import BaseCommand

from cinemix.settings import YOUTUBE_DATA_API_KEY
from movie.models import Movie


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}


def get_trailers():
    # select films without trailer
    movies = Movie.objects.filter(trailer__exact='').only('title', 'trailer')
    for movie in movies:
        title = ('+').join(movie.title.split())
        search_query = title + '+трейлер'
        print(movie.title)
        trailer = crawler(search_query)
        if trailer:
            movie.trailer = trailer
            movie.save()
            print('Success!!!')
        else:
            continue


def crawler(query):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    search_params = {
        'part': 'snippet',
        'q': query,
        'key': YOUTUBE_DATA_API_KEY,
        'maxResults': 1,
        'type': 'video',
        'videoDuration': 'short' # 4 minutes video
    }
    session = requests.Session()
    request = session.get(search_url, params=search_params, headers=headers)
    if request.status_code == 200:
        results = request.json()['items']
        video_id = results[0]['id']['videoId']
        video = f'https://www.youtube.com/watch?v={video_id}'
        # video_ids = []
        # for result in results:
        #     video_ids.append(result['id']['videoId'])
        # video = f'https://www.youtube.com/watch?v={video_ids[0]}'
        print('Video:', video)

        return video
    else:
        print(request.status_code)


class Command(BaseCommand):
    help = 'Running trailer scraper'

    def handle(self, *args, **options):
        get_trailers()
        print('Done!')
