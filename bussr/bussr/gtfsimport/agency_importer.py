'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from gtfs.models import Agency
from gtfsimporterutils import csvValueOrNone
from importer_base import CSVImporterBase

class AgencyImporter(CSVImporterBase):
    '''
    Import the agencies from agency.txt
    '''

    def __init__(self, filename, source, logger):
        '''
        Constructor.
        @param filename: file name to import (full path to agency.txt)
        @param source: source of importer
        @param logger: logger
        '''
        super(AgencyImporter, self).__init__()
        self.filename = filename
        self.source = source
        self.logger = logger
        assert self.source is not None
        
    def parse(self):
        '''
        Parse the agency.txt csv file creating an Agency
        record per csv record
        '''
        # Delete existing entries
        agenciesToDelete = Agency.objects.filter(source=self.source)
        self.logger.debug('Cleaning existing Agencies %s', agenciesToDelete)
        agenciesToDelete.delete()
        
        # Iterate over all entries
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        agency = None
        for row in reader:
            #Parse row
            self.logger.info('Parsing agency row: %s', row)
            agencyId = csvValueOrNone(row, 'agency_id')
            agency = Agency()
            agency.source = self.source
            agency.agencyId = agencyId
            agency.agencyName = row['agency_name']
            agency.agencyUrl= row['agency_url']
            agency.agencyTimezone = row['agency_timezone']
            agency.agencyLang = csvValueOrNone(row, 'agency_lang')
            agency.agencyPhone = csvValueOrNone(row, 'agency_phone')
            agency.agencyFareUrl = csvValueOrNone(row, 'agency_fare_url')
            agency.save()
        
        return agency