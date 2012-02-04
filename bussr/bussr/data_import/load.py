import sys
import os
sys.path.append("..")
from django.core.management import setup_environ
from bussr import settings
setup_environ(settings)
from bussr.gtfs.models import Agency
from route_importer import RouteImporter
from stop_importer import StopImporter
from agency_importer import AgencyImporter
from calendar_importer import CalendarImporter
from shape_importer import ShapeImporter
from trip_importer import TripImporter
from stoptime_importer import StopTimeImporter

class GTFSImporter:
    
    def __init__(self, dataDir, agencyPK):
        self.dataDir = dataDir
        self.routeIdToRouteMapping = None
        self.agency = self.importAgencies(agencyPK=agencyPK)
        
    def importAgencies(self, agencyPK):
        filename = os.path.join(self.dataDir, 'agency.txt')
        print 'Importing agencies from ', filename
        importer = AgencyImporter(filename=filename, agencyPK=agencyPK)
        importer.parse()
        agency = Agency.objects.get(id=agencyPK)
        return agency
    
    def importStops(self, agency, stopIdsToImport = None):
        ctaFilename = os.path.join(self.dataDir, 'stops.txt')
        print 'Importing stops from ', ctaFilename
        stopImporter = StopImporter(filename=ctaFilename, agency=agency, stopIdsToImport=stopIdsToImport)
        stopIdToStopMapping = stopImporter.parse()
        return stopIdToStopMapping
    
    def importRoutes(self, agency):
        ctaFilename = os.path.join(self.dataDir, 'routes.txt')
        print 'Importing routes from ', ctaFilename
        importer = RouteImporter(filename=ctaFilename, agency=agency)
        routeIdToRouteMapping = importer.parse()
        return routeIdToRouteMapping
    
    def importCalendar(self, agency):
        ctaFilename = os.path.join(self.dataDir, 'calendar.txt')
        print 'Importing calendar from ', ctaFilename
        importer = CalendarImporter(filename=ctaFilename, agency=agency)
        serviceIdToCalendarMapping = importer.parse()
        return serviceIdToCalendarMapping
    
    #def importShapes():
    #    filePath = os.path.dirname(__file__)
    #    ctaFilename = os.path.join(filePath, 'cta/shapes.txt')
    #    print 'Importing shapes from ', ctaFilename
    #    importer = ShapeImporter(ctaFilename)
    #    importer.parse()
    
    def importTrips(self, agency, routeIdToRouteMapping, serviceIdToCalendarMapping):
        ctaFilename = os.path.join(self.dataDir, 'trips.txt')
        print 'Importing trips from ', ctaFilename
        importer = TripImporter(filename=ctaFilename, agency=agency, routeIdToRouteMapping=routeIdToRouteMapping, serviceIdToCalendarMapping=serviceIdToCalendarMapping)
        tripIdToTripMapping = importer.parse()
        return tripIdToTripMapping
    
    def importStopTimes(self, agency, tripIdToTripMapping, stopIdToStopMapping, routeIdToRouteMapping, stopIdsToImport = None, tripIdsToImport = None, tripToRouteMapping = None):
        ctaFilename = os.path.join(self.dataDir, 'stop_times.txt')
        print 'Importing stop times from ', ctaFilename
        stopImporter = StopTimeImporter(ctaFilename, agency=agency, tripIdToTripMapping=tripIdToTripMapping, stopIdToStopMapping=stopIdToStopMapping, routeIdToRouteMapping=routeIdToRouteMapping, stopIdsToImport=stopIdsToImport, tripIdsToImport=tripIdsToImport)
        stopImporter.parse()
    
    def importall(self):
        self.routeIdToRouteMapping = self.importRoutes(self.agency)
        self.serviceIdToCalendarMapping = self.importCalendar(self.agency)
        # importShapes()
        self.tripIdToTripMapping = self.importTrips(self.agency, self.routeIdToRouteMapping, self.serviceIdToCalendarMapping)
        self.serviceIdToCalendarMapping = None
        
        self.stopIdToStopMapping = self.importStops(self.agency)
        self.importStopTimes(self.agency, self.tripIdToTripMapping, self.stopIdToStopMapping, self.routeIdToRouteMapping, stopIdsToImport = None, tripIdsToImport = None, tripToRouteMapping = None)
    

class DataLoader:
    def __init__(self, rawDataDir, agencyIdsToImport=None):
        self.agencyIdsToImport = agencyIdsToImport
        self.rawDataDir = rawDataDir
        self.agencyImportMapping = [
                         {'agencyId':'1', 'friendlyName':'Metra', 'dataRelDir': 'metra',    'importer': None},
                         {'agencyId':'2', 'friendlyName':'CTA',   'dataRelDir': 'cta',      'importer': None},
                         ];
        
    def importAgencyMapping(self, mapping):
        dataDir = os.path.join(self.rawDataDir, mapping['dataRelDir'])
        print 'importAgencyMapping dataDir', dataDir
        importer = GTFSImporter(dataDir=dataDir, agencyPK=mapping['agencyId'])
        importer.importall()
    
    
    def importAllAgencies(self):
        for mapping in self.agencyImportMapping:
            if self.agencyIdsToImport is None or mapping['agencyId'] in self.agencyIdsToImport:
                print 'Importing agency mapping', mapping
                self.importAgencyMapping(mapping)
                
                

if __name__=='__main__':
    if len(sys.argv) < 2:
        print 'ERROR - Specify the raw data directory containing the folder(s) containing the raw gtfs data'
    else:
        rawDataDir = os.path.abspath(sys.argv[1])
        print 'Import gtfs data from', rawDataDir
        
        agencyIdsToImport = None
        if len(sys.argv) > 2:
            agencyIdsToImport = [sys.argv[2]]
            print 'Import agency ids:', agencyIdsToImport
        dataLoader = DataLoader(rawDataDir, agencyIdsToImport)
        dataLoader.importAllAgencies()
        