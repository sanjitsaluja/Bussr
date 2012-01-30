import os
from bussr.gtfs.models import Agency
from bussr.gtfs.data_import.route_importer import RouteImporter
from bussr.gtfs.data_import.stop_importer import StopImporter
from bussr.gtfs.data_import.agency_importer import AgencyImporter 
from bussr.gtfs.data_import.calendar_importer import CalendarImporter
from bussr.gtfs.data_import.shape_importer import ShapeImporter
from bussr.gtfs.data_import.trip_importer import TripImporter
from bussr.gtfs.data_import.stoptime_importer import StopTimeImporter

def importAgencies():
    filePath = os.path.dirname(__file__)
    filename = os.path.join(filePath, 'cta/agency.txt')
    print 'Importing agencies from ', filename
    importer = AgencyImporter(filename)
    importer.parse()
    agencies = Agency.objects.all()
    assert len(agencies) == 1
    return agencies[0]
    
def importStops(stopIdsToImport = None):
    filePath = os.path.dirname(__file__)
    ctaFilename = os.path.join(filePath, 'cta/stops.txt')
    print 'Importing stops from ', ctaFilename
    stopImporter = StopImporter(ctaFilename, stopIdsToImport)
    stopImporter.parse()
    
def importRoutes(agency):
    filePath = os.path.dirname(__file__)
    ctaFilename = os.path.join(filePath, 'cta/routes.txt')
    print 'Importing routes from ', ctaFilename
    importer = RouteImporter(ctaFilename, agency)
    importer.parse()

def importCalendar():
    filePath = os.path.dirname(__file__)
    ctaFilename = os.path.join(filePath, 'cta/calendar.txt')
    print 'Importing calendar from ', ctaFilename
    importer = CalendarImporter(ctaFilename)
    importer.parse()
    
def importShapes():
    filePath = os.path.dirname(__file__)
    ctaFilename = os.path.join(filePath, 'cta/shapes.txt')
    print 'Importing shapes from ', ctaFilename
    importer = ShapeImporter(ctaFilename)
    importer.parse()
    
def importTrips():
    filePath = os.path.dirname(__file__)
    ctaFilename = os.path.join(filePath, 'cta/trips.txt')
    print 'Importing trips from ', ctaFilename
    importer = TripImporter(ctaFilename)
    tripToRouteMapping = importer.parse()
    return tripToRouteMapping
    
def importStopTimes(stopIdsToImport = None, tripIdsToImport = None, tripToRouteMapping = None):
    filePath = os.path.dirname(__file__)
    ctaFilename = os.path.join(filePath, 'cta/stop_times.txt')
    print 'Importing stop times from ', ctaFilename
    stopImporter = StopTimeImporter(ctaFilename, stopIdsToImport, tripIdsToImport, tripToRouteMapping=tripToRouteMapping)
    stopImporter.parse()

def importall():
    agency = importAgencies()
    importStops()
    importRoutes(agency)
    importCalendar()
    # importShapes()
    tripToRouteMapping = importTrips()
    importStopTimes(tripToRouteMapping=tripToRouteMapping)

def devImportNoDeps():    
    agency = importAgencies()
    importRoutes(agency)
    importCalendar()
    
def devImport():
    stopIdsToImport = [str(i) for i in range(10)]
    importStops(stopIdsToImport)
    # importShapes()
    importTrips()
    importStopTimes(stopIdsToImport=stopIdsToImport)