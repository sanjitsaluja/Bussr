'''
Created on Jan 22, 2012

@author: sanjits
'''

import csv
from bussr.gtfs.models import Shape
from django.contrib.gis.geos import Point

class ShapeImporter(object):
    '''
    classdocs
    '''

    def __init__(self, filename, agency):
        '''
        Constructor
        '''
        self.filename = filename
        self.agency = agency
        
    def parse(self):
        reader = csv.DictReader(open(self.filename, 'r'), skipinitialspace=True)
        for row in reader:
            shapeId = row['shape_id']
            shape = Shape.objects.filter(agency=self.agency).get(shapeId=shapeId)
            if shape is None:
                shape = Shape()
            shape.shapeId = shapeId
            shape.lat = float(row['shape_pt_lat'])
            shape.lng = float(row['shape_pt_lon'])
            shape.point = Point(y=shape.lat, x=shape.lng)
            shape.sequence = int(row['shape_pt_sequence'])
            shape.distanceTraveled = 'shape_dist_travelled' in row and float(row['shape_dist_travelled']) or None
            shape.save()