from django.http import HttpResponse

def service(request,stopIdParam):
    stopId = int(stopIdParam)
    return HttpResponse(stopId)
