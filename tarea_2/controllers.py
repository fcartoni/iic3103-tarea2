from . models import Artist, Album, Track
from . serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from . import views
from base64 import b64encode

class ArtistController(object):

    def get_all_artists():
        artists = Artist.objects.all()
        return artists

    def create_artist(artist_data):
        id_encoded =  b64encode(artist_data['name'].encode()).decode('utf-8')
        id_encoded = id_encoded[:22]
        if Artist.objects.filter(artist_id=id_encoded):
            new_artist = None
            return new_artist
        else: 
            if "albums" not in artist_data.keys():
                artist_data['albums'] = ''
            if "tracks" not in artist_data.keys():
                artist_data['tracks'] = ''
            if "self" not in artist_data.keys():
                artist_data['self'] = ''
        new_artist = Artist.objects.create(artist_id=id_encoded, name=artist_data['name'], 
                    age=artist_data['age'], albums=artist_data['albums'], tracks=artist_data['tracks'],
                    self_url=artist_data['self'])
        new_artist.save()
        return new_artist

    def artist_by_id(artist_id):
        try:
            artist = Artist.objects.get(artist_id=artist_id)
        except:
            artist = None
        return artist
    
    def delete_artist(artist_id):
        try:
            artist = Artist.objects.get(artist_id=artist_id)
            artist = Artist.objects.filter(artist_id=artist_id).delete()
        except:
            artist = None
        try:
            albums_of_artist = Album.objects.filter(artist=artist).delete()
        except:
            pass
        return artist

class AlbumController(object):

    def get_all_albums():
        albums = Album.objects.all()
        return albums

    def obtain_album_by_artist(artist):
        albums_by_artist = Album.objects.filter(artist=artist) #no va a encontrar eso, artist es un objeto
        return albums_by_artist

    def create_album(album_data, artist_id):
        id_encoded =  b64encode(album_data['name'].encode()).decode('utf-8')
        id_encoded = id_encoded[:22]
        if Album.objects.filter(album_id=id_encoded):
            new_album = None
            return new_album
        else:
            if "artist" not in album_data.keys():
                album_data['artist'] = ''
            if "tracks" not in album_data.keys():
                album_data['tracks'] = ''
            if "self" not in album_data.keys():
                album_data['self'] = ''
        new_album = Album.objects.create(album_id=id_encoded, name=album_data['name'], 
                    genre=album_data['genre'], artist=album_data['artist_id'], artist_url=album_data['artist'], tracks_url=album_data['tracks'],
                    self_url=album_data['self'])
        new_album.save()
        return new_album
    
    def obtain_album_by_id(album_id):
        try:
            album_by_id = Album.objects.get(album_id=album_id)
        except:
            album_by_id = None
        return album_by_id
    
    def delete_album(album_id):
        try:
            album = Album.objects.get(album_id=album_id)
            album = Album.objects.filter(album_id=album_id).delete()
        except:
            album = None
        return album

class TrackController(object):

    def get_all_tracks():
        tracks = Track.objects.all()
        return tracks