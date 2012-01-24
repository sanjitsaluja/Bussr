# django
from django.http import HttpResponse
from django.contrib.gis.geos import Polygon
from django.core import serializers

# non django
import logging
import json

# bussr
from BaseRequestHandler import BaseRequestHandler
from bussr.gtfs.models import Stop, encode_bussr_model

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
        stops = Stop.objects.filter(point__within=boundsRect)
        jsonOut = serializers.serialize('json', stops)
        return HttpResponse(
            jsonOut,
            content_type = 'application/javascript; charset=utf8'
        )
