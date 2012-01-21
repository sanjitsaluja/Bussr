# django
from django.http import HttpResponse

# non django
import logging
import json

# other
from BaseRequestHandler import BaseRequestHandler
from bussr.gft.gftapi import GFDataSource

logger = logging.getLogger(__name__)

def service(request,latParam,lngParam):
    lat = float(latParam)
    lng = float(lngParam)
    getStops = GetStops()
    return getStops.service(request, lat, lng)

class GetStops(BaseRequestHandler):
    def service(self, request, lat, lng):
        dataSource = GFDataSource()
        parsedRows = dataSource.parsedResultsNear(lat, lng)
        jsonOut = json.dumps({'stops':parsedRows})
        return HttpResponse(
            jsonOut,
            content_type = 'application/javascript; charset=utf8'
        )
