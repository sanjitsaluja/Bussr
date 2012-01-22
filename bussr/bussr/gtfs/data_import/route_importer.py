'''
Created on Jan 21, 2012
@author: sanjits
'''
import sys
import os
import csv
from bussr.gtfs.models import Route

class RouteImporter(object):
    '''
    Import stops.txt gtfs file
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.filename = filename
        
    def parse(self):
        '''
        Parse the stops.txt gtfs file
        '''
        reader = csv.DictReader(open(self.filename, 'r'))
        # Skip the header line
        next(reader)
        for row in reader:
            route = Route()
            route.routeId
        
        
def importRoutes():
    filePath = os.path.dirname(__file__)
    ctaFilename = os.path.join(filePath, 'cta/routes.txt')
    print ctaFilename
    importer = RouteImporter(ctaFilename)
    importer.parse()
    