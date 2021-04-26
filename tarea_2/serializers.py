from rest_framework import serializers 
from tarea_2.models import Artist, Album, Track
 
 
class ArtistSerializer(serializers.ModelSerializer):
    self = serializers.SerializerMethodField('get_self_url')
    id = serializers.SerializerMethodField('get_artist_id')
    self = serializers.SerializerMethodField('generate_self')
    albums = serializers.SerializerMethodField('genereate_albums_url')
    tracks = serializers.SerializerMethodField('generate_tracks_url')

    class Meta:
        model = Artist
        fields = ('id',
                  'name',
                  'age',
                  'albums',
                  'tracks',
                  'self')

    def get_self_url(self, obj):
        return obj.self_url

    def get_artist_id(self, obj):
        return obj.artist_id

    def genereate_albums_url(self, obj):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/artists/{obj.artist_id}/albums'

    def generate_tracks_url(self, obj):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/artists/{obj.artist_id}/tracks'


    def generate_self(self, obj):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/artists/{obj.artist_id}'

class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_album_id')
    self = serializers.SerializerMethodField('get_self_url')
    self = serializers.SerializerMethodField('generate_self')
    artist = serializers.SerializerMethodField('generate_artist_url')
    artist_id = serializers.SerializerMethodField('get_artist_id')
    tracks = serializers.SerializerMethodField('generate_tracks_url')
    #falta generar el artist_url

    class Meta:
        model = Album
        fields = ('id',
                  'artist_id',
                  'name',
                  'genre',
                  'artist',
                  'tracks',
                  'self')

    def get_album_id(self, obj):
        return obj.album_id
    
    def get_self_url(self, obj):
        return obj.self_url

    def get_artist_id(self, obj): #artist en mi bbdd es artist_id
        return obj.artist.artist_id
    
    def generate_self(self, obj):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/albums/{obj.album_id}'
    
    def generate_artist_url(self, obj):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/artists/{obj.artist.artist_id}'

    def generate_tracks_url(self, obj):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/albums/{obj.album_id}/tracks'

class TrackSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_track_id')
    self = serializers.SerializerMethodField('get_self_url')
    self = serializers.SerializerMethodField('generate_self')
    album_id = serializers.SerializerMethodField('get_album_id')
    artist = serializers.SerializerMethodField('generate_artist_url')
    album = serializers.SerializerMethodField('generate_album_url')

    class Meta:
        model = Track
        fields = ('id', #track_id
                  'album_id', #album --> object
                  'name',
                  'duration',
                  'times_played',
                  'artist', #artist_url
                  'album', #album_url
                  'self') #self_url

    def get_track_id(self, obj):
        return obj.track_id

    def get_self_url(self, obj):
        return obj.self_url
    
    def get_album_id(self, obj):
        return obj.album.album_id

    def generate_self(self, obj):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/tracks/{obj.track_id}'
    
    def generate_artist_url(self, obj):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/artists/{obj.album.artist.artist_id}'

    def generate_album_url(self, obj):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/albums/{obj.album.album_id}'