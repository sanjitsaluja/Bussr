'''
Created on Jan 21, 2012
@author: sanjits
'''
import csv
from bussr.gtfs.models import StopTime, Trip, Stop
import re

class StopTimeImporter(object):
    '''
    Import stops.txt gtfs file
    '''

    def __init__(self, filename, stopIdsToImport=None):
        '''
        Constructor
        '''
        self.filename = filename
        self.stopIdsToImport = stopIdsToImport
        
        
    def parse(self):
        '''
        Parse the stoptimes.txt gtfs file
        '''
        reader = csv.DictReader(open(self.filename, 'r'))
        for row in reader:
            stopId = row['stop_id']
            if self.stopIdsToImport is None or stopId in self.stopIdsToImport:
                stopTime = StopTime()
                trip = self.tripForId(row['trip_id'])
                stopTime.trip = trip
                stopTime.tripId = row['trip_id']
                stopTime.routeId = trip.routeId
                stopTime.stop = self.stopForId(row['stop_id'])
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
    
    def stopForId(self, stopId):
        return Stop.objects.get(stopId=stopId)
        
    def parseTime(self, value):
        parts = re.split(':', value)
        hr = int(parts[0])
        mn = int(parts[1])
        ss = int(parts[2])
        return ss + (mn * 60) + (hr * 3600)
    