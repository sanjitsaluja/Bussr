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
from source_importer import SourceImporter

class GTFSImporter:
    
    def __init__(self, dataDir, onlyNew, source):
        self.dataDir = dataDir
        self.routeIdToRouteMapping = None
        self.onlyNew = onlyNew
        self.source = source
        
    def importAgencies(self):
        filename = os.path.join(self.dataDir, 'agency.txt')
        print 'Importing agencies from ', filename
        importer = AgencyImporter(filename=filename, source=self.source)
        importer.parse()
    
    def importStops(self, stopIdsToImport = None):
        ctaFilename = os.path.join(self.dataDir, 'stops.txt')
        print 'Importing stops from ', ctaFilename
        stopImporter = StopImporter(filename=ctaFilename, source=self.source, onlyNew=self.onlyNew, stopIdsToImport=stopIdsToImport)
        stopIdToStopMapping = stopImporter.parse()
        return stopIdToStopMapping
    
    def importRoutes(self):
        ctaFilename = os.path.join(self.dataDir, 'routes.txt')
        print 'Importing routes from ', ctaFilename
        importer = RouteImporter(filename=ctaFilename, source=self.source, onlyNew=self.onlyNew)
        routeIdToRouteMapping = importer.parse()
        return routeIdToRouteMapping
    
    def importCalendar(self):
        ctaFilename = os.path.join(self.dataDir, 'calendar.txt')
        print 'Importing calendar from ', ctaFilename
        importer = CalendarImporter(filename=ctaFilename, source=self.source, onlyNew=self.onlyNew)
        serviceIdToCalendarMapping = importer.parse()
        return serviceIdToCalendarMapping
    
    def importShapes(self):
        ctaFilename = os.path.join(self.dataDir, 'shapes.txt')
        print 'Importing trips from ', ctaFilename
        importer = ShapeImporter(ctaFilename, source=self.source)
        importer.parse()
    
    def importTrips(self, routeIdToRouteMapping, serviceIdToCalendarMapping):
        ctaFilename = os.path.join(self.dataDir, 'trips.txt')
        print 'Importing trips from ', ctaFilename
        importer = TripImporter(filename=ctaFilename, source=self.source, routeIdToRouteMapping=routeIdToRouteMapping, serviceIdToCalendarMapping=serviceIdToCalendarMapping, onlyNew=self.onlyNew)
        tripIdToTripMapping = importer.parse()
        return tripIdToTripMapping
    
    def importStopTimes(self, tripIdToTripMapping, stopIdToStopMapping, routeIdToRouteMapping, stopIdsToImport = None, tripIdsToImport = None, tripToRouteMapping = None):
        ctaFilename = os.path.join(self.dataDir, 'stop_times.txt')
        print 'Importing stop times from ', ctaFilename
        stopImporter = StopTimeImporter(ctaFilename, source=self.source, tripIdToTripMapping=tripIdToTripMapping, stopIdToStopMapping=stopIdToStopMapping, routeIdToRouteMapping=routeIdToRouteMapping, onlyNew=self.onlyNew, stopIdsToImport=stopIdsToImport, tripIdsToImport=tripIdsToImport)
        stopImporter.parse()
    
    def importall(self):
        self.importAgencies()
        self.routeIdToRouteMapping = self.importRoutes()
        self.serviceIdToCalendarMapping = self.importCalendar()
        self.importShapes()
        self.tripIdToTripMapping = self.importTrips(self.routeIdToRouteMapping, self.serviceIdToCalendarMapping)
        self.serviceIdToCalendarMapping = None
#        
        self.stopIdToStopMapping = self.importStops()
        self.importStopTimes(self.tripIdToTripMapping, self.stopIdToStopMapping, self.routeIdToRouteMapping, stopIdsToImport = None, tripIdsToImport = None, tripToRouteMapping = None)
    

class DataLoader:
    def __init__(self, rawDataDir, onlyNew, sourceIdsToImport=None):
        self.sourceIdsToImport = sourceIdsToImport
        self.rawDataDir = rawDataDir
        self.onlyNew = onlyNew
        self.sourceMapping = [
{'id':'1', 'codeName':'METRA',    'dataDir': 'metra',                     'importUrl': 'http://www.gtfs-data-exchange.com/agency/metra/latest.zip'                        },
{'id':'2', 'codeName':'CTA',      'dataDir': 'cta',                       'importUrl': 'http://www.gtfs-data-exchange.com/agency/chicago-transit-authority/latest.zip'    },
{'id':'3', 'codeName':'KCM',      'dataDir': 'king-county-metro-transit', 'importUrl': 'http://www.gtfs-data-exchange.com/agency/king-county-metro-transit/latest.zip'    },    
        ];
        
    def importSource(self, mapping):
        sourceImporter = SourceImporter(mapping)
        source = sourceImporter.parse()
        dataDir = os.path.join(self.rawDataDir, mapping['dataDir'])
        importer = GTFSImporter(dataDir=dataDir, onlyNew=self.onlyNew, source=source)
        importer.importall()
    
    
    def importAllSources(self):
        for mapping in self.sourceMapping:
            if self.sourceIdsToImport is None or mapping['id'] in self.sourceIdsToImport:
                print 'Importing source mapping', mapping
                self.importSource(mapping)
                
                

if __name__=='__main__':
    if len(sys.argv) < 2:
        print 'ERROR - Specify the raw data directory containing the folder(s) containing the raw gtfs data'
    else:
        rawDataDir = os.path.abspath(sys.argv[1])
        print 'Import gtfs data from', rawDataDir
        
        sourceIdsToImport = None
        if len(sys.argv) > 2:
            sourceIdsToImport = [sys.argv[2]]
            print 'Import agency ids:', sourceIdsToImport
        dataLoader = DataLoader(rawDataDir, onlyNew=(len(sys.argv)==4), sourceIdsToImport=sourceIdsToImport)
        dataLoader.importAllSources()
        