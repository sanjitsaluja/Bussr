import getopt
import json
import sys
import os
sys.path.append("..")
from django.core.management import setup_environ
from bussr import settings
setup_environ(settings)
from source_importer import SourceImporter    
from gtfsimporter import GTFSImporter
from subprocess import call
from tempfile import mkdtemp
import logging

class DataLoader:
    '''
    @summary: Object to fetch gtfs data and import all its contents
    '''
    def __init__(self, onlyNew=False, sourceIdsToImport=None, cleanExistingData=False, logger=None):
        '''
        @param onlyNew: Import only new data, entries that dont existing in model database
        @param sourceIdsToImport: List of source ids to import (see sources.json)
        @param cleanExistingData: Clean existing data for this source
        @param logger: logger
        '''
        self.sourceIdsToImport = sourceIdsToImport
        self.onlyNew = onlyNew
        self.cleanExistingData = cleanExistingData
        self.logger = logger
        if logger is None:
            self.logger = logging.getLogger(__name__)
        filePath = os.path.abspath(os.path.dirname(__file__))
        sourcesFilePath = os.path.join(filePath, 'sources.json')
        self.sourceMapping = json.load(open(sourcesFilePath))['sources']
        assert not (onlyNew and cleanExistingData)
        
    def importSource(self, mapping):
        '''
        @param mapping: mapping from sources.json to import 
        Import all data for the given source mapping
        '''
        #Import the source
        sourceImporter = SourceImporter(mapping)
        source = sourceImporter.parse()
        
        #Fetch newest gtfs data
        fetchCommand = os.path.join(os.path.dirname(__file__), 'fetch')
        tempDir = mkdtemp()
        call(['sh', fetchCommand, tempDir, mapping['importUrl']])
        
        #Parse gtfs data
        importer = GTFSImporter(dataDir=tempDir, onlyNew=self.onlyNew, source=source, cleanExistingData=self.cleanExistingData, logger=self.logger)
        importer.importall()
    
    def performImport(self):
        '''
        @return: None
        Import data from all specified sources
        '''
        for mapping in self.sourceMapping:
            if self.sourceIdsToImport is None or mapping['id'] in self.sourceIdsToImport:
                self.importSource(mapping)
                
                
def usage():
    print '''
usage: %s 
    Options and arguments:
    -h, --help : print this help
    -o, --onlyNew : only import new data
    -c, --clean : clean existing data
    -s, --source : source id to import
    ''' % sys.argv[0]
    
def processCmdArgs():
    '''
    @return: (success, sources to import)
    '''
    if len(sys.argv) < 2:
        return (True, None, False, False)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:oc', ['help', 'source=', 'onlyNew', 'clean'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
    
    sourceIdsToImport = None
    onlyNew = False
    cleanExistingData = False
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            return (False, None, None, None)
        elif o in ('-s', '--source'):
            sourceIdsToImport = [a]
        elif o in ('-o', '--onlyNew'):
            onlyNew = True
        elif o in ('-c', '--clean'):
            cleanExistingData = True
        else:
            assert False, 'unhandled reportOption'
            
    return (True, sourceIdsToImport, onlyNew, cleanExistingData)

if __name__=='__main__':
    (success, sourceIdsToImport, onlyNew, cleanExistingData) = processCmdArgs()
    print 'sourceIdsToImport', sourceIdsToImport
    print 'onlyNew', onlyNew 
    print 'cleanExistingData', cleanExistingData
    if success:
        dataLoader = DataLoader(onlyNew=onlyNew, sourceIdsToImport=sourceIdsToImport, cleanExistingData=cleanExistingData)
        dataLoader.performImport()