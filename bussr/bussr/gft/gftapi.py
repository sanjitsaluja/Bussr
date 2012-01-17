# non django
import urllib2
import urllib

class GFDataSource:
    def __init__(self):
        self.fusionTableUrl = r'https://www.google.com/fusiontables/api/query'
        self.postDataBody = 'SELECT * FROM 1-pwM2heV1EslsSH96hdz4-bgETwb-CjSXQXfXkQ WHERE ST_INTERSECTS(Location, CIRCLE(LATLNG(%f, %f),1000)) LIMIT 500'

    def parseCsv(self, csvStr):
        rows = csvStr.split('\n')
        parsedRows = []
        for row in rows:
            cols = row.split(',')
            if len(cols) == 3:
                stopId = cols[0]
                stopName = cols[1]
                latlng = cols[2].split(" ")
                if len(latlng) == 2:
                    parsedRows.append({'stopName':stopName, 'stopId':stopId, 'lat':float(latlng[0]), 'lng':float(latlng[1])})
        return parsedRows

    def resultsNear(self, lat, lng):
        response = None
        try:
            postStr = self.postDataBody % (lat, lng)
            data = urllib.urlencode([('sql', postStr)])
            response = urllib2.urlopen(self.fusionTableUrl, data)
        except IOError, e:
            raise e
        return response.read()

    def parsedResultsNear(self, lat, lng):
        raw = self.resultsNear(lat, lng)
        return self.parseCsv(raw)

