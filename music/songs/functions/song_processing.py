# Processing functions for Song Objects
from django.core.exceptions import MultipleObjectsReturned
from django.db import close_connection, reset_queries
from songs.models import *

def set_song_values(song, fields):
    """
    Sets the values of a Song object from a line of an uploaded file, doing 
    validation and verification.
    If errors, return error message for failure, else return None
    """
    # Check title validity and set if passes, else return error message
    if fields[0] == "":
        return None, "No Title Found"
    else:
        song.title = "%s" %(fields[0])

    # Check for author existence, else skip
    if fields[1] != "":
        song.author = "%s" %(fields[1])

    # Look up key-signature from table and return id
    if fields[2] != "":
        try:        
            key = KeySigs.objects.get(key_sig = fields[2])
            song.key_sig_id = key.id
        except KeySigs.DoesNotExist:
            return None, "Error with key signature"
        
    # Add themes
    if fields[3] != "":
        song.theme = "%s" %(fields[3])

    # Look up Source id and return
    if fields[4] != "":
        try:
            src = SourceMusic.objects.get(source = str(fields[4]))
            song.source_id = src.id
        except (SourceMusic.DoesNotExist):
            return None, "Error with Music Source"

    return song, None