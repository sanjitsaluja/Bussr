'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from bussr.gtfs.models import Trip
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
        tripToRouteMapping = {}
        reader = csv.DictReader(open(self.filename, 'r'))
        for row in reader:
            trip = Trip()
            trip.tripId = row['trip_id']
            trip.routeId = row['route_id']
            tripToRouteMapping[trip.tripId] = trip.routeId
            trip.serviceId = row['service_id']
            trip.headSign = csvValueOrNone(row, 'trip_headsign')
            trip.shortName = csvValueOrNone(row, 'trip_short_name')
            trip.directionId = 'direction_id' in row and row['direction_id'] or None
            trip.blockId = csvValueOrNone(row, 'block_id')
            trip.shapeId = self.shapeIdForRow(row)
            trip.save()
        return tripToRouteMapping
        
    def shapeIdForRow(self, row):
        shapeId = csvValueOrNone(row, 'shape_id')
        return shapeId