'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
import datetime
from gtfs.models import Calendar
from importer_base import CSVImporterBase

class CalendarImporter(CSVImporterBase):
    '''
    Import the calendar from calendar.txt.
    '''

    def __init__(self, filename, source, onlyNew, cleanExistingData, logger):
        '''
        @param filename: path to the file to import
        @param source: source model object. The source that this service belongs to
        @param onlyNew: only import new entries not already in the database
        '''
        super(CalendarImporter, self).__init__()
        self.filename = filename
        self.source = source
        self.onlyNew = onlyNew
        self.cleanExistingData = cleanExistingData
        self.logger = logger
        
    def parse(self):
        '''
        Parse the input file
        '''
        if self.cleanExistingData:
            toDelete = Calendar.objects.filter(source=self.source)
            self.logger.info('Cleaning existing Calendars %s', toDelete)
            toDelete.delete()
        
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        
        # output is a serviceId->service object mapping
        serviceIdToCalendarMapping = {}
        
        for row in reader:            
            serviceId = row['service_id']
            
            # Get existing calendar object otherwise create new one
            try:
                calendar = Calendar.objects.filter(source=self.source).get(serviceId=serviceId)
                if self.onlyNew:
                    continue
            except Calendar.DoesNotExist:
                calendar = None
            
            if calendar is None:
                calendar = Calendar()
                
            if self.verboseParse:
                self.logger.debug('Parsing service row: %s', row)
                
            calendar.source = self.source
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
        '''
        @param csvRow: row for the csv file
        @param colName: col name to parse as boolean
        '''
        return csvRow[colName] == "1"
    
    def csvDate(self, csvRow, colName):
        '''
        @param csvRow: row for the csv file
        @param colName: col name to parse as date
        '''
        value = "%s" % csvRow[colName]
        d = datetime.datetime.strptime(value, "%Y%m%d")
        return d