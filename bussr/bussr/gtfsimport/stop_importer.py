'''
Created on Jan 21, 2012
@author: sanjits
'''
import csv
from gtfs.models import Stop
from django.contrib.gis.geos import Point
from importer_base import CSVImporterBase

class StopImporter(CSVImporterBase):
    '''
    Import stops.txt gtfs file into the Stop table
    '''

    def __init__(self, filename, source, logger):
        '''
        Constructor
        '''
        super(StopImporter, self).__init__()
        self.filename = filename
        self.source = source
        self.logger=logger
        
    def locationTypeForRow(self, row):
        try:
            return 'location_type' in row and int(row['location_type']) or 0
        except ValueError:
            return 0
        
    def parse(self):
        '''
        Parse the stops.txt gtfs file
        @return: stopId->object mapping
        '''
        toDel = Stop.objects.filter(source=self.source)
        self.logger.debug('Cleaning existing stops %s', toDel)
        toDel.delete()
        
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        stopIdToStopMapping = {}
        for row in reader:
            self.logger.info('Parsing stop row: %s', row)
            stopId = row['stop_id']
            stop = Stop()
            stop.sourceId = self.source.sourceId
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
            stop.locationType = self.locationTypeForRow(row)
            stop.parentStation = 'parent_station' in row and row['parent_station'] or None
            stop.wheelchairAccessible = 'wheelchair_boarding' in row and row['wheelchair_boarding'] or True
            stop.save()
            stopIdToStopMapping[stopId] = stop
        return stopIdToStopMapping