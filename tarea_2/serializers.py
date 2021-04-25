from rest_framework import serializers 
from tarea_2.models import Artist
 
 
class ArtistSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Artist
        fields = ('artist_id',
                  'name',
                  'age',
                  'albums',
                  'tracks',
                  'self_url')
