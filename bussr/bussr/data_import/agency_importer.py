'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from bussr.gtfs.models import Agency
from gtfsimporterutils import csvValueOrNone

class AgencyImporter(object):
    '''
    Import the agencies from agency.txt
    '''


    def __init__(self, filename, agencyPK):
        '''
        Constructor.
        '''
        self.filename = filename
        self.agencyPK = agencyPK
        
    def parse(self):
        '''
        Parse the agency.txt csv file creating an Agency
        record per csv record
        '''
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        agency = None
        for row in reader:
            print 'Parsing agency row', row
            agency = Agency.objects.get(id=self.agencyPK)
            if agency is None:
                agency = Agency()
                agency.id = self.agencyPK
            agency.agencyId = csvValueOrNone(row, 'agency_id')
            agency.agencyName = row['agency_name']
            agency.agencyUrl= row['agency_url']
            agency.agencyTimezone = row['agency_timezone']
            agency.agencyLang = csvValueOrNone(row, 'agency_lang')
            agency.agencyPhone = csvValueOrNone(row, 'agency_phone')
            agency.agencyFareUrl = csvValueOrNone(row, 'agency_fare_url')
            agency.save()