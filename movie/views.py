from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from django.views.generic import DetailView, ListView
from django.views.generic.base import View, TemplateView
from star_ratings.models import Rating

from movie.models import Movie, Category, MovieType, Genre


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
        # movies_query = Movie.objects.all()
        context['movies'] = Movie.objects.all()[:8]

        return context


class MovieList(ListView):
    template_name = 'movie_list.html'
    model = Movie
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        movies_list = Movie.objects.filter(type__slug=self.kwargs['type'])
        # genres = movies_list.

        genres = self.request.GET.get('genres', '')
        if genres:
            for genre in genres:
                movies_list = movies_list.filter(genres__slug=genre)

        order_by = self.request.GET.get('order_by', '')
        if order_by == 'newest':
            movies_list = movies_list.order_by('-year')
        elif order_by == 'oldest':
            movies_list = movies_list.order_by('year')

        movie_type = self.kwargs['type']

        genres_list = Genre.objects.all()


        paginator = Paginator(movies_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)

        context = {
            'movies': movies,
            'genres': genres_list,
            'type': movie_type,
            # 'category': movie_category,
        }

        return context


class MovieCategoryList(ListView):
    template_name = 'movie_category_list.html'
    model = Movie
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        movies_list = Movie.objects.filter(type__slug=self.kwargs['type'], categories__slug=self.kwargs['category'])

        genres = self.request.GET.getlist('genres', '')

        if genres:
            for genre in genres:
                movies_list = movies_list.filter(genres__slug=genre)

        year_from = self.request.GET.get('year_from', '')
        year_to = self.request.GET.get('year_to', '')

        if year_from and year_to:
            movies_list = movies_list.filter(year__range=(year_from, year_to))

        order_by = self.request.GET.get('order_by', '')
        if order_by == 'newest':
            movies_list = movies_list.order_by('-year')
        elif order_by == 'oldest':
            movies_list = movies_list.order_by('year')

        movie_type = self.kwargs['type']
        movie_category = self.kwargs['category']

        genres_list = Genre.objects.all()


        paginator = Paginator(movies_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)

        context = {
            'movies': movies,
            'genres': genres_list,
            'type': movie_type,
            'category': movie_category,
        }

        return context


class SearchView(ListView):
    template_name = 'search.html'
    model = Movie
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        search_movie = self.request.GET.get('q', '')
        if search_movie:
            movies = Movie.objects.filter(title__icontains=search_movie)

        # apply pagination, 10 students per page
        # context = paginate(movies, 10, self.request, context)

        context = {
            'movies': movies
        }

        return context
