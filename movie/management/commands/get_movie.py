"""for rezka.ag"""
import sys

# from slugify import slugify
from concurrent.futures.thread import ThreadPoolExecutor
from decimal import Decimal

from django.utils.text import slugify
from threading import Thread
from requests_html import HTMLSession
from django.core.management.base import BaseCommand

from movie.models import *


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    title = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[1]/h1')[0].text
    print(title)
    slug = slugify(title)
    type = url.split('/')[3]
    year = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[3]/td[2]/a')
    year = str(year).split('/')[-1]
    runtime = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[10]/td[2]')
    runtime = str(runtime).split()[0]
    genres = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[6]/td[2]')
    countries = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[4]/td[2]')
    categories = response.html.xpath('/html/body/div[1]/div/div[5]/div/div/span[3]/a')
    categories_slug = url.split('/')[4]
    image = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[1]/div/div/a/img/@src')
    # video1 = url
    plot = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[4]/div[2]/text()')
    imdb = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[1]/td[2]/span[1]/span/text()')
    # imdb = Decimal(int(str(imdb)))
    kinopoisk = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[1]/td[2]/span[2]/span/text()')
    kinopoisk = Decimal(int(str(kinopoisk)))

    # actor = response.html.xpath('//*[@id="main"]/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[12]/td/div/span[2]/span/a/span')
    # actor2 = response.html.xpath('//*[@id="main"]/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[12]/td/div/span[3]/span/a/span')
    # actor3 = response.html.xpath('//*[@id="main"]/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[12]/td/div/span[4]/span/a/span')
    director = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[5]/td[2]/div/span/span/a/span/text()')

    actors = []
    for i in range(2, 7):
        item = '/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[12]/td/div/span[' + str(i) + ']/span/a/span/text()'
        actors.append(response.html.xpath(item))

    try:
        with HTMLSession() as session2:
            img_resp = session2.get(image)

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
        'type': type,
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
        country, created = Genre.objects.get_or_create(title=country, slug=slugify(country))
        stuff.countries.add(country)

    for actor in actors:
        actor, created = Actor.objects.get_or_create(title=actor, slug=slugify(actor))
        stuff.actors.add(actor)

    category = {'title': categories, 'slug': slugify(categories_slug)}
    category, created = Category.objects.get_or_create(**category)
    stuff.category.add(category)

    director = {'title': director, 'slug': slugify(director)}
    director, created = Director.objects.get_or_create(**director)
    stuff.director.add(director)

    print('Success:', url)


class Command(BaseCommand):
    help = 'Running movies scraper'

    def handle(self, *args, **options):
        url = ''
        # Thread(target=crawler, args=(url, )).start()
        # print('Done!')
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(crawler, url)
        print('Done!')
