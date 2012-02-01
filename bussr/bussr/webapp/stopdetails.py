from django.shortcuts import render_to_response
from bussr.gtfs.models import Stop, StopTime
from datetime import datetime
import math
from bussr.external.ctarealtime import getPredictionsForStopId

def timeInSecondsSinceDawn(date):
    return date.hour * 3600 + date.minute * 60 + date.second

def currentTimeInSecondsSinceDawn():
    '''
    Get the current time in seconds in noon-12h
    '''
    return timeInSecondsSinceDawn(datetime.now())

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


def dequeueNextPredictionForRoute(realTimePredictions, routeId, headSign):
    arrivalPrediction = None
    if len(realTimePredictions) > 0:
        for i in range(len(realTimePredictions)):
            (route, date, hs) = realTimePredictions[i]
            if route == routeId and hs == headSign:
                arrivalPrediction = date
                del realTimePredictions[i]
                break
    return arrivalPrediction

# returns (string, diffString)
def timeDeltaStringForStopTime(stopTime, predictionDate=None):                
    if predictionDate is None:
        return (timeDeltaStringForSeconds(stopTime.arrivalSeconds), "")
    else:
        origArrival = stopTime.arrivalSeconds
        predictedArrival = timeInSecondsSinceDawn(predictionDate)
        diff = math.ceil(math.fabs(predictedArrival - origArrival)/60.0)
        diffString = "on time"
        if diff > 0:
            # late
            diffString = "%d min late" % math.ceil(diff/60.0)
        elif diff < 0:
            # early
            diffString = "%d min early" % math.ceil(math.fabs(diff)/60.0)
            
        return (timeDeltaStringForSeconds(timeInSecondsSinceDawn(predictionDate)), diffString)

def service(request, stopId):
    '''
    service the request to get details for a stop
    '''
    realTimePredictions = getPredictionsForStopId(stopId)
    stop = Stop.objects.get(stopId=stopId)
    times = stopTimes(stopId, 60)
    stopTimesOut = []
    for time in times:
        trip = time.trip
        route = trip.route
        service = trip.service
        if service.today():
            predictionDate = dequeueNextPredictionForRoute(realTimePredictions, route.routeId, time.headSign)
            stopTimeOut = {}
            stopTimeOut['routeId'] = route.routeId
            stopTimeOut['routeName'] = route.routeLongName or route.routeShortName or route.routeId
            stopTimeOut['headSign'] = time.headSign
            (displayDeltaString, diffString) = timeDeltaStringForStopTime(time, predictionDate)
            stopTimeOut['displayTimeDelta'] = displayDeltaString
            stopTimeOut['timeDifference'] = len(diffString)>0 and "(%s)" % diffString or ""
            stopTimeOut['tripId'] = trip.tripId
            stopTimesOut.append(stopTimeOut)
            
    return render_to_response('stopdetails.html',
                                {
                                 'stop': stop,
                                 'times': stopTimesOut,
                                })
    
