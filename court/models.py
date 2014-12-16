from django.db import models

class Court(models.Model):
    uuid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    updated_at = models.CharField(max_length=200)
    closed = models.BooleanField(default=False)
    alert = models.CharField(max_length=2000, blank=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    number = models.CharField(max_length=200, blank=True)
    dx = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name
