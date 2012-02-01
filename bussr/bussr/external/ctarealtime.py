import urllib
from cElementTree import XMLParser
from datetime import datetime 

basePredictionsUrl = 'http://www.ctabustracker.com/bustime/api/v1/getpredictions?key=XNJJY6RMwcBiS9RCeGXGzNBQj&stpid=%s&top=20'

def getPredictionsUrlForStopId(stopId):
    return basePredictionsUrl % stopId

def getPredictionsForStopId(stopId):
    predictionsUrl = getPredictionsUrlForStopId(stopId)
    request = urllib.urlopen(predictionsUrl)
    xmlResponse = request.read()
    print xmlResponse
    xmlParser = XMLParser()
    xmlParser.feed(xmlResponse)
    busResponseElement = xmlParser.close()
    routePredictionTimes = []
    try:
        for prd in busResponseElement.getchildren():
            route = prd.find('rt').text
            tmstmp = prd.find('prdtm').text
            heading = prd.find('des').text
            timeStamp = datetime.strptime(tmstmp, '%Y%m%d %H:%M')
            routePredictionTimes.append((route, timeStamp, heading))
    except:
        pass
    
    return routePredictionTimes
        
if __name__=='__main__':
    print getPredictionsForStopId('70')
