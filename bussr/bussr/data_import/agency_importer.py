'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from bussr.gtfs.models import Agency
from gtfsimporterutils import csvValueOrNone
from importer_base import CSVImporterBase

class AgencyImporter(CSVImporterBase):
    '''
    Import the agencies from agency.txt. It imports the file into the supplied
    agency primary key. It assumes you only have one record in the agency.txt
    file.
    '''

    def __init__(self, filename, agencyPK):
        '''
        Constructor.
        @param filename: file name to import (full path to agency.txt)
        @param agencyPK: primary key id for Agency
        '''
        super(AgencyImporter, self).__init__()
        self.filename = filename
        self.agencyPK = agencyPK
        
    def parse(self):
        '''
        Parse the agency.txt csv file creating an Agency
        record per csv record
        '''
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        
        # Importer assumes we only have 1 entry
        assert len([row for row in reader]) == 1
        
        agency = None
        for row in reader:
            
            if self.verboseParse:
                print 'Parsing agency row:', row
            
            # Retrieve existing agency if only exists otherwise, create a new one
            try:
                agency = Agency.objects.get(id=self.agencyPK)
            except Agency.DoesNotExist:
                agency = None
            
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
        
        return agency