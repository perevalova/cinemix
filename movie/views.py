import random

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from movie.forms import MovieForm
from movie.models import Movie, Genre
from movie.util import paginate, filtering


class MovieDetail(DetailView):
    model = Movie
    template_name = 'movie_detail.html'

    def get_object(self, queryset=None):
        obj = Movie.objects.select_related('type', 'director').prefetch_related('genres', 'countries', 'actors', 'categories').get(type__slug=self.kwargs['type'], categories__slug=self.kwargs['category'], slug=self.kwargs['movie'])

        return obj

    def post(self, request, *args, **kwargs):
        # form for send rating
        movie = self.get_object()
        form = MovieForm(data=self.request.POST, instance=movie)
        if form.is_valid():
            form.save()

        return JsonResponse({'status': 'success'})

    # def get_context_data(self, **kwargs):
    #     sim_movies = Movie.objects.filter(type__slug=self.kwargs['type'], genres=)


class MainPage(ListView):
    template_name = 'index.html'
    queryset = Movie.objects.all().select_related('type').prefetch_related('categories')[:12]
    context_object_name = 'movies'


class MovieList(ListView):
    template_name = 'movie_list.html'
    model = Movie
    context_object_name = 'movies'
    paginate_by = 10

    def get_queryset(self):
        movies_list = Movie.objects.filter(
            type__slug=self.kwargs['type']).select_related(
            'type').prefetch_related('genres', 'countries', 'categories')
        # filtering
        movies_list = filtering(self.request, movies_list)

        return movies_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        movie_amount = self.get_queryset().count()
        movie_type = self.kwargs['type']
        # show genres for filtering
        genres_list = Genre.objects.only('slug', 'title')

        context = paginate(self.get_queryset(), self.paginate_by, self.request, context, var_name='movies')

        context['genres_list'] = genres_list
        context['type'] = movie_type
        context['movie_amount'] = movie_amount

        return context


class CollectionList(ListView):
    template_name = 'movie_list.html'
    model = Movie
    context_object_name = 'movies'
    paginate_by = 10

    def get_queryset(self):
        movies_list = Movie.objects.filter(
            collections__slug=self.kwargs['collection']).select_related(
            'type').prefetch_related('genres', 'countries', 'categories')
        # filtering
        movies_list = filtering(self.request, movies_list)

        return movies_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        movie_amount = self.get_queryset().count()
        movie_collection = self.kwargs['collection']
        # show genres for filtering
        genres_list = Genre.objects.only('slug', 'title')

        context = paginate(self.get_queryset(), self.paginate_by, self.request, context, var_name='movies')

        context['genres_list'] = genres_list
        context['type'] = movie_collection
        context['movie_amount'] = movie_amount

        return context


class MovieCategoryList(ListView):
    template_name = 'movie_category_list.html'
    model = Movie
    context_object_name = 'movies'
    paginate_by = 10

    def get_queryset(self):
        movies_list = Movie.objects.filter(type__slug=self.kwargs['type'],
                                           categories__slug=self.kwargs[
                                               'category']).select_related(
            'type').prefetch_related('genres', 'countries', 'categories')
        # filtering
        movies_list = filtering(self.request, movies_list)

        return movies_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        movie_amount = self.get_queryset().count()
        movie_type = self.kwargs['type']
        movie_category = self.kwargs['category']

        # show genres for filtering
        genres_list = Genre.objects.only('slug', 'title')

        context = paginate(self.get_queryset(), self.paginate_by, self.request, context, var_name='movies')

        context['genres_list'] = genres_list
        context['type'] = movie_type
        context['category'] = movie_category
        context['movie_amount'] = movie_amount

        return context


class SearchView(ListView):
    template_name = 'search.html'
    model = Movie
    context_object_name = 'movies'
    paginate_by = 10

    def get_queryset(self):
        movies = Movie.objects.none()
        search_movie = self.request.GET.get('q', '')
        if search_movie:
            movies = Movie.objects.filter(
                title__search=search_movie).select_related(
                'type', 'director').prefetch_related(
                'genres', 'countries', 'actors', 'categories')

        return movies

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        movie_amount = self.get_queryset().count()
        context = paginate(self.get_queryset(), self.paginate_by, self.request,
                           context, var_name='movies')
        context['movie_amount'] = movie_amount

        return context


class RandomMovie(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'random_movie.html')

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('random', ''):
            from django.db.models import Max
            max_id = Movie.objects.all().aggregate(max_id=Max("id"))['max_id']
            while True:
                pk = random.randint(1, max_id)
                movie = Movie.objects.filter(pk=pk).select_related('type', 'director').prefetch_related('genres', 'countries', 'categories', 'actors').first()

                if movie:
                    return render(request, 'random_movie.html',
                                  {'object': movie})
