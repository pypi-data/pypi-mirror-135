# Copyright (c) 2004-2021 WUR, Wageningen
import png
from .const import Const, constants as const
from .raster import Raster
from .gridenvelope2d import GridEnvelope2D;
import os
import zlib
from struct import unpack
from array import array
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    
__author__ = "Steven B. Hoek"

recon = None

class PngRaster(Raster, GridEnvelope2D):
    """A raster represented by a binary file - with extension 'png'. """
    """Support for interlacing is not envisaged!                     """
    __mode      = 'r'
    dataformat  = 'i'
    nbands      = 1 # default
    reader      = None
    writer      = None
    iter        = None # default
    nplanes      = 1
    chunksize   = 1
    chunkwise   = True
    curchunk    = None
    posinchunk  = 0
    compression = None
        
    def __init__(self, filepath, *datatype):
        global recon 
        
        # Check input
        if filepath == '':
            print('File path cannot be an empty string (method __init__).')

        # Module wide constants
        self._const = Const()
        self._const.FILEXT = "png"
        recon = None

        # Already assign whay is obvious
        self.name = os.path.basename(filepath)
        self.folder = os.path.dirname(filepath)

    def open(self, mode, ncols=1, nrows=1, nbands=1, xll=0.0, yll=0.0, cellsize=1.0, nodatavalue=-9999.0, **kwargs):
        filepath = os.path.join(self.folder, self.name)
        if mode[0] == 'r':
            # Retrieve all metadata
            reader = png.Reader(filepath)
            reader.preamble()
            
            # Check input further
            signature = str(reader.signature)
            try:
                signature.index('89PNG')
            except ValueError:
                raise ValueError("File %s is not a valid PNG file!" % self.name)
            if reader.interlace:
                raise ValueError("Interlaced images are not supported!")
            self.__nrows = reader.height
            self.__ncols = reader.width
            self.nbands  = reader.planes
            if (not reader.atchunk is None) and (len(reader.atchunk) > 0):
                self.chunksize = reader.atchunk[0]
            if not reader.transparent is None:
                self.nodatavalue = reader.transparent[0]
            self.compression = reader.compression
            self.reader = reader 
            
            if "chunkwise" in kwargs.keys():
                idx = list(kwargs.keys()).index("chunkwise")
                self.chunkwise = bool(list(kwargs.values())[idx])
            
            if not self.chunkwise:
                # We'll have the image read from file in one go
                ptr = reader.asDirect()
                info = ptr[3]
                if isinstance(info, dict) and ("planes" in info.keys()): 
                    self.nplanes = info["planes"]
                    self.iter = ptr[2] # rows
            
        elif mode[0] == 'w':
            # Process input
            self.__ncols = ncols
            self.__nrows = nrows
            self.cellsize = cellsize
            self.dx = cellsize
            self.dy = cellsize
            self.nodatavalue = nodatavalue
            
            # Also use the input to create a Writer object
            writer = png.Writer(width=ncols, height=nrows, greyscale=True, transparent=nodatavalue, bitdepth=16, compression=0, interlace=False, colormap=None)
            self.writer = writer
      
            # Already write a few chunks with the above specified data
            writer.write_preamble(filepath)
        return True
    
    # TODO: adapt
    def get_straight_packed(self, byte_blocks):
        """Iterator that undoes the effect of filtering; returns each row as a sequence of packed bytes.
        Assumes input is straightlaced. `byte_blocks` should be an iterable that yields the raw bytes
        in blocks of arbitrary size.
        """
        global recon

        # length of row, in bytes
        rb = self.reader.row_bytes
        a = bytearray()
        
        # The previous (reconstructed) scanline.
        # None indicates first line of image.
        for some_bytes in byte_blocks:
            a.extend(some_bytes)
            while len(a) >= rb + 1:
                filter_type = a[0]
                scanline = a[1: rb + 1]
                del a[: rb + 1]
                recon = self.reader.undo_filter(filter_type, scanline, recon)
                return recon
        if len(a) != 0:
            # :file:format We get here with a file format error:
            # when the available bytes (after decompressing) do not
            # pack into exact rows.
            raise png.FormatError('Wrong size for decompressed IDAT chunk.')
        assert len(a) == 0
    
    def next(self, parseLine=True):
        result = None
        
        if not self.chunkwise:
            # The image is stored in memory - get 1 row
            try:
                pngdata = self.iter.__next__()
                image_2d = np.vstack(pngdata)
                image_2d = np.reshape(image_2d, (self.__ncols, self.nplanes))
                result = image_2d[:, 0]
            except ValueError as e:
                print(e)
            except Exception as e:
                raise StopIteration
            finally:
                return result
        else:     
            # We'll retrieve a chunk from disk anytime it's necessary               
            try:
                # If there is no current chunk, get it!
                while self.curchunk is None:
                    tag, data = self.reader.chunk() 
                    if tag == b"IDAT":
                        # Is it possible to decompress a separate chunk?
                        if self.compression >= 0:
                            self.curchunk = zlib.decompress(data) # How to decode?
                        else:
                            self.curchunk = data
                        self.posinchunk = 0

                # Assume that the chunk is long enough and contains 1 or more complete lines
                # Take into account that each scanline is preceded by a filter type (1 byte)!
                rowlen = 1 + (self.__ncols * self.reader.psize) # no. of bytes               
                remlines = (len(self.curchunk) - self.posinchunk) // rowlen # remaining lines
                
                # Are there still lines to be retrieved from the current chunk?
                if remlines > 0:
                    # Yes: extract the next line from the current chunk
                    line = self.curchunk[self.posinchunk:self.posinchunk+rowlen]
                    self.posinchunk += rowlen
                else:
                    # No: get values from a new chunk 
                    self.curchunk = None
                    self.next(parseLine)
                    
                # We have to undo the effect of filtering for this line
                bs = self.get_straight_packed([line])

                # Convert bytestring
                #if self.reader.bitdepth == 16:
                np = self.nbands
                result = array('H', unpack('!%dH' % (len(bs) // 2), bs))
                #elif self.reader.bitdepth == 8:
                #    result = array('B', unpack('!%dB' % (len(bs)), bs))
                #else:
                #    result = self.reader._bytes_to_values(bytes)
                        
            except Exception as e:
                print(e)
                raise StopIteration
            finally:
                return result

    def writenext(self, sequence_with_data):
        # Continue adding incoming data to an array until the chunksize
        # self.writer.write_chunk(self.datafile, b"IDAT", data)
        pass
    
    def close(self):
        pass
    
    def reset(self):
        global recon
        recon = None
        super().reset()