# -*- coding: latin-1 -*-
# Copyright (c) 2004-2021 WUR, Wageningen
"""StripLib - a Python library for extracting raster data in strips"""
from ..formats.gridenvelope2d import GridEnvelope2D
from ..formats.raster import Raster 
from ..formats.inmemoryraster import InMemoryRaster
from ..formats.const import constants as const

__author__ = "Steven B. Hoek"

class StripManager():
    '''
    Class that retrieves enough rows of data from a given raster grid to return a strip
    with a given number of rows - also as a raster grid
    '''
    # Default settings
    __depth = 1
    __currow = 0
    
    def __init__(self, rg, stripheight):
        '''
        Initialisation of the strip manager with strip height.  
        
        Input variables:
        rg - raster grid which serves as the source for the strip
        stripheight - height of the strip to be produced
        
        '''
        
        # Check the inputs
        if not isinstance(rg, Raster):
            raise TypeError("Input is not a raster!")
        if not isinstance(rg, GridEnvelope2D):
            raise TypeError("Input is not a grid envelope!")
       
        # Assume: rg is a raster grid with an open file at position 0
        self.__rg = rg
        self.__xll = rg.xll
        self.__yll = rg.yll
        self.__ncols = rg.ncols
        self.__nrows = rg.nrows
        if hasattr(rg, "nbands"):
            self.__nbands = rg.nbands
        else:
            self.__nbands = 1
        self.__currow = 0
        self.__depth = stripheight
        self.__datatype = rg.datatype
            
    def move(self, rowoffset):
        '''Skip lines, i.e. rowoffset in number'''
        if rowoffset < 0: raise ValueError("Row offset cannot be negative!")
        for i in range(rowoffset):
            try:
                line = self.__rg.next(False)
            finally:
                self.__currow += 1
        return True
    
    def __iter__(self):
        return StripIterator(self)
        
    def next(self, buffer=None, rowoverlap=0):
        '''
        Returns a strip with a number of rows, possibly with as first rows those in the buffer
        For the first strip, the buffer can be None and the rowoverlap > 0; for later rows,
        when the buffer contains rows, the rowoverlap can be left unspecified.
        '''
        result = None
        
        if self.__currow + self.__depth > self.__nrows:
            depth = self.__nrows - self.__currow
        else:
            depth = self.__depth
        if depth > 0: 
            # In case buffer contains rows, prepare to add them at the beginning of the output raster
            nbrows = 0
            if (not buffer is None): 
                if self.__nbands == 1:
                    nbrows = len(buffer)
                else:
                    nbrows = buffer.shape[1]
            else: depth += rowoverlap
            
            # Prepare a new InMemoryRaster which will be able to hold the needed data
            yll = self.__yll + (self.__nrows - self.__currow - depth) * self.__rg.dy
            imr = InMemoryRaster("dummy_file.ext", None, self.__datatype)
            imr.open('w', self.__ncols, nbrows + depth, self.__nbands, self.__xll, yll, self.__rg.dy, self.__rg.nodatavalue) 
            
            # If relevant, add the buffer rows first
            if self.__nbands == 1:
                for i in range(nbrows):
                    imr.writenext(buffer[i, :])
            else:
                for i in range(nbrows):
                    imr.writenext(buffer[:, i, :])
                                  
            # Retrieve enough lines from the source raster to fill the new InMemoryRaster
            for i in range(depth):
                try:
                    line = self.__rg.next()
                    imr.writenext(line)
                finally:
                    self.__currow += 1
            result = imr
        return result
    
    def close(self):
        self.__rg = None
        self.__initialised = False
        
    @property
    def stripheight(self):
        return self.__depth

    @stripheight.setter
    def stripheight(self, stripheight):
        self.__depth = stripheight
        
    @property
    def currow(self):
        return self.__currow
    
    @property
    def nrows(self):
        return self.__nrows
        
class StripIterator:
    ''' Class that actally makes sure that the StripManager is iterable'''
    def __init__(self, stripmanager):
        self.__stripmanager = stripmanager
    
    def __next__(self):
        result = None
        currow = self.__stripmanager.currow 
        height = self.__stripmanager.stripheight
        nrows = self.__stripmanager.nrows
        stripsleft = (nrows - currow) // height
        if stripsleft > 0:
            result = self.__stripmanager.next()
        else:
            raise StopIteration
        return result
            
    