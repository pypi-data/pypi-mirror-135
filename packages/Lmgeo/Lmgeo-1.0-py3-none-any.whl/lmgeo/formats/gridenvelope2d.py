from .const import constants as const
import math

__author__ = "Steven B. Hoek"

# Helper class, to be used together with classes derived from Raster
class GridEnvelope2D(object):
    # Data attributes
    __nrows = 1;
    __ncols = 1;
    __xll = 0.0;
    __yll = 0.0;
    dx = 2.0;
    dy = 2.0;
    xcoords_sort = const.ASC;  # ascending
    ycoords_sort = const.DESC; # descending
    envelope = None

    # We define a grid by means of a number of rows, columns, 
    # a lower left corner as well as by steps in x and y direction
    def __init__(self, ncols, nrows, xll, yll, dx, dy):
        self.__ncols = ncols;
        self.__nrows = nrows;
        self.__xll = xll;
        self.__yll = yll;
        self.dx = dx;
        self.dy = dy;

    def getDimension(self): 
        return 2;

    # The following 4 functions are about the extent of the envelope    
    def getMinX(self):
        # X-coordinate of the lower left corner
        return self.__xll;
    
    def getMinY(self):
        # Y-coordinate of the lower left corner
        return self.__yll;
    
    def getMaxX(self):
        # X-coordinate of the upper right corner
        return self.__xll + self.__ncols * self.dx;
    
    def getMaxY(self):
        # Y-coordinate of the upper right corner
        return self.__yll + self.__nrows * self.dy;

    def getColAndRowIndex(self, x, y):
        # Return the zero-based row and column numbers of the grid cell
        # which houses the given point; count rows either from the bottom upwards (ASC)
        # or from the top downwards (DESC), depending on the way the coordinates are sorted
        eps = const.epsilon; # we'll use this constant to prevent negative indices
        if self.xcoords_sort == const.ASC:
            k = int(round((x - self.__xll - 0.5*self.dx + eps) / self.dx));
        else:
            k = int(round((self.getMaxX() - x - 0.5*self.dy + eps) / self.dy)); # TODO: check
        if self.ycoords_sort == const.ASC:
            i = int(round((y - self.__yll - 0.5*self.dy + eps) / self.dy));
        else:
            i = int(round((self.getMaxY() - y - 0.5*self.dy + eps) / self.dy)); # TODO: check
        return k, i;
    
    def getXandYfromIndices(self, k, i):
        # TODO implement also for xcoords_sort == 'DESC' and ycoords_sort == 'ASC'
        lon = float('inf');
        lat = float('inf');
        if self.xcoords_sort == const.ASC:
            lon = self.getMinX() + k*self.dx + 0.5*self.dx;
        if self.ycoords_sort == const.DESC:
            lat = self.getMaxY() - i*self.dy - 0.5*self.dy;
        return lon, lat;
        
    def getNearestCenterPoint(self, x, y):
        # Rows are counted from the top downwards
        k, i = self.getColAndRowIndex(x, y);
        if self.xcoords_sort == const.ASC:
            cx = self.__xll + (k + 0.5) * self.dx;
        else:
            cx = self.getMaxX() - (k + 0.5) * self.dx;
        if self.ycoords_sort == const.ASC:
            cy = self.__yll + (i + 0.5) * self.dy;
        else:
            cy = self.getMaxY() - (i + 0.5) * self.dy;
        return (cx, cy);
    
    def hasSameExtent(self, obj, epsilon=const.epsilon):
        # Check input
        if (not isinstance(obj, GridEnvelope2D)): 
            return False;
        if epsilon < 0:
            return False;
        
        # Now check the extent
        if self.__ncols != obj.ncols:
            return False;
        if self.__nrows != obj.nrows:
            return False;
        if abs(self.dy - obj.dy) > epsilon:
            return False;
        if abs(self.dx - obj.dx) > epsilon:
            return False;
        if abs(self.__xll - obj.xll) > epsilon:
            return False;
        if abs(self.__yll - obj.yll) > epsilon:
            return False;
        else:
            return True;        
    
    def compareSorting(self, obj):
        result = True;
        if (not isinstance(obj, GridEnvelope2D)): 
            result = False;
        if self.xcoords_sort != obj.xcoords_sort:
            result = False;
        if self.ycoords_sort != obj.ycoords_sort:
            result = False;
        return result; 
    
    @staticmethod
    def _getStep(mincoord, maxcoord, numcells):
        # Coordinates & number of cells either in X or in Y direction
        return math.ceil(maxcoord - mincoord) / numcells;
    
    def isWithinExtent(self, x, y):
        A = (x >= self.getMinX());
        B = (x <= self.getMaxX());
        C = (y >= self.getMinY());
        D = (y <= self.getMaxY());
        return (A and B and C and D);

    def get_envelope2d(self):
        return self;
    
    def get_area(self, i):
        # Assume that we're dealing with a lat lon reference system!
        # TODO implement for xcoords_sort != 'DESC'
        R = 6371
        result = 0
        if self.ycoords_sort == const.DESC:
            # Use an approximation to estimate the area of the cell in sq. kilometers
            # If it's possible to use a local coord. system, your result will be more accurate
            lat = self.getMaxY() - i*self.dy - 0.5*self.dy;
            height = self.dy * 2 * math.pi * R / 360.0
            width = height * math.cos(2 * math.pi * lat / 360.0)
            result = height * width
        else:
            raise Warning("Unexpected sorting of Y-coordinates")
        return result
    
    def getEnvelope(self):
        return GridEnvelope2D(self.__ncols, self.__nrows, self.__xll, self.__yll, self.cellsize, self.cellsize)
    
    @property
    def nrows(self):
        return self.__nrows
    
    @nrows.setter
    def nrows(self, nrows):
        self.__nrows = nrows
        
    @property
    def ncols(self):
        return self.__ncols
    
    @ncols.setter
    def ncols(self, ncols):
        self.__ncols = ncols
    
    @property
    def xll(self):
        return self.__xll
    
    @xll.setter
    def xll(self, xll):
        self.__xll = xll
        
    @property
    def yll(self):
        return self.__yll
    
    @yll.setter
    def yll(self, yll):
        self.__yll = yll   
    