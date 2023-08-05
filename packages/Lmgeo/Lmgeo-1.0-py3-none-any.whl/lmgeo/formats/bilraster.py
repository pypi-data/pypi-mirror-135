# -*- coding: utf-8 -*-
import os.path
import stat
import struct
from array import array
from math import fabs
from .bandraster import BandRaster
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

__author__ = "Steven B. Hoek"

class BilRaster(BandRaster):
    "A raster represented by 2 files, with extensions 'bil' and 'bil.hdr'"
    
    # TODO: change some function calls so that it's more obvious how to use "with" statements
    # Use of such statements are essential when files are written to disk!
    
    # Data attributes - assign some dummy values for the mean time
    _const = None
    name = "";

    def __init__(self, filepath='', *dataformat):
        # Process input
        if filepath == '':
            print('File path cannot be an empty string (method __init__).')
        if len(dataformat) == 0:
            print("Data type 'float' assumed (method __init__).")
            dataformat = 'f'
        
        # Initialise super class instance
        BandRaster.__init__(self, filepath, dataformat[0])
        if self._const == None:
            raise AttributeError("BIL raster not properly initialised!")
        self._const.DATAFILEXT = "bil"
        self._const.WORLDEXT = "blw"
        self.byteorder = self._const.INTEL
        self.pixeltype = self._const.UNSIGNEDINT
        if self.name == "":
            self.name = "dummy." + self._const.DATAFILEXT
        self.currow = -1
    
    def open(self, mode, ncols=1, nrows=1, nbands=1, xll=0, yll=0, cellsize=100, nodatavalue=256):
        self.nbits = struct.calcsize(self.dataformat)*8
        result = super(BilRaster, self).open(mode, ncols, nrows, nbands, xll, yll, cellsize, nodatavalue);
        if (mode[0] == 'w'):
            return result
        else:
            # Open the file
            if os.path.exists(os.path.join(self.folder, self.name)):            
                # Check given format string is valid
                bytesperpix = 2 #default
                try:
                    bytesperpix = struct.calcsize(self.dataformat)
                except:
                    raise ValueError("Supplied data format " + str(self.dataformat) + " is invalid")
                # end try
                
                # Check file size matches with size attributes
                fileinfo = os.stat(os.path.join(self.folder, self.name))
                filesize = fileinfo[stat.ST_SIZE]
                if (filesize == 0) and (mode[0] == 'w'):
                    print("Empty BIL file found. I'm going to overwrite it ...")
                else:
                    checknum = (((filesize / float(self.nbands)) / float(self.nrows)) / float(bytesperpix)) / self.ncols
                    if checknum != 1:
                        if fabs(checknum - 1) < 0.00003:
                            raise ValueError("File size and size calculated from attributes only match approximately")
                        else:
                            raise ValueError("File size and supplied attributes do not match at all!")
                
                # Open the file for reading in binary mode
                try:
                    self.datafile = open(os.path.join(self.folder, self.name), mode[0] + "b")
                except:
                    msg = "Failed to open BIL file " + os.path.join(self.folder, self.name)
                    raise IOError(msg)          
                return True;
            else: return False; 

    def next(self, parseLine=True):
        super(BilRaster, self).next()
        
        # Read the next row if possible, otherwise generate StopIteration
        try:
            self.currow += 1;
            if (self.currow > self.nrows): raise StopIteration;
            
            # Get the size in bytes for the given data format
            line = []
            itemsize = struct.calcsize(self.dataformat)
            if not parseLine:
                self.datafile.read(self.nbands * self.ncols * itemsize)
                return line
            
            # Arrange the following: each line should be a list of length self.ncols, with
            # arrays that each contain self.nbands values  
            if not HAS_NUMPY:
                # The following is for the case without numpy: each line should be
                # a list of length self.ncols, with arrays of length self.nbands
                for _ in range(0, self.ncols):
                    line.append(array(self.dataformat, self.nbands*[0]))
            else:
                line = np.zeros((self.ncols, self.nbands))
                
            # For each pixel in each band, read a data item, unpack it and store it in the output list
            itemsize = struct.calcsize(self.dataformat)
            for bandnum in range(self.nbands):
                mybuffer = self.datafile.read(self.ncols*itemsize)
                dataitems = struct.unpack_from(self.ncols*self.dataformat, mybuffer)
                if not HAS_NUMPY:
                    for pixnum in range(self.ncols):
                        line[pixnum][bandnum] = dataitems[pixnum]
                    # end for
                else:
                    line[:, bandnum] = dataitems
                # end if
            # end for
            return line            
                   
        except StopIteration:
            raise StopIteration;  
        except Exception as e:
            raise Exception(e)

    def writenext(self, sequence_with_data):
        super(BilRaster, self).writenext(sequence_with_data)
        # TODO: test!
        # Write the next data if possible, otherwise generate StopIteration
        # Assume that the input sequence is a sequence of length self.ncols
        # with at each position another sequence of length self.nbands
        try:
            # Perform a number of checks
            if not self._is_sequence(sequence_with_data):
                raise ValueError("Input value is not a sequence!")
            if len(sequence_with_data) != self.ncols:
                raise ValueError("Input sequence has not got the expected length")
            if not HAS_NUMPY:
                if not isinstance(sequence_with_data[0][0], (int, float)) and len(sequence_with_data[0]) != self.nbands:
                    raise ValueError("Input sequence elements haven't got the expected number of values")
            else:
                if isinstance(sequence_with_data, np.ndarray) and len(sequence_with_data.shape) == 1:
                    sequence_with_data = np.reshape(sequence_with_data, (sequence_with_data.shape[0], 1))
                if (not isinstance(sequence_with_data[0][0], (int, float, np.int32, np.float32, np.float64))) or len(sequence_with_data[0]) != self.nbands:
                    raise ValueError("Input sequence elements haven't got the expected number of values") 
            if self.nbands > 1 and not self._is_sequence(sequence_with_data[0]):
                raise ValueError("Format of input sequence elements not as expected")

            # Now assign the data to the right data structure
            itemsize = struct.calcsize(self.dataformat)
            for bandnum in range(self.nbands):
                if not HAS_NUMPY:
                    line = []
                    for pixnum in range(self.ncols):
                        line.append(sequence_with_data[pixnum][bandnum])
                    # end for
                else:
                    # Assume the sequence is a numpy array
                    line = sequence_with_data[:, bandnum]
                # end if    
                mybuffer = bytearray(self.ncols * itemsize)
                struct.pack_into(self.ncols*self.dataformat, mybuffer, 0, *line)
                self.datafile.write(mybuffer)
                self.datafile.flush()
            # end for

            return True
        except StopIteration:
            raise StopIteration
        except ValueError as e:
            print(str(e))
            raise ValueError
        except Exception as e:
            raise IOError(str(e));   


    