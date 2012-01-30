from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from bussr.gtfs.models import Stop, StopTime, Calendar, Trip
from datetime import datetime
import math

def stopsForTrip(trip):
    stopTimes = StopTime.objects.filter(trip=trip).order_by('stopSequence')
    stops = []
    for time in stopTimes:
        stops.append(time.stop)
    return stops

def service(request, tripIdParam, stopIdParam=None):
    headSign = None
    
    tripId = int(tripIdParam)
    trip = Trip.objects.get(tripId=tripId)
    
    if stopIdParam is not None:
        stopId = stopIdParam and int(stopIdParam) or -1
        stopTimes = StopTime.objects.filter(stopId=stopId).filter(tripId=tripId)
        if len(stopTimes) == 1:
            headSign = stopTimes[0].headSign
    
    if headSign is None:
        headSign = trip.route.routeLongName
    
    stops = stopsForTrip(trip)
    return render_to_response('tripdetails.html',
                                {
                                 'routeId': trip.routeId,
                                 'headSign' : headSign,
                                 'stops' : stops,
                                 
                                })
    
def routeIdsForStop(stop):
    setRouteIds = set([])
    stopTimes = stop.stoptime_set.all()
    for time in stopTimes:
        setRouteIds.add(time.routeId)
    return setRouteIds
    
