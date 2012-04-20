'''
Created on Jan 22, 2012

@author: sanjits
'''

from gtfs.models import Source
from importer_base import CSVImporterBase

class SourceImporter(CSVImporterBase):
    '''
    file.
    '''

    def __init__(self, sourceDict, logger):
        '''
        Constructor.
        @param pk: primary key id for Source
        @param sourceDict: dict containing the data
        '''
        super(SourceImporter, self).__init__()
        self.sourceDict = sourceDict
        self.logger = logger
        
    def parse(self):
        '''
        Parse the sourceDict into a Source model object
        '''
        self.logger.info('Parsing source row:', self.sourceDict)
        
        # Retrieve existing source if only exists otherwise, create a new one
        try:
            source = Source.objects.get(sourceId=self.sourceDict['id'])
            self.logger.debug('Found existing source', source)
        except Source.DoesNotExist:
            self.logger.debug('Creating new source.')
            source = Source()
            source.sourceId = self.sourceDict['id']
        
        source.dataDir = self.sourceDict['dataDir']
        source.importUrl = self.sourceDict['importUrl']
        source.codeName = self.sourceDict['codeName']
        source.save()
        return source