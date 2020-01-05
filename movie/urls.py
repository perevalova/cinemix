from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import MainPage, MovieDetail, MovieList, SearchView, \
    MovieCategoryList

app_name = 'movie'
urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    # path('random/', Random.as_view(), name='random'),
    path('<slug:type>/', MovieList.as_view(), name='list'),
    path('<slug:type>/<slug:category>/', MovieCategoryList.as_view(), name='list_category'),
    path('<slug:type>/<slug:category>/<slug:movie>/', MovieDetail.as_view(), name='detail'),
]