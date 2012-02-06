'''
Created on Jan 22, 2012

@author: sanjits
'''
import os
class CSVImporterBase(object):
    '''
    Base parser
    '''

    def __init__(self):
        self.verboseParse = True
        #self.verboseParse = (os.environ['VERBOSE_CSV_PARSE'] == 1)
        print 'Verbose import', self.verboseParse
            