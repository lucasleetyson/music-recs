import json

from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse

from musicovery import musicoveryclient
from youtube import youtubeclient
from genius import geniusclient

def index(request: HttpRequest):
    if request.method == 'POST':
        parameters = list()
        for param in request.POST:
            if param is not 'csrfmiddlewaretoken':
                parameters.append(param + "=" + request.POST.get(param))
        query = "&".join(parameters)
        return redirect(reverse('list_tracks') + '?' + query)
    moods = musicoveryclient.get_moods()
    template = loader.get_template('index.html')
    context = {
        "moods": moods,
    }
    return HttpResponse(template.render(context, request))


def list_tracks(request):
    mood = request.GET.get('mood', 'sad')
    min_popularity = int(request.GET.get('minpopularity', 25))
    max_popularity = int(request.GET.get('maxpopularity', 100))
    min_year = int(request.GET.get('minyear', 2010))
    max_year = int(request.GET.get('maxyear', 2020))
    items = musicoveryclient.playlist_from_tag(mood, min_popularity, max_popularity, min_year, max_year)
    tracks = list()
    for item in items:
        track = {
            'title': item['title'],
            'artist': item['artist_display_name'],
            'genre': item['genre']
        }
        #try:
         #   youtube_result = youtubeclient.search_youtube(track['title'])
          #  print(youtube_result)
           # youtube_url = 'https://www.youtube.com/watch?v=' + youtube_result[0]['id']['videoId']
            #track['youtube_url'] = youtube_url
            #track['thumbnail'] = youtube_result[0]['snippet']['thumbnails']['high']['url']
        #except:
         #   track['youtube_url'] = youtube_url
           # track['thumbnail'] = youtube_result[0]['snippet']['thumbnails']['high']['url']
        track['youtube_url'] = 'https://www.youtube.com/results?search_query=' + track['artist'] + ' ' + track['title']
        try:
            genius_response = geniusclient.search(track['title'])
            track['thumbnail'] = genius_response['response']['hits'][0]['result']['song_art_image_thumbnail_url']
        except Exception as e:
            track['thumbnail'] = ''
        tracks.append(track)
    context = {
        "tracks": tracks
    }
    template = loader.get_template('list_tracks.html')
    return HttpResponse(template.render(context, request))
