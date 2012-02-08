'''
Created on Jan 21, 2012
@author: sanjits
'''
import csv
from bussr.gtfs.models import Route, Agency
from importer_base import CSVImporterBase

class RouteImporter(CSVImporterBase):
    '''
    Import routes.txt gtfs file.
    '''

    def __init__(self, filename, source, onlyNew):
        '''
        Constructor.
        @param filename: file name to import (full path to routes.txt)
        @param agency: associated agency
        @param onlyNew: Only import new entries
        '''
        super(RouteImporter, self).__init__()
        self.filename = filename
        self.source = source
        self.onlyNew = onlyNew
        
    def parse(self):
        '''
        Parse file
        '''
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        routeIdToRouteMapping = {}
        for row in reader:
            routeId = self.csvValueOrNone(row, 'route_id')
            try:
                route = Route.objects.filter(source=self.source).get(routeId=routeId)
                if self.onlyNew:
                    continue
            except Route.DoesNotExist:
                route = None
            
            if route is None:
                route = Route()
                
            if self.verboseParse:
                print 'Parsing route row:', row
            
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

    