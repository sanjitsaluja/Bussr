'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from bussr.gtfs.models import Agency
from bussr.gtfs.data_import.gtfsimporterutils import csvValueOrNone

class AgencyImporter(object):
    '''
    Import the agencies from agency.txt
    '''


    def __init__(self, filename):
        '''
        Constructor.
        '''
        self.filename = filename
        
    def parse(self):
        '''
        Parse the agency.txt csv file creating an Agency
        record per csv record
        '''
        reader = csv.DictReader(open(self.filename, 'r'))
        agency = None
        for row in reader:
            agency = Agency()
            agency.agencyId = csvValueOrNone(row, 'agency_id')
            agency.agencyName = row['agency_name']
            agency.agencyUrl= row['agency_url']
            agency.agencyTimezone = row['agency_timezone']
            agency.agencyLang = csvValueOrNone(row, 'agency_lang')
            agency.agencyPhone = csvValueOrNone(row, 'agency_phone')
            agency.agencyFareUrl = csvValueOrNone(row, 'agency_fare_url')
            agency.save()