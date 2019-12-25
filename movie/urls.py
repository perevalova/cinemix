from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import MainPage, MovieDetail, CategoryView

app_name = 'movie'
urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    # path('search/', Search.as_view(), name='searching'),
    # path('random/', Random.as_view(), name='random'),
    path('<slug:type>/<slug:category>/', CategoryView.as_view(), name='category'),
    path('<slug:type>/<slug:category>/<slug:movie>/', MovieDetail.as_view(), name='movie_detail'),
]