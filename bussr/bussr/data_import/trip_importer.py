'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from bussr.gtfs.models import Trip, Route, Calendar
from gtfsimporterutils import csvValueOrNone
from importer_base import CSVImporterBase

class TripImporter(CSVImporterBase):
    '''
    classdocs
    '''

    def __init__(self, filename, source, routeIdToRouteMapping, serviceIdToCalendarMapping, onlyNew):
        '''
        Constructor
        '''
        super(TripImporter, self).__init__()
        self.filename = filename
        self.source = source
        self.routeIdToRouteMapping = routeIdToRouteMapping
        self.serviceIdToCalendarMapping = serviceIdToCalendarMapping
        self.onlyNew = onlyNew
        
        
    def parse(self):
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        tripIdToTripMapping = {}
        for row in reader:

            tripId = row['trip_id']
            try:
                trip = Trip.objects.filter(source=self.source).get(tripId=tripId)
                if self.onlyNew:
                    continue
            except Trip.DoesNotExist:
                trip = None
            if trip is None:
                trip = Trip()

            if self.verboseParse:
                print 'Parsing trip row:', row
            
            trip.source = self.source
            trip.tripId = tripId
            trip.routeId = row['route_id']
            trip.route = trip.routeId in self.routeIdToRouteMapping and self.routeIdToRouteMapping[trip.routeId] or Route.objects.filter(source=self.source).get(routeId=trip.routeId)
            trip.serviceId = row['service_id']
            trip.service = row['service_id'] in self.serviceIdToCalendarMapping and self.serviceIdToCalendarMapping[row['service_id']] or Calendar.objects.filter(source=self.source).get(serviceId=row['service_id'])
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