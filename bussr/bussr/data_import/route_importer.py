'''
Created on Jan 21, 2012
@author: sanjits
'''
import csv
from bussr.gtfs.models import Route

class RouteImporter(object):
    '''
    Import routes.txt gtfs file
    '''

    def __init__(self, filename, agency):
        '''
        Constructor
        '''
        self.filename = filename
        self.agency = agency
        
    def parse(self):
        '''
        Parse the routes.txt gtfs file
        '''
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        routeIdToRouteMapping = {}
        for row in reader:
            routeId = self.csvValueOrNone(row, 'route_id')
            try:
                route = Route.objects.filter(agency=self.agency).get(routeId=routeId)
            except Route.DoesNotExist:
                route = None
            if route is None:
                route = Route()
            route.routeId       = routeId
            route.agency        = self.agency
            route.routeShortName= self.csvValueOrNone(row, 'route_short_name')
            if route.routeShortName is None:
                print route.routeId
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

    