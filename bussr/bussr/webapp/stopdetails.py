from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from bussr.gtfs.models import Stop

def service(request,stopIdParam):
    stopId = int(stopIdParam)
    stop = Stop.objects.get(stopId=stopId)
    print stop
    return render_to_response('stopdetails.html',
                              {'stop' : stop})
