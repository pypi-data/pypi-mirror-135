# Copyright (c) 2004-2020 WUR, Wageningen
from .gridenvelope2d import GridEnvelope2D;

__author__ = "Steven B. Hoek"

class Netcdf4Envelope2D(GridEnvelope2D):
    # Constants
    __X = 'lon';
    __Y = 'lat';
    TIME = 'time'
    
    # TODO: here the names for the dimensions are hardcoded, but they can be retrieved
    # from the netCDF4 file 
    def __init__(self, ds, X='lon', Y='lat'):
        # Initialise
        self.__X = X;
        self.__Y = Y;
        
        # Make sure you can call the __init__ method of the base class
        if ds != None:
            # Assume it's open; get hold of the dimensions and variables
            self.__dataset = ds;
            _dims = ds.dimensions;
            _vars = ds.variables;
            x_range = self._readRange(_vars[self.__X]);
            y_range = self._readRange(_vars[self.__Y]);
            
            # Now get the necessary properties for initialising an envelope object
            dx = GridEnvelope2D._getStep(x_range[0], x_range[1], len(_dims[self.__X]));
            dy = GridEnvelope2D._getStep(y_range[0], y_range[1], len(_dims[self.__Y]));
            xll = min(_vars[self.__X]) - 0.5*dx;
            yll = min(_vars[self.__Y]) - 0.5*dy;
            GridEnvelope2D.__init__(self, len(_dims[self.__X]), len(_dims[self.__Y]), xll, yll, dx, dy);
        
            # In some netCDF files the longitudes and latitudes are stored differently
            if _vars[self.__X][0] > _vars[self.__X][-1]: self.xcoords_sort = 'DESC';
            if _vars[self.__Y][0] < _vars[self.__Y][-1]: self.ycoords_sort = 'ASC';
    
    def _readRange(self, varxy):
        # Argument is either x or y
        minxy = min(varxy);
        maxxy = max(varxy);
        return [minxy, maxxy];
    
    def getDimension(self, ds): 
        result = 2;
        if ds != None:
            result = len(ds.dimensions.keys());
        return result;
    