from django.contrib.gis.db import models
import json
from datetime import datetime

# Create your models here.

class Agency(models.Model):
    '''
    Model object representing an Agency (agency.txt)
    '''
    
    ''' Optional
    The agency_id field is an ID that uniquely identifies a transit agency. 
    A transit feed may represent data from more than one agency. The agency_id 
    is dataset unique. This field is optional for transit feeds that only contain 
    data for a single agency.
    '''
    agencyId = models.CharField(max_length=20, null=True, blank=True)
    
    ''' Required
    The agency_name field contains the full name of the transit agency. 
    Google Maps will display this name.
    '''
    agencyName = models.CharField(max_length=100, primary_key=True)
    
    ''' Required
    The agency_url field contains the URL of the transit agency
    '''
    agencyUrl = models.URLField()
    
    ''' Required
    The agency_timezone field contains the timezone where the transit 
    agency is located. Timezone names never contain the space character
     but may contain an underscore. Please refer to 
     http://en.wikipedia.org/wiki/List_of_tz_zones for a list of valid 
     values. If multiple agencies are specified in the feed, each must 
     have the same agency_timezone.
     '''
    agencyTimezone = models.CharField(max_length=50)
    
    ''' Optional
    The agency_lang field contains a two-letter ISO 639-1 code for the 
    primary language used by this transit agency. The language code is 
    case-insensitive (both en and EN are accepted). This setting defines 
    capitalization rules and other language-specific settings for all 
    text contained in this transit agency's feed. Please refer to 
    http://www.loc.gov/standards/iso639-2/php/code_list.php for a 
    list of valid values.
    '''
    agencyLang = models.CharField(max_length=2, null=True, blank=True)
    
    ''' Optional    
    The agency_phone field contains a single voice telephone number for 
    the specified agency. This field is a string value that presents the 
    telephone number as typical for the agency's service area. It can and 
    should contain punctuation marks to group the digits of the number. 
    Dialable text (for example, TriMet's "503-238-RIDE") is permitted, 
    but the field must not contain any other descriptive text.
     '''
    agencyPhone = models.CharField(max_length=20, null=True, blank=True)
    
    ''' O
    The agency_fare_url specifies the URL of a web page that allows a 
    rider to purchase tickets or other fare instruments for that agency online.
    '''
    agencyFareUrl = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.agencyName


class Stop(models.Model):
    '''
    Model object representing a Stop (stops.txt)
    '''
    
    ''' R
    The stop_id field contains an ID that uniquely identifies a stop or 
    station. Multiple routes may use the same stop
    '''
    stopId = models.CharField(max_length=20, primary_key=True)
    
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
    ''' R
    The route_id field contains an ID that uniquely identifies a route. 
    The route_id is dataset unique.
    '''
    routeId = models.CharField(max_length=20, primary_key=True)
    
    ''' O
    The agency_id field defines an agency for the specified route.
    '''
    agencyId = models.CharField(max_length=20, blank=True, null=True)
    
    ''' 
    Agency object foreign key
    '''
    agency = models.ForeignKey(Agency)
    
    ''' R
    The route_short_name contains the short name of a route. 
    This will often be a short, abstract identifier like "32", 
    "100X", or "Green" that riders use to identify a route, 
    but which doesn't give any indication of what places the 
    route serves. If the route does not have a short name, 
    please specify a route_long_name and use an empty string 
    as the value for this field.
    '''
    routeShortName = models.CharField(max_length=50, blank=True)
    
    ''' R
    The route_long_name contains the full name of a route. 
    This name is generally more descriptive than the 
    route_short_name and will often include the route's 
    destination or stop. If the route does not have a 
    long name, please specify a route_short_name and 
    use an empty string as the value for this field.
    '''
    routeLongName = models.CharField(max_length=100, blank=True)
    
    ''' O
    The route_desc field contains a description of a route. 
    Please provide useful, quality information. Do not 
    simply duplicate the name of the route. For example, 
    "A trains operate between Inwood-207 St, Manhattan 
    and Far Rockaway-Mott Avenue, Queens at all times. 
    Also from about 6AM until about midnight, additional 
    A trains operate between Inwood-207 St and Lefferts 
    Boulevard (trains typically alternate between 
    Lefferts Blvd and Far Rockaway)."
    '''
    routeDesc = models.CharField(max_length=100, blank=True, null=True)
    
    ''' R
    The route_type field describes the type of transportation 
    used on a route.
    '''
    routeType = models.IntegerField(choices=ROUTETYPES)
    
    ''' O
    The route_url field contains the URL of a web page 
    about that particular route
    '''
    routeUrl = models.URLField(blank=True, null=True)
    
    ''' O
    In systems that have colors assigned to routes, the route_color field 
    defines a color that corresponds to a route.
    '''
    routeColor = models.CharField(max_length=10, blank=True, null=True)
    
    ''' O
    The route_text_color field can be used to 
    specify a legible color to use 
    for text drawn against a background of route_color
    '''
    routeTextColor = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return u'%s, %s' % (self.routeId, self.routeLongName)


