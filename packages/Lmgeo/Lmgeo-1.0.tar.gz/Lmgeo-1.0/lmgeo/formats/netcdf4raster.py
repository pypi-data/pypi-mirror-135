# Copyright (c) 2004-2021 WUR, Wageningen
from .netcdf4envelope2d import Netcdf4Envelope2D
from .gridenvelope2d import GridEnvelope2D
import os
try:
    from netCDF4 import Dataset
    HAS_NETCDF4 = True
except ImportError:
    HAS_NETCDF4 = False
    raise Exception("If one wants to use the module netcdf4raster, he / she needs to install Python package netCDF4!")

__author__ = "Steven B. Hoek"

class Netcdf4Raster(Netcdf4Envelope2D):  
    # Constants
    DATAFILEXT = 'nc4';
    _original_name = "Band1" # TODO: set it when a template file is opened for appending
    
    # Data attributes - assign some dummy values for the mean time
    name = "dummy.nc4";
    folder = os.getcwd();
    _dataset = None;
    _varname = "";
    _currow = 0;
    cellsize = 1;
    nodatavalue = -9999.0;
    __X = ""
    __Y = ""
    
    def __init__(self, filepath):
        # Initialise
        Netcdf4Envelope2D.__init__(None) 

        # Retrieve the name from the filepath and assign - incl. extension
        self.name = os.path.basename(filepath);
        # Also derive the folder
        self.folder = os.path.dirname(filepath);
        
    def set_xy_ranges(self, xvar, yvar):
        self.__X = xvar
        self.__Y = yvar

    def open(self, mode, ncols=1, nrows=1, xll=0, yll=0, cellsize=1, nodatavalue=-9999.0):
        # If file does not exist and mode[0] = 'w', create it!
        fpath = os.path.join(self.folder, self.name);
        
        # Raise error again if netCDF4 is not installed
        if not HAS_NETCDF4:
            raise Exception("If one wants to use the module netcdf4raster, he / she needs to install Python package netCDF4!")
        
        # Now prepare to read from file or to write it
        if mode[0] == 'a':
            if os.path.exists(fpath):
                print("About to open file " + fpath + " in append mode");
            self._dataset = Dataset(fpath, 'a', format='NETCDF4');
            self.nodatavalue = nodatavalue
            if (self.__X == "") or (self.__Y == ""):
                Netcdf4Envelope2D.__init__(self, self._dataset);
            else:
                Netcdf4Envelope2D.__init__(self, self._dataset, self.__X, self.__Y);
            return True;
        else:
            if os.path.exists(fpath):  
                # Open the netCDF4 file          
                ds = Dataset(fpath, 'r');
                if (self.__X == "") or (self.__Y == ""):
                    Netcdf4Envelope2D.__init__(self, ds);
                else:
                    Netcdf4Envelope2D.__init__(self, self._dataset, self.__X, self.__Y);   
                self._dataset = ds;
                self._varname = self._get_varname();
                try:
                    self.nodatavalue = ds.variables[self._varname]._FillValue
                except Exception as e:
                    print(e)
                return True;
            else: return False;    
    
    def _get_varname(self):
        # Establish which variable is stored in it - assume it's only 1!
        ds = self._dataset; 
        diff = set(ds.variables) - set(ds.dimensions);
        if len(diff) > 0:
            return diff.pop();
        else:
            return "";
            
    def readheader(self):
        pass;
    
    def __iter__(self):
        return self;
        
    def next(self, parseLine=True):
        # The netCDF4 format is not one that is read in a sequential manner. Is it a good idea
        # that this method is part of the interface?
        result = None;
        if self._varname != "":
            if parseLine:
                # Indexing: 1. years 2. by rows 3. columns
                # 3D: result = self.getVariables(self._varname)[:, self._currow, :]; 
                result = self.getVariables(self._varname)[self._currow, :] # 2D
            self._currow += 1;  # row index is zero-based! 
            return result;
    
    @staticmethod
    def getDataFileExt(self):
        return self.DATAFILEXT;
    
    def writeheader(self, name, long_name, units):
        # TODO: if _original_name is not one of the variables in the file -> error
        v = self._dataset.variables[self._original_name]
        v.setncattr("long_name", long_name)
        v.setncattr("units", units)
        if self._original_name != name:
            self._dataset.renameVariable(self._original_name, name)
        self._varname = name; 
        self._dataset.variables[self._varname].missing_value = self.nodatavalue
    
    def writenext(self, sequence_with_data):
        # Assume that the sequence is indexed 1. by year and 2. by column
        key = self._varname;
        if not hasattr(sequence_with_data, '__iter__'):
            raise ValueError("Input value not an array")
        if len(sequence_with_data.shape) != 2:
            raise ValueError("Input array has unexpected shape")
        if sequence_with_data.shape[1] != self.ncols:
            raise ValueError("Input array has unexpected dimension")
        # TODO adapt so that Netcdf files with different dimensions can be written
        # 3D: self._dataset.variables[key][:, self._currow, :] = sequence_with_data
        self._dataset.variables[key][self._currow, :] = sequence_with_data #2D
        self._currow += 1;
        
    def close(self):
        if not self._dataset is None:
            if self._dataset.isopen():
                self._dataset.close(); 

    def reset(self):
        self._currow = 0; 
    
    def getEnvelope(self):
        # TODO: this cannot be solved by invoking super or so?
        return GridEnvelope2D(self.ncols, self.nrows, self.xll, self.yll, self.dx, self.dy);
        
    def getVariables(self, dimDescriptor):
        return self._dataset.variables[dimDescriptor];
    
    def getFilePath(self):
        filepath = os.path.join(self.folder, self.name);
        return filepath;
    
    def getVariableName(self):
        return self._varname;
    
    def get_value(self, i, k):    
        # Return the wanted value
        for _ in range(0, i): self.next(False)
        line = self.next()
        self.reset()
        return line[int(k)]
    
"""
def write_nc4_file(filename, crop_no):
    # Write the data to the file
    pass
       
def initialise_nc4_file(filename, crop_no):
    ds = None
    try:
        # Open file
        ncdfname_fp = os.path.join(run_settings.output_folder, filename)
        ds = Dataset(ncdfname_fp, 'w', format='NETCDF4')
        
        # Create dimensions        
        ds.createDimension("lon", 720)
        ds.createDimension("lat", 360)
        ds.createDimension("time", None)
        
        # Create variables and fill them
        longitudes = ds.createVariable('lon', np.float32, ('lon',))
        longitudes[:] = arange(-179.75, 180.25, 0.5)
        longitudes.units = 'degrees east'
        latitudes  = ds.createVariable('lat', np.float32, ('lat',))
        latitudes[:] = arange(-89.75, 90.25, 0.5)
        latitudes.units = 'degrees north'
        times = ds.createVariable('time', np.float64, ('time',))
        # times.units = 'hours since 0001-01-01 00:00:00.0' ???

    except RuntimeError:
        msg = "Error opening netCDF4 dataset on crop %i." % crop_no
        print msg
        logging.exception(msg)
    return ds
"""
        