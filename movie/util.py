from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


def filtering(request, object_list):
    """Filter objects provided by view.

    This function takes:
    * request:
    * list of elements;

    It returns filtered Queryset.
    """

    # filtering by genres
    genres = request.GET.getlist('genres', '')
    if genres:
        for genre in genres:
            object_list = object_list.filter(genres__slug=genre)

    # filtering by rating
    rating = request.GET.get('rating', '')
    if rating:
        object_list = object_list.filter(rating__gte=rating)

    # filtering by year
    year_from = request.GET.get('year_from', '')
    year_to = request.GET.get('year_to', '')

    if year_from and year_to:
        object_list = object_list.filter(year__range=(year_from, year_to))

     # order Queryset
    order_by = request.GET.get('order_by', '')
    if order_by == 'newest':
        object_list = object_list.order_by('-year', 'id')
    elif order_by == 'oldest':
        object_list = object_list.order_by('year', 'id')

    return object_list


def paginate(objects, size, request, context, var_name='object_list'):
    """Paginate objects provided by view.

    This function takes:
    * list of elements;
    * number of objects per page;
    * request object to get url parameters from;
    * context to set new variables into;
    * var_name - variable name for list of objects.

    It returns updated context object.
    """

    # apply pagination
    paginator = Paginator(objects, size)

    # try to get page number from request
    page = request.GET.get('page', 1)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        object_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999),
        # deliver last page of results
        object_list = paginator.page(paginator.num_pages)

    # set variables into context
    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context
