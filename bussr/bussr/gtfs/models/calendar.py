from django.contrib.gis.db import models
from datetime import datetime
from agency import Agency

class Calendar(models.Model):
    class Meta:
        app_label = 'gtfs'
        
        # Agency and stopId are a natural composite key
        unique_together = (('agency', 'serviceId'))
    
    '''
    Model object representing a service entry (calendar.txt)
    '''
    
    agency = models.ForeignKey(Agency)
    
    ''' R
    The service_id contains an ID that uniquely identifies a 
    set of dates when service is available for one or 
    more routes.
    '''
    serviceId = models.CharField(max_length=20)
    
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