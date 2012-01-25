from django.views.generic.simple import direct_to_template

def service(request,stopIdParam):
    stopId = int(stopIdParam)
    return direct_to_template(request,
                              'stopdetails.html',
                              None)
