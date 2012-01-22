'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
import datetime
from bussr.gtfs.models import Calendar
from django.db import models

class CalendarImporter(object):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.filename = filename
        
    def parse(self):
        reader = csv.DictReader(open(self.filename, 'r'))
        for row in reader:
            calendar = Calendar()
            calendar.serviceId = row['service_id']
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
            
    def csvBoolean(self, csvRow, colName):
        return csvRow[colName] == "1"
    
    def csvDate(self, csvRow, colName):
        value = "%s" % csvRow[colName]
        d = datetime.datetime.strptime(value, "%Y%m%d")
        return d