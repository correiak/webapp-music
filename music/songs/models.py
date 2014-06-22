from django.db import models

# Create your models here.
class KeySigs(models.Model):
    """Model forr containing key signatures of songs"""
    key_sig = models.CharField(max_length = 10)

    def __unicode__(self):
        return self.key_sig

class SourceMusic(models.Model):
    """Model for storing sources and locations of songs by publication"""
    source = models.CharField(max_length = 20)

    def __unicode__(self):
        return self.source

class Song(models.Model):
    """Model which stores choral repertoire of music"""
    title = models.CharField(max_length = 50)
    author = models.CharField(max_length = 50, default = "", null = True)
    key_sig = models.ForeignKey(KeySigs, null = True)
    theme = models.CharField(max_length = 30, null = True)
    source = models.ForeignKey(SourceMusic)

    class Meta:
        unique_together = ('title', 'author')

    def __unicode__(self):
        return self.title

class Schedule(models.Model):
    """Model for storing the choral singing schedule"""
    sunday_date = models.DateField(unique = True)
    entrance = models.ForeignKey(Song, related_name='schedule_entrance')
    offertory = models.ForeignKey(Song, related_name='schedule_offertory')
    communion = models.ForeignKey(Song, related_name='schedule_communion')
    meditation = models.ForeignKey(Song, null = True, related_name='schedule_meditation')
    recessional = models.ForeignKey(Song, related_name='schedule_recessional')

    def __unicode__(self):
        return self.sunday_date