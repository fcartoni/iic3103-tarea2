from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Artist, Album, Track
from . serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from . controllers import ArtistController, AlbumController, TrackController

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
            return HttpResponse(status=400)
        elif type(artist_data['name']) == str and type(artist_data['age']) == int:
            new_artist = ArtistController.create_artist(artist_data)
            serializer = ArtistSerializer(new_artist)
            if not new_artist:
                serializer = ArtistSerializer(existing)
                return Response(serializer.data, status=status.HTTP_409_CONFLICT)
                #return JsonResponse({'message': 'This artist already exists'}, status=status.HTTP_409_CONFLICT)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return HttpResponse(status=404)
        
@api_view(['GET', 'DELETE'])
def get_artist_by_id(request, artist_id):

    if request.method not in ('GET', 'DELETE'):
        return HttpResponse(status=405)
    
    if request.method == 'GET':
        artist = ArtistController.artist_by_id(artist_id)
        if not artist:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This artist does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        else:
            serializer = ArtistSerializer(artist, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        artist = ArtistController.delete_artist(artist_id) #se borra el artista y sus albumes
        if not artist:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This artist does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        else:
            albums = AlbumController.obtain_album_by_artist(artist)
            serializers_album = []
            for album in albums:
                tracks_by_album = TrackController.obtain_tracks_by_album(album)
                serializer = TrackSerializer(tracks_by_album, many=True)
                serializers.append(serializer.data)
                track_deleted = TrackController.delete_track(album=serializer.album)
        return HttpResponse(status=204)
        #return JsonResponse({'message': 'Artist deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST']) #/artist/artist_id/album
def get_albums_by_artist(request, artist_id):

    if request.method not in ('GET', 'POST'):
        return HttpResponse(status=405)

    elif request.method == 'GET':
        artist = ArtistController.artist_by_id(artist_id)
        if not artist:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            albums_by_artist = AlbumController.obtain_album_by_artist(artist)
            serializer = AlbumSerializer(albums_by_artist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST': # fijarme q esten los campos, q no exista el album y si no existe el artista return 422
        album_data = request.data
        artist = ArtistController.artist_by_id(artist_id)
        if not artist:
            return HttpResponse(status=422)
        elif "name" not in album_data.keys() or "genre" not in album_data.keys():
            return HttpResponse(status=400)
            #return JsonResponse({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif type(album_data['name']) == str and type(album_data['genre']) == str:
            album_data['artist_id'] = artist
            new_album = AlbumController.create_album(album_data, artist_id)
            serializer = AlbumSerializer(new_album)
            if not new_album:
                serializer = AlbumSerializer(existing)
                return Response(serializer.data, status=status.HTTP_409_CONFLICT)
                #return JsonResponse({'message': 'This album already exists'}, status=status.HTTP_409_CONFLICT)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return HttpResponse(status=400)
            #return JsonResponse({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def get_albums(request): # /albums

    if request.method not in ('GET'):
        return HttpResponse(status=405)

    if request.method == 'GET':
        albums = AlbumController.get_all_albums()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'DELETE'])
