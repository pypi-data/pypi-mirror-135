from .raster import Raster
import os.path, sys
from libtiff.libtiff_ctypes import TIFFFieldInfo, TIFFDataType, FIELD_CUSTOM, add_tags
from .const import Const, constants as const
from math import fabs
#from itertools import zip
import numpy as np

__author__ = "Steven B. Hoek"

class BaseTiffRaster(Raster):
    # Data attributes - assign some dummy values for the mean time
    name = "";
    folder = os.getcwd();
    nodatavalue = -9999.0;
    byteorder = 'II'; # Little endian
    roty = 0.0;
    rotx = 0.0;
    pageNumber = [0, 1]
    modelPixelScale = [0.0, 0.0, 0.0]
    modelTiepoint = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ModelTransformation = 16 * [0.0]
    GeoKeyDirectory = 32 * [0]
    GeoDoubleParams = 1.0e-317
    GeoAsciiParams = "GCS_WGS_1984|"
    GdalMetadata = '<GDALMetadata>\n  <Item name="RepresentationType" sample="0">ATHEMATIC</Item>\n</GDALMetadata>'
        
    def __init__(self, filepath='', *datatype):
        # Check input
        if filepath == '':
            print('File path cannot be an empty string (method __init__).')
            
        # Initialise
        Raster.__init__(self, filepath)
        
        # Module wide constants
        self._const = Const()
        self._const.DATAFILEXT = "tif"
        self._const.WORLDEXT = "tfw"
        self._const.PAGE_NUMBER = b"PageNumber"
        self._const.IMAGE_WIDTH = "ImageWidth"
        self._const.IMAGE_LENGTH = "ImageLength"
        self._const.BITS_PER_SAMPLE = "BitsPerSample"
        self._const.SAMPLE_FORMAT = "SampleFormat"
        self._const.SAMPLE_PER_PIXEL = "SamplesPerPixel"
        self._const.PLANAR_CONFIG = "PlanarConfig"
        self._const.ORIENTATION = b"Orientation"
        self._const.FILL_ORDER = b"FillOrder"
        self._const.COMPRESSION = b"Compression"
        self._const.GDAL_NODATA = b"GDAL_NODATA"
        self._const.GDAL_METADATA = b"GDAL_METADATA"
        self._const.COLORMAP = b"ColorMap"
        self._const.PHOTOMETRIC = b"PhotoMetric"
        self._const.epsilon = 0.0001
        
        # Retrieve the name from the filepath and assign - incl. extension
        if filepath != "":
            if os.path.isdir(filepath):
                self.name = "dummy." + self._const.DATAFILEXT
                raise UserWarning("No filename given! IO from / to: %s" % self.name)
            else:
                self.name = os.path.basename(filepath)
            self.folder = os.path.dirname(filepath);
        else:
            self.name = "dummy." + self._const.DATAFILEXT
            self.folder = os.path.dirname(sys.argv[0])
            raise UserWarning("No path given! IO from / to: %s" % self.folder)
    
    def open(self, mode, ncols=1, nrows=1, xll=0.0, yll=0.0, cellsize=1.0, nodatavalue=-9999.0):
        super(BaseTiffRaster, self).open(mode)
        extra_tags = [
            TIFFFieldInfo(297, 2, 2, TIFFDataType.TIFF_SHORT, FIELD_CUSTOM, True, False, self._const.PAGE_NUMBER),          
            TIFFFieldInfo(33550, 3, 3, TIFFDataType.TIFF_DOUBLE, FIELD_CUSTOM, True, False, b"ModelPixelScaleTag"),
            TIFFFieldInfo(33922, 6, 6, TIFFDataType.TIFF_DOUBLE, FIELD_CUSTOM, True, False, b"ModelTiepointTag"),
            TIFFFieldInfo(34264, 16, 16, TIFFDataType.TIFF_DOUBLE, FIELD_CUSTOM, True, False, b"ModelTransformationTag"),
            TIFFFieldInfo(34735, 32, 32, TIFFDataType.TIFF_SHORT, FIELD_CUSTOM, True, False, b"GeoKeyDirectoryTag"),
            TIFFFieldInfo(34736, -1, -1, TIFFDataType.TIFF_DOUBLE, FIELD_CUSTOM, True, False, b"GeoDoubleParamsTag"),
            TIFFFieldInfo(34737, -1, -1, TIFFDataType.TIFF_ASCII, FIELD_CUSTOM, True, False, b"GeoAsciiParamsTag"),
            TIFFFieldInfo(42112, -1, -1, TIFFDataType.TIFF_ASCII, FIELD_CUSTOM, True, False, self._const.GDAL_METADATA),
            TIFFFieldInfo(42113, -1, -1, TIFFDataType.TIFF_ASCII, FIELD_CUSTOM, True, False, self._const.GDAL_NODATA)
        ]
        add_tags(extra_tags)
        
    def set_extra_tags(self):
        # The following is in view of the georeferencing
        self.datafile.SetField(self._const.PAGE_NUMBER, self.pageNumber)
        self.datafile.SetField(b"ModelPixelScaleTag", self.modelPixelScale) 
        self.datafile.SetField(b"ModelTiepointTag", self.modelTiepoint)
        self.datafile.SetField(b"ModelTransformationTag", self.ModelTransformation)
        self.datafile.SetField(b"GeoKeyDirectoryTag", self.GeoKeyDirectory)
        #self.datafile.SetField("GeoDoubleParamsTag", self.GeoDoubleParams)
        self.datafile.SetField(b"GeoAsciiParamsTag", str(self.GeoAsciiParams))
        self.datafile.SetField(self._const.GDAL_METADATA, str(self.GdalMetadata))
        
    def get_extra_tags(self):        
        # The following is in view of the georeferencing  
        self.pageNumber = self.datafile.GetField(self._const.PAGE_NUMBER)   
        self.modelPixelScale = self.datafile.GetField(b"ModelPixelScaleTag")
        self.modelTiepoint = self.datafile.GetField(b"ModelTiepointTag")
        self.ModelTransformation = self.datafile.GetField(b"ModelTransformationTag")
        self.GeoKeyDirectory = self.datafile.GetField(b"GeoKeyDirectoryTag")
        #self.GeoDoubleParams = self.datafile.GetField("GeoDoubleParamsTag")
        self.GeoAsciiParams = self.datafile.GetField(b"GeoAsciiParamsTag")
        self.GdalMetadata = self.datafile.GetField(self._const.GDAL_METADATA)
                
    def copy_extra_tags(self, rg):
        # Check input
        if not isinstance(rg, BaseTiffRaster):
            raise TypeError("Input is not a raster!")
        
        # Ok, go ahead
        if rg.pageNumber != None: self.pageNumber = rg.pageNumber
        self.modelPixelScale = rg.modelPixelScale
        self.modelTiepoint = rg.modelTiepoint
        if rg.ModelTransformation != None: self.ModelTransformation = rg.ModelTransformation
        self.GeoKeyDirectory = rg.GeoKeyDirectory
        #self.GeoDoubleParams = rg.GeoDoubleParams
        self.GeoAsciiParams = rg.GeoAsciiParams
        self.GdalMetadata = rg.GdalMetadata
        
    def readheader(self):
        # Header has 6 lines - without labels!
        # TODO rather use class WorldFile         
        sign = lambda x: (1, -1)[x<0];
        pos = str.rfind(str(self.name), "." + self._const.DATAFILEXT);
        if pos != -1: hdrFilename = self.name[0:pos] + "." + self._const.WORLDEXT
        else: raise ValueError("Invalid file name: " + self.name);
        if os.path.exists(os.path.join(self.folder, hdrFilename)):
            # Adapt the following so that it accounts also for rotated mapsheets
            hf = open(os.path.join(self.folder, hdrFilename), 'r');
            hl = hf.readline();
            self.dx = float(hl.strip());
            hl = hf.readline();
            self.roty = float(hl.strip());
            hl = hf.readline();
            self.rotx = float(hl.strip());
            eps = self._const.epsilon
            if abs(self.rotx)>eps or abs(self.roty)>eps:
                raise NotImplementedError("Cannot handle rotated mapsheets yet!")
            hl = hf.readline();            
            self.dy = fabs(float(hl.strip()));
            if sign(float(hl.strip())) == 1.0: self.ycoords_sort = const.ASC
            hl = hf.readline();
            self.xul = float(hl.strip()) - 0.5 * self.dx;
            hl = hf.readline();
            self.yul = float(hl.strip()) + 0.5 * self.dy;
            hf.close();
        else: 
            msg = "Header file " + hdrFilename + " not found in folder " + self.folder;
            raise IOError(msg);
                
    def writeheader(self):
        # Write header file with all attributes 
        pos = str.rfind(str(self.name), "." + self._const.DATAFILEXT);
        if pos != -1: hdrFilename = self.name[0:pos] + "." + self._const.WORLDEXT
        else: raise ValueError("Invalid file name: " + self.name);
        try:
            # Open the file if it exists, otherwise create it
            if os.path.exists(os.path.join(self.folder, hdrFilename)):
                hf = open(os.path.join(self.folder, hdrFilename), 'w');
            else:
                hf = open(os.path.join(self.folder, hdrFilename), 'w');
   
            # Now write all the attributes
            hf.write(str(self.dx) + "\n");
            eps = self._const.epsilon
            if abs(self.rotx)>eps or abs(self.roty)>eps:
                raise NotImplementedError("Cannot handle rotated mapsheets yet!")
            hf.write(str(self.rotx) + "\n");
            hf.write(str(self.roty) + "\n");
            if self.ycoords_sort == const.ASC:
                hf.write(str(self.dy) + "\n");
            else:
                hf.write(str(-1 * self.dy) + "\n");
            hf.write(str(self.xll + 0.5 * self.dx) + "\n");
            hf.write(str(self.yll + self.nrows * self.dy - 0.5 * self.dx) + "\n");
        except Exception as e:
            msg = "Header file " + hdrFilename + " could not be written in folder " + self.folder;
            raise IOError(msg + "(" + str(e) + ")");
        
    def get_colormap(self):
        return self.datafile.GetField(self._const.COLORMAP)
        
    def write_colormap(self, rgbTable=None, palette=None):
        # Palette is assumed to be a list with a length that is 3 times the no.
        # of colors, filled with r, g and b values alternating each other
        if palette != None:
            rgb_gen = zip(palette[0::3], palette[1::3], palette[2::3])
            cmap = list(rgb_gen)
            numcolors = 1 << self.__bits_per_sample
            rgbTable = np.zeros((3, numcolors), np.int)
            for k in range(len(cmap)):
                rgbTable[:, k] = cmap[k]
        else:
            if rgbTable == None:
                raise ValueError("No palette and no RGB table provided")
        self.datafile.SetField(self._const.PHOTOMETRIC, 3)
        self.datafile.SetField(self._const.COLORMAP, rgbTable)
