import os.path
from math import fabs
from .raster import Raster
from .const import constants as const
import traceback

__author__ = "Steven B. Hoek"

# Helper class, to be used together with classes derived from Raster
# Reads and writes world files for those format which require it
class WorldFile(object):
    """A helper class ..."""
    datafile = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        try:
            if exc_type is not None:
                traceback.print_exception(exc_type, exc_value, tb)
                return False
            else:
                return True
        finally:
            if self.datafile is not None: self.datafile.close()
    
    def __getpath(self, aRaster):
        name_wo_ext = os.path.splitext(os.path.join(aRaster.folder, aRaster.name))[0] 
        result = os.path.normpath(os.path.join(name_wo_ext + "." + aRaster.getWorldFileExt()))
        return result
    
    def read(self, aRaster):
        try:
            if not isinstance(aRaster, Raster):
                raise ValueError("Not a valid Lmgeo raster!")
            path = self.__getpath(aRaster)
            self.datafile = open(path, 'r')
            line = self.datafile.readline()
            aRaster.dx = float(line.strip())
            line = self.datafile.readline();
            aRaster.roty = float(line.strip())
            line = self.datafile.readline()
            aRaster.rotx = float(line.strip())
            eps = 0.0001;
            if abs(aRaster.rotx)>eps or abs(aRaster.roty)>eps:
                raise NotImplementedError("Cannot handle rotated mapsheets yet!")
            line = self.datafile.readline()
            aRaster.dy = fabs(float(line.strip()))
            sign = lambda x: (1, -1)[x<0]
            if sign(float(line.strip())) == 1.0: aRaster.ycoords_sort = const.ASC;
            line = self.datafile.readline()
            aRaster.xul = float(line.strip()) - 0.5 * aRaster.dx
            line = self.datafile.readline()
            aRaster.yul = float(line.strip()) + 0.5 * aRaster.dy
            aRaster.xll = aRaster.xul
            aRaster.yll = aRaster.yul - (aRaster.nrows * aRaster.dy)
        except Exception as e:
            print(e)
            raise e
    
    def write(self, aRaster):
        try:
            if not isinstance(aRaster, Raster):
                raise ValueError("Not a valid Lmgeo raster!")
            path = self.__getpath(aRaster)

            # Open the file if it exists, otherwise create it
            self.datafile = open(path, 'w')
            
            # Now write all the attributes
            self.datafile.write(str(aRaster.dx) + "\n")
            eps = const.epsilon
            if abs(aRaster.rotx)>eps or abs(aRaster.roty)>eps:
                raise NotImplementedError("Cannot handle rotated mapsheets yet!")
            self.datafile.write(str(aRaster.rotx) + "\n")
            self.datafile.write(str(aRaster.roty) + "\n")
            if aRaster.ycoords_sort == const.ASC:
                self.datafile.write(str(aRaster.dy) + "\n")
            else:
                self.datafile.write(str(-1 * aRaster.dy) + "\n")
            self.datafile.write(str(aRaster.xll + 0.5 * aRaster.dx) + "\n")
            self.datafile.write(str(aRaster.yll + abs(aRaster.nrows) * aRaster.dy - 0.5 * aRaster.dx) + "\n")
            
        except Exception as e:
            print(e)
            raise e            