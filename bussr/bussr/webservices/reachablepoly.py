from os.path import abspath, dirname
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from os.path import abspath, dirname
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))

sys.path = ['/home/sanjits/Projects/bussr/bussr/bussr/../bussr', '/home/sanjits/Projects/bussr/bussr/bussr', '/home/sanjits/Projects/bussr/bussr/bussr', '/home/sanjits/Projects/bussr/local/lib/python2.7/site-packages/setuptools-0.6c11-py2.7.egg', '/home/sanjits/Projects/bussr/local/lib/python2.7/site-packages/pip-1.0.2-py2.7.egg', '/home/sanjits/Projects/bussr/lib/python2.7/site-packages/setuptools-0.6c11-py2.7.egg', '/home/sanjits/Projects/bussr/lib/python2.7/site-packages/pip-1.0.2-py2.7.egg', '/home/sanjits/Projects/bussr/lib/python2.7', '/home/sanjits/Projects/bussr/lib/python2.7/plat-linux2', '/home/sanjits/Projects/bussr/lib/python2.7/lib-tk', '/home/sanjits/Projects/bussr/lib/python2.7/lib-old', '/home/sanjits/Projects/bussr/lib/python2.7/lib-dynload', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-linux2', '/usr/lib/python2.7/lib-tk', '/home/sanjits/Projects/bussr/local/lib/python2.7/site-packages', '/home/sanjits/Projects/bussr/lib/python2.7/site-packages', '/home/sanjits/Projects/bussr/local/lib/python2.7/site-packages/IPython/extensions']

from gtfs.models import Stop, StopTime, Source

source = Source.objects.filter(id='4')
print source

stop = Stop.objects.filter(source=source).all()[0]
lat = stop.lat
lng = stop.lng
print lat, lng