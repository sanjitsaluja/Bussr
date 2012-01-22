from django.db import models

# Create your models here.

class Stop(models.Model):
    stopId = models.CharField(max_length=20, primary_key=True)
    stopCode = models.CharField(max_length=20, blank=True, null=True)
    stopName = models.CharField(max_length=100)
    stopDesc = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    zoneId = models.CharField(max_length=20, blank=True, null=True)
    stopUrl = models.URLField(blank=True, null=True)
    locationType = models.IntegerField()
    parentStation = models.CharField(max_length=20, blank=True, null=True)
    wheelchairAccessible = models.BooleanField(blank=True) 
    
    def __unicode__(self):
        return u'%s, %s' % (self.stopId, self.stopName)
    
    
class Route(models.Model):
    routeId = models.CharField(max_length=20, primary_key=True)
    agencyId = models.CharField(max_length=20, blank=True, null=True)
    routeShortName = models.CharField(max_length=20)
    routeLongName = models.CharField(max_length=100)
    routeDesc = models.CharField(max_length=100, blank=True, null=True)
    routeType = models.IntegerField()
    routeUrl = models.URLField(blank=True, null=True)
    routeColor = models.CharField(max_length=10, blank=True, null=True)
    routeTextColor = models.CharField(max_length=10, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s, %s' % (self.routeId, self.routeShortName)