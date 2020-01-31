from django.forms import ModelForm

from movie.models import Movie


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['rating']
