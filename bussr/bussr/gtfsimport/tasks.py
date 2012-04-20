from celery.decorators import task
from gtfsimport.load import DataLoader
import os
import json


@task(ignore_result=True)
def importGTFSSourceId(sourceId):
    logger = importGTFSSourceId.get_logger()
    logger.info('Starting job gtfsImportSourceId {0}'.format(sourceId))
    dataLoader = DataLoader(sourceIdsToImport=[sourceId], logger=logger)
    dataLoader.performImport()
    logger.info('Completed job gtfsImportSourceId {0}'.format(sourceId))

@task(ignore_result=True)
def bussrImportDevData():
    importGTFSSourceId.apply_async(args=['1']) #CUMTD
    

@task(ignore_result=True)
def bussrImportAllData():
    filePath = os.path.abspath(os.path.dirname(__file__))
    sourcesFilePath = os.path.join(filePath, 'data_import/sources.json')
    sourceMappings = json.load(open(sourcesFilePath))['sources']
    for mapping in sourceMappings:
        print mapping
    pass

    