class Calendar(models.Model):
    '''
    Model object representing a service entry (calendar.txt)
    '''
    
    ''' R
    The service_id contains an ID that uniquely identifies a 
    set of dates when service is available for one or 
    more routes.
    '''
    serviceId = models.CharField(max_length=20, primary_key=True)
    
    ''' R
    The monday field contains a binary value that indicates 
    whether the service is valid for all Mondays.
    '''
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
        '''
        Return unicode description of this object
        '''
        weekday = datetime.now().isoweekday()
        serviceDays = []
        if weekday is 1:
            serviceDays.append(u'mon')
        elif weekday is 2:
            serviceDays.append(u'tue')
        elif weekday is 3:
            serviceDays.append(u'wed')
        elif weekday is 4:
            serviceDays.append(u'thu')
        elif weekday is 5:
            serviceDays.append(u'fri')
        elif weekday is 6:
            serviceDays.append(u'sat')
        else:
            serviceDays.append(u'sun')
        return u','.join(serviceDays)
    
    def today(self):
        '''
        bool if the service is on today or false otherwise
        '''
        weekday = datetime.now().isoweekday()
        if weekday is 1:
            return self.monday
        elif weekday is 2:
            return self.tuesday
        elif weekday is 3:
            return self.wednesday
        elif weekday is 4:
            return self.thursday
        elif weekday is 5:
            return self.friday
        elif weekday is 6:
            return self.saturday
        else:
            return self.sunday
        

