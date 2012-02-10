'''
Created on Jan 21, 2012
@author: sanjits
'''
from bussr.gtfs.models import StopTime, Trip, Stop, Route
from importer_base import CSVImporterBase
import csv
import re

class StopTimeImporter(CSVImporterBase):
    '''
    Import stops.txt gtfs file
    '''

    def __init__(self, filename, source, tripIdToTripMapping, stopIdToStopMapping, routeIdToRouteMapping, onlyNew, stopIdsToImport=None, tripIdsToImport=None):
        '''
        Constructor
        '''
        super(StopTimeImporter, self).__init__()
        self.filename = filename
        self.stopIdsToImport = stopIdsToImport
        self.tripIdsToImport = tripIdsToImport
        self.source = source
        self.tripIdToTripMapping = tripIdToTripMapping
        self.stopIdToStopMapping = stopIdToStopMapping
        self.routeIdToRouteMapping = routeIdToRouteMapping
        self.onlyNew = onlyNew
        
    def shapeDistForRow(self, row):
        try:
            return 'shape_dist_traveled' in row and float(row['shape_dist_traveled']) or None
        except ValueError:
            return None
        
    def parse(self):
        '''
        Parse the stoptimes.txt gtfs file
        '''
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        for row in reader:

            stopId = row['stop_id']
            tripId = row['trip_id']
            stopSequence = row['stop_sequence']
            
            if (self.stopIdsToImport is None or stopId in self.stopIdsToImport) and (self.tripIdsToImport is None or tripId in self.tripIdsToImport):
                try:
                    stopTime = StopTime.objects.filter(source=self.source).filter(stopId=stopId).filter(tripId=tripId).get(stopSequence=stopSequence)
                    if self.onlyNew:
                        continue
                except StopTime.DoesNotExist:
                    stopTime = StopTime()

                if self.verboseParse:
                    print 'Parsing stoptime row:', row

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
    