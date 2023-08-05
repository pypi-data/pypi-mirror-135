from .const import Const, constants as const
import os.path
import array
from .raster import Raster
from .gridenvelope2d import GridEnvelope2D;
from builtins import int

__author__ = "Steven B. Hoek"

class AsciiGrid(Raster, GridEnvelope2D):
    """A raster represented by an ASCII file, with extension 'asc'"""
    
    # Data attributes - assign some dummy values for the mean time
    _const = None
    name = ""
    folder = os.getcwd();
    cellsize = 100.0;
    nodatavalue = -9999.0;
    datatype = const.FLOAT;
    dataformat='f'
    
    # Private attributes
    datafile = None;
    currow = 0;
    __mode = 'r';
    __digitspercell = 7;
    
    def __init__(self, filepath='', *datatype):
        # Check input
        if filepath == '':
            print('File path cannot be an empty string (method __init__).')
            
        # Module wide constants
        self._const = Const()
        self._const.FILEXT = "asc";     
        self._const.MAXDIGITSPERCELL = 8 # TODO this is hardcoded - change this
        self.name = "dummy." + self._const.FILEXT;
        
        # Initialise further
        Raster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)
        
        # Retrieve the name from the filepath and assign - incl. extension
        self.name = os.path.basename(filepath);
        # Also derive the folder
        self.folder = os.path.dirname(filepath);
        # Finally set the datatype
        if len(datatype) > 0:
            if (datatype[0] == const.INTEGER): 
                self.datatype = const.INTEGER;
                self.dataformat = 'i'
            else: 
                self.datatype = const.FLOAT;
                
    def open(self, mode, ncols=1, nrows=1, xll=0.0, yll=0.0, cellsize=100.0, nodatavalue=-9999.0):
        # Initialise
        super(AsciiGrid, self).open(mode); 
    
        # If file does not exist and mode[0] = 'w', create it!
        if (mode[0] == 'w') and (not self.file_exists):
            self.datafile = open(os.path.join(self.folder, self.name), 'w');
            self.__mode = mode;
            GridEnvelope2D.__init__(self, ncols, nrows, xll, yll, cellsize, cellsize);
            self.cellsize = cellsize;
            self.nodatavalue = nodatavalue;
            self.writeheader();
            return True;
        else:    
            # Open the file
            if self.file_exists:            
                self.datafile = open(os.path.join(self.folder, self.name), mode[0]); 
                if (mode[0] == 'w'):
                    # Assign the data attributes 
                    self.ncols = ncols;
                    self.nrows = nrows;                    
                    self.xll = xll;
                    self.yll = yll;
                    self.cellsize = cellsize;
                    self.nodatavalue = nodatavalue;
                    self.writeheader();
                else: 
                    # File is open - retrieve the data attributes from the header of the file
                    self.readheader();
                    
                    # Also find out how many digits per cell were used - assume it's constant
                    pos = self.datafile.tell();
                    line = self.datafile.readline();
                    self.__digitspercell = ((1 + len(line)) / self.ncols) - 1;
                    self.datafile.seek(pos);  # return to first line with data
                    GridEnvelope2D.__init__(self, self.ncols, self.nrows, self.xll, self.yll, self.cellsize, self.cellsize);
                return True;
            else: return False;
            
    def readheader(self):
        # Assume that the file is open; read header of the file and assign all attributes 
        if (self.datafile != None):
            # TODO: make this case-insensitive!
            if (not self.datafile.closed):            
                hl = self.datafile.readline();
                self.ncols = int(hl.replace(const.NCOLS, ''));
                hl = self.datafile.readline();
                self.nrows = int(hl.replace(const.NROWS, ''));
                hl = self.datafile.readline();
                self.xll = float(hl.replace(const.XLLCORNER.lower(), ''));        
                hl = self.datafile.readline();
                self.yll = float(hl.replace(const.YLLCORNER.lower(), ''));        
                hl = self.datafile.readline();
                self.cellsize = float(hl.replace(const.CELLSIZE, ''));        
                hl = self.datafile.readline();
                if (self.datatype == const.INTEGER): 
                    self.nodatavalue = int(hl.replace(const.NODATA_VALUE, ''));
                else: 
                    self.nodatavalue = float(hl.replace(const.NODATA_VALUE, ''));
            else: 
                msg = "File " + self.name + " not found in folder " + self.folder;
                raise IOError(msg);                
    
    def next(self, parseLine=True):
        # Read the next row if possible, otherwise generate StopIteration
        # Assume that the header lines have been read and are correct wrt. ncols and nrows
        result = None;
        try:
            if (self.datafile != None):
                if (not self.datafile.closed):
                    self.currow += 1;
                    if (self.currow > self.nrows): 
                        raise StopIteration("Attempt to move beyond last row.");
                    
                    # Allocate a new array with ncols of the right type
                    if (self.datatype == const.INTEGER):
                        result = array.array('l', self.ncols * [self.nodatavalue]);
                    else:
                        result = array.array('f', self.ncols * [self.nodatavalue]);

                    # Now fill the array - first translate whitespace into space
                    rawline = self.datafile.readline();
                    if parseLine:
                        i = 0;                    
                        for x in rawline.split(): 
                            if (i < self.ncols):
                                if (self.datatype == const.INTEGER):
                                    result[i] = int(x);
                                else:
                                    result[i] = float(x);
                            i = i + 1;
                    return result;
                else: raise StopIteration("Attempt to read raster data from a closed file.");
            else: raise StopIteration("Attempt to read raster data from an unassigned file.")
        except Exception as e:
            print("Error: " + str(e));
            raise StopIteration;
           
    @staticmethod
    def getFileExt(self):
        return Raster.getDataFileExt()
        
    def writeheader(self):
        # Assume that the file is open; write header of the file with all attributes 
        if (self.datafile != None):
            if (not self.datafile.closed):
                try:
                    maxdigits = self._const.MAXDIGITSPERCELL + 1
                    self.datafile.write(const.NCOLS + "         " + str(self.ncols).rjust(maxdigits) + "\n");
                    self.datafile.write(const.NROWS + "         " + str(self.nrows).rjust(maxdigits) + "\n");
                    self.datafile.write(const.XLLCORNER.lower() + "     " + str(self.xll).rjust(maxdigits) + "\n");
                    self.datafile.write(const.YLLCORNER.lower() + "     " + str(self.yll).rjust(maxdigits) + "\n");
                    self.datafile.write(const.CELLSIZE + "      " + str(self.cellsize).rjust(maxdigits) + "\n");
                    self.datafile.write(const.NODATA_VALUE + "  " + str(self.nodatavalue).rjust(maxdigits) + "\n");
                except Exception as e:
                    print(e);
                    msg = "Header lines could not be written to file " + self.name + " in folder " + self.folder;
                    raise IOError(msg);
        
    def writenext(self, sequence_with_data):
        # Write the next line if possible, otherwise generate StopIteration
        # We assume that exactly 1 row is included.
        try:          
            if (self.datatype == const.INTEGER):
                # TODO deal with numpy arrays if necessary
                for k in range(0, self.ncols):
                    s = str(sequence_with_data[k]).rjust(self._const.MAXDIGITSPERCELL + 1);
                    self.datafile.write(s);  
            else:
                totalwidth = self._const.MAXDIGITSPERCELL - 1
                fmtstr = "{:" + str(totalwidth) + ".3f}" # TODO format is hardcoded - change this!
                for k in range(0, self.ncols):
                    s = fmtstr.format(sequence_with_data[k]).rjust(self._const.MAXDIGITSPERCELL + 1);
                    self.datafile.write(s);                 
            return self.datafile.write("\n");
        except Exception as e:
            print(e);            
            raise StopIteration
    
    def flush(self):
        self.datafile.flush();
                
    def reset(self):
        self.datafile.seek(0);
        if (self.__mode[0] == 'r'):
            self.readheader();
        super(AsciiGrid, self).reset() 
      
    def get_value(self, i, k):    
        # Return the wanted value
        for _ in range(0, i): self.next(False)
        line = self.next()
        self.reset()
        return line[int(k)]
    
    def get_type(self):
        if self.dataformat == 'i':
            return int
        else:
            return float
        