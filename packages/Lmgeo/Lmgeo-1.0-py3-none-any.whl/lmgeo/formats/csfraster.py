from .const import Const, constants as const
import os.path
from array import array
from .raster import Raster
from .gridenvelope2d import GridEnvelope2D
import struct
import sys
try:
    import numpy as np
    import numpy.ma as ma
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

__author__ = "Steven B. Hoek"

class CsfRaster(Raster, GridEnvelope2D):
    """A raster represented by a binary file - with extension 'map' - as used esp. by PCRaster software"""
    __cellrepr = 'UNKNOWN'
    __valuescale = 'VS_UNDEFINED'
    __version = 2
    __mode = 'r'
    dataformat = 'f'
    __MAIN_HDR = [
        {'type':'char', 'name':'signature', 'endpos':32},
        {'type':'H', 'name':'version', 'endpos':34},
        {'type':'I',  'name':'gisFileId', 'endpos':38},
        {'type':'H', 'name':'projection', 'endpos':40},
        {'type':'I', 'name':'attrTable', 'endpos': 44},
        {'type':'H', 'name':'mapType', 'endpos':46},
        {'type':'I', 'name':'byteOrder', 'endpos':50}
    ]
    
    __RASTER_HDR = [
        {'name':'valueScale', 'type':'x', 'endpos':66},
        {'name':'cellRepr', 'type':'y', 'endpos':68},
        {'name':'minVal', 'type':'char', 'endpos':76},
        {'name':'maxVal', 'type':'char', 'endpos':84},
        {'name':'xUL', 'type':'d', 'endpos': 92},
        {'name':'yUL', 'type':'d', 'endpos':100},
        {'name':'nrRows', 'type':'I', 'endpos':104},
        {'name':'nrCols', 'type':'I', 'endpos':108},
        {'name':'cellSizeX', 'type':'d', 'endpos':116},
        {'name':'cellSizeY', 'type':'d', 'endpos':124},
        {'name':'angle', 'type':'d', 'endpos':132}
    ]

    def __get_csf_cellrepr(self, value):
        result = -1
        if self.__version == 2:
            # preferred version 2 cell representations
            if value == b'\x00': result = 'CR_UINT1' # boolean, ldd and small nominal and small ordinal 
            elif value == b'\x26': result = 'CR_INT4' # large nominal and large ordinal 
            elif value == b'\x5A': result = 'CR_REAL4' # single scalar and single directional 
            elif value == b'\xDB': result = 'CR_REAL8'  # double scalar or directional; also the only type that can hold all 
                                                        # cell representation without loss of precision
        else:
            # version 1 cell representations
            if value == b'\x04': result = 'CR_INT1'
            elif value == b'\x15': result = 'CR_INT2'
            elif value == b'\x11': result = 'CR_UINT2'
            elif value == b'\x22': result = 'CR_UINT4'
        return result
    
    def __set_csf_cellrepr(self, value):
        # We're only going to set version 2 map files
        item = self.__get_header_item(self.__RASTER_HDR, 'cellRepr')
        if value == 'CR_UINT1': item['value'] = b'\x00'
        elif value == 'CR_INT4': item['value'] = b'\x26'
        elif value == 'CR_REAL4': item['value'] = b'\x5A'
        elif value == 'CR_REAL8': item['value'] = b'\xDB'
    
    def __cellrepr2dataformat(self, value):
        if self.__version == 2:
            if  (value == 'CR_REAL8'): dataformat = 'd'
            elif (value == 'CR_REAL4'): dataformat = 'f'
            elif (value == 'CR_INT4'): dataformat = 'i'
            elif (value == 'CR_UINT1'): dataformat = 'h'
        else:
            if (value == 'CR_INT1'): dataformat = 'b'
            elif (value == 'CR_INT2'): dataformat = 'h' 
            elif (value == 'CR_UINT2'): dataformat = 'H'
            elif (value == 'CR_UINT4'): dataformat = 'I'
        return dataformat
    
    @classmethod
    def dataformat2cellrepr(cls, value):
        # We're only going to write version 2 map files
        result = 'CR_REAL4'
        if value == 'd': result = 'CR_REAL8'
        elif value == 'i': result = 'CR_INT4'
        elif value == 'h': result = 'CR_UINT1'
        return result
    
    # The lowest value for signed integers and the highest value for unsigned integers are omitted from
    # the valid range. These values are called missing values (MV) and have a special meaning in the
    # format. They specify a non specified feature or a value of no interest. The two floating point types
    # have a bit-pattern (all bits set to 1) that is a NAN as their missing value.
    @classmethod
    def get_min_max_nodata(cls, raster, cellrepr):
        try:
            # Initialise
            result = [None, None, None]
            
            # The following works only for CSF version 2
            # TODO check that this also works for Python 64-bits
            if sys.version[0] == '2': 
                minimum = sys.maxint
            else: 
                minimum = sys.maxsize
            maximum = -1 * (minimum + 1)
            
            # Assume that raster is to be copied
            if cellrepr == 'CR_UINT1':
                nodatavalue = minimum # should be 2147483647
            elif cellrepr == 'CR_INT4':
                nodatavalue = maximum # should be -2147483648
            else:
                if not np.isnan(raster.nodatavalue): 
                    nodatavalue = raster.nodatavalue
                
            # Check that numpy is installed
            if not HAS_NUMPY:
                raise Exception("Not yet implemented for Python instances without numpy!")
            else:
                if raster != None:
                    for i in range(raster.nrows):
                        line = raster.next()
                        mline = ma.array(line, mask = abs(np.array(line) - raster.nodatavalue) < 0.0000001)
                        if ma.any(mline):
                            maximum = max(np.max(mline), maximum)
                            minimum = min(np.min(mline), minimum)
                    raster.reset()   
                
            # Prepare to return result      
            result = (minimum, maximum, nodatavalue)

        except Exception as e:
            print(e)
        finally:
            return result
    
    def __get_csf_valuescale(self, value):
        result = 'VS_UNDEFINED'
        if self.__version == 1:
            if value == 0: result = 'VS_NOTDETERMINED'
            elif value == 1: result = 'VS_CLASSIFIED'
            else: result = 'VS_CONTINUOUS'
        else:
            if (value == b'\xe0'): result = 'VS_BOOLEAN' # boolean, always UINT1, values: 0,1 or MV_UINT1 
            elif (value == b'\xe2'): result = 'VS_NOMINAL' # nominal, UINT1 or INT4 
            elif (value == b'\xf2'): result = 'VS_ORDINAL' # ordinal, UINT1 or INT4 
            elif (value == b'\xeb'): result = 'VS_SCALAR' # directional REAL4 or (maybe) REAL8, -1 means no direction 
            elif (value == b'\xf0'): result = 'VS_LDD' # local drain direction, always UINT1, values: 1-9 or MV_UINT1 */
        return result
    
    def __set_csf_valuescale(self, value):
        item = self.__get_header_item(self.__RASTER_HDR, 'valueScale')
        if value == 'VS_BOOLEAN': item['value'] = b'\xe0' 
        elif value == 'VS_NOMINAL': item['value'] = b'\xe2'
        elif value == 'VS_ORDINAL': item['value'] = b'\xf2'
        elif value == 'VS_SCALAR': item['value'] = b'\xeb'
        elif value == 'VS_LDD': item['value'] =  b'\xf0'
    
    def __get_header_item(self, header, itemname):
        result = None
        for item in header:
            if (item['name'] == itemname):
                result = item
        return result
    
    def __get_header_value(self, header, itemname):
        result = ''
        for item in header:
            if (item['name'] == itemname) and ('value' in item):
                result = item['value']
                break
        return result
    
    def __set_header_value(self, header, itemname, value):
        for item in header:
            if (item['name'] == itemname):
                item['value'] = value
                return

    def get_main_header(self):
        return self.__MAIN_HDR
    
    def get_raster_header(self):
        return self.__RASTER_HDR;

    def __init__(self, filepath='', *args):
        # Check input
        if filepath == '':
            print('File path cannot be an empty string (method __init__).')
            
        # Module wide constants
        self._const = Const()
        self._const.FILEXT = "map"

        # Initialise further
        Raster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)

        # Retrieve the name from the filepath and assign - incl. extension; idem folder
        self.name = os.path.basename(filepath);
        self.folder = os.path.dirname(filepath);
        
        # Arrange that the dataformat is set
        if len(args) > 0:
            self.dataformat = args[0]
        if len(args) > 1:
            self.minimum = args[1]
            self.maximum = args[2]
        if len(args) > 3:
            self.__cellrepr = args[3]
        
    def open(self, mode, ncols=1, nrows=1, xll=0.0, yll=0.0, cellsize=100.0, nodatavalue=-9999.0, valueScale='VS_UNDEFINED'):
        # Initialise
        super(CsfRaster, self).open(mode);
        
        # If file does not exist and mode[0] = 'w', create it!
        if (mode[0] == 'w') and (not self.file_exists):
            self.datafile = open(os.path.join(self.folder, self.name), 'wb')
            self.__mode = mode;
            GridEnvelope2D.__init__(self, ncols, nrows, xll, yll, cellsize, cellsize);
            self.cellsize = cellsize;
            self.nodatavalue = nodatavalue;
            self.__set_header_value(self.__RASTER_HDR, "valueScale", valueScale)
            self.writeheader();
            return True;
        else:  
            # Open the file
            if self.file_exists:            
                self.datafile = open(os.path.join(self.folder, self.name), mode[0]+'b'); 
                if (mode[0] == 'w'):
                    # Assign the data attributes 
                    self.ncols = ncols;
                    self.nrows = nrows;                    
                    self.xll = xll;
                    self.yll = yll;
                    self.cellsize = cellsize;
                    self.nodatavalue = nodatavalue;
                    if valueScale == 'VS_UNDEFINED':
                        raise Exception("A valid value scale is required!")
                    self.__set_csf_valuescale(valueScale)
                    self.writeheader();
                else: 
                    # File is open - retrieve the data attributes from the header of the file
                    self.readheader();
                    
                    # Initialise the instance also for the second class from which it inherits
                    GridEnvelope2D.__init__(self, self.ncols, self.nrows, self.xll, self.yll, self.cellsize, self.cellsize);
                return True;
            else: return False;

    def readheader(self):
        if (self.datafile != None) and (not self.datafile.closed):
            # Assume that the file is at position 0
            fileheader = self.datafile.read(256)
            hdrdata = bytearray(fileheader)
            
            # Loop over the items expected in the main header  
            prevpos = 0
            for item in self.__MAIN_HDR:
                endpos = int(item['endpos'])
                rawbytes = hdrdata[prevpos:endpos]
                if item['type'] == 'char':
                    value = rawbytes.decode('ascii').strip('\x00') 
                else:
                    value = array(item['type'], rawbytes)
                item['value'] = value
                prevpos = endpos
             
            fmtdesc = 'RUU CROSS SYSTEM MAP FORMAT'    
            if self.__get_header_value(self.__MAIN_HDR, 'signature') != fmtdesc:
                raise ValueError('Not a valid CSF file!')
    
        # Make sure that the items in the raster header get the right values
        valuescale = self.__get_csf_valuescale(bytes(hdrdata[64:65]))
        self.__get_header_item(self.__RASTER_HDR, "valueScale")["value"] = valuescale
        cellrepr = self.__get_csf_cellrepr(bytes(hdrdata[66:67])) 
        self.__get_header_item(self.__RASTER_HDR, "cellRepr")["value"] = cellrepr
        self.dataformat = self.__cellrepr2dataformat(cellrepr)      
        prevpos = 68    
        for item in self.__RASTER_HDR[2:]:
            endpos = int(item['endpos'])
            rawbytes = hdrdata[prevpos:endpos]
            value = None
            if item['type'] == 'char':
                # minVal and maxVal
                if ((valuescale != 'VS_BOOLEAN') and (valuescale != 'VS_LDD')):
                    value = array(self.dataformat, rawbytes)                         
            else:
                value = array(item['type'], rawbytes)
            if value != None: item['value'] = value
            prevpos = endpos
            
        # Determine the number of rows and columns
        self.nrows = int(self.__get_header_value(self.__RASTER_HDR, 'nrRows')[0])
        self.ncols = int(self.__get_header_value(self.__RASTER_HDR, 'nrCols')[0])
        self.dx = float(self.__get_header_value(self.__RASTER_HDR, 'cellSizeX')[0])
        self.dy = float(self.__get_header_value(self.__RASTER_HDR, 'cellSizeY')[0])
        self.cellsize = 0.5 * (self.dx + self.dy)
        self.xll = float(self.__get_header_value(self.__RASTER_HDR, 'xUL')[0])
        self.yll = float(self.__get_header_value(self.__RASTER_HDR, 'yUL')[0]) - self.nrows*self.cellsize

        # The NODATA value is not stored in the header
        minVal = int(self.__get_header_value(self.__RASTER_HDR, 'minVal')[0])
        maxVal = int(self.__get_header_value(self.__RASTER_HDR, 'maxVal')[0])
        if (self.dataformat.lower() in ['b', 'h', 'i']):
            # In case of integers we'll have to scan the file until a very low negative value is found < minVal (signed integers) 
            # or a rather high positive number is found > maxVal (unsigned integers)
            for i in range(self.nrows):
                line = self.next()
                if not HAS_NUMPY:
                    raise Exception("Not yet implemented for Python instances without numpy!")
                else:
                    if self.dataformat in ['b', 'h', 'i']:
                        minimum = np.max(line)
                        if minimum < minVal:
                            self.nodatavalue = minimum
                            break
                    else:
                        maximum = np.min(line)
                        if maximum > maxVal:
                            self.nodatavalue = minimum
                            break 
            self.datafile.seek(256);
        else:
            # In case of floats / doubles, then missing values (MV) are stored as nan 
            self.nodatavalue = minVal - 1.0

    def writeheader(self):
        if (self.datafile != None) and (not self.datafile.closed):
            try:
                # The signature is a special case  
                item = self.__get_header_item(self.__MAIN_HDR, "signature")
                if (item != None): item['value'] = bytes('RUU CROSS SYSTEM MAP FORMAT\x00\x00\x00\x00\x00', 'ascii')
                buflen = int(item['endpos'])
                mybuffer = bytearray(buflen)
                struct.pack_into(buflen*'b', mybuffer, 0, *item['value'])
                self.datafile.write(mybuffer)
                self.datafile.flush()
                prevpos = item['endpos']
                
                # Assign values to the remaining items of the main header
                self.__set_header_value(self.__MAIN_HDR, "version", 2)
                self.__set_header_value(self.__MAIN_HDR, "gisFileId", 0)
                self.__set_header_value(self.__MAIN_HDR, "projection", 1) 
                self.__set_header_value(self.__MAIN_HDR, "attrTable", 0) 
                self.__set_header_value(self.__MAIN_HDR, "mapType", 1)
                self.__set_header_value(self.__MAIN_HDR, "byteOrder", 1)
                
                # Write the remaining items of the main header to file
                for item in self.__MAIN_HDR[1:]:
                    mybuffer = struct.pack(item['type'], item['value'])
                    self.datafile.write(mybuffer)
                prevpos = int(item['endpos'])
                self.datafile.flush()
                
                # Fill 14 bytes with \x00 before continuing with the raster header
                self.datafile.write(14*b'\x00')
                self.datafile.flush()
                
                # Write the first 2 of the raster header - valueScale was already set in the open statement
                item = self.__get_header_item(self.__RASTER_HDR, 'valueScale')
                self.datafile.write(item['value'] + b"\x00")
                prevpos = int(item['endpos'])
                dtype = self.dataformat2cellrepr(self.dataformat)
                self.__set_csf_cellrepr(dtype)
                item = self.__get_header_item(self.__RASTER_HDR, 'cellRepr')
                self.datafile.write(item['value'] + b"\x00")
                prevpos = int(item['endpos'])
                self.datafile.flush()
                
                # Now use all values to assign to the raster header
                self.__set_header_value(self.__RASTER_HDR, "minVal", self.minimum)
                self.__set_header_value(self.__RASTER_HDR, "maxVal", self.maximum)
                self.__set_header_value(self.__RASTER_HDR, "xUL", self.xll)  
                self.__set_header_value(self.__RASTER_HDR, "yUL", self.yll + self.nrows*self.cellsize)
                self.__set_header_value(self.__RASTER_HDR, "nrRows", self.nrows)
                self.__set_header_value(self.__RASTER_HDR, "nrCols", self.ncols)
                self.__set_header_value(self.__RASTER_HDR, "cellSizeX", self.cellsize)
                self.__set_header_value(self.__RASTER_HDR, "cellSizeY", self.cellsize)
                self.__set_header_value(self.__RASTER_HDR, "angle", 0)   
                
                # Write the values              
                for item in self.__RASTER_HDR[2:]:
                    buflen = int(item['endpos']) - prevpos
                    dtype = item['type'][0]
                    if dtype == 'c': dtype = self.dataformat
                    arrlen = buflen / struct.calcsize(dtype)
                    mybuffer = array(dtype, int(arrlen) * [0])
                    mybuffer[0] = item['value']
                    self.datafile.write(mybuffer)
                    prevpos = int(item['endpos'])
                
                # Write bytes with value zero until position 256
                mybuffer = bytearray(256 - prevpos)
                self.datafile.write(mybuffer)
                self.datafile.flush()
                
            except Exception as e:
                print(e)
                raise Exception(e)
    
    def next(self, parseLine=True):
        try:
            # The actual data start from position 256
            itemsize = struct.calcsize(self.dataformat)
            rawline = bytearray(self.datafile.read(self.ncols*itemsize)) 
            line = struct.unpack_from(self.ncols*self.dataformat, rawline)
            return line
        except StopIteration as e:
            raise StopIteration(e)
            
    
    def writenext(self, sequence_with_data):
        try:
            # Perform a number of checks
            if not self._is_sequence(sequence_with_data):
                raise ValueError("Input value is not a sequence!")
            if len(sequence_with_data) != self.ncols:
                raise ValueError("Input sequence has not got the expected length")
            if not HAS_NUMPY:
                if not isinstance(sequence_with_data[0][0], (int, float)):
                    raise ValueError("Input sequence elements haven't got the expected number of values")
            else:
                if isinstance(sequence_with_data, np.ndarray) and len(sequence_with_data.shape) == 1:
                    sequence_with_data = np.reshape(sequence_with_data, (sequence_with_data.shape[0], 1))
                if (not isinstance(sequence_with_data[0][0], (int, float, np.int32, np.float32, np.float64))):
                    raise ValueError("Input sequence elements haven't got the expected number of values") 

            # Now assign the data to the right data structure
            itemsize = struct.calcsize(self.dataformat)
            if not HAS_NUMPY:
                line = []
                for pixnum in range(self.ncols):
                    line.append(sequence_with_data[pixnum][0])
                # end for
            else:
                # Assume the sequence is a numpy array
                line = sequence_with_data[:, 0]
            # end if  
            if (self.__cellrepr != 'CR_INT4') and (self.__cellrepr != 'CR_UINT1'): 
                line[abs(line - self.nodatavalue) < 0.0000001] = np.nan
            mybuffer = bytearray(self.ncols * itemsize)
            struct.pack_into(self.ncols*self.dataformat, mybuffer, 0, *line)
            self.datafile.write(mybuffer)
            return True
        
        except StopIteration:
            raise StopIteration
        except ValueError as e:
            print(str(e))
            raise ValueError
        except Exception as e:
            raise IOError(str(e));

    def _is_sequence(self, arg):
        return (not hasattr(arg, "strip") and hasattr(arg, "__getitem__") or hasattr(arg, "__iter__"))
    
    @staticmethod
    def getFileExt(self):
        return Raster.getDataFileExt()
    
    def flush(self):
        self.datafile.flush();
                
    def reset(self):
        if (self.__mode[0] == 'r'):
            self.datafile.seek(256)
        super(CsfRaster, self).reset() 
      
    def get_value(self, i, k):    
        # Return the wanted value
        for _ in range(0, i): self.next(False)
        line = self.next()
        self.reset()
        return line[int(k)]
    