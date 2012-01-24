'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from bussr.gtfs.models import Trip, Route, Calendar
from bussr.gtfs.data_import.gtfsimporterutils import *

class TripImporter(object):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.filename = filename
        
        
    def parse(self):
        reader = csv.DictReader(open(self.filename, 'r'))
        for row in reader:
            trip = Trip()
            trip.tripId = row['trip_id']
            trip.route = self.routeForRow(row)
            trip.service = self.calendarForRow(row)
            trip.headSign = csvValueOrNone(row, 'trip_headsign')
            trip.shortName = csvValueOrNone(row, 'trip_short_name')
            trip.directionId = 'direction_id' in row and row['direction_id'] or None
            trip.blockId = csvValueOrNone(row, 'block_id')
            trip.shapeId = self.shapeIdForRow(row)
            trip.save()
    
    
    def routeForRow(self, row):
        routeId = row['route_id']
        routes = Route.objects.filter(routeId = routeId)
        assert len(routes) == 1
        return routes[0]
    
    
    def calendarForRow(self, row):
        serviceId = row['service_id']
        services = Calendar.objects.filter(serviceId = serviceId)
        assert len(services) == 1
        return services[0]
    
    
    def shapeIdForRow(self, row):
        shapeId = csvValueOrNone(row, 'shape_id')
        return shapeId