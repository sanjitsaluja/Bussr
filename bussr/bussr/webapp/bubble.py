from django.shortcuts import render_to_response
from bussr.gtfs.models import Stop, Agency

def routeIdsForStop(agency, stop):
    '''
    Get all routes for a given stop. 
    TODO: slow operation. fix it.
    '''
    setRouteIds = set([])
    stopTimes = stop.stoptime_set.filter(agency=agency)
    for time in stopTimes:
        setRouteIds.add(time.routeId)
    return setRouteIds


def service(request, agencyId, stopIdParam):
    '''
    service the ajax request for the bubble
    '''
    agency = Agency.objects.get(id=agencyId)
    if stopIdParam is not None and len(stopIdParam) > 0:
        stop = Stop.objects.filter(agency=agency).get(stopId=stopIdParam)
        routeIds = routeIdsForStop(agency, stop)
        return render_to_response('bubble.html',
                                {
                                    'agencyId' : agencyId,
                                    'stop' : stop,
                                    'routeIds' : routeIds,
                                })
    
