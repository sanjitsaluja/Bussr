from celery.decorators import task
from data_import.load import DataLoader

@task()
def add(x, y):
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
    gtfsImportSourceId('1', onlyNew=True, cleanExistingData=False).apply_async() #Metra
    gtfsImportSourceId('4', onlyNew=True, cleanExistingData=False).apply_async() #CUMTD

@task(ignore_result=True)
def gtfsimportall():
    pass


