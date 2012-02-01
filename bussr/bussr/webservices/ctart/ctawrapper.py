import urllib
import urllib2
from cElementTree import *
from xml.dom.minidom import parseString

basePredictionsUrl = 'http://www.ctabustracker.com/bustime/api/v1/getpredictions?key=XNJJY6RMwcBiS9RCeGXGzNBQj&stpid=%s&top=20'

def getPredictionsUrlForStopId(stopId):
    return basePredictionsUrl % stopId

def getPredictionsForStopId(stopId):
    predictionsUrl = getPredictionsUrlForStopId(stopId)
    print predictionsUrl
    request = urllib.urlopen(predictionsUrl)
    xmlResponse = request.read()
    xmlParser = XMLParser()
    xmlParser.feed(xmlResponse)
    xmlElement = xmlParser.close()
    print xmlElement
    
    
if __name__=='__main__':
    getPredictionsForStopId('70')
    
stopId='70'
predictionsUrl = getPredictionsUrlForStopId(stopId)
print predictionsUrl
request = urllib.urlopen(predictionsUrl)
xmlResponse = request.read()
xmlParser = XMLParser()
xmlParser.feed(xmlResponse)
xmlElement = xmlParser.close()
print xmlElement
    