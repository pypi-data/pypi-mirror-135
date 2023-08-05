# https://gdal.org/drivers/raster/bmp.html#raster-bmp
# https://en.wikipedia.org/wiki/BMP_file_format
# http://webhelp.esri.com/arcims/9.3/General/topics/author_world_files.htm
# https://github.com/Simon3335/Python-Bitmap/tree/master/bitmap
from .const import Const, constants as const
import os.path
from array import array
import xml.dom.minidom
from .raster import Raster
from .gridenvelope2d import GridEnvelope2D
from .auxiliaryfile import AuxiliaryFile
from .worldfile import WorldFile
from math import ceil
import struct
import sys
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

__author__ = "Steven B. Hoek"

class BitmapRaster(Raster, GridEnvelope2D):
    """A raster represented by a binary file - with extension 'bmp' - so-called device-independent bitmaps or DIBs"""
    __mode          = 'r'
    dataformat      = 'i'
    datatype        = 'c'
    nbands          = 1 # default  
    __type          = 'BM'
    __colortable    = None
    __offset        = 1078   
    __compression   = -1
    __bitcount      = 8 # Possible: 1, 2, 4, 8, 16, 24 and 32 bits per pixel (bpp)
    __rowsize       = 8
    __top_to_bottom = True
    
    __BMP_HDR = [
        {'type':'char', 'name':'type', 'endpos':2},
        {'type':'I', 'name':'size', 'endpos':6},
        {'type':'I', 'name':'reserved', 'endpos':10},
        {'type':'I',  'name':'offset', 'endpos':14},
    ]
    
    __DIB_HDR = [
        {'name':'headersize', 'type':'I', 'endpos':18},
        {'name':'width', 'type':'i', 'endpos':22},
        {'name':'height', 'type':'i', 'endpos':26},
        {'name':'numbands', 'type':'h', 'endpos':28},
        {'name':'bitcount', 'type':'h', 'endpos': 30},
        {'name':'compression', 'type':'I', 'endpos':34},
        {'name':'imagesize', 'type':'I', 'endpos':38},
        {'name':'reshorizontal', 'type':'I', 'endpos':42},
        {'name':'resvertical', 'type':'I', 'endpos':46},
        {'name':'numcolors', 'type':'I', 'endpos':50},
        {'name':'dummy', 'type':'I', 'endpos':54}
    ]    

    def __init__(self, filepath='', *args):
        # Check input
        if filepath == '':
            print('File path cannot be an empty string (method __init__).')
            
        # Module wide constants
        self._const = Const()
        self._const.FILEXT = "bmp"
        
        # Initialise further
        Raster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)

        # Retrieve the name from the filepath and assign - incl. extension; idem folder
        self.name = os.path.basename(filepath);
        self.folder = os.path.dirname(filepath);
        
        # Arrange that the dataformat is set
        if len(args) > 0:
            self.dataformat = args[0]
            if self.dataformat != const.INTEGER:
                raise Exception("Unsupported data type!")
            
        if len(args) > 1:
            self.__top_to_bottom = args[1]

    # overrides same method of Raster
    def getWorldFileExt(self):
        return 'bmpw' 

    def writeheader(self, keep_original_values=False):
        # Make it easier to read the pixel values later by writing them "top to bottom"
        self.__top_to_bottom = True
        
        # Bitmap file header 
        self.__set_header_value(self.__BMP_HDR, "type", "BM")
        numcolors = self.__get_num_colors()
        size = 54 + (4 * numcolors) + abs(self.ncols * self.nrows)
        self.__set_header_value(self.__BMP_HDR, "size", size)
        self.__set_header_value(self.__BMP_HDR, "reserved", 0)
        self.__offset = 54 + 4*self.__get_num_colors()
        self.__set_header_value(self.__BMP_HDR, "offset", self.__offset)
        
        # DIB header incl. extra bit masks - assign values 
        self.__set_header_value(self.__DIB_HDR, "headersize", 40)
        self.__set_header_value(self.__DIB_HDR, "width", self.ncols)
        if self.__top_to_bottom:
            self.__set_header_value(self.__DIB_HDR, "height", self.nrows) 
        else:    
            self.__set_header_value(self.__DIB_HDR, "height", -1 * self.nrows) 
        self.__set_header_value(self.__DIB_HDR, "numbands", self.nbands) 
        self.__set_header_value(self.__DIB_HDR, "bitcount", self.__bitcount)
        self.__set_header_value(self.__DIB_HDR, "compression", 0)
        self.__set_header_value(self.__DIB_HDR, "imagesize", abs(self.ncols * self.nrows))
        self.__set_header_value(self.__DIB_HDR, "reshorizontal", 0)
        self.__set_header_value(self.__DIB_HDR, "resvertical", 0)
        self.__set_header_value(self.__DIB_HDR, "numcolors", self.__get_num_colors())
        self.__set_header_value(self.__DIB_HDR, "dummy", 0) # TODO: write no. of unique values
        
        try:
            prevpos = 0
            for header in [self.__BMP_HDR, self.__DIB_HDR]:
                for item in header:
                    buflen = int(item['endpos']) - prevpos
                    self.datatype = item['type'][0]
                    if self.datatype == 'c':                         
                        mybuffer = bytearray(buflen)
                        value = bytes(item['value'], 'ascii')
                        struct.pack_into(buflen*'b', mybuffer, 0, *value)
                    else:
                        arrlen = buflen / struct.calcsize(self.datatype)
                        mybuffer = array(self.datatype, int(arrlen) * [0])
                        mybuffer[0] = item['value']
                    self.datafile.write(mybuffer)
                    prevpos = int(item['endpos'])
            
            # Color table 
            for i in range(numcolors):
                rgba = array('B', 4 * [0])
                for j in range(3): rgba[j] = i
                self.datafile.write(rgba)
                
            # Prepare to write pixel array by filling the gap            
            prevpos += numcolors * 4
            if prevpos < self.__offset:
                self.datafile.write(array('B', (self.__offset - prevpos) * [0]))
            
            # Write a matching *.bmp.aux.xml file with a nodata value, if appropriate. Assume only a single band
            with AuxiliaryFile() as af:
                af.write(self)
                
            # Write a matching world file
            with WorldFile() as wf:
                wf.write(self) 
                
        except Exception as e:
            print("Error in method writeheader of class BitmapRaster:" + str(e))
            raise e

    def open(self, mode, ncols=1, nrows=1, xll=0.0, yll=0.0, cellsize=100.0, nodatavalue=-9999):
        assert isinstance(mode, str) and (mode[0] in ['w', 'r']), "Invalid argument for mode!"
        self.datafile = open(os.path.join(self.folder, self.name), str(mode[0]) + 'b')
        
        # Deal with the header
        if (mode[0] == 'w'):
            if self.__top_to_bottom: 
                GridEnvelope2D.__init__(self, ncols, -1 * nrows, xll, yll, cellsize, cellsize)
            else:
                GridEnvelope2D.__init__(self, ncols, nrows, xll, yll, cellsize, cellsize)
            self.cellsize = cellsize
            self.nodatavalue = nodatavalue
            self.__colortable = 256 * [4 * [0]]
            self.writeheader()
            self.flush()
        else: 
            self.readheader()
            
        # Deal with the pixel array
        if (mode == 'r'):
            if self.__top_to_bottom: self.datafile.seek(self.__offset)
            else: self.datafile.seek(self.__offset + self.nrows * self.__rowsize) 

    def readheader(self):
        # Bitmap file header 
        bmpfilehdr = self.datafile.read(14)
        bytes = bmpfilehdr[0:2] 
        header_field = (b'BM', b'BA', b'CI', b'CP', b'IC', b'PT') # Different types        
        if bytes in header_field: self.__type = bytes
        bmpsize = int.from_bytes(bmpfilehdr[2:6], byteorder='little') 
        self.__offset = int.from_bytes(bmpfilehdr[10:14], byteorder='little')        
        
        # DIB header
        dibhdr               = self.datafile.read(40)
        hdrsize              = int.from_bytes(dibhdr[0:4], byteorder='little')
        self.ncols           = int.from_bytes(dibhdr[4:8], byteorder='little')
        tmp                  = int.from_bytes(dibhdr[8:12], byteorder='little', signed=True)
        self.nrows           = abs(tmp)
        self.__top_to_bottom = (tmp < 0)
        imgplane             = int.from_bytes(dibhdr[12:14], byteorder='little') 
        self.__bitcount      = int.from_bytes(dibhdr[14:16], byteorder='little') # bits per pixel
        self.__compression   = int.from_bytes(dibhdr[16:20], byteorder='little') 
        imgsize              = int.from_bytes(dibhdr[20:24], byteorder='little')
        if self.__compression == -1: raise ValueError("Unknown compression type!")
        if self.__compression != 0: 
            method = self.get_compression_method(self.__compression)
            print("Time to implement compression method %s!" % method)
        
        # Extra bit masks  
        tmp = int.from_bytes(dibhdr[24:28], byteorder='little') 
        if tmp != 0: self.dx = 1 / tmp
        tmp = int.from_bytes(dibhdr[28:32], byteorder='little')
        if tmp != 0: self.dy = 1 / tmp
        numcolors = int.from_bytes(dibhdr[32:36], byteorder='little')
        tmp = int.from_bytes(dibhdr[36:40], byteorder='little')
        
        # Color table         
        if self.__bitcount <= 8:
            tblsize = 4 * self.__bitcount * numcolors  
            rawtable = self.datafile.read(tblsize)
            self.__colortable = []
            for i in range(numcolors):
                rgba = [0, 0, 0, 0]
                for j in range(4):
                    pos = 4*i + j
                    rgba[j] = int.from_bytes(rawtable[pos:pos+1], byteorder='little')
                self.__colortable.append(rgba)
        else:
            # Color table is normally not used when the pixels are in the 16-bit per pixel format
            self.__colortable = numcolors * [4 * [0]]
            
        # Prepare to read lines
        self.__rowsize = 4 * ceil((self.__bitcount * self.ncols) / 32)  
        
        # Check if there is a matching *.bmp.aux.xml file. If so, try to extract the nodata value
        with AuxiliaryFile() as af:
            self.nodatavalue = af.read(self)
            
        # Also check whether there is a corresponding world file 
        with WorldFile() as wf:
            wf.read(self) 
        
    def get_compression_method(self, value):
        methods = ['BI_RGB', 'BI_RLE8', 'BI_RLE4', 'BI_BITFIELDS', 'BI_JPEG', 'BI_PNG', 'BI_ALPHABITFIELDS']
        if value < len(methods): return methods[value]
        else: return -1
        
    def __set_header_value(self, header, itemname, value):
        for item in header:
            if (item['name'] == itemname):
                item['value'] = value
                return
        raise Exception("Item with name %s not found!" % itemname)
            
                
    def __get_num_colors(self):
        result = 0
        if self.__colortable != None:
            if hasattr(self.__colortable, '__len__'):
                result = len(self.__colortable)
        return result

    def next(self, parseLine=True):
        result = None;
        try:
            self.currow += 1;
            if (self.currow > self.nrows): 
                raise StopIteration("Attempt to move beyond last row.")            
            
            if self.__top_to_bottom:
                # Just get the next number of bytes
                rawline = self.datafile.read(self.__rowsize)
            else:
                # Position the cursor at the right position for this line
                pos = self.__offset + (self.nrows - self.currow) * self.__rowsize 
                self.datafile.seek(pos)
                rawline = self.datafile.read(self.__rowsize)
             
            # Process the raw line   
            result = []
            for k in range(self.ncols):                         
                result.append(rawline[k])                
                
        except Exception as e:
            print("Error: " + str(e));
            raise StopIteration
        finally:
            return result    
    
    def writenext(self, sequence_with_data):
        # Assume that the file has been written up to the position indicated by self.__offset
        # In code invoking this method, the value of __top_to_bottom must be taken into account
        dataformat = 'B' # TODO: adjust acc. to bitcount
        itemsize = struct.calcsize('B') 
        if not HAS_NUMPY:
            line = []
            for k in range(self.ncols):
                line.append(sequence_with_data[k])
        else: 
            line = sequence_with_data[:]
        mybuffer = bytearray(self.ncols * itemsize)
        struct.pack_into(self.ncols*dataformat, mybuffer, 0, *line)
        self.datafile.write(mybuffer)

    def flush(self):
        self.datafile.flush();
                
    def reset(self):
        if self.__top_to_bottom: self.datafile.seek(self.__offset)
        super(BitmapRaster, self).reset() 
      
    def get_value(self, i, k):    
        # Return the wanted value
        for _ in range(0, i): self.next(False)
        line = self.next()
        self.reset()
        return line[int(k)]