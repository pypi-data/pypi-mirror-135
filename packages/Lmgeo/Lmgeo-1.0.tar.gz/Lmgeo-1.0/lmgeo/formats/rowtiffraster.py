# Copyright (c) 2004-2020 WUR, Wageningen
from __future__ import division
from .const import constants as const
from .gridenvelope2d import GridEnvelope2D;
from .basetiffraster import BaseTiffRaster
from libtiff import TIFF
import numpy as np
import os

# TODO Python library pytiff may work better than libtiff. The problem is that it is difficult 
# if not impossible at this moment to install / run it on Windows. Let's hope this will be solved
# in the near future. If it is, then switch to pytiff.

__author__ = "Steven B. Hoek"

class RowTiffRaster(BaseTiffRaster, GridEnvelope2D):
    "A raster represented by 2 files, with extensions 'tif' and 'tfw'"
    "This class can ONLY deal with tiff files which have 1 row per strip"
    "Different layers - e.g. RGB - are as planes: contiguously = chunky = interleaved"
    "or separately = per channel. More info: http://www.fileformat.info/format/tiff/egff.htm"
    "It means that the number of planes and the planar configuration determines the shape"
    "of the array written as bitmapped data, with dimensions image_depth, image_height, "
    "image_width and samples. E.g. in the case of rgb and contiguous configuration, the last"
    "dimension of the array is expected to be 3 and the field samples per pixel will also be 3"
    # Private attributes
    _const = None
    __mode = 'r'
    __datatype = const.FLOAT;
    currow = -1;
    __envelope = None;
    __bits_per_sample = 8
    __sample_format = 1
    __samples_per_pixel = 1
    __numpy_type = np.uint8
    __itemsize = 1
    __layer_size = 1
    
    # Predefine __ReadStrip with a dummy function
    def dummy(self, *args): pass;
    __ReadStrip = dummy(0, 0, 1)
    __WriteStrip = dummy(0, 0, 1)

    def __init__(self, filepath='', *datatype):
        # Check input
        if filepath == '':
            print('File path cannot be an empty string (method __init__).')
            
        # Initialise
        BaseTiffRaster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)
        if self._const == None:
            raise AttributeError("TIFF raster not properly initialised!")
        
        # Finally set the datatype
        if len(datatype) > 0:
            if (datatype[0] == const.INTEGER): 
                self.__datatype = const.INTEGER;
            else: 
                self.__datatype = const.FLOAT; 
                
    def __get_sample_format(self, arr):
        result = None
        
        # Not considered: SAMPLEFORMAT_VOID=4 and SAMPLEFORMAT_COMPLEXINT=5
        if arr.dtype in np.sctypes['float']:
            result = 3 #SAMPLEFORMAT_IEEEFP
        elif arr.dtype in np.sctypes['uint']+[np.bool]:
            result = 1 #SAMPLEFORMAT_UINT
        elif arr.dtype in np.sctypes['int']:
            result = 2 #SAMPLEFORMAT_INT
        elif arr.dtype in np.sctypes['complex']:
            result = 6 #SAMPLEFORMAT_COMPLEXIEEEFP
        else:
            raise NotImplementedError(arr.dtype)
        return result
    
    def set_numpy_type(self, mytype):
        self.__numpy_type = mytype
    
    def get_numpy_type(self):
        return self.datafile.get_numpy_type(self.__bits_per_sample, self.__sample_format)
    
    def open(self, mode, ncols=1, nrows=1, xll=0, yll=0, cellsize=100, nodatavalue=-9999.0, byteorder='II', compression=1):     
        # Initialise
        super(RowTiffRaster, self).open(mode);
        
        # If file does not exist and mode[0] = 'w', create it!
        if (mode[0] == 'w'):
            self.__mode = mode
            self.datafile = TIFF.open(os.path.join(self.folder, self.name), mode='w');
            self.__envelope = GridEnvelope2D.__init__(self, ncols, nrows, xll, yll, cellsize, cellsize);
            self.datafile.SetField(self._const.IMAGE_WIDTH, ncols)
            self.datafile.SetField(self._const.IMAGE_LENGTH, nrows)
            self.datafile.SetField(self._const.BITS_PER_SAMPLE, self.__bits_per_sample)
            self.datafile.SetField(self._const.SAMPLE_PER_PIXEL, self.__samples_per_pixel)
            self.datafile.SetField("RowsPerStrip", 1)
            self.datafile.SetField(self._const.PLANAR_CONFIG, 1) # contiguous
            self.datafile.SetField(self._const.ORIENTATION, 1)  # top left
            self.datafile.SetField(self._const.PAGE_NUMBER, (0, 1))
            self.datafile.SetField(self._const.FILL_ORDER, 1) # MSB2LSB
            self.datafile.SetField(self._const.COMPRESSION, compression)
            super(RowTiffRaster, self).set_extra_tags()
            
            # Prepare to write per strip
            if compression == 1: # none
                self.__WriteStrip = self.datafile.WriteRawStrip
            else:
                self.__WriteStrip = self.datafile.WriteEncodedStrip
            self.writeheader()
            return True;
        else: 
            # Open the file as well as the header file
            if self.file_exists:            
                self.datafile = TIFF.open(os.path.join(self.folder, self.name), mode='r');
                self.readheader();
                
                # Check whether found values warrant further execution
                self.ncols = int(self.datafile.GetField(self._const.IMAGE_WIDTH))
                self.nrows = int(self.datafile.GetField(self._const.IMAGE_LENGTH))
                rows_per_strip = self.datafile.GetField("RowsPerStrip")
                if (rows_per_strip == None) :
                    msg = "Image file does not store data with 1 row per strip. This class is unable to handle this"
                    raise ValueError(msg) 
                if int(rows_per_strip) > 1:
                    msg = "Image file stores data with more than 1 row per strip. This class is unable to handle this"
                    raise ValueError(msg)
                
                # Process further information from the header file
                self.xll = self.xul;
                if self.ycoords_sort == const.DESC:
                    self.yll = self.yul - self.nrows * self.dy;
                else:
                    self.yll = self.yul + self.nrows * self.dy; 
                    
                # Prepare to read the file
                self.__bits_per_sample = self.datafile.GetField(self._const.BITS_PER_SAMPLE)
                self.__sample_format = self.datafile.GetField(self._const.SAMPLE_FORMAT)
                self.__samples_per_pixel = self.datafile.GetField(self._const.SAMPLE_PER_PIXEL)
                self.__numpy_type = self.datafile.get_numpy_type(self.__bits_per_sample, self.__sample_format)
                self.__itemsize = self.__bits_per_sample / 8
                self.__layer_size = self.ncols * self.__samples_per_pixel * self.__itemsize

                if self.datafile.GetField(self._const.GDAL_NODATA) != None:
                    if self.__datatype == const.INTEGER:
                        self.nodatavalue = int(self.datafile.GetField(self._const.GDAL_NODATA))                    
                    else:
                        self.nodatavalue = float(self.datafile.GetField(self._const.GDAL_NODATA))
                else:
                    if self.__datatype == const.INTEGER:
                        self.nodatavalue = int(self.nodatavalue)  
                super(RowTiffRaster, self).get_extra_tags()

                if self.datafile.GetField(self._const.COMPRESSION) == 1: # none
                    self.__ReadStrip = self.datafile.ReadRawStrip
                else:
                    self.__ReadStrip = self.datafile.ReadEncodedStrip  
                return True;
            else: return False;
    
    def next(self, parseLine=True):
        # Is it possible to proceed? Otherwise generate StopIteration
        self.currow += 1;
        if (self.currow > self.nrows): raise StopIteration;
        if (self.currow > int(self.datafile.NumberOfStrips())): raise StopIteration;
        
        # Read the next row
        buf = np.zeros((self.ncols, self.__samples_per_pixel), self.__numpy_type)
        self.__ReadStrip(self.currow, buf.ctypes.data, int(self.__layer_size))
        return buf      
    
    def writenext(self, sequence_with_data):
        # Write the next data if possible, otherwise generate StopIteration
        # We cannot know whether exactly 1 row is included or not.
        # Is it possible to proceed? Otherwise generate StopIteration
        if self.currow == -1:
            sample_format = self.__get_sample_format(sequence_with_data)
            self.datafile.SetField(self._const.SAMPLE_FORMAT, sample_format)
        self.currow += 1;
        if (self.currow > self.nrows): raise StopIteration;
        if (self.currow > int(self.datafile.NumberOfStrips())): raise StopIteration;
        
        # Ok, try to write the data
        try:
            #data_sequence = np.ascontiguousarray(sequence_with_data)
            size = self.ncols * self.__samples_per_pixel * sequence_with_data.itemsize
            if len(sequence_with_data.shape) == 1 or sequence_with_data.shape[1] == 1:
                self.__WriteStrip(self.currow, sequence_with_data.ctypes.data, int(size))
            else:
                size = size * sequence_with_data.shape[0]
                sequence_with_data = np.ascontiguousarray(sequence_with_data)
                self.__WriteStrip(self.currow, sequence_with_data.ctypes.data, int(size))
            
            return True
        except StopIteration:
            raise StopIteration
        except ValueError as e:
            print(str(e))
            raise ValueError
        except Exception as e:
            raise IOError(str(e)); 
        
    def reset(self):
        self.currow = -1;  
    
    def close(self):
        try:
            if self.__mode[0] == 'w':
                self.datafile.WriteDirectory()
        except Exception as e:
            print(e)
        finally:
            super(RowTiffRaster, self).close()
        