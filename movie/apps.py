from django.apps import AppConfig


class MovieConfig(AppConfig):
    name = 'movie'

    def ready(self):
        from movie import signals
