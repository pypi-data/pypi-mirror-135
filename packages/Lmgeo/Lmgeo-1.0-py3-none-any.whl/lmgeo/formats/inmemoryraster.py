# Copyright (c) 2004-2020 WUR, Wageningen
from .gridenvelope2d import GridEnvelope2D;
from .raster import Raster
import numpy as np
from .const import constants as const

__author__ = "Steven B. Hoek"

class InMemoryRaster(Raster, GridEnvelope2D):
    '''
    A class with raster interface that is not based on a particular file format, but can rather
    keep data in memory in view of testing and operations that require more lines than only one
    '''
    # Data attributes
    data = None
    __datatype = None
    __open = False
    __nbands = 1 # default
    dataformat = 'f'

    def __init__(self, filepath, data=None, *datatype):
        # Initialise
        Raster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)

        if not data is None:
            self.data = data
        if len(datatype) > 0:
            if (datatype[0] == const.INTEGER): 
                self.__datatype = const.INTEGER;
                self.dataformat = 'i'
            else: 
                self.__datatype = const.FLOAT; 
                self.dataformat = 'f'
    
    def open(self, mode, ncols=1, nrows=1, nbands=1, xll=0.0, yll=0.0, cellsize=1.0, nodatavalue=-9999.0):
        super(InMemoryRaster, self).open(mode);
        self.__open = True
        if self.__datatype == const.INTEGER:
            dtype = np.int 
        else:
            dtype = np.float  
        self.__nbands = nbands 
        if mode[0] == 'w':
            # Writing mode
            if self.data is None: 
                self.data = np.zeros((nbands*nrows*ncols), dtype=dtype)    
            else:
                # Establish height and width
                if nbands == 1:
                    height = self.data.shape[0]
                    width = self.data.shape[1]
                else: 
                    height = self.data.shape[1]
                    width = self.data.shape[2]
                    
                # Now check that the data already has dimensions as indicated
                errmsg = "Shape of input data does not match given dimensions!"
                if height != nrows: 
                    raise Exception(errmsg)
                if (height > 0) and (width != ncols):
                    raise Exception(errmsg)
        else:
            # Reading mode
            if self.data == None: raise Exception("Memory was not initialised!")
            self.data = np.array(self.data, dtype=dtype)
            
        # Make sure that the data have the right shape
        self.data = self.data.flatten()
        if nbands == 1: 
            self.data.shape = (nrows, ncols)
        else: 
            self.data.shape = (nbands, nrows, ncols)
            
        # We need to also initialise the grid envelope
        self.xll = xll
        self.yll = yll
        self.dx = cellsize
        self.dy = cellsize
        self.cellsize = cellsize
        self.nodatavalue = nodatavalue
        GridEnvelope2D.__init__(self, ncols, nrows, self.xll, self.yll, self.dx, self.dy)
        return True;
    
    def next(self, parseLine=True):
        if not self.__open: raise Exception("Not yet fully initialised!") 
        self.currow += 1;
        if (self.currow > self.nrows): raise StopIteration;
        if parseLine:
            if self.__nbands == 1:
                return self.data[self.currow - 1, :]
            else:
                return self.data[:, self.currow - 1, :]
        else:
            return None
    
    def writenext(self, sequence_with_data):
        # Initialise
        self.currow += 1
        
        # Check a few things
        if not self.__open: raise Exception("Not yet fully initialised!")
        if (self.currow > self.nrows): raise StopIteration
        if self.__nbands == 1:
            width = len(sequence_with_data) 
        else:
            width = sequence_with_data.shape[1]
        if width != self.ncols:
            raise Exception("Attempt to assign line of wrong length!")
        
        # Assign the input line to the internal memory structure
        if self.__nbands == 1:
            self.data[self.currow - 1, :] = sequence_with_data
        else:
            self.data[:, self.currow - 1, :] = sequence_with_data
        return True
    