from django.urls import path
from django.conf.urls import url 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artists', views.get_artists, name='get_artists'),
    path('artists/<artist_id>', views.get_artist_by_id, name='get_artist_by_id')
]