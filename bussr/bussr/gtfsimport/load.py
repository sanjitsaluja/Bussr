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
    def __init__(self, onlyNew=False, sourceIdsToImport=None, logger=None):
        '''
        @param sourceIdsToImport: List of source ids to import (see sources.json)
        @param logger: logger
        '''
        self.sourceIdsToImport = sourceIdsToImport
        self.logger = logger
        if logger is None:
            self.logger = logging.getLogger(__name__)
        filePath = os.path.abspath(os.path.dirname(__file__))
        sourcesFilePath = os.path.join(filePath, 'sources.json')
        sourcesText = open(sourcesFilePath, "r").read()
        self.sourceMapping = json.loads(sourcesText)['sources']
        
    def importSource(self, mapping):
        '''
        @param mapping: mapping from sources.json to import 
        Import all data for the given source mapping
        '''
        #Import the source
        sourceImporter = SourceImporter(sourceDict=mapping, logger=self.logger)
        source = sourceImporter.parse()
        
        #Fetch newest gtfs data
        fetchCommand = os.path.join(os.path.dirname(__file__), 'fetch')
        tempDir = mkdtemp()
        call(['sh', fetchCommand, tempDir, mapping['importUrl']])
        
        #Parse gtfs data
        importer = GTFSImporter(dataDir=tempDir, source=source, logger=self.logger)
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
    -s, --source : source id to import
    ''' % sys.argv[0]
    
def processCmdArgs():
    '''
    @return: (success, sources to import)
    '''
    if len(sys.argv) < 2:
        return (True, None)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:', ['help', 'source='])
    except getopt.GetoptError, err:
        print str(err)
        usage()
    
    sourceIdsToImport = None
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            return (False, None)
        elif o in ('-s', '--source'):
            sourceIdsToImport = [a]
        else:
            assert False, 'unhandled reportOption'
            
    return (True, sourceIdsToImport)

if __name__=='__main__':
    (success, sourceIdsToImport) = processCmdArgs()
    print 'sourceIdsToImport', sourceIdsToImport
    
    if success:
        dataLoader = DataLoader(sourceIdsToImport=sourceIdsToImport)
        dataLoader.performImport()