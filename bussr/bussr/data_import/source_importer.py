'''
Created on Jan 22, 2012

@author: sanjits
'''

from gtfs.models import Source
from gtfsimporterutils import csvValueOrNone
from importer_base import CSVImporterBase

class SourceImporter(CSVImporterBase):
    '''
    file.
    '''

    def __init__(self, sourceDict):
        '''
        Constructor.
        @param pk: primary key id for Source
        @param sourceDict: dict containing the data
        '''
        super(SourceImporter, self).__init__()
        self.sourceDict = sourceDict
        
    def parse(self):
        '''
        Parse the sourceDict into a Source model object
        '''
        if self.verboseParse:
            print 'Parsing source row:', self.sourceDict
        
        # Retrieve existing source if only exists otherwise, create a new one
        try:
            source = Source.objects.get(id=self.sourceDict['id'])
        except Source.DoesNotExist:
            source = Source()
            source.id = self.sourceDict['id']
        
        source.dataDir = self.sourceDict['dataDir']
        source.importUrl = self.sourceDict['importUrl']
        source.codeName = self.sourceDict['codeName']
        source.save()
        return source