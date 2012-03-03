from django.http import HttpResponse
import logging
import json
from BaseRequestHandler import BaseRequestHandler
from bussr.gtfs.models import Stop, ModelJSONEncoder, Source

logger = logging.getLogger(__name__)

def service(request, sourceId, stopId):
    handler = StopDetailsHandler()
    return handler.service(request, sourceId, stopId)

class StopDetailsHandler(BaseRequestHandler):
    def service(self, request, sourceId, stopId):
        source = Source.objects.get(id=sourceId)
        
        
        #jsonOut = json.dumps({'stops' : list(stopGeoQuerySet)}, cls=ModelJSONEncoder)
        #print 'Area', boundsRect.area
        jsonOut = ""
        return HttpResponse(
            jsonOut,
            content_type = 'application/javascript; charset=utf8'
        )
