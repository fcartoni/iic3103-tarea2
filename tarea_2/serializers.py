from rest_framework import serializers 
from tarea_2.models import Artist
 
 
class ArtistSerializer(serializers.ModelSerializer):
    self = serializers.SerializerMethodField('get_self_url')
    id = serializers.SerializerMethodField('get_artist_id')
    self = serializers.SerializerMethodField('generate_self')

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

    def generate_self(self, id):
        return f'https://iic3103-tarea2-fcartoni.herokuapp.com/artists/{id}'

