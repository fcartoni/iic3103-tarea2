from django.urls import path
from django.conf.urls import url 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artists', views.get_artists, name='get_artists'),
    path('artists/<artist_id>', views.get_artist_by_id, name='get_artist_by_id'),
    path('albums', views.get_albums, name='get_albums'),
    path('artists/<artist_id>/albums', views.get_albums_by_artist, name='get_albums_by_artist'), #get y post de album
    path('albums/<album_id>', views.get_album_by_id, name='get_album_by_id'),
    path('tracks', views.get_tracks, name='get_tracks'),
    path('albums/<album_id>/tracks', views.get_tracks_by_album_id, name='get_tracks_by_album_id'),
    path('artists/<artist_id>/tracks', views.get_tracks_by_artist_id, name='get_tracks_by_artist_id'),
    path('tracks/<track_id>', views.get_track_by_id, name='get_track_by_id'),
    path('artists/<artist_id>/albums/play', views.play_artist_tracks, name='play_artist_tracks'),
    path('albums/<album_id>/tracks/play', views.play_album_tracks, name='play_album_tracks'),
    path('tracks/<track_id>/play', views.play_track, name='play_track')
]