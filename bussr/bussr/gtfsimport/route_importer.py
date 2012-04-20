'''
Created on Jan 21, 2012
@author: sanjits
'''
import csv
from gtfs.models import Route, Agency
from importer_base import CSVImporterBase

class RouteImporter(CSVImporterBase):
    '''
    Import routes.txt gtfs file.
    '''

    def __init__(self, filename, source, logger):
        '''
        Constructor.
        @param filename: file name to import (full path to routes.txt)
        @param agency: associated agency
        @param logger: logger
        '''
        super(RouteImporter, self).__init__()
        self.filename = filename
        self.source = source
        self.logger=logger
        
    def parse(self):
        '''
        Parse file
        @return: routeId->object mapping
        '''
        routesToDelete = Route.objects.filter(source=self.source)
        self.logger.debug('Cleaning existing Routes %s', routesToDelete)
        routesToDelete.delete()
        
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        routeIdToRouteMapping = {}
        for row in reader:
            routeId = self.csvValueOrNone(row, 'route_id')
            route = Route()
            self.logger.info('Parsing route row: %s', row)
            route.source        = self.source
            route.routeId       = routeId
            route.agencyId      = self.csvValueOrNone(row, 'agency_id')
            route.agency        = Agency.objects.filter(source=self.source).get(agencyId=route.agencyId)
            route.routeShortName= self.csvValueOrNone(row, 'route_short_name')
            if route.routeShortName is None:
                route.routeShortName = "%s" % route.routeId
            route.routeLongName = self.csvValueOrNone(row, 'route_long_name')
            route.routeDesc     = self.csvValueOrNone(row, 'route_desc')
            route.routeType     = self.routeTypeValue(row)
            route.routeUrl      = self.csvValueOrNone(row, 'route_url')
            route.routeColor    = self.csvValueOrNone(row, 'route_color')
            route.routeTextColor= self.csvValueOrNone(row, 'route_text_color')
            route.save()
            routeIdToRouteMapping[route.routeId] = route
        return routeIdToRouteMapping
        
    def csvValueOrNone(self, csvRow, colName):
        return colName in csvRow and csvRow[colName] or None
    
    def routeTypeValue(self, csvRow):
        return csvRow['route_type']

    