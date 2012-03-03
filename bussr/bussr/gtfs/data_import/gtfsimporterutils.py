def csvValueOrNone(csvRow, colName):
    '''
    Find the value for the given col in the csv or return None
    @param csvRow: 
    @param colName: 
    '''
    return keyValueOrNone(csvRow, colName)


def keyValueOrNone(dict, key):
    '''
    Find the value for the given key in the dict or return None
    @param dict: 
    @param key: 
    '''
    return key in dict and dict[key] or None


def cleanGTFSId(strId):
    '''
    @param strId: id string to remove the slashes from
    '''
    return strId.replace('/', '-')
