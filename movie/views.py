from django.shortcuts import render, get_object_or_404

from django.views.generic import DetailView, ListView
from django.views.generic.base import View, TemplateView
from star_ratings.models import Rating

from movie.models import Movie, Category, MovieType


class MovieDetail(DetailView):
    model = Movie
    template_name = 'movie_detail.html'

    def get_object(self, query_set=None):
        return get_object_or_404(
            Movie,
            type__slug=self.kwargs['type'],
            categories__slug=self.kwargs['category'],
            slug=self.kwargs['movie'],
        )


class MainPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = Movie.objects.all()[:8]
        # movie_id = []
        # for movie in movies:
        #     movie_id.append(movie.id)
        context['movies'] = movies
        # ratings = []
        # rating = Rating.objects.all()
        # for rate in movie_id:
        #     from django.core.exceptions import ObjectDoesNotExist
        #     try:
        #         ratings.append(rating.get(object_id=rate))
        #     except Exception as e:
        #         import sys
        #         print(e, type(e), sys.exc_info()[-1].tb_lineno)
        # context['ratings'] = ratings

        return context


class CategoryView(ListView):
    template_name = 'movie_list.html'
    model = Movie

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = Movie.objects.filter(type__slug=self.kwargs['type'], categories__slug=self.kwargs['category'])
        movie_type = self.kwargs['type']
        movie_category = self.kwargs['category']
        context = {
            'movies': movies,
            'type': movie_type,
            'category': movie_category,
        }

        return context
