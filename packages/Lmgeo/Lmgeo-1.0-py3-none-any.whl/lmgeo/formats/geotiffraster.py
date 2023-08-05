# Copyright (c) 2004-2015 Alterra, Wageningen-UR
# Steven Hoek (steven.hoek@wur.nl), April 2015
from formats.gridenvelope2d import GridEnvelope2D;
from formats.raster import Raster
from math import fabs;
from formats.const import constants as const
import os;
from tifffile import memmap, TiffFile;
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False 

__author__ = "Steven B. Hoek"

class GeotiffRaster(Raster, GridEnvelope2D):
    "A raster represented by 2 files, with extensions 'tif' and 'tfw'"
    
    # Constants
    DATAFILEXT = "tif";
    HEADEREXT = "tfw"; # WORLD_EXT?
    __BYTESPERCELL = 4;
    #const.epsilon = 0.00000001;
    
    # Data attributes - assign some dummy values for the mean time
    name = "dummy.tif";
    folder = os.getcwd();
    nodatavalue = -9999.0;
    byteorder = 'II'; # Little endian
    roty = 0.0;
    rotx = 0.0;
    
    # Private attributes
    __datatype = const.FLOAT;
    #datafile = None;
    currow = -1;
    __envelope = None;
    __image = None;
    __memmappable = False;
    __memmap = None;
    
    def __init__(self, filepath, *datatype):
        # Initialise
        Raster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)
        
        # Retrieve the name from the filepath and assign - incl. extension
        self.name = os.path.basename(filepath);
        # Also derive the folder
        self.folder = os.path.dirname(filepath);
        # Finally set the datatype
        if len(datatype) > 0:
            if (datatype[0] == const.INTEGER): 
                self.__datatype = const.INTEGER;
            else: 
                self.__datatype = const.FLOAT; 
    
    def open(self, mode, ncols=1, nrows=1, xll=0, yll=0, cellsize=100, nodatavalue=-9999.0, byteorder='II'):
        # Initialise
        super(GeotiffRaster, self).open(mode);
        
        # If file does not exist and mode[0] = 'w', create it!
        if (mode[0] == 'w') and (not os.path.exists(self.folder + os.path.sep + self.name)):
            # We assume that no compression is needed
            if self.__datatype == const.FLOAT: dtype = 'float32'
            else: dtype = 'int32';
            self.__memmap = np.memmap(self.folder + os.path.sep + self.name, dtype, mode='w+', shape=(nrows, ncols))
            self.__envelope = GridEnvelope2D.__init__(self, ncols, nrows, xll, yll, cellsize, cellsize);
            return True;
        else: 
            # Open the file
            if os.path.exists(self.folder + os.path.sep + self.name):            
                self.datafile = TiffFile(self.folder + os.path.sep + self.name, multifile=False);
                if (mode[0] == 'w'):
                    # Assign the data attributes. TODO distinguish between dx and dy
                    dx = cellsize;
                    dy = cellsize; 
                    self.ncols = ncols;
                    self.nrows = nrows;                    
                    self.xul = xll;
                    if self.ycoords_sort == 'DESC':
                        self.yul = yll + nrows * dy;
                    else:
                        self.yul = yll - nrows * dy;
                    self.dx = dx;
                    self.dy = dy;
                    self.writeheader();
                else: 
                    # Retrieve some data attributes from the header file
                    self.readheader();
                    self.xll = self.xul;
                        
                    # Retrieve other ones from the TIFF file itself 
                    if self.datafile.byteorder == '<': self.byteorder = 'II';
                    else: self.byteorder = 'MM';
                    
                    # Get hold of the page 
                    if len(self.datafile.pages) > 1:
                        raise Warning('Unable to handle TIFF file with multiple pages!')
                    page = self.datafile.pages[0];
                    self.nrows = page.tags['ImageLength'].value;
                    self.ncols = page.tags['ImageWidth'].value;
                    try:
                        page = self.datafile.pages[0];
                        if 'GDAL_NODATA' in page.tags: self.nodatavalue = float(page.tags['GDAL_NODATA'].value);
                    except: pass;
                    
                    # Use memmap where possible, i.e. when ismemmappable is true
                    series = None
                    offset = None 
                    if len(self.datafile.series) == 0: raise Exception("No series found in TIFF file!")
                    else:
                        series = self.datafile.series[0]
                        offset = series.offset
                    self.__memmappable = page.is_memmappable or ((series is not None) and (offset is not None))
                    if not self.__memmappable:
                        self.__image = self.datafile.asarray();
                        if len(self.__image.shape) > 3:
                            raise ValueError("Not sure how to handle data with more than 3 dimensions!");
                    else:
                        self.datafile.close();
                        self.datafile = None;
                        self.__memmap = memmap(self.folder + os.path.sep + self.name, mode='r', offset=0);

                    # Check a few things, where appropriate
                    if not self.__memmappable:
                        #axes = self.datafile.series[0].axes;
                        #posx = axes.index('X')
                        #posy = axes.index('Y')
                        #posc = 3 - posx - posy
                        #self.ncols = self.__image.shape[posx]; 
                        #self.nrows = self.__image.shape[posy];
                        #if HAS_NUMPY:
                        #    self.__image = np.rollaxis(self.__image, posc, 1)
                        #else:
                        #    raise ImportError("Numpy not found on this system")
                        msg = "Data not properly dimensioned"
                        if not self.__image.shape[0] == self.nrows: raise Exception(msg)
                        if not self.__image.shape[1] == self.ncols: raise Exception(msg)
                        
                    # Calculate yll and find out the NODATA value
                    if self.ycoords_sort == 'DESC':
                        self.yll = self.yul - self.nrows * self.dy;
                    else:
                        self.yll = self.yul + self.nrows * self.dy; 
                    
                self.__envelope = GridEnvelope2D.__init__(self, self.ncols, self.nrows, self.xll, self.yll, self.dx, self.dy);
                return True;
            else: return False;
    
    def readheader(self):
        # header has 6 lines - without labels!
        sign = lambda x: (1, -1)[x<0];
        pos = str.rfind(str(self.name), "." + self.DATAFILEXT);
        if pos != -1: hdrFilename = self.name[0:pos] + "." + self.HEADEREXT
        else: raise ValueError("Invalid file name: " + self.name);
        if os.path.exists(self.folder + os.path.sep + hdrFilename):
            # Adapt the following so that it accounts also for rotated mapsheets
            hf = open(self.folder + os.path.sep + hdrFilename, 'r');
            hl = hf.readline();
            self.dx = float(hl.strip());
            hl = hf.readline();
            self.roty = float(hl.strip());
            hl = hf.readline();
            self.rotx = float(hl.strip());
            eps = 0.0001;
            if abs(self.rotx)>eps or abs(self.roty)>eps:
                raise NotImplementedError("Cannot handle rotated mapsheets yet!")
            hl = hf.readline();            
            self.dy = fabs(float(hl.strip()));
            if sign(float(hl.strip())) == 1.0: self.ycoords_sort = 'ASC';
            hl = hf.readline();
            self.xul = float(hl.strip()) - 0.5 * self.dx;
            hl = hf.readline();
            self.yul = float(hl.strip()) + 0.5 * self.dy;
            hf.close();
        else: 
            msg = "Header file " + hdrFilename + " not found in folder " + self.folder;
            raise IOError(msg);
        
    def next(self, parseLine=True):
        # Read the next row if possible, otherwise generate StopIteration
        result = None;
        try:
            self.currow += 1;
            if (self.currow >= self.nrows): raise StopIteration;
            if self.__memmappable:
                if parseLine:
                    result = self.__memmap[self.currow];
            else:
                if parseLine:
                    #if len(self.__image.shape) == 1:
                    result = self.__image[self.currow];  
                    #else:
                    #   result = self.__image[:, self.currow]
            return result     
        except:
            raise StopIteration; 
    
    def writeheader(self):
        # Write header file with all attributes 
        pos = str.rfind(str(self.name), "." + self.DATAFILEXT);
        if pos != -1: hdrFilename = self.name[0:pos] + "." + self.HEADEREXT
        else: raise ValueError("Invalid file name: " + self.name);
        try:
            # Open the file if it exists, otherwise create it
            hf = open(self.folder + os.path.sep + hdrFilename, 'w');
   
            # Now write all the attributes
            hf.write(str(self.dx) + "\n");
            eps = 0.0001;
            if abs(self.rotx)>eps or abs(self.roty)>eps:
                raise NotImplementedError("Cannot handle rotated mapsheets yet!")
            hf.write(str(self.rotx) + "\n");
            hf.write(str(self.roty) + "\n");
            if self.ycoords_sort == 'DESC':
                hf.write(str(self.dy) + "\n");
            else:
                hf.write(str(-1 * self.dy) + "\n");
            hf.write(str(self.xul + 0.5 * self.dx) + "\n");
            hf.write(str(self.yul + 0.5 * self.dy) + "\n");
        except Exception as e:
            msg = "Header file " + hdrFilename + " could not be written in folder " + self.folder;
            raise IOError(msg + "(" + str(e) + ")");
    
    def writenext(self, sequence_with_data):
        # Write the next data if possible, otherwise generate StopIteration
        # We cannot know whether exactly 1 row is included or not.
        # If there's no need for compression, use memmap
        self.__memmappable = True
        
                
    def reset(self):
        self.currow = -1;   
    
    def get_colormap(self):
        try:
            page = self.datafile.pages[0];
            return page.color_map
        except:
            print("Unable to get color map")
            
    def get_numpy_type(self):
        if HAS_NUMPY:
            result = np.int8
            if self.__image != None:
                result = self.__image.dtype
            return result
        else:
            ImportError("Numpy not found on this system")
            
    def close(self):
        super(GeotiffRaster, self).close();
        self.__memmap = None;
              