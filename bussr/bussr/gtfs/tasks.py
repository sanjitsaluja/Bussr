from celery.decorators import task
from data_import.load import DataLoader
import os
import json

@task()
def add(x, y):
    logger = add.get_logger()
    logger.info('hello')
    return x + y



@task(ignore_result=True)
def gtfsImportSourceId(sourceId, onlyNew, cleanExistingData):
    logger = gtfsImportSourceId.get_logger()
    logger.info('Starting job gtfsImportSourceId {0}'.format(sourceId))
    dataLoader = DataLoader(onlyNew=onlyNew, sourceIdsToImport=[sourceId], cleanExistingData=cleanExistingData, logger=logger)
    dataLoader.performImport()
    logger.info('Completed job gtfsImportSourceId {0}'.format(sourceId))

@task(ignore_result=True)
def gtfsImportDev():
    # gtfsImportSourceId.apply_async(args=['1', True, False]) #CUMTD
    gtfsImportSourceId.apply_async(args=['4', True, False]) #Metra
    

@task(ignore_result=True)
def gtfsimportall():
    filePath = os.path.abspath(os.path.dirname(__file__))
    sourcesFilePath = os.path.join(filePath, 'data_import/sources.json')
    sourceMappings = json.load(open(sourcesFilePath))['sources']
    for mapping in sourceMappings:
        print mapping
    pass

    
