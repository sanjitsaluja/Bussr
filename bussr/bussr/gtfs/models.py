from django.db import models

# Create your models here.

class Stop(models.Model):
    stopId = models.CharField(max_length=20)
    stopCode = models.CharField(max_length=20, null=True)
    stopName = models.CharField(max_length=100)
    stopDesc = models.CharField(max_length=100, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    zoneId = models.CharField(max_length=20, null=True)
    stopUrl = models.URLField(null=True)
    locationType = models.IntegerField(null=True)
    parentStation = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.stopId + ' ' + self.stopName