'''
Created on Jan 21, 2012
@author: sanjits
'''
import csv
from bussr.gtfs.models import StopTime, Trip, Stop, Route
import re
from importer_base import CSVImporterBase

class StopTimeImporter(CSVImporterBase):
    '''
    Import stops.txt gtfs file
    '''

    def __init__(self, filename, agency, tripIdToTripMapping, stopIdToStopMapping, routeIdToRouteMapping, onlyNew, stopIdsToImport=None, tripIdsToImport=None):
        '''
        Constructor
        '''
        super(StopTimeImporter, self).__init__()
        self.filename = filename
        self.stopIdsToImport = stopIdsToImport
        self.tripIdsToImport = tripIdsToImport
        self.agency = agency
        self.tripIdToTripMapping = tripIdToTripMapping
        self.stopIdToStopMapping = stopIdToStopMapping
        self.routeIdToRouteMapping = routeIdToRouteMapping
        self.onlyNew = onlyNew
        
        
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
                    stopTime = StopTime.objects.filter(agency=self.agency).filter(stopId=stopId).filter(tripId=tripId).get(stopSequence=stopSequence)
                    if self.onlyNew:
                        continue
                except StopTime.DoesNotExist:
                    stopTime = None
                if stopTime is None:
                    stopTime = StopTime()

                if self.verboseParse:
                    print 'Parsing stoptime row:', row

                stopTime.agency = self.agency
                stopTime.tripId = tripId
                stopTime.trip = tripId in self.tripIdToTripMapping and self.tripIdToTripMapping[tripId] or None
                if stopTime.trip is None:
                    stopTime.trip = Trip.objects.filter(agency=self.agency).get(tripId=tripId)
                stopTime.routeId = stopTime.trip.routeId
                stopTime.route = stopTime.routeId in self.routeIdToRouteMapping and self.routeIdToRouteMapping[stopTime.routeId] or None
                if stopTime.route is None:
                    stopTime.route = Route.objects.filter(agency=self.agency).get(routeId=stopTime.routeId)
                stopTime.stopId = stopId
                stopTime.stop = stopId in self.stopIdToStopMapping and self.stopIdToStopMapping[stopId] or None
                if stopTime.stop is None:
                    stopTime.stop = Stop.objects.filter(agency=self.agency).get(stopId=stopId)
                stopTime.stopSequence = stopSequence
                stopTime.arrivalSeconds = self.parseTime(row['arrival_time'])
                stopTime.departureSeconds = self.parseTime(row['departure_time'])
                stopTime.headSign = 'stop_headsign' in row and row['stop_headsign'] or None
                stopTime.pickUpType = 'pickup_type' in row and row['pickup_type'] or None
                stopTime.dropOffType = 'dropoff_type' in row and row['dropoff_type'] or None
                stopTime.distanceTraveled = 'shape_dist_traveled' in row and float(row['shape_dist_traveled']) or None
                stopTime.save()
        
            
    def parseTime(self, value):
        parts = re.split(':', value)
        hr = int(parts[0])
        mn = int(parts[1])
        ss = int(parts[2])
        return ss + (mn * 60) + (hr * 3600)
    