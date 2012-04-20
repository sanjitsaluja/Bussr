'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from gtfs.models import Shape
from django.contrib.gis.geos import Point
from importer_base import CSVImporterBase

class ShapeImporter(CSVImporterBase):
    '''
    classdocs
    '''

    def __init__(self, filename, source, logger):
        '''
        Constructor
        '''
        super(ShapeImporter, self).__init__()
        self.filename = filename
        self.source = source
        self.logger = logger
        
    def parse(self):
        toDel = Shape.objects.filter(source=self.source)
        self.logger.info('Cleaning existing Shape %s', toDel)
        toDel.delete()
        
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)        
        for row in reader:
            self.logger.info('Parsing shape row: %s', row)
            sequence = int(row['shape_pt_sequence'])
            shapeId = row['shape_id']
            shape = Shape()
            shape.source = self.source
            shape.shapeId = shapeId
            shape.lat = float(row['shape_pt_lat'])
            shape.lng = float(row['shape_pt_lon'])
            shape.point = Point(y=shape.lat, x=shape.lng)
            shape.sequence = sequence
            shape.distanceTraveled = 'shape_dist_travelled' in row and float(row['shape_dist_travelled']) or None
            shape.save()