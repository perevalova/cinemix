from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.urls import reverse
from django.utils.text import slugify


class MovieType(models.Model):
    slug = models.SlugField(max_length=10, blank=True)
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Country(models.Model):
    slug = models.SlugField(max_length=50, blank=True)
    title = models.CharField(max_length=50)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.title


class Category(models.Model):
    slug = models.SlugField(max_length=255, blank=True)
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Genre(models.Model):
    slug = models.SlugField(max_length=50, blank=True)
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Actor(models.Model):
    slug = models.SlugField(max_length=255, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Director(models.Model):
    slug = models.SlugField(max_length=255, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Movie(models.Model):
    RATING_CHOICES = [(i, f'{i}') for i in range(11)]

    slug = models.SlugField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    type = models.ForeignKey(MovieType, on_delete=models.CASCADE, blank=True, null=True)
    year = models.PositiveSmallIntegerField()
    runtime = models.PositiveSmallIntegerField()
    genres = models.ManyToManyField(Genre)
    countries = models.ManyToManyField(Country)
    categories = models.ManyToManyField(Category, blank=True)
    image = models.ImageField(upload_to='img/', blank=True)
    trailer = models.URLField(blank=True)
    video1 = models.URLField(blank=True)
    video2 = models.URLField(blank=True)
    plot = models.TextField()
    imdb = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    kinopoisk = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    actors = models.ManyToManyField(Actor)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, blank=True, null=True)
    watched = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        category = self.categories.all()[0].slug
        kwargs = {
            'type': self.type.slug,
            'category': category,
            'movie': self.slug,
        }

        return reverse('movie:detail', kwargs=kwargs)


class Collection(models.Model):
    slug = models.SlugField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    movie = models.ManyToManyField(Movie, related_name='collections', blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title