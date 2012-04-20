import os
from route_importer import RouteImporter
from stop_importer import StopImporter
from agency_importer import AgencyImporter
from calendar_importer import CalendarImporter
from shape_importer import ShapeImporter
from trip_importer import TripImporter
from stoptime_importer import StopTimeImporter

class GTFSImporter:
    
    def __init__(self, dataDir, source, logger):
        self.dataDir = dataDir
        self.routeIdToRouteMapping = None
        self.source = source
        self.logger = logger
        
    def importAgencies(self):
        filename = os.path.join(self.dataDir, 'agency.txt')
        self.logger.info('Importing agencies from %s', filename)
        importer = AgencyImporter(filename=filename, source=self.source, logger=self.logger)
        importer.parse()
    
    def importStops(self):
        ctaFilename = os.path.join(self.dataDir, 'stops.txt')
        self.logger.info('Importing stops from %s', ctaFilename)
        stopImporter = StopImporter(filename=ctaFilename, source=self.source, logger=self.logger)
        stopIdToStopMapping = stopImporter.parse()
        return stopIdToStopMapping
    
    def importRoutes(self):
        ctaFilename = os.path.join(self.dataDir, 'routes.txt')
        self.logger.info('Importing routes from %s', ctaFilename)
        importer = RouteImporter(filename=ctaFilename, source=self.source, logger=self.logger)
        routeIdToRouteMapping = importer.parse()
        return routeIdToRouteMapping
    
    def importCalendar(self):
        ctaFilename = os.path.join(self.dataDir, 'calendar.txt')
        self.logger.info('Importing calendar from %s', ctaFilename)
        importer = CalendarImporter(filename=ctaFilename, source=self.source, logger=self.logger)
        serviceIdToCalendarMapping = importer.parse()
        return serviceIdToCalendarMapping
    
    def importShapes(self):
        ctaFilename = os.path.join(self.dataDir, 'shapes.txt')
        self.logger.info('Importing trips from %s', ctaFilename)
        importer = ShapeImporter(ctaFilename, source=self.source, logger=self.logger)
        importer.parse()
    
    def importTrips(self, routeIdToRouteMapping, serviceIdToCalendarMapping):
        ctaFilename = os.path.join(self.dataDir, 'trips.txt')
        self.logger.info('Importing trips from %s', ctaFilename)
        importer = TripImporter(filename=ctaFilename, source=self.source, routeIdToRouteMapping=routeIdToRouteMapping, serviceIdToCalendarMapping=serviceIdToCalendarMapping, logger=self.logger)
        tripIdToTripMapping = importer.parse()
        return tripIdToTripMapping

    def importStopTimes(self, tripIdToTripMapping, stopIdToStopMapping, routeIdToRouteMapping, stopIdsToImport = None, tripIdsToImport = None, tripToRouteMapping = None):
        ctaFilename = os.path.join(self.dataDir, 'stop_times.txt')
        self.logger.info('Importing stop times from %s', ctaFilename)
        stopImporter = StopTimeImporter(ctaFilename, source=self.source, tripIdToTripMapping=tripIdToTripMapping, stopIdToStopMapping=stopIdToStopMapping, routeIdToRouteMapping=routeIdToRouteMapping, stopIdsToImport=stopIdsToImport, tripIdsToImport=tripIdsToImport, logger=self.logger)
        stopImporter.parse()

    def importall(self):
        self.importAgencies()
        self.routeIdToRouteMapping = self.importRoutes()
        self.serviceIdToCalendarMapping = self.importCalendar()
        self.tripIdToTripMapping = self.importTrips(self.routeIdToRouteMapping, self.serviceIdToCalendarMapping)
        self.serviceIdToCalendarMapping = None
        # self.importShapes()
        self.stopIdToStopMapping = self.importStops()
        self.importStopTimes(self.tripIdToTripMapping, self.stopIdToStopMapping, self.routeIdToRouteMapping, stopIdsToImport = None, tripIdsToImport = None, tripToRouteMapping = None)