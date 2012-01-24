'''
Created on Jan 21, 2012

@author: sanjits
'''
from django.contrib.gis import admin
from bussr.gtfs.models import Stop

admin.site.register(Stop, admin.OSMGeoAdmin)