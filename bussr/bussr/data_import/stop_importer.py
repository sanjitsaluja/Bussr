'''
Created on Jan 21, 2012
@author: sanjits
'''
import csv
from bussr.gtfs.models import Stop
from django.contrib.gis.geos import Point
from importer_base import CSVImporterBase

class StopImporter(CSVImporterBase):
    '''
    Import stops.txt gtfs file into the Stop table
    '''

    def __init__(self, filename, source, onlyNew, stopIdsToImport=None):
        '''
        Constructor
        '''
        super(StopImporter, self).__init__()
        self.filename = filename
        self.stopIdsToImport = stopIdsToImport
        self.source = source
        self.onlyNew = onlyNew
        
    def parse(self):
        '''
        Parse the stops.txt gtfs file
        '''
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        stopIdToStopMapping = {}
        for row in reader:
            stopId = row['stop_id']
            if self.stopIdsToImport is None or stopId in self.stopIdsToImport:
                try:
                    stop = Stop.objects.filter(source=self.source).get(stopId=stopId)
                    if self.onlyNew:
                        continue
                except Stop.DoesNotExist:
                    stop = None
                if stop is None:
                    stop = Stop()

                if self.verboseParse:
                    print 'Parsing stop row:', row
                
                stop.sourceId = self.source.id
                stop.source = self.source
                stop.stopId = stopId
                stop.stopCode = 'stop_code' in row and row['stop_code'] or None
                stop.stopName = row['stop_name']
                stop.stopDesc = 'stop_desc' in row and row['stop_desc'] or None
                stop.lat = float(row['stop_lat'])
                stop.lng = float(row['stop_lon'])
                stop.point = Point(y=stop.lat, x=stop.lng)
                stop.zoneId = 'zone_id' in row and row['zone_id'] or None
                stop.stopUrl = 'stop_url' in row and row['stop_url'] or None
                stop.locationType = 'location_type' in row and int(row['location_type']) or 0
                stop.parentStation = 'parent_station' in row and row['parent_station'] or None
                stop.wheelchairAccessible = 'wheelchair_boarding' in row and row['wheelchair_boarding'] or True
                stop.save()
                stopIdToStopMapping[stopId] = stop
        return stopIdToStopMapping