# Copyright (c) 2004-2021 WUR, Wageningen
import os.path
import sys
sys.path.append("../lmgeo")
from lmgeo.formats.raster import Raster
from lmgeo.formats.gridenvelope2d import GridEnvelope2D
from lmgeo.formats.const import constants as const
from lmgeo.formats.worldfile import WorldFile
import numpy as np

try:
    from rasterio.windows import Window
    from rasterio.crs import CRS
    from rasterio.transform import Affine
    from rasterio.windows import Window
    import rasterio as rio
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False
    raise Exception("If one wants to use the module rioraster, he / she needs to install Python package rasterio!")
    
__author__ = "Steven B. Hoek"

class RioRaster(Raster, GridEnvelope2D):
    '''
    A raster that makes use of the rasterio package for access to various file formats, but 
    with an interface similar to the classes found in the formats folder of package lmgeo. 
    '''
    data = None    
    nbands = 1 # default
    datatype = 'i'
    __numpy_type = np.int
    __rows_per_strip = 128 # default for reading
    __number_of_strips = 1
    __currow = -1
    __crs = CRS.from_epsg(4326) # default
    __ext = "tif" # default

    def __init__(self, filepath, *datatype):
        '''Initialisation of a RioRaster instance
        
        Input variables:
        filepath - full path to the file
        datatype - e.g. integer or float, indicated as 'i' or 'f' repectively
        '''
        Raster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)
        
        # Process input
        if filepath == '':
            print('File path cannot be an empty string (method __init__).')
        self.name = os.path.basename(filepath);
        self.folder = os.path.dirname(filepath);
        self.datatype = datatype[0]                           

    # overrides same method of Raster
    def getWorldFileExt(self):
        result = 'tfw' # default
        extensions = [".jpg", ".png", ".gif", ".bmp"]
        if self.__ext in extensions:
            idx = extensions.index(self.__ext)
            result = ["jgw", "pgw", "gfw", "bpw"][idx]
        return result 

    def open(self, mode, ncols=1, nrows=1, nbands=1, xll=0, yll=0, cellsize=100, nodatavalue=-9999.0):
        '''After the instance has been initialised, it might be necessary to specify the size of the
        raster grid, the size of the cells. This is esp. true in the case of write mode: mode == 'w'.
        
        Input variables:
        mode - read ('r') or write ('w')
        ncols - number of columns of the raster grid
        nrows - number of rows of the raster grid
        nbands - number of bands
        xll - x-coordinate of the lower left point
        yll - y-coordinate of the lower left point
        cellsize - cell size
        nodatavalue - value used to indicate that there are no data for that cell 
        '''
        # Initialise
        fn = os.path.join(self.folder, self.name)
        
        # Raise error again if Python package rasterio is not installed
        if not HAS_RASTERIO:
            raise Exception("If one wants to use the module rioraster, he / she needs to install Python package rasterio!")
        
        # Now prepare to read from file or to write it
        if (mode[0] == 'w'):
            # Get the driver name - see also https://gdal.org/drivers/raster/index.html
            self.__ext = os.path.splitext(fn)[1]
            drivers = {".tif": 'GTiff', '.asc':'AAIGrid', '.nc4':'netCDF', '.img':'HFA', '.map':'PCRaster'}
            if self.__ext in drivers: 
                driver = drivers[self.__ext]
            else:
                driver = self.__ext.lstrip('.').upper()
                
            # Get the datatype
            if self.datatype == const.BYTE:
                dtype = "byte"
            elif self.datatype == const.UINT8:
                dtype = "uint8"
            elif  self.datatype == const.SHORT:
                dtype = "short"
            elif self.datatype == const.UINT16:
                dtype = "uint16"
            elif self.datatype == const.UINT32:
                dtype = "uint32"
            elif self.datatype == const.INTEGER:
                dtype = "int32"
            elif self.datatype == const.FLOAT:
                dtype = "float"
            elif self.datatype == const.DOUBLE:
                dtype = "double"
            
            # Idea is to write 16 lines at once
            self.ncols = ncols
            self.nrows = nrows
            self.nbands = nbands
            self.xll = xll
            self.yll = yll
            self.dx = cellsize
            self.dy = cellsize
            self.nodatavalue = nodatavalue
            yul = self.yll + self.nrows * self.dy
            self.__rows_per_strip = 16 # default for writing
            numblocks = (1 + self.ncols // 16)
            if self.nbands == 1:
                self.data = np.empty((self.__rows_per_strip, ncols), dtype=dtype)
            else:
                self.data = np.empty((self.nbands, self.__rows_per_strip, ncols), dtype=dtype)
            self.data.fill(nodatavalue)
            
            # Prepare a profile and then open the TIFF file for writing
            # TODO: make this suitable for more other coordinate reference systems
            with rio.Env():
                profile = {'driver': driver, 'dtype': dtype, 'nodata': nodatavalue, 'width': ncols, 'height': nrows, \
                       'count': nbands, 'crs': self.__crs, 'transform': Affine(cellsize, 0.0, xll, 0.0, -1*cellsize, yul), \
                       'blockxsize':  numblocks * 16, 'blockysize': self.__rows_per_strip , 'tiled': False, 'compress': 'lzw', \
                       'interleave': 'band'}
            src = rio.open(fn, 'w', **profile)
            self.datafile = src 
            
            # Write a matching world file
            if self.__ext in [".jpg", ".png", ".gif", ".bmp"]:
                with WorldFile() as wf:
                    wf.write(self)
            
        else:
            src = rio.open(fn, 'r')
            self.datafile = src
            if "width" in src.meta: 
                self.ncols = src.meta["width"]
            if "height" in src.meta: 
                self.nrows = src.meta["height"]
            if "count" in src.meta:
                self.nbands = src.meta["count"]
            if "crs" in src.meta:
                self.__crs = src.meta["crs"]
            if "nodata" in src.meta:
                self.nodatavalue = src.meta["nodata"]
            if ("transform" in src.meta) and (not src.meta["transform"] is None):
                transform = src.meta["transform"]
                self.dx = transform[0]
                self.dy = -1 * transform[4]
                self.xll = transform[2]
                self.yll = transform[5] - self.nrows * self.dy
                self.rotx = transform[3] 
                self.roty = transform[1]
                
            # Try to find out the datatype
            if "dtype" in src.meta:
                if src.meta["dtype"] == "byte":
                    self.datatype = const.BYTE
                    self.__numpy_type = np.byte
                elif src.meta["dtype"] == "uint8":
                    self.datatype = const.UINT8
                    self.__numpy_type = np.uint8
                elif src.meta["dtype"] == "short":
                    self.datatype = const.SHORT 
                    self.__numpy_type = np.short    
                elif src.meta["dtype"] == "uint16": 
                    self.datatype = const.UINT16
                    self.__numpy_type = np.uint16 
                elif src.meta["dtype"] == "int16":
                    self.datatype = const.INTEGER
                    self.__numpy_type = np.int
                elif src.meta["dtype"] == "uint32":
                    self.datatype = const.UINT32 
                    self.__numpy_type = np.uint32
                elif src.meta["dtype"] == "float":
                    self.datatype = const.FLOAT 
                    self.__numpy_type = np.float32
                elif src.meta["dtype"] == "double":
                    self.datatype = const.DOUBLE
                    self.__numpy_type = np.float64
                    
            if src.meta["transform"] is None:
                with WorldFile() as wf:
                    wf.read(self) 
                    
            # Depending on the image format and other characteristics
            # decide how many rows should be retrieved at a time from disk            
            if hasattr(src, "profiles") and "blockysize" in src.profiles:
                self.__rows_per_strip = src.profiles["blockysize"]
            self.__number_of_strips = 1 + (self.nrows // self.__rows_per_strip)
            
        return True
    
    def next(self, parseLine=True):
        # Is it possible to proceed? Otherwise generate StopIteration
        result = None;
        self.__currow += 1
        try:
            if (self.__currow >= self.nrows): raise StopIteration
            
            # Read a new strip when necessary
            row_in_strip = self.__currow % self.__rows_per_strip # zero-based
            curstrip = self.__currow // self.__rows_per_strip    # zero-based
            if (curstrip >= self.__number_of_strips): raise StopIteration
            if row_in_strip == 0:
                src = self.datafile
                nrows = min(self.__rows_per_strip, self.nrows - self.__currow)
                
                # We read only part of the image at the time
                if self.nbands == 1:
                    self.data = src.read(1, window=Window(0, self.__currow, self.ncols, nrows))
                else:
                    self.data = src.read(window=Window(0, self.__currow, self.ncols, nrows))
                            
            if parseLine:
                # Extract the next row
                if self.nbands == 1:
                    result = self.data[row_in_strip, :]
                else:
                    result = self.data[:, row_in_strip, :]
        except StopIteration:
            raise StopIteration;   
        except Exception as e:
            print(str(e))
        finally:
            return result
        
    def writenext(self, sequence_with_data):
        # Initialise
        self.__currow += 1
        row_in_strip = self.__currow % self.__rows_per_strip # zero-based
        curstrip = self.__currow // self.__rows_per_strip # zero-based!
        
        # Now let's see what we can do
        A = (self.__currow != 0) and (row_in_strip == 0) # previous strip is ready: can be written to disk
        B = (self.__currow == self.nrows - 1) # very last strip still has to be written
        if A:
            # Prepare to write the complete strip that is ready
            ioffset = (-1 + curstrip) * self.__rows_per_strip
            height = self.__rows_per_strip
            
            # Write the data to file and prepare for the next loop
            self.__writestrip(ioffset, height)
            self.data.fill(self.nodatavalue)
            
        if B:  
            # Prepare the very last strip of the raster
            ioffset = curstrip * self.__rows_per_strip
            height = self.nrows - (curstrip * self.__rows_per_strip)
                
            # Now we assign the last data and then we write
            if self.nbands == 1:
                self.data[row_in_strip, :] = sequence_with_data
                self.data = self.data[0:height, :]
            else:
                self.data[:, row_in_strip, :] = sequence_with_data
                self.data = self.data[:, 0:height, :]
            self.__writestrip(ioffset, height)
        else:
            # We have not yet reached the end of the raster - update the data
            if self.nbands == 1:
                self.data[row_in_strip, :] = sequence_with_data
            else:
                self.data[:, row_in_strip, :] = sequence_with_data
                
    def __writestrip(self, ioffset, height):
        # Write the data to file and prepare for the next loop
        mywindow = Window(col_off=0, row_off=ioffset, width=self.ncols, height=height)
        if self.nbands == 1:
            self.datafile.write(self.data, window=mywindow, indexes=1)
        else:
            if height == 1: self.data = np.reshape(self.data, (self.nbands, 1, self.ncols))
            self.datafile.write(self.data, window=mywindow)
        self.data.fill(self.nodatavalue)
    
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
        self.__currow = -1 
        
    @property
    def crs(self):
        return self.__crs

    @crs.setter
    def crs(self, crs):
        # TODO: differentiate dx and dy!
        self.__crs = crs