from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from bussr.gtfs.models import Stop, StopTime, Calendar, Trip, Agency
from datetime import datetime
import math

def stopsForTrip(agency, tripId):
    stopTimes = StopTime.objects.filter(agency=agency).filter(tripId=tripId).order_by('stopSequence')
    stops = []
    for time in stopTimes:
        stops.append(time.stop)
    return stops

def service(request, agencyId, tripId, stopIdParam=None):
    headSign = None
    agency = Agency.objects.get(id=agencyId)
    trip = Trip.objects.filter(agency=agency).get(tripId=tripId)
    
    if stopIdParam is not None:
        stopId = stopIdParam
        stopTimes = StopTime.objects.filter(agency=agency).filter(stopId=stopId).filter(tripId=tripId)
        if len(stopTimes) == 1:
            headSign = stopTimes[0].headSign
    
    if headSign is None:
        headSign = trip.route.routeLongName
    
    stops = stopsForTrip(agency, trip.tripId)
    return render_to_response('tripdetails.html',
                                {
                                 'agencyId' : agencyId,
                                 'routeId': trip.routeId,
                                 'headSign' : headSign,
                                 'stops' : stops,
                                })
    
