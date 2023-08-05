# Copyright (c) 2004-2020 WUR, Wageningen
from .const import constants as const
import os;

__author__ = "Steven B. Hoek"

# Abstract base class
class Raster(object):
    # Attributes
    datafile = None
    name = "dummy";
    folder = os.getcwd();
    nodatavalue = -9999.0;
    cellsize = 1;
    currow = 0
    roty = 0.0
    rotx = 0.0  
    file_exists = False
    
    def __init__(self, filepath):
        self.file_exists = os.path.exists(filepath)

    def open(self, mode, ncols=1, nrows=1, xll=0.0, yll=0.0, cellsize=1.0, nodatavalue=-9999.0):
        pass
    
    def readheader(self):
        pass

    def writeheader(self):
        pass
    
    def __iter__(self):
        return self; 
    
    def next(self, parseLine=True):
        pass

    def writenext(self, sequence_with_data):
        # input is sequence type - e.g. list, array.array or numpy.array
        pass
    
    @staticmethod
    def getDataFileExt(self):
        result = "xxx"
        if self != None and hasattr(self, "_const"):
            result = self._const.DATAFILEXT
        return result
    
    @staticmethod
    def getHeaderFileExt(self):
        return const.HEADEREXT 
    
    def getWorldFileExt(self):
        return const.WORLDFILEXT   
    
    def close(self):
        try:
            if self.datafile:
                if hasattr(self.datafile, 'closed'):
                    if not self.datafile.closed:
                        self.datafile.close()
                else:
                    self.datafile.close()
        except Exception as e:
            print(e)

    def reset(self):
        self.currow = 0; 
        
    # TODO: Raster and GridEnvelope2D are often used together; both have dx and dy, so this causes ambiguity!
    @property
    def dx(self):
        return self.cellsize

    @dx.setter
    def dx(self, dx):
        self.cellsize = dx
        
    @property
    def dy(self):
        # TODO: differentiate dx and dy!
        return self.cellsize

    @dy.setter
    def dy(self, dy):
        # TODO: differentiate dx and dy!
        self.cellsize = dy
    