"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from models import *
from functions.song_processing import set_song_values

class BulkUploadTests(TestCase):
    def test_set_song_values_song_with_no_title(self):
        """
        set_song_values should return a tuple of None, "No Title Found"
        if no song title is set to a song object
        """
        testsong = Song()
        fields = ['' for x in range(5)]
        result = (None, "No Title Found")
        self.assertEqual(set_song_values(testsong, fields), result)

    def test_set_song_values_song_with_invalid_keysig(self):
        """
        set_song_values should return a tuple of None, "Error with key signature"
        if an incorrect key signature, not present in that table, is set to the song object
        """
        testsong = Song()
        fields =['title', 'author', 'Z-major', 'theme', ''] # Leave source blank to skip
        result = (None, "Error with key signature")
        self.assertEqual(set_song_values(testsong, fields), result)

    def test_set_song_values_song_with_invalid_source(self):
        """
        set_song_values should return a tuple of None, "Error with source"
        if an incorrect key signature, not present in that table, is set to the song object
        """
        testsong = Song()
        fields = ['title', 'author', '', 'theme', 'ABC'] # Leave key signature blank to skip
        result = (None, "Error with Music Source")
        self.assertEqual(set_song_values(testsong, fields), result)