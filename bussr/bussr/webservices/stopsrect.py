from django.http import HttpResponse
from django.contrib.gis.geos import Polygon
import logging
import json
from BaseRequestHandler import BaseRequestHandler
from bussr.gtfs.models import Stop, ModelJSONEncoder

logger = logging.getLogger(__name__)

def service(request,neLatParam,neLngParam, swLatParam, swLngParam):
    nelat = float(neLatParam)
    nelng = float(neLngParam)
    swlat = float(swLatParam)
    swlng = float(swLngParam)
    getStops = GetStopsInRectangle()
    return getStops.service(request, nelat, nelng, swlat, swlng)

class GetStopsInRectangle(BaseRequestHandler):
    def service(self, request, nelat, nelng, swlat, swlng):
        boundsRect = Polygon.from_bbox((min(nelng, swlng), min(nelat,swlat), max(nelng, swlng), max(nelat, swlat)))
        stopGeoQuerySet = Stop.objects.filter(point__within=boundsRect)[:50]
        jsonOut = json.dumps({'stops' : list(stopGeoQuerySet)}, cls=ModelJSONEncoder)
        print 'Area', boundsRect.area
        return HttpResponse(
            jsonOut,
            content_type = 'application/javascript; charset=utf8'
        )
