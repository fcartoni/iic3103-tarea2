from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Artist
from . serializers import ArtistSerializer
from . controllers import ArtistController

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view

from base64 import b64encode

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the tarea_2 index")

@api_view(['GET', 'POST'])
def get_artists(request):

    if request.method not in ('GET', 'POST'):
        return HttpResponse(status=405)

    if request.method == 'GET':
        artists = ArtistController.get_all_artists()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        artist_data = request.data
        if "name" not in artist_data.keys() or "age" not in artist_data.keys():
            return JsonResponse({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif type(artist_data['name']) == str and type(artist_data['age']) == int:
                new_artist = ArtistController.create_artist(artist_data)
                serializer = ArtistSerializer(new_artist)
                if new_artist == 'Already Exists':
                    return JsonResponse({'message': 'This artist already exists'}, status=status.HTTP_409_CONFLICT)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'DELETE'])
def get_artist_by_id(request, artist_id):

    if request.method not in ('GET', 'DELETE'):
        return HttpResponse(status=405)
    
    if request.method == 'GET':
        artist = ArtistController.artist_by_id(artist_id)
        if artist == 'Does Not Exist':
            return JsonResponse({'message': 'This artist does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        else:
            serializer = ArtistSerializer(artist, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        artist = ArtistController.delete_artist(artist_id)
        if artist == 'Does Not Exist':
            return JsonResponse({'message': 'This artist does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        else:
            return JsonResponse({'message': 'Artist deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['POST'])
# def create_artist(request):
#         artist_data = JSONParser().parse(request)
#         artist_serializer = ArtistSerializer(data=tutorial_data)
#         if artist_serializer.is_valid():
#             artist_serializer.save()
#             return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         #return JsonResponse(tutorial_serializer.errors, status=status.HTTP_409_CONFLICT)


# class ArtistView(APIView):
#     serializer_class = ArtistSerializer

#     def get_all_artists(self):
#         artists = Artist.objects.all()
#         return artists
    
#     def get_artist_by_id(self, artist_id):
#         try: 
#             artist = Artist.objects.get(artist_id=artist_id) 
#         except Artist.DoesNotExist: 
#             return JsonResponse({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

#     def get(self, request, *args, **kwargs):
#         artist_id = request.query_params()
#         artists = self.get_all_artists()
#         serializer = ArtistSerializer(artists, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         artist_data = request.data
#         id_encoded =  b64encode(artist_data['name'].encode()).decode('utf-8')
#         if len(id_encoded) > 22:
#             id_encoded = id_encoded[:22]
#         new_artist = Artist.objects.create(artist_id=id_encoded, name=artist_data['name'], 
#         age=artist_data['age'], albums=artist_data['albums'], tracks=artist_data['tracks'], self_url=artist_data['self_url'])

#         new_artist.save()
#         serializer = ArtistSerializer(new_artist)

#         return Response(serializer.data)
