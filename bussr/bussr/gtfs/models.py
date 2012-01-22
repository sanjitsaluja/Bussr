from django.db import models

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
    zoneId = models.CharField(max_length=20, blank=True, null=True)
    stopUrl = models.URLField(blank=True, null=True)
    locationType = models.IntegerField()
    parentStation = models.CharField(max_length=20, blank=True, null=True)
    wheelchairAccessible = models.BooleanField(blank=True) 
    
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
    sequence = models.IntegerField()
    distanceTraveled = models.FloatField(null=True, blank=True)
    
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
    