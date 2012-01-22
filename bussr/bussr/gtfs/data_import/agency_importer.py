'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from bussr.gtfs.models import Agency
from bussr.gtfs.data_import.gtfsimporterutils import *

class AgencyImporter(object):
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