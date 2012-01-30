'''
Created on Jan 21, 2012
@author: sanjits
'''
import csv
from bussr.gtfs.models import StopTime, Trip
import re

class StopTimeImporter(object):
    '''
    Import stops.txt gtfs file
    '''

    def __init__(self, filename, stopIdsToImport=None, tripIdsToImport=None, tripToRouteMapping=None):
        '''
        Constructor
        '''
        self.filename = filename
        self.stopIdsToImport = stopIdsToImport
        self.tripIdsToImport = tripIdsToImport
        self.tripToRouteMapping = tripToRouteMapping
        
        
    def parse(self):
        '''
        Parse the stoptimes.txt gtfs file
        '''
        reader = csv.DictReader(open(self.filename, 'r'))
        for row in reader:
            stopId = row['stop_id']
            tripId = row['trip_id']
            if (self.stopIdsToImport is None or stopId in self.stopIdsToImport) and (self.tripIdsToImport is None or tripId in self.tripIdsToImport):
                stopTime = StopTime()
                stopTime.tripId = tripId
                stopTime.routeId = self.routeIdForTripId(tripId)
                stopTime.stopId = row['stop_id']
                stopTime.stopSequence = row['stop_sequence']
                stopTime.arrivalSeconds = self.parseTime(row['arrival_time'])
                stopTime.departureSeconds = self.parseTime(row['departure_time'])
                stopTime.headSign = 'stop_headsign' in row and row['stop_headsign'] or None
                stopTime.pickUpType = 'pickup_type' in row and row['pickup_type'] or None
                stopTime.dropOffType = 'dropoff_type' in row and row['dropoff_type'] or None
                stopTime.distanceTraveled = 'shape_dist_traveled' in row and float(row['shape_dist_traveled']) or None
                stopTime.save()
        
    def tripForId(self, tripId):
        return Trip.objects.get(tripId=tripId)
    
    def routeIdForTripId(self, tripId):
        if self.tripToRouteMapping is not None and tripId in self.tripToRouteMapping:
            return self.tripToRouteMapping[tripId]
        else:
            assert False
            trip = self.tripForId(tripId)
            return trip.routeId
            
    def parseTime(self, value):
        parts = re.split(':', value)
        hr = int(parts[0])
        mn = int(parts[1])
        ss = int(parts[2])
        return ss + (mn * 60) + (hr * 3600)
    