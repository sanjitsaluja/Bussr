def csvValueOrNone(csvRow, colName):
    return colName in csvRow and csvRow[colName] or None
