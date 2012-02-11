from django.shortcuts import render_to_response
from bussr.gtfs.models import Stop, Source

def routeIdsForStop(source, stop):
    '''
    Get all routes for a given stop. 
    TODO: slow operation. fix it.
    '''
    setRouteIds = set([])
    stopTimes = stop.stoptime_set.filter(source=source)
    for time in stopTimes:
        setRouteIds.add(time.routeId)
    return setRouteIds


def service(request, sourceId, stopIdParam):
    '''
    service the ajax request for the bubble
    '''
    source = Source.objects.get(id=sourceId)
    if stopIdParam is not None and len(stopIdParam) > 0:
        stop = Stop.objects.filter(source=source).get(stopId=stopIdParam)
        routeIds = routeIdsForStop(source, stop)
        return render_to_response('bubble.html',
                                {
                                    'sourceId' : sourceId,
                                    'stop' : stop,
                                    'routeIds' : routeIds,
                                })
    
