from django.shortcuts import render, get_object_or_404

from songs.models import Song

# Create your views here.
def index(request):
    return render(request, 'songs/music_base.html', {'message': "This is the index"})

def detail(request, song_id):
    song = get_object_or_404(Song, pk = song_id)
    context = {'message': {'note':"This is song page: %s" %(song_id)},
               'song': song
               }
    return render(request, 'songs/song.html', context)