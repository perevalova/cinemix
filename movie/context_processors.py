from movie.models import Category


def film_processor(request):
    """Returns film category objects"""
    films = Category.objects.filter(movie__type='2').distinct()
    
    return {'FILMS': films}


def cartoon_processor(request):
    """Returns cartoon category objects"""
    cartoons = Category.objects.filter(movie__type='3').distinct()

    return {'CARTOONS': cartoons}


def serial_processor(request):
    """Returns serial category objects"""
    serials = Category.objects.filter(movie__type='4').distinct()

    return {'SERIALS': serials}


def animation_processor(request):
    """Returns animation category objects"""
    animations = Category.objects.filter(movie__type='1').distinct()
    
    return {'ANIMATIONS': animations}
