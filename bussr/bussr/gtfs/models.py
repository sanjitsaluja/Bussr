from django.contrib.gis.db import models
import json
from django.contrib.gis.db.models.query import GeoQuerySet

# Create your models here.

class Agency(models.Model):
    '''
    Model object representing an Agency (agency.txt)
    '''
    agencyId = models.CharField(max_length=20, null=True, blank=True)
    agencyName = models.CharField(max_length=100, primary_key=True)
    agencyUrl = models.URLField()
    agencyTimezone = models.CharField(max_length=50)
    agencyLang = models.CharField(max_length=2, null=True, blank=True)
    agencyPhone = models.CharField(max_length=20, null=True, blank=True)
    agencyFareUrl = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.agencyName


class Stop(models.Model):
    '''
    Model object representing a Stop (stops.txt)
    '''
    stopId = models.CharField(max_length=20, primary_key=True)
    stopCode = models.CharField(max_length=20, blank=True, null=True)
    stopName = models.CharField(max_length=100)
    stopDesc = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    point = models.PointField()
    zoneId = models.CharField(max_length=20, blank=True, null=True)
    stopUrl = models.URLField(blank=True, null=True)
    locationType = models.IntegerField()
    parentStation = models.CharField(max_length=20, blank=True, null=True)
    wheelchairAccessible = models.BooleanField(blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s, %s' % (self.stopId, self.stopName)

ROUTETYPES = (
    (0, 'Tram, Streetcar, Light rail'),
    (1, 'Subway, Metro'),
    (2, 'Rail'),
    (3, 'Bus'),
    (4, 'Ferry'),
    (5, 'Cable car'),
    (6, 'Gondola'),
    (7, 'Funicular'),
)

class Route(models.Model):
    routeId = models.CharField(max_length=20, primary_key=True)
    agencyId = models.CharField(max_length=20, blank=True, null=True)
    agency = models.ForeignKey(Agency)
    routeShortName = models.CharField(max_length=50)
    routeLongName = models.CharField(max_length=100)
    routeDesc = models.CharField(max_length=100, blank=True, null=True)
    routeType = models.IntegerField(choices=ROUTETYPES)
    routeUrl = models.URLField(blank=True, null=True)
    routeColor = models.CharField(max_length=10, blank=True, null=True)
    routeTextColor = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return u'%s, %s' % (self.routeId, self.routeLongName)


class Calendar(models.Model):
    '''
    Model object representing a service entry (calendar.txt)
    '''
    serviceId = models.CharField(max_length=20, primary_key=True)
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    startDate = models.DateField()
    endDate = models.DateField()

    def __unicode__(self):
        return self.serviceId


class Shape(models.Model):
    '''
    Model object represeting a Shape (shapes.txt)
    '''
    shapeId = models.CharField(max_length=20)
    lat = models.FloatField()
    lng = models.FloatField()
    point = models.PointField()
    sequence = models.IntegerField()
    distanceTraveled = models.FloatField(null=True, blank=True)
    objects = models.GeoManager()
    def __unicode__(self):
        return u"%s %d" % (self.shapeId, self.sequence)


DIRECTIONID = (
    (0, 'DIR-0'),
    (1, 'DIR-1'),
)

class Trip(models.Model):
    '''
    Model object representing a Trip (trips.txt)
    '''
    tripId = models.CharField(max_length=20, primary_key=True)
    route = models.ForeignKey(Route)
    service = models.ForeignKey(Calendar)
    headSign = models.CharField(max_length=50, null=True, blank=True)
    shortName = models.CharField(max_length=50, null=True, blank=True)
    directionId = models.IntegerField(choices=DIRECTIONID, null=True, blank=True)
    blockId = models.CharField(max_length=20, null=True, blank=True)
    shapeId = models.CharField(max_length=20, null=True, blank=True)

class StopTime(models.Model):
    '''
    Model object representing stop_times.txt
    '''
    
    # Trip object that identifies the vehicle stop time
    trip = models.ForeignKey(Trip)
    
    # The arrival_time specifies the arrival time at a 
    # specific stop for a specific trip on a route.
    # The time is measured from "noon minus 12h
    arrivalSeconds = models.IntegerField()
    
    # The arrival_time specifies the dep time at a 
    # specific stop for a specific trip on a route.
    # The time is measured from "noon minus 12h
    departureSeconds = models.IntegerField()
    
    # The stop obj field contains an ID that uniquely 
    # identifies a stop. Multiple routes may use the same stop
    stop = models.ForeignKey(Stop)
    
    # The stop_sequence field identifies the order of the 
    # stops for a particular trip.
    stopSequence = models.IntegerField()
    headSign = models.CharField(max_length=50, null=True, blank=True)
    pickUpType = models.IntegerField(null=True, blank=True)
    dropOffType = models.IntegerField(null=True, blank=True)
    distanceTraveled = models.FloatField(null=True, blank=True)


SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)
class ModelJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Stop):
            return {
                'stopId' : obj.stopId,
                'stopName' : obj.stopName,
                'lat' : obj.lat,
                'lng' : obj.lng
                }
        elif obj is None or isinstance(obj, SIMPLE_TYPES):
            return json.JSONEncoder.default(self, obj)
        else:
            print obj.__class__
            return ''

