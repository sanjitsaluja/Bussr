from django.shortcuts import render_to_response
from bussr.gtfs.models import Stop, StopTime

def routeIdsForStop(stop):
    '''
    Get all routes for a given stop. 
    TODO: slow operation. fix it.
    '''
    setRouteIds = set([])
    stopTimes = StopTime.objects.filter(stopId=stop.stopId)
    for time in stopTimes:
        setRouteIds.add(time.routeId)
    return setRouteIds


def service(request, stopIdParam):
    '''
    service the ajax request for the bubble
    '''
    if stopIdParam is not None and len(stopIdParam) > 0:
        stop = Stop.objects.get(stopId=stopIdParam)
        routeIds = routeIdsForStop(stop)
        return render_to_response('bubble.html',
                                {
                                    'stop' : stop,
                                    'routeIds' : routeIds,
                                })
    