class Shape(models.Model):
    '''
    Model object represeting a Shape (shapes.txt)
    '''
    
    shapeId = models.CharField(max_length=20)
    lat = models.FloatField()
    lng = models.FloatField()
    point = models.PointField()
    
    ''' R
    The shape_pt_sequence field associates the latitude 
    and longitude of a shape point with its sequence 
    order along the shape. The values for 
    shape_pt_sequence must be non-negative integers, 
    and they must increase along the trip.
    
    For example, if the shape "A_shp" has three points 
    in its definition, the shapes.txt file might contain 
    these rows to define the shape:

    A_shp,37.61956,-122.48161,0
    A_shp,37.64430,-122.41070,6
    A_shp,37.65863,-122.30839,11
    '''
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
    
    ''' R
    The trip_id field contains an ID that identifies a trip. 
    The trip_id is dataset unique.
    '''
    tripId = models.CharField(max_length=20, primary_key=True)
    
    '''
    Route id for ease of access
    '''
    routeId = models.CharField(max_length=20)
        
    '''
    Service id in the calendar
    '''
    serviceId = models.CharField(max_length=20)
    
    ''' O
    The trip_headsign field contains the text that appears 
    on a sign that identifies the trip's destination to 
    passengers. Use this field to distinguish between 
    different patterns of service in the same route. 
    If the headsign changes during a trip, you can 
    override the trip_headsign by specifying values 
    for the the stop_headsign field in stop_times.txt.
    '''
    headSign = models.CharField(max_length=50, null=True, blank=True)
    
    ''' O
    The trip_short_name field contains the text that appears 
    in schedules and sign boards to identify the trip to 
    passengers, for example, to identify train numbers for 
    commuter rail trips. If riders do not commonly rely on 
    trip names, please leave this field blank.

    A trip_short_name value, if provided, should uniquely 
    identify a trip within a service day; it should not be 
    used for destination names or limited/express designations.
    '''
    shortName = models.CharField(max_length=50, null=True, blank=True)
    
    ''' O
    The direction_id field contains a binary value that 
    indicates the direction of travel for a trip. Use 
    this field to distinguish between bi-directional 
    trips with the same route_id. This field is not 
    used in routing; it provides a way to separate 
    trips by direction when publishing time tables. 
    You can specify names for each direction with the 
    trip_headsign field.

    0 - travel in one direction (e.g. outbound travel)
    1 - travel in the opposite direction (e.g. inbound travel)
    
    For example, you could use the trip_headsign and 
    direction_id fields together to assign a name to 
    travel in each direction on trip "1234", the trips.txt 
    file would contain these rows for use in time tables:

    trip_id, ... ,trip_headsign,direction_id
    1234, ... , to Airport,0
    1505, ... , to Downtown,1
    '''
    directionId = models.IntegerField(choices=DIRECTIONID, null=True, blank=True)
    
    '''
    The block_id field identifies the block to which the trip 
    belongs. A block consists of two or more sequential trips 
    made using the same vehicle, where a passenger can 
    transfer from one trip to the next just by staying 
    in the vehicle. The block_id must be referenced by 
    two or more trips in trips.txt.
    '''
    blockId = models.CharField(max_length=20, null=True, blank=True)
    
    ''' O
    The shape_id field contains an ID that defines a shape for the trip
    '''
    shapeId = models.CharField(max_length=20, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s, %s' % (self.tripId, self.routeId, self.headSign)
    
    @property
    def route(self):
        return Route.objects.get(routeId=self.routeId)
        
    @property
    def service(self):
        return Calendar.objects.get(serviceId=self.serviceId)


class StopTime(models.Model):
    '''
    Model object representing stop_times.txt
    '''
    
    '''
    Trip id for ease of access. identifies the vehicle stop times
    '''
    tripId = models.CharField(max_length=20)
    
    '''
    Route id for ease of access
    '''
    routeId = models.CharField(max_length=20)
    
    '''
    The arrival_time specifies the arrival time at a specific 
    stop for a specific trip on a route. The time is measured 
    from "noon minus 12h" (effectively midnight, except for 
    days on which daylight savings time changes occur) at 
    the beginning of the service date. For times occurring 
    after midnight on the service date, enter the time as a 
    value greater than 24:00:00 in HH:MM:SS local time for 
    the day on which the trip schedule begins. If you 
    don't have separate times for arrival and departure 
    at a stop, enter the same value for arrival_time 
    and departure_time.

    You must specify arrival times for the first and 
    last stops in a trip. If this stop isn't a time 
    point, use an empty string value for the 
    arrival_time and departure_time fields. Stops 
    without arrival times will be scheduled based 
    on the nearest preceding timed stop. To ensure 
    accurate routing, please provide arrival and 
    departure times for all stops that are time 
    points. Do not interpolate stops.

    Times must be eight digits in HH:MM:SS 
    format (H:MM:SS is also accepted, 
    if the hour begins with 0). Do not 
    pad times with spaces. The following 
    columns list stop times for a trip and t
    he proper way to express those times in 
    the arrival_time field:

    Time    arrival_time value
    08:10:00 A.M.    08:10:00 or 8:10:00
    01:05:00 P.M.    13:05:00
    07:40:00 P.M.    19:40:00
    01:55:00 A.M.    25:55:00
    
    Note: Trips that span multiple dates will 
    have stop times greater than 24:00:00. For example, 
    if a trip begins at 10:30:00 p.m. and ends at 
    2:15:00 a.m. on the following day, the stop 
    times would be 22:30:00 and 26:15:00. 
    Entering those stop times as 22:30:00 
    and 02:15:00 would not produce the desired results.
    '''
    arrivalSeconds = models.IntegerField()
    
    # The arrival_time specifies the dep time at a 
    # specific stop for a specific trip on a route.
    # The time is measured from "noon minus 12h
    departureSeconds = models.IntegerField()
    
    # The stop obj field contains an ID that uniquely 
    # identifies a stop. Multiple routes may use the same stop
    stopId = models.CharField(max_length=20)
    
    # The stop_sequence field identifies the order of the 
    # stops for a particular trip.
    stopSequence = models.IntegerField()
    headSign = models.CharField(max_length=50, null=True, blank=True)
    pickUpType = models.IntegerField(null=True, blank=True)
    dropOffType = models.IntegerField(null=True, blank=True)
    
    ''' O
    When used in the stop_times.txt file, the 
    shape_dist_traveled field positions a stop as a 
    distance from the first shape point. 
    The shape_dist_traveled field represents a 
    real distance traveled along the route in 
    units such as feet or kilometers. For example, 
    if a bus travels a distance of 5.25 kilometers 
    from the start of the shape to the stop, the 
    shape_dist_traveled for the stop ID would be 
    entered as "5.25". This information allows the 
    trip planner to determine how much of the shape 
    to draw when showing part of a trip on the map. 
    The values used for shape_dist_traveled must 
    increase along with stop_sequence: they cannot 
    be used to show reverse travel along a route.
    '''
    distanceTraveled = models.FloatField(null=True, blank=True)
    
    @property
    def route(self):
        return Route.objects.get(routeId=self.routeId)
        
    @property
    def trip(self):
        return Trip.objects.get(tripId=self.tripId)
        
    @property
    def stop(self):
        return Stop.objects.get(stopId=self.stopId)
        
    def __unicode__(self):
        return u'%s, %s, %s' % (self.routeId, self.headSign, self.stop.stopName)


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

