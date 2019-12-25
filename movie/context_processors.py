from movie.models import Category


def film_processor(request):
    """Returns film category objects"""

    films = []
    categories = Category.objects.filter(movie__type__slug='films')
    for film in categories:
        if {'slug': film.slug, 'title': film.title,} not in films:
            films.append({
                'slug': film.slug,
                'title': film.title,
            })

    return {'FILMS': films}


def cartoon_processor(request):
    """Returns cartoon category objects"""

    cartoons = []
    categories = Category.objects.filter(movie__type__slug='cartoons')
    for cartoon in categories:
        if {'slug': cartoon.slug, 'title': cartoon.title, } not in cartoons:
            cartoons.append({
                'slug': cartoon.slug,
                'title': cartoon.title,
            })

    return {'CARTOONS': cartoons}


def serial_processor(request):
    """Returns serial category objects"""

    serials = []
    categories = Category.objects.all()
    for serial in categories.filter(movie__type__slug='serials'):
        if {'slug': serial.slug, 'title': serial.title, } not in serials:
            serials.append({
                'slug': serial.slug,
                'title': serial.title,
            })

    return {'SERIALS': serials}


def animation_processor(request):
    """Returns animation category objects"""

    animations = []
    categories = Category.objects.filter(movie__type__slug='animation')
    for animation in categories:
        if {'slug': animation.slug, 'title': animation.title, } not in animations:
            animations.append({
                'slug': animation.slug,
                'title': animation.title,
            })

    return {'ANIMATIONS': animations}
