class RealtimePrediction():
    def __init__(self):
        '''
        Route id of the prediction
        '''
        self.routeId = None
        
        '''
        Arrival time in seconds from noon-12h
        '''
        self.predictedArrivalTime = None


class RealtimePredictionSet():
    def __init__(self):
        '''
        Stop id of the prediction
        '''
        self.stopId = None
        
        '''
        Array of predictions
        '''
        self.predictions = None
        
        '''
        '''
        
    def getNextArrivalTimeForRouteId(self, routeId):
        pass
    
    
class RealtimePredictorBase():
    def getPredictionsForStopId(self, stopId):
        '''
        Retuns RealtimePredictionSet object containing the predictions
        for the requested stopId
        '''
        return None