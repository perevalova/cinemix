from movie.models import Category, Collection


def movie_processor(request):
    """Returns movies category objects"""
    films = Category.objects.filter(movie__type='2').distinct()
    cartoons = Category.objects.filter(movie__type='3').distinct()
    serials = Category.objects.filter(movie__type='4').distinct()
    animations = Category.objects.filter(movie__type='1').distinct()
    collections = Collection.objects.all()

    return {'FILMS': films,
            'CARTOONS': cartoons,
            'SERIALS': serials,
            'ANIMATIONS': animations,
            'COLLECTIONS': collections}

