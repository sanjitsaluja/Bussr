from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import mapview
import listview
import stopdetails
import tripdetails
import bubble

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cta.views.home', name='home'),
    # url(r'^cta/', include('cta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', mapview.service),
    url(r'^maps/', mapview.service),
    url(r'^list/([-+]?[0-9]*\.?[0-9]*),([-+]?[0-9]*\.?[0-9]*)/$', listview.service),
    url(r'^s/([0-9]+)/stop/([^/]+)/$', stopdetails.service),
    url(r'^s/([0-9]+)/trip/([^/]+)/$', tripdetails.service),
    url(r'^s/([0-9]+)/trip/([^/]+)/stop/([^/]+)/$', tripdetails.service),
    url(r'^s/([0-9]+)/bubble/([^/]+)/', bubble.service)
)
