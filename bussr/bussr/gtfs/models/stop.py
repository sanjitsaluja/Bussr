from django.contrib.gis.db import models
from agency import Agency

class Stop(models.Model):
    class Meta:
        app_label = 'gtfs'
        
        # Agency and stopId are a natural composite key
        unique_together = (('agency', 'stopId'))
    
    '''
    Model object representing a Stop (stops.txt)
    '''
    agency = models.ForeignKey(Agency)
    
    ''' R
    The stop_id field contains an ID that uniquely identifies a stop or 
    station. Multiple routes may use the same stop
    '''
    stopId = models.CharField(max_length=20)
    
    ''' 0
    The stop_code field contains short text or a number that uniquely 
    identifies the stop for passengers. Stop codes are often used in 
    phone-based transit information systems or printed on stop signage 
    to make it easier for riders to get a stop schedule or real-time 
    arrival information for a particular stop.
    The stop_code field should only be used for stop codes that are 
    displayed to passengers. For internal codes, use stop_id. 
    This field should be left blank for stops without a code.
    '''
    stopCode = models.CharField(max_length=20, blank=True, null=True)
    
    ''' R
    The stop_name field contains the name of a stop or station. 
    Please use a name that people will understand in the local 
    and tourist vernacular.
    '''
    stopName = models.CharField(max_length=100)
    
    ''' 0
    The stop_desc field contains a description of a stop. Please 
    provide useful, quality information. Do not simply duplicate 
    the name of the stop.
    '''
    stopDesc = models.CharField(max_length=100, blank=True, null=True)
    
    ''' WGS 84 stop latitude '''
    lat = models.FloatField()
    
    ''' WGS 84 stop longitude '''
    lng = models.FloatField()
    
    ''' geodjango point field (lat, lng) '''
    point = models.PointField()
    
    ''' O
    The zone_id field defines the fare zone for a stop ID. Zone IDs 
    are required if you want to provide fare information using 
    fare_rules.txt. If this stop ID represents a station, 
    the zone ID is ignored.
    '''
    zoneId = models.CharField(max_length=20, blank=True, null=True)
    
    ''' O
    The stop_url field contains the URL of a web page about a particular stop. 
    This should be different from the agency_url and the route_url fields.
    '''
    stopUrl = models.URLField(blank=True, null=True)
    
    ''' 0
    The location_type field identifies whether this stop ID 
    represents a stop or station. If no location type is 
    specified, or the location_type is blank, stop IDs are 
    treated as stops. Stations may have different properties 
    from stops when they are represented on a map or used in 
    trip planning. 
    0 A location where passengers board or disembark from a transit vehicle.
    1 Station. A physical structure or area that contains one or more stop.
    '''
    locationType = models.IntegerField()
    
    '''
    See gtfs spec
    '''
    parentStation = models.CharField(max_length=20, blank=True, null=True)
    
    ''' Is stop wheel chair accessible '''
    wheelchairAccessible = models.BooleanField(blank=True)
    
    ''' geo manager for geodjango '''
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s, %s, %s' % (self.agency, self.stopId, self.stopName)