from django.shortcuts import render_to_response

from bussr.gft.gftapi import GFDataSource

def service(request,latParam,lngParam):
    lat = float(latParam)
    lng = float(lngParam)
    print lat, lng
    dataSource = GFDataSource()
    results = dataSource.parsedResultsNear(lat, lng)
    return render_to_response('list.html', locals())
