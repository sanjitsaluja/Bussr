from django.contrib.gis.db import models

class Source(models.Model):
    class Meta:
        app_label = 'gtfs'
        
    importUrl = models.URLField()
    
    updated = models.DateField(auto_now=True)
    
    created = models.DateField(auto_now_add=True)
    
    dataDir = models.CharField(max_length=256)
    
    codeName= models.CharField(max_length=256)
    
    def __unicode__(self):
        return u'%s %s' % (self.codeName, self.dataDir)