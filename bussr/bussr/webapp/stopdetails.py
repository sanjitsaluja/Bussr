from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from bussr.gtfs.models import Stop, StopTime, Calendar
from datetime import datetime
import math

def currentTimeInSecondsSinceDawn():
    now = datetime.now()
    return now.hour * 3600 + now.minute * 60 + now.second

def stopTimes(stop, minutes):
    startTime = currentTimeInSecondsSinceDawn()
    endTime = startTime + minutes*60.0
    stopTimes = StopTime.objects.filter(stop=stop).filter(arrivalSeconds__gte=startTime).filter(arrivalSeconds__lte=endTime).order_by("arrivalSeconds")
    print endTime, stopTimes
    return stopTimes

def timeStringForSeconds(seconds):
    hr = ((seconds/3600) % 12) or 12
    mn = (seconds / 60) % 60
    return '%d : %02d' % (hr, mn)

def timeDeltaStringForSeconds(seconds):
    mn = seconds / 60.0
    mn_now = currentTimeInSecondsSinceDawn() / 60.0
    return '%d min' % math.ceil(mn - mn_now)

def service(request,stopIdParam):
    stopId = int(stopIdParam)
    stop = Stop.objects.get(stopId=stopId)
    times = stopTimes(stop, 60)
    stopTimesOut = []
    for time in times:
        trip = time.trip
        route = trip.route
        service = trip.service
        if service.today():
            stopTimeOut = {}
            stopTimeOut['routeId'] = route.routeId
            stopTimeOut['routeName'] = route.routeLongName or route.routeShortName or route.routeId
            stopTimeOut['headSign'] = time.headSign
            stopTimeOut['displayTime'] = timeStringForSeconds(time.arrivalSeconds)
            stopTimeOut['displayTimeDelta'] = timeDeltaStringForSeconds(time.arrivalSeconds)
            stopTimesOut.append(stopTimeOut)
            
    return render_to_response('stopdetails.html',
                                {
                                 'stop': stop,
                                 'times': stopTimesOut,
                                })
    
def routeIdsForStop(stop):
    setRouteIds = set([])
    stopTimes = stop.stoptime_set.all()
    for time in stopTimes:
        setRouteIds.add(time.routeId)
    return setRouteIds
    
def serviceBubble(request, stopIdParam):
    stopId = int(stopIdParam)
    stop = Stop.objects.get(stopId=stopId)
    return render_to_response('bubble.html',
                                {
                                    'stop' : stop,
                                    'routeIds' : routeIdsForStop(stop)
                                })
    
