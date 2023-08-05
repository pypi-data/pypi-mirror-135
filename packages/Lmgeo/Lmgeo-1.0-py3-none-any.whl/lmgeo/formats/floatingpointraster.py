import os.path;
import stat
from array import array
from .const import Const, constants as const
from .raster import Raster
from .gridenvelope2d import GridEnvelope2D;

__author__ = "Steven B. Hoek"

class FloatingPointRaster(Raster, GridEnvelope2D):
    """A raster represented by 2 files, with extensions 'flt' and 'hdr'"""
    
    # Attributes - assign some dummy values for the mean time
    _const = None

    # Data attributes 
    name = "dummy.flt";
    folder = os.getcwd();
    cellsize = 1; # default
    nodatavalue = -9999.0; # default
    
    # Private attributes
    datatype = const.FLOAT;
    datafile = None;
    currow = 0;
    __envelope = None;
    
    def __init__(self, filepath='', *datatype): 
        # Check input
        if filepath == '':
            print('File path cannot be an empty string (method __init__).')
        
        # Initialise
        Raster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)
        self._const = Const()
        
        # Class and subclass wide constants
        self._const.LSBFIRST = "LSBFIRST";
        self._const.BYTESPERCELL = 4;
        self._const.DATAFILEXT = "flt"
        self._const.DATAFILEXTALT = "int"
        self._const.WORLDEXT = "wld"
        self.byteorder = self._const.LSBFIRST        

        # Retrieve the name from the filepath and assign - incl. extension
        self.name = os.path.basename(filepath);
        # Also derive the folder
        self.folder = os.path.dirname(filepath);
        # Finally set the datatype
        if len(datatype) > 0:
            if (datatype[0] == const.INTEGER): 
                self.datatype = const.INTEGER;
            else: 
                self.datatype = const.FLOAT;        
        
    def open(self, mode, ncols=1, nrows=1, xll=0, yll=0, cellsize=100, nodatavalue=-9999.0, byteorder="LSBFIRST"):
        # Initialise
        super(FloatingPointRaster, self).open(mode); 
        
        # If file does not exist and mode[0] = 'w', create it!
        if (mode[0] == 'w') and (not os.path.exists(self.folder + os.path.sep + self.name)):
            self.datafile = open(self.folder + os.path.sep + self.name, 'wb');
            self.__envelope = GridEnvelope2D.__init__(self, ncols, nrows, xll, yll, cellsize, cellsize);
            return True;
        else:    
            # Open the file
            if os.path.exists(self.folder + os.path.sep + self.name):            
                self.datafile = open(self.folder + os.path.sep + self.name, mode[0] + 'b'); 
                if (mode[0] == 'w'):
                    # Assign the data attributes 
                    self.ncols = ncols;
                    self.nrows = nrows;                    
                    self.xll = xll;
                    self.yll = yll;
                    self.cellsize = cellsize;
                    self.nodatavalue = nodatavalue;
                    self.byteorder = byteorder;
                    self.writeheader();
                else: 
                    # Retrieve the data attributes from the header file
                    self.readheader();
                self.__envelope = GridEnvelope2D.__init__(self, self.ncols, self.nrows, self.xll, self.yll, self.cellsize, self.cellsize);
                return True;
            else: return False; 
          
    
    def readheader(self):
        # Read header file and assign all attributes
        pos1 = str.rfind(str(self.name), "." + self._const.DATAFILEXT)
        pos2 = str.rfind(str(self.name), "." + self._const.DATAFILEXTALT)
        pos = max(pos1, pos2)
        if pos != -1: hdrFilename = self.name[0:pos] + "." + const.HEADEREXT
        else: raise ValueError("Invalid file name: " + self.name);
        if os.path.exists(self.folder + os.path.sep + hdrFilename):
            fileinfo = os.stat(os.path.join(self.folder, self.name))
            filesize = fileinfo[stat.ST_SIZE]
            if filesize == 0:
                raise RuntimeError("Empty header file found!")
            hf = open(self.folder + os.path.sep + hdrFilename, 'r');
            hl = hf.readline();
            self.ncols = int(hl.replace('ncols', '').strip());
            hl = hf.readline();
            self.nrows = int(hl.replace('nrows', '').strip());
            hl = hf.readline();
            self.xll = float(hl.replace('xllcorner', '').strip());        
            hl = hf.readline();
            self.yll = float(hl.replace('yllcorner', '').strip());        
            hl = hf.readline();
            self.cellsize = float(hl.replace('cellsize', '').strip());        
            hl = hf.readline();
            if (self.datatype == const.INTEGER): 
                self.nodatavalue = int(hl.replace('NODATA_value', '').strip());
            else: 
                self.nodatavalue = float(hl.replace('NODATA_value', '').strip());
            hl = hf.readline();
            self.byteorder = hl.replace('byteorder', '');         
            hf.close();
        else: 
            msg = "Header file " + hdrFilename + " not found in folder " + self.folder;
            raise IOError(msg);
        
    def next(self):
        # Read the next row if possible, otherwise generate StopIteration
        try:
            self.currow += 1;
            if (self.currow > self.nrows): raise StopIteration;
            result = self.datafile.read(self.ncols * self._const.BYTESPERCELL);  
            return array(self.datatype, result);      
        except:
            raise StopIteration;       
        
    @staticmethod
    def getDataFileExt(self):
        return self._const.DATAFILEXT;
    
    @staticmethod
    def getHeaderFileExt(self):
        return self._const.HEADEREXT;    
    
    @staticmethod
    def getBytesPerCell(self):
        return self._const.BYTESPERCELL;
    
    def writeheader(self):
        # Write header file with all attributes 
        pos1 = str.rfind(str(self.name), "." + self._const.DATAFILEXT)
        pos2 = str.rfind(str(self.name), "." + self._const.DATAFILEXTALT)
        pos = max(pos1, pos2)
        if pos != -1: hdrFilename = self.name[0:pos] + "." + const.HEADEREXT
        else: raise ValueError("Invalid file name: " + self.name);
        try:
            # Open the file if it exists, otherwise create it
            hf = open(self.folder + os.path.sep + hdrFilename, 'w');
   
            # Now write all the attributes
            hf.write("ncols         " + str(self.ncols) + "\n");
            hf.write("nrows         " + str(self.nrows) + "\n");
            hf.write("xllcorner     " + str(self.xll) + "\n");
            hf.write("yllcorner     " + str(self.yll) + "\n");
            hf.write("cellsize      " + str(self.cellsize) + "\n");
            hf.write("NODATA_value  " + str(self.nodatavalue) + "\n");
            hf.write("byteorder     " + self.byteorder + "\n");
        except Exception as e:
            msg = "Header file " + hdrFilename + " could not be written in folder " + self.folder;
            raise IOError(msg + "(" + str(e) + ")");
        
    def writenext(self, sequence_with_data):
        # Write the next data if possible, otherwise generate StopIteration
        # We cannot know whether exactly 1 row is included or not.
        try:          
            return self.datafile.write(sequence_with_data);
        except Exception as e:
            raise IOError(str(e));            
            raise StopIteration;       
                
    def reset(self):
        self.datafile.seek(0);
        super(FloatingPointRaster, self).reset()   
        