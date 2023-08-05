# Copyright (c) 2004-2020 WUR, Wageningen
from __future__ import division
from .const import constants as const
from .gridenvelope2d import GridEnvelope2D;
from .basetiffraster import BaseTiffRaster
from libtiff import TIFF, libtiff
import numpy as np
import os
from math import floor, ceil, sqrt

__author__ = "Steven B. Hoek"

class TileTiffRaster(BaseTiffRaster, GridEnvelope2D):
    '''
    A raster represented by 2 files, with extensions 'tif' and 'tfw'
    This class can deal with tiff files of which the data are stored in tiles
    Different layers - e.g. RGB - are as planes: contiguously = chunky = interleaved
    or separately = per channel. More info: http://www.fileformat.info/format/tiff/egff.htm
    It means that the number of planes and the planar configuration determines the shape
    of the array written as bitmapped data, with dimensions image_depth, image_height, 
    image_width and samples. E.g. in the case of rgb and contiguous configuration, the last
    dimension of the array is expected to be 3 and the field samples per pixel will also be 3
    '''
    # Private attributes
    _const = None
    __mode = 'r'
    __datatype = const.FLOAT;
    currow = -1;
    __envelope = None;
    __image = None; # contains current strip
    __bits_per_sample = 8
    __sample_format = 1
    __samples_per_pixel = 1
    __numpy_type = np.uint8
    __itemsize = 1
    __layer_size = 1
    __tile_width = 1
    __tile_length = 1
    __ntiles = 1
    __nstrips = 1 
    
    def __init__(self, filepath, *datatype):
        # Initialise
        BaseTiffRaster.__init__(filepath)
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
    
    def set_numpy_type(self, atype):
        self.__numpy_type = atype
    
    def get_numpy_type(self):
        return self.datafile.get_numpy_type(self.__bits_per_sample, self.__sample_format)
    
    def open(self, mode, ncols=1, nrows=1, xll=0, yll=0, cellsize=100, nodatavalue=-9999.0, byteorder='II', compression=1):
        # Initialise
        super(TileTiffRaster, self).open(mode);
        
        # If file does not exist and mode[0] = 'w', create it!
        if (mode[0] == 'w'):
            self.__mode = mode
            self.datafile = TIFF.open(os.path.join(self.folder, self.name), mode='w');
            self.__envelope = GridEnvelope2D.__init__(self, ncols, nrows, xll, yll, cellsize, cellsize);
            self.datafile.SetField(self._const.IMAGE_WIDTH, ncols)
            self.datafile.SetField(self._const.IMAGE_LENGTH, nrows)
            self.datafile.SetField(self._const.BITS_PER_SAMPLE, self.__bits_per_sample)
            self.datafile.SetField(self._const.SAMPLE_PER_PIXEL, self.__samples_per_pixel)
            super(TileTiffRaster, self).set_extra_tags()
             
            # Data are organised into square tiles. Let each tile be about 8K bytes
            bits_per_pixel = self.__samples_per_pixel * self.__bits_per_sample
            pixels_per_tile = max(int(floor(8 * 8000 / bits_per_pixel)), 1)
            self.__tile_width = floor(sqrt(pixels_per_tile))
            self.__tile_length = self.__tile_width
            self.__ntiles = int(ceil(ncols / self.__tile_width) * ceil(nrows / self.__tile_length))
            self.__nstrips = int(self.ntiles / ceil(self.ncols / self.__tile_width))
            self.datafile.SetField(b"TileWidth", self.__tile_width)
            self.datafile.SetField(b"TileLength", self.__tile_length)
            self.datafile.SetField(self._const.PLANAR_CONFIG, 1) # contiguous
            self.datafile.SetField(self._const.ORIENTATION, 1)  # top left
            self.datafile.SetField(self._const.PAGE_NUMBER, 1, 1)
            self.datafile.SetField(self._const.FILL_ORDER, 1) # MSB2LSB
            self.datafile.SetField(self._const.COMPRESSION, compression)
            self.writeheader()
            shape = (self.__tile_length * self.ncols, self.__samples_per_pixel)
            self.__image = np.zeros(shape, self.__numpy_type)
            return True;
        else: 
            # Open the file as well as the header file
            if self.file_exists:            
                self.datafile = TIFF.open(os.path.join(self.folder, self.name), mode='r');
                self.readheader();
                
                # Check whether found values warrant further execution
                self.ncols = int(self.datafile.GetField(self._const.IMAGE_WIDTH))
                self.nrows = int(self.datafile.GetField(self._const.IMAGE_LENGTH))
                self.__tile_width = int(self.datafile.GetField("TileWidth"))
                self.__tile_length = int(self.datafile.GetField("TileLength"))
                self.__ntiles = libtiff.TIFFNumberOfTiles(self.datafile).value
                
                # Tiles can be joined to form strips: ceil(ncols / tile_width) in number, with height = tile_length
                # Those strips can be joined to form the image: ceil(nrows / tile_length) in number 
                msg = "Number of tiles not in accordance with tile and image dimensions!"
                self.__nstrips = int(ceil(self.nrows / self.__tile_length))
                num_tiles_per_strip = int(ceil(self.ncols / self.__tile_width))
                assert self.__ntiles == self.__nstrips * num_tiles_per_strip, msg
                planar_config = self.datafile.GetField(self._const.PLANAR_CONFIG)
                if (planar_config > 1):
                    raise NotImplementedError("Not yet able to deal with data organised in separate planes")
                
                if self.datafile.GetField(self._const.GDAL_NODATA) != None:
                    if self.__datatype == const.INTEGER:
                        self.nodatavalue = int(self.datafile.GetField(self._const.GDAL_NODATA))
                    else:
                        self.nodatavalue = float(self.datafile.GetField(self._const.GDAL_NODATA))
                super(TileTiffRaster, self).get_extra_tags()
                
                # Process further information from the header file
                self.xll = self.xul;
                if self.ycoords_sort == const.DESC:
                    self.yll = self.yul - self.nrows * self.dy;
                else:
                    self.yll = self.yul + self.nrows * self.dy; 
                    
                # Prepare to read the file (strip by strip and under the hood tile by tile)
                self.__bits_per_sample = self.datafile.GetField(self._const.BITS_PER_SAMPLE)
                self.__sample_format = self.datafile.GetField(self._const.SAMPLE_FORMAT)
                self.__samples_per_pixel = self.datafile.GetField(self._const.SAMPLE_PER_PIXEL)
                self.__numpy_type = self.datafile.get_numpy_type(self.__bits_per_sample, self.__sample_format)
                self.__itemsize = self.__bits_per_sample / 8
                shape = (self.__tile_length * self.ncols, self.__samples_per_pixel)
                self.__image = np.zeros(shape, self.__numpy_type)
                return True;
            else: return False;
    
    def get_tag(self, name):
        return self.datafile.get_tag_name(name)
    
    def next(self, parseLine=True):
        # Is it possible to proceed? Otherwise generate StopIteration
        result = None;
        self.currow += 1;
        try:
            if (self.currow >= self.nrows): raise StopIteration;
        
            # Read a new strip when necessary
            row_in_strip = self.currow % self.__tile_length # also zero-based!
            curstrip = int(floor(self.currow / self.__tile_length)) 
            if curstrip >= self.__nstrips: raise StopIteration;
            if row_in_strip == 0:
                # Are we dealing with one plane or with more? What configuratin?
                # self.datafile.GetField("PlanarConfig", 1)) 
                if curstrip == self.__nstrips-1:
                    # Last strip
                    length = self.nrows - self.__tile_length * curstrip
                    self.__layer_size = (self.ncols) * length * (self.__samples_per_pixel) * (self.__itemsize) 
                    self.__image = np.zeros((length, self.ncols, self.__samples_per_pixel), dtype=self.__numpy_type) 
                    #.resize((last_length, self.ncols, self.__samples_per_pixel)) 
                else:
                    length = self.__tile_length
                    self.__layer_size = (self.ncols) * length * (self.__samples_per_pixel) * (self.__itemsize) 
                    

                # Before trying to read, reset the buffer           
                self.__image.fill(0.0)
                self.__ReadStrip(curstrip, self.__image, int(self.__layer_size))
                self.__image = self.__image.reshape(length, self.ncols, self.__samples_per_pixel)
          
            # Read the next row
            result = self.__image[row_in_strip, :, 0]
            return result     
        except StopIteration:
            raise StopIteration;   
        except Exception as e:
            print(str(e))
    
    def writenext(self, sequence_with_data):
        raise NotImplementedError("Not implemented yet")
    
    def reset(self):
        self.currow = -1;  
    
    def __ReadStrip(self, strip, buf, size):
        result = False
        try:
            num_tiles_per_strip = int(ceil(self.ncols / self.__tile_width))
            numpy_type = self.datafile.get_numpy_type(self.__bits_per_sample, self.__sample_format)
            if (strip == self.__nstrips-1): 
                length = self.nrows - (strip*self.__tile_length)
            else:
                length = self.__tile_length
            buf = buf.reshape(length, self.ncols, self.__samples_per_pixel)
            for k in range(num_tiles_per_strip): 
                if (k == num_tiles_per_strip-1):
                    # We only need part of the tile because we are on the edge
                    width = self.ncols - (num_tiles_per_strip-1)*self.__tile_width
                else:
                    width = self.__tile_width
                tmp_buf = np.ascontiguousarray(np.zeros((self.__tile_length, self.__tile_width), numpy_type))
                seq = libtiff.TIFFReadTile(self.datafile, tmp_buf.ctypes.data, k*self.__tile_width, strip*self.__tile_length, 0, 0)
                if seq != None:
                    start = k*self.__tile_width
                    buf[0:length, start:start+width, 0] = tmp_buf[0:length, 0:width]
            result = True
        except Exception as e:    
            print(str(e))
        finally:
            return result
    
    def __WriteStrip(self,strip, buf, size):
        raise NotImplementedError("Not implemented yet")
    
    def close(self):
        if self.__mode[0] == 'w':
            self.datafile.WriteDirectory()
        super(TileTiffRaster, self).close()
    
    