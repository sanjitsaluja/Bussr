'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from bussr.gtfs.models import Trip
from gtfsimporterutils import csvValueOrNone

class TripImporter(object):
    '''
    classdocs
    '''

    def __init__(self, filename, agency, routeIdToRouteMapping, serviceIdToCalendarMapping):
        '''
        Constructor
        '''
        self.filename = filename
        self.agency = agency
        self.routeIdToRouteMapping = routeIdToRouteMapping
        self.serviceIdToCalendarMapping = serviceIdToCalendarMapping
        
        
    def parse(self):
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        tripIdToTripMapping = {}
        for row in reader:
            tripId = row['trip_id']
            trip = Trip.objects.filter(agency=self.agency).get(tripId=tripId)
            if trip is None:
                trip = Trip()
            trip.agency = self.agency
            trip.tripId = tripId
            trip.routeId = row['route_id']
            trip.route = self.routeIdToRouteMapping[trip.routeId]
            trip.serviceId = row['service_id']
            trip.service = self.serviceIdToCalendarMapping[row['service_id']]
            trip.headSign = csvValueOrNone(row, 'trip_headsign')
            trip.shortName = csvValueOrNone(row, 'trip_short_name')
            trip.directionId = 'direction_id' in row and row['direction_id'] or None
            trip.blockId = csvValueOrNone(row, 'block_id')
            trip.shapeId = self.shapeIdForRow(row)
            trip.save()
            tripIdToTripMapping[trip.tripId] = trip
        return tripIdToTripMapping
        
    def shapeIdForRow(self, row):
        shapeId = csvValueOrNone(row, 'shape_id')
        return shapeId