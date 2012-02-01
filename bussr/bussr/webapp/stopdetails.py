from django.shortcuts import render_to_response
from bussr.gtfs.models import Stop, StopTime
from datetime import datetime
import math

def currentTimeInSecondsSinceDawn():
    '''
    Get the current time in seconds in noon-12h
    '''
    now = datetime.now()
    return now.hour * 3600 + now.minute * 60 + now.second

def stopTimes(stopId, minutes):
    '''
    Get all stop times for the given stopId in the next 'minutes' minutes
    @param stopId: Stop id for which to fetch times for
    @param minutes: minutes value
    '''
    assert minutes > 0
    startTime = currentTimeInSecondsSinceDawn()
    endTime = startTime + minutes*60
    stopTimes = StopTime.objects.filter(stopId=stopId).\
                                 filter(arrivalSeconds__gte=startTime).\
                                 filter(arrivalSeconds__lte=endTime).\
                                 order_by("arrivalSeconds")
    return stopTimes

def timeStringForSeconds(seconds):
    '''
    Get seconds representing seconds since noon-12h formatted as as HH: MM
    @param seconds: seconds input
    '''
    hr = ((seconds/3600) % 12) or 12
    mn = (seconds / 60) % 60
    return '%d : %02d' % (hr, mn)

def timeDeltaStringForSeconds(seconds):
    '''
    Get the arrival time in minutes since now()
    @param seconds: the future time we want the difference from
    '''
    seconds_now = currentTimeInSecondsSinceDawn()
    assert seconds > seconds_now
    mn = seconds / 60.0
    mn_now = seconds_now / 60.0
    return '%d min' % math.ceil(mn - mn_now)

def service(request, stopId):
    '''
    service the request to get details for a stop
    '''
    stop = Stop.objects.get(stopId=stopId)
    times = stopTimes(stopId, 60)
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
            stopTimeOut['tripId'] = trip.tripId
            stopTimesOut.append(stopTimeOut)
            
    return render_to_response('stopdetails.html',
                                {
                                 'stop': stop,
                                 'times': stopTimesOut,
                                })
    
