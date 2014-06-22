from django.shortcuts import render
from django.contrib import admin
from django.conf.urls import patterns, url
from django.db import IntegrityError
from django import forms

from songs.models import Song, SourceMusic, KeySigs
from songs.functions.song_processing import set_song_values

# Form Object for File Upload
class BulkForm(forms.Form):
    file = forms.FileField()

# Function for handling bulk file uploads. Do not use bulk_create
# so we can check the validity of each new Song object
def bulk_upload_songs(songfile):
    """
    Given a file of songs, will insert them into the database.
    Will not insert songs that are not (title, author) unique
    Returns a list of failed songs that trigger IntegrityError Exception
    """
    errors = []
    # skip headers
    songfile.readline()
    # Extract information from each row and create song objects, validating info.
    for line in songfile:
        fields = line.strip().split(",")
        song = Song()
        song, status = set_song_values(song, fields)
        
        if status is not None:
            errors.append([fields, status])
            continue
        else:
            try:
                song.save()
            except IntegrityError:
                errors.append([fields, "Failed to write to DB. Possible duplicate"])
    
    if len(errors) == 0:
        errors.append("No errors. All songs successfully inserted")
    
    return errors

class SongAdmin(admin.ModelAdmin):
    fields = ['title', 'author', 'key_sig', 'theme', 'source']
    raw_id_fields = ['source', 'key_sig']

    def get_urls(self):
        urls = super(SongAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'^bulk/$', self.bulk, name="bulk")
                           )

        return my_urls + urls


    def bulk(self, request):
        if request.method == "POST":
            form = BulkForm(request.POST, request.FILES)
            if form.is_valid():
                errors = bulk_upload_songs(request.FILES['file'])
                                
                context = {'post-submit': 'success',
                            'status': 'win',
                            'message': errors
                            }
            else:
                context = {'status' : 'fail',
                       'message': 'form not valid'}
        else:
            form = BulkForm()
            context = {'form': form}
        return render(request, 'admin/bulk.html', context)

admin.site.register(Song, SongAdmin)
admin.site.register(SourceMusic)
admin.site.register(KeySigs)
