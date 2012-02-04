'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
import datetime
from bussr.gtfs.models import Calendar

class CalendarImporter(object):
    '''
    classdocs
    '''

    def __init__(self, filename, agency):
        '''
        Constructor
        '''
        self.filename = filename
        self.agency = agency
        
    def parse(self):
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        serviceIdToCalendarMapping = {}
        for row in reader:
            serviceId = row['service_id']
            calendar = Calendar.objects.filter(agency=self.agency).get(serviceId=serviceId)
            if calendar is None:
                calendar = Calendar()
            calendar.agency = self.agency
            calendar.serviceId = serviceId
            calendar.monday = self.csvBoolean(row, 'monday')
            calendar.tuesday = self.csvBoolean(row, 'tuesday')
            calendar.wednesday = self.csvBoolean(row, 'wednesday')
            calendar.thursday = self.csvBoolean(row, 'thursday')
            calendar.friday = self.csvBoolean(row, 'friday')
            calendar.saturday = self.csvBoolean(row, 'saturday')
            calendar.sunday = self.csvBoolean(row, 'sunday')
            calendar.startDate = self.csvDate(row, 'start_date')
            calendar.endDate = self.csvDate(row, 'end_date')
            calendar.save()
            serviceIdToCalendarMapping[calendar.serviceId] = calendar
        return serviceIdToCalendarMapping
            
    def csvBoolean(self, csvRow, colName):
        return csvRow[colName] == "1"
    
    def csvDate(self, csvRow, colName):
        value = "%s" % csvRow[colName]
        d = datetime.datetime.strptime(value, "%Y%m%d")
        return d