"""for rezka.ag with BeautifulSoup without motto and slogan"""
import sys
from threading import Thread

import requests
from bs4 import BeautifulSoup as bs
from django.core.management import BaseCommand

from movie.models import *


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
url = ''

def crawler():
    session = requests.Session()
    request = session.get(url, headers=headers)
    from slugify import slugify

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')

        title = soup.find('h1', attrs={'itemprop': 'name'}).get_text()
        movie_type = url.split('/')[3]
        image = soup.find('img', attrs={'itemprop': 'image'})['src']
        plot = soup.find('div', attrs={'class': 'b-post__description_text'}).get_text().lstrip()
        rating = soup.find_all('span', attrs={'class': 'bold'})
        imdb = rating[0].get_text()
        kinopoisk = rating[1].get_text()
        kinopoisk = kinopoisk[:3]
        table = soup.find_all('tr')
        year = table[1].find('a').get_text()
        year = year.split()[0]
        slug = slugify(title + '-' + year)
        runtime = soup.find('td', attrs={'itemprop': 'duration'}).get_text().split()[0]
        director = soup.find('span', attrs={'itemprop': 'director'}).find('span').get_text()
        categories = soup.find_all('span', attrs={'itemprop': 'genre'})[0].get_text()
        categories_slug = url.split('/')[4]

        genres = []
        for genre in soup.find_all('span', attrs={'itemprop': 'genre'}):
            genres.append(genre.get_text())

        countries = []
        for country in table[2].find_all('a'):
            countries.append(country.get_text())

        actors = []
        actors_items = soup.find_all('div', attrs={'class': 'persons-list-holder'})[1].find_all('span', attrs={'itemprop': 'name'})[:3]
        for actor in actors_items:
            actors.append(actor.get_text())

        try:
            img_resp = requests.get(image)

            image_name = 'img/' + slug + image[-4:]

            with open(f'media/{image_name}', 'wb') as imgf:
                imgf.write(img_resp.content)

            del img_resp
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno)
            image_name = 'default.jpg'


        movie = {
            'title': title,
            'slug': slug,
            'image': image_name,
            'video1': url,
            'year': year,
            'runtime': runtime,
            'plot': plot,
            'imdb': imdb,
            'kinopoisk': kinopoisk,
        }
        try:
            stuff = Movie.objects.create(**movie)
        except Exception as e:
            print(type(e), e)
            return

        for genre in genres:
            genre, created = Genre.objects.get_or_create(title=genre, slug=slugify(genre))
            stuff.genres.add(genre)

        for country in countries:
            country, created = Country.objects.get_or_create(title=country, slug=slugify(country))
            stuff.countries.add(country)

        for actor in actors:
            actor, created = Actor.objects.get_or_create(name=actor, slug=slugify(actor))
            stuff.actors.add(actor)

        category = {'title': categories, 'slug': slugify(categories_slug)}
        category, created = Category.objects.get_or_create(**category)
        stuff.categories.add(category)

        create_type = {'title': movie_type.title(), 'slug': slugify(movie_type)}
        create_type, created = MovieType.objects.get_or_create(**create_type)
        stuff.type = create_type
        stuff.save()

        director = {'name': director, 'slug': slugify(director)}
        director, created = Director.objects.get_or_create(**director)
        stuff.director = director
        stuff.save()

        print('Success:', url)


class Command(BaseCommand):
    help = 'Running movies scraper'

    def handle(self, *args, **options):
        crawler()
        print('Done!')
        # with ThreadPoolExecutor(max_workers=10) as executor:
        #     executor.map(crawler, url)
