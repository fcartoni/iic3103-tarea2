from . models import Artist
from . serializers import ArtistSerializer
from . import views
from base64 import b64encode

class ArtistController(object):

    def get_all_artists():
        artists = Artist.objects.all()
        return artists

    def create_artist(artist_data):
        id_encoded =  b64encode(artist_data['name'].encode()).decode('utf-8')
        if len(id_encoded) > 22:
            id_encoded = id_encoded[:22]
        if Artist.objects.filter(artist_id=id_encoded):
            new_artist = 'Already Exists'
            return new_artist
        else: 
            if "albums" not in artist_data.keys():
                artist_data['albums'] = ''
            if "tracks" not in artist_data.keys():
                artist_data['tracks'] = ''
            if "self_url" not in artist_data.keys():
                artist_data['self_url'] = ''
        new_artist = Artist.objects.create(artist_id=id_encoded, name=artist_data['name'], 
                    age=artist_data['age'], albums=artist_data['albums'], tracks=artist_data['tracks'],
                    self_url=artist_data['self_url'])
        new_artist.save()
        return new_artist

    def artist_by_id(artist_id):
        try:
            artist = Artist.objects.get(artist_id=artist_id)
        except:
            artist = 'Does Not Exist'
        return artist
    
    def delete_artist(artist_id):
        try:
            artist = Artist.objects.get(artist_id=artist_id)
            artist = Artist.objects.filter(artist_id=artist_id).delete()
        except:
            artist = 'Does Not Exist'
            
        return artist