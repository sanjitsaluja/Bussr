from django.contrib.gis.db import models

class Source(models.Model):
    '''
    Model object representing an import source
    '''
    class Meta:
        app_label = 'gtfs'
        
    sourceId = models.CharField(max_length=128, primary_key=True)
       
    '''
    Url of the gtfs zip.
    ''' 
    importUrl = models.URLField()
    
    '''
    Date when the gtfs data source was last imported
    '''
    updated = models.DateField(auto_now=True)
    
    '''
    Date when the gtfs data source was first imported
    '''
    created = models.DateField(auto_now_add=True)
    
    '''
    @todo: What is this?
    '''
    dataDir = models.CharField(max_length=1024)
    
    '''
    Data source code name
    '''
    codeName= models.CharField(max_length=256)
    
    def __unicode__(self):
        return u'%s %s' % (self.codeName, self.dataDir)