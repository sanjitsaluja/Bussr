from django.contrib.gis.db import models

class Agency(models.Model):
    class Meta:
        app_label = 'gtfs'
        
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
    agencyName = models.CharField(max_length=100, unique=True)
    
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
