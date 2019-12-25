"""for filmix"""
import sys

from slugify import slugify
from concurrent.futures.thread import ThreadPoolExecutor
from decimal import Decimal

from threading import Thread
from requests_html import HTMLSession
from django.core.management.base import BaseCommand

from movie.models import *


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    title = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[2]/div[1]/h1/text()')
    print(title)
    slug = slugify(title)
    type = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/div[1]/span[3]/a/@href')
    type = str(type).split('/')[-1]
    year = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[2]/div[13]/span[2]')
    print(year)
    year = str(year).split()[-1]
    print(year)
    runtime = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[2]/div[17]/span[2]')
    runtime = str(runtime).split()[0]
    print(runtime)
    # genres = response.html.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[6]/td[2]')
    # print('genres ' + genres)
    countries = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[2]/div[15]/span[2]/span/a/text()')
    categories = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/div[1]/span[5]/a/span/text()')
    # categories_slug = url.split('/')[4]
    image = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[1]/span/a/img/@src')
    # video1 = url
    plot = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[2]/div[3]/div[1]/text()')
    print(plot)
    imdb = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[3]/div[1]/footer/span[2]/p[1]')
    print(imdb)
    imdb = Decimal(int(str(imdb)[:3]))
    print(str(imdb))
    print(Decimal(int(str(imdb)[:3])))
    kinopoisk = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[3]/div[1]/footer/span[1]/p[1]')
    print(kinopoisk)
    print(str(kinopoisk))
    print(Decimal(int(str(kinopoisk)[:3])))
    kinopoisk = Decimal(int(str(kinopoisk)[:3]))

    # actor = response.html.xpath('//*[@id="main"]/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[12]/td/div/span[2]/span/a/span')
    # actor2 = response.html.xpath('//*[@id="main"]/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[12]/td/div/span[3]/span/a/span')
    # actor3 = response.html.xpath('//*[@id="main"]/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[12]/td/div/span[4]/span/a/span')
    director = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[2]/div[5]/span[2]/span/a/span/text()')
    actors1 = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[2]/div[6]/span[2]')
    genres2 = response.html.xpath('/html/body/div[4]/div[1]/div[3]/section/div/div/article/div[2]/div[12]/span[2]')
    # actors = []
    # for i in range(2, 7):
    #     item = '/html/body/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr[12]/td/div/span[' + str(i) + ']/span/a/span/text()'
    #     actors.append(response.html.xpath(item))

    try:
        with HTMLSession() as session2:
            img_resp = session2.get(image)

        image_name = 'img/' + slug + image[-1]

        with open(f'media/{image_name}', 'wb') as imgf:
            imgf.write(img_resp.content)

        del img_resp
    except Exception as e:
        print(e, type(e), sys.exc_info()[-1].tb_lineno)
        image_name = 'default.jpg'


    movie = {
        'title': title,
        # 'slug': slug,
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

    for genre in genres2:
        genre, created = Genre.objects.get_or_create(title=genre, slug=slugify(genre))
        stuff.genres.add(genre)

    for country in countries:
        country, created = Genre.objects.get_or_create(title=country, slug=slugify(country))
        stuff.countries.add(country)

    for actor in actors1:
        actor, created = Actor.objects.get_or_create(title=actor, slug=slugify(actor))
        stuff.actors.add(actor)

    category = {'title': categories}
    category, created = Category.objects.get_or_create(**category)
    stuff.category.add(category)

    director = {'title': director, 'slug': slugify(director)}
    director, created = Director.objects.get_or_create(**director)
    stuff.director.add(director)

    print('Success:', url)


class Command(BaseCommand):
    help = 'Running movies scraper'

    def handle(self, *args, **options):
        url = 'https://filmix.co/dramy/63613-elizium-2013.html'
        Thread(target=crawler, args=(url, )).start()
        print('Done!')
        # with ThreadPoolExecutor(max_workers=10) as executor:
        #     executor.map(crawler, url)
