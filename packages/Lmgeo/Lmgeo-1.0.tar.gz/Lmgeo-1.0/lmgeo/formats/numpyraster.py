# Copyright (c) 2004-2021 WUR, Wageningen
import os.path
from .raster import Raster
from .gridenvelope2d import GridEnvelope2D
from .const import constants as const
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    raise Exception("If one wants to use the module numpyraster, he / she needs to install Python package numpy!")

__author__ = "Steven B. Hoek"

class NumpyRaster(Raster, GridEnvelope2D):
    '''
    Convenience class which reads and writes all the data at once from *.npy files, 
    contrary to most classes found in this folder. Based on numpy.
    '''
    __data = None
    datatype = const.FLOAT
    cellsize = 1
    
    def __init__(self, filepath, *datatype):
        # Initialise
        Raster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)
        
        # Retrieve the name from the filepath and assign - incl. extension
        self.name = os.path.basename(filepath)
        # Also derive the folder
        self.folder = os.path.dirname(filepath)

        # Also set the datatype
        if len(datatype) > 0:
            if (datatype[0] == const.INTEGER): 
                self.datatype = const.INTEGER;
            else: 
                self.datatype = const.FLOAT;   
    
    def open(self, mode, ncols=1, nrows=1, xll=0., yll=0., cellsize=1., nodatavalue=-9999.0):
        super(NumpyRaster, self).open(mode);
        fpath = os.path.join(self.folder, self.name)
        
        # Raise error again if numpy is not installed
        if not HAS_NUMPY:
            raise Exception("If one wants to use the module numpyraster, he / she needs to install Python package numpy!")
        
        if (mode[0] == 'w'):
            # Open the file
            self.datafile = None
            
            # Assign the data attributes 
            self.ncols = ncols
            self.nrows = nrows
            self.xll = xll
            self.yll = yll
            self.cellsize = cellsize
            self.nodatavalue = nodatavalue
            self.writeheader()
            
            # Prepare memory
            if self.datatype == const.INTEGER:
                self.__data = np.zeros([self.nrows, self.ncols], dtype=np.int32)
            else:
                self.__data = np.zeros([self.nrows, self.ncols], dtype=np.float32)
        else:
            # Read header file
            self.readheader()
            
            # Read all the data here already
            if os.path.exists(fpath):
                self.__data = np.load(fpath)
                
    def readheader(self):
        hdrFilename = ""
        if os.path.isfile(os.path.join(self.folder, self.name + "." + const.HEADEREXT)): 
            hdrFilename = os.path.join(self.folder, self.name + "." + const.HEADEREXT)
        with open(hdrFilename) as f:   
            hls = f.readlines()
            self.ncols = int(hls[0].replace('ncols', '').strip())
            self.nrows = int(hls[1].replace('nrows', '').strip())
            self.xll = float(hls[2].replace('xllcorner', ''))
            self.yll = float(hls[3].replace('yllcorner', ''))
            self.cellsize = float(hls[4].replace('cellsize', ''))
            if self.datatype == const.INTEGER:
                self.nodatavalue = int(hls[5].replace('NODATA_value', '').strip())
            else:
                self.nodatavalue = float(hls[5].replace('NODATA_value', '').strip())
    
    def writeheader(self):
        # Write header file with all attributes 
        hdrFilename = os.path.join(self.folder, self.name + "." + const.HEADEREXT)

        try:
            # Open the file if it exists, otherwise create it
            with open(hdrFilename, 'w') as hf:
                # Now write all the attributes
                hf.write("ncols         " + str(self.ncols) + "\n")
                hf.write("nrows         " + str(self.nrows) + "\n")
                hf.write("xllcorner     " + str(self.xll) + "\n")
                hf.write("yllcorner     " + str(self.yll) + "\n")
                hf.write("cellsize      " + str(self.cellsize) + "\n")
                hf.write("NODATA_value  " + str(self.nodatavalue) + "\n")
        except Exception as e:
            msg = "Header file " + hdrFilename + " could not be written in folder " + self.folder
            raise IOError(msg + "(" + str(e) + ")")
    
    def next(self, parseLine=False):
        result = None;
        try:
            result = self.__data[self.currow, :]
            self.currow += 1
        except Exception:
            raise StopIteration
        finally:
            return result
        
    def writenext(self, sequence_with_data=None):
        # Fill the memory with extra
        self.__data[self.currow, :] = sequence_with_data
        
        # Write the data at once
        if self.currow == self.nrows - 1:
            fpath = os.path.join(self.folder, self.name)
            np.save(fpath, self.__data)
        self.currow += 1

    def close(self):
        pass