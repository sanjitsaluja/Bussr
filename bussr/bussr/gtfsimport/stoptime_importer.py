'''
Created on Jan 21, 2012
@author: sanjits
'''
from gtfs.models import StopTime, Trip, Stop, Route
from importer_base import CSVImporterBase
import csv
import re

class StopTimeImporter(CSVImporterBase):
    '''
    Import stops.txt gtfs file
    '''

    def __init__(self, filename, source, tripIdToTripMapping, stopIdToStopMapping, routeIdToRouteMapping, logger):
        '''
        Constructor
        '''
        super(StopTimeImporter, self).__init__()
        self.filename = filename
        self.source = source
        self.tripIdToTripMapping = tripIdToTripMapping
        self.stopIdToStopMapping = stopIdToStopMapping
        self.routeIdToRouteMapping = routeIdToRouteMapping
        self.logger=logger
        
    def shapeDistForRow(self, row):
        try:
            return 'shape_dist_traveled' in row and float(row['shape_dist_traveled']) or None
        except ValueError:
            return None
        
    def parse(self):
        '''
        Parse the stoptimes.txt gtfs file
        '''
        toDel = Route.objects.filter(source=self.source)
        self.logger.info('Cleaning existing StopTimes %s', toDel)
        toDel.delete()
        
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        for row in reader:
            stopId = row['stop_id']
            tripId = row['trip_id']
            stopSequence = row['stop_sequence']
            stopTime = StopTime()
            self.logger.info('Parsing stoptime row: %s', row)
            stopTime.source = self.source
            stopTime.tripId = tripId
            stopTime.trip = tripId in self.tripIdToTripMapping and self.tripIdToTripMapping[tripId] or Trip.objects.filter(source=self.source).get(tripId=tripId)
            stopTime.routeId = stopTime.trip.routeId
            stopTime.route = stopTime.routeId in self.routeIdToRouteMapping and self.routeIdToRouteMapping[stopTime.routeId] or Route.objects.filter(source=self.source).get(routeId=stopTime.routeId)
            stopTime.stopId = stopId
            stopTime.stop = stopId in self.stopIdToStopMapping and self.stopIdToStopMapping[stopId] or Stop.objects.filter(source=self.source).get(stopId=stopId)
            stopTime.stopSequence = stopSequence
            stopTime.arrivalSeconds = self.parseTime(row['arrival_time'])
            stopTime.departureSeconds = self.parseTime(row['departure_time'])
            stopTime.headSign = 'stop_headsign' in row and row['stop_headsign'] or None
            stopTime.pickUpType = 'pickup_type' in row and row['pickup_type'] or None
            stopTime.dropOffType = 'dropoff_type' in row and row['dropoff_type'] or None
            stopTime.distanceTraveled = self.shapeDistForRow(row)
            stopTime.save()
        
    def parseTime(self, value):
        parts = re.split(':', value)
        hr = int(parts[0])
        mn = int(parts[1])
        ss = int(parts[2])
        return ss + (mn * 60) + (hr * 3600)
    