def get_album_by_id(request, album_id): #/album/album_id

    if request.method not in ('GET', 'DELETE'):
        return HttpResponse(status=405)

    elif request.method == 'GET':
        album_by_id = AlbumController.obtain_album_by_id(album_id)
        if not album_by_id:
            return HttpResponse(status=404) 
            #return JsonResponse({'message': 'This album does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        else:
            serializer = AlbumSerializer(album_by_id, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE': #delete album with all its tracks
        album = AlbumController.delete_album(album_id)
        if not album:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This album does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        else:
            return HttpResponse(status=204)
            #return JsonResponse({'message': 'Album deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET'])
def get_tracks(request): # /tracks

    if request.method not in ('GET'):
        return HttpResponse(status=405)

    elif request.method == 'GET':
        tracks = TrackController.get_all_tracks()
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def get_tracks_by_album_id(request, album_id): # /albums/<album_id>/tracks

    if request.method not in ('GET', 'POST'):
        return HttpResponse(status=405)
    
    elif request.method == 'GET': # chequear que exista el album
        album = AlbumController.obtain_album_by_id(album_id)
        if not album:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This album does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            tracks_by_album = TrackController.obtain_tracks_by_album(album)
            serializer = TrackSerializer(tracks_by_album, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST': #chequear que exista el album  y que la track no exista y q me entregue lo acampos

        track_data = request.data
        album = AlbumController.obtain_album_by_id(album_id)
        if not album:
            return HttpResponse(status=422) #unprocessable entity
        elif "name" not in track_data.keys() or "duration" not in track_data.keys():
            return HttpResponse(status=400)
            #return JsonResponse({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif type(track_data['name']) == str and type(track_data['duration']) == float:
            track_data['album_id'] = album
            new_track = TrackController.create_track(track_data, album_id)
            serializer = TrackSerializer(new_track)
            if not new_track:
                serializer = TrackSerializer(existing)
                return Response(serializer.data, status=status.HTTP_409_CONFLICT)
                #return JsonResponse({'message': 'This track already exists'}, status=status.HTTP_409_CONFLICT)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return HttpResponse(status=400)
            #return JsonResponse({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def get_tracks_by_artist_id(request, artist_id): # /artist/<artist_id>/tracks
    
    if request.method not in ('GET'):
        return HttpResponse(status=405)
    
    elif request.method == 'GET': #revisar q existe el artist
        artist = ArtistController.artist_by_id(artist_id)
        if not artist:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializers = []
            albums = AlbumController.obtain_album_by_artist(artist)
            for album in albums:
                tracks_by_album = TrackController.obtain_tracks_by_album(album)
                serializer = TrackSerializer(tracks_by_album, many=True)
                serializers.append(serializer.data)
            #tracks_by_artist = TrackController.obtain_tracks_by_artist(artist)
            list_final = []
            for serializer in serializers:
                for s in serializer:
                    list_final.append(s)
            return Response(list_final, status=status.HTTP_200_OK)

@api_view(['GET', 'DELETE'])
def get_track_by_id(request, track_id): # /tracks/track_id
    
    if request.method not in ('GET', 'DELETE'):
        return HttpResponse(status=405)
    
    elif request.method == 'GET':
        track = TrackController.get_tracks_by_id(track_id)
        if not track:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This track does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = TrackSerializer(track, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        track = TrackController.delete_track(track_id)
        if not track:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This track does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        else:
            return HttpResponse(status=204)
            #return JsonResponse({'message': 'Track deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def play_artist_tracks(request, artist_id):
    
    if request.method not in ('PUT'):
        return HttpResponse(status=405)
    
    else:
        artist = ArtistController.artist_by_id(artist_id=artist_id)
        if not artist:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            tracks = []
            albums = AlbumController.obtain_album_by_artist(artist)
            for album in albums:
                tracks_by_album = TrackController.obtain_tracks_by_album(album)
                track = TrackSerializer(tracks_by_album, many=True)
                tracks.append(track.data)
            list_final = []
            for track in tracks:
                for t in track:
                    list_final.append(t)
            for l in list_final:
                track_added = TrackController.add_times_played(l['id'])
                serializer = TrackSerializer(track_added, many=False)                
            return HttpResponse(status=200)
        
@api_view(['PUT'])
def play_album_tracks(request, album_id): #que exista el album
    
    if request.method not in ('PUT'):
        return HttpResponse(status=405)
    
    else:
        album = AlbumController.obtain_album_by_id(album_id=album_id)
        if not album:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This album does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            tracks = TrackController.obtain_tracks_by_album(album)
            for track in tracks:
                track_added = TrackController.add_times_played(track.track_id)
                serializer = TrackSerializer(track_added, many=False)
            return HttpResponse(status=200)

@api_view(['PUT'])
def play_track(request, track_id): #ver q exista si no 404
    
    if request.method not in ('PUT'):
        return HttpResponse(status=405)
    
    else:
        track = TrackController.get_tracks_by_id(track_id)
        if not track:
            return HttpResponse(status=404)
            #return JsonResponse({'message': 'This track does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            track_added = TrackController.add_times_played(track_id)
            serializer = TrackSerializer(track_added, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        


