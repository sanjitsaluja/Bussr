from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

def service(request):
    return direct_to_template(request,
                              'map.html',
                              None)
