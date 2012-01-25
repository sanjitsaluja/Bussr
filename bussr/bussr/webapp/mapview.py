from django.views.generic.simple import direct_to_template

def service(request):
    return direct_to_template(request,
                              'map.html',
                              None)
