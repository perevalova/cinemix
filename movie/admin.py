from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from star_ratings.models import Rating

from .models import Movie, MovieType, Category, Country, Director, Actor, Genre


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ActorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class RatingInline(GenericStackedInline):
    model = Rating
    fields = ['total']
    extra = 0


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'year',)
    list_filter = ('type',)
    search_fields = ['title', 'genres']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
    inlines = (RatingInline,)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(MovieType)