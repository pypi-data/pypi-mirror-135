__author__ = "Steven B. Hoek"

class Const:
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name]=value
      
constants = Const()
constants.BYTE = 'b'
constants.UINT8 = 'B'
constants.SHORT = 'h'
constants.UINT16 = 'H'
constants.INTEGER = 'i'
constants.UINT32 = 'I'
constants.INT64 = 'q'
constants.UINT64 = 'Q'
constants.FLOAT = 'f'
constants.DOUBLE = 'd'
constants.HEADEREXT = "hdr"
constants.WORLDFILEXT = 'wld'

constants.XLLCORNER = "XLLCORNER"  
constants.YLLCORNER = "YLLCORNER"
constants.NCOLS = "ncols"
constants.NROWS = "nrows"
constants.CELLSIZE = "cellsize"
constants.NODATA_VALUE = 'NODATA_value'
constants.BYTEORDER = 'BYTEORDER'

constants.LON = 'lon'
constants.LAT = 'lat'
constants.TIME = 'time'
constants.DESC = "DESC"
constants.ASC = "ASC"
constants.epsilon = 0.0000001
