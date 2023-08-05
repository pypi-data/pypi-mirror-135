# Copyright (c) 2004-2020 WUR, Wageningen
import formats.inmemoryraster as imr
from formats.raster import Raster
from formats.gridenvelope2d import GridEnvelope2D
import numpy as np

__author__ = "Steven B. Hoek"

def copy_to_memory(myraster):
    # Check input
    if not isinstance(myraster, Raster):
        raise Exception("Input is not a raster")
    if not isinstance(myraster, GridEnvelope2D):
        raise Exception("Input is not a grid envelope")
    
    result = None
    try:
        # Get particulars from the input 
        numpy_type = myraster.get_numpy_type()
        mydata = np.zeros((myraster.nrows, myraster.ncols), dtype=numpy_type)
        if numpy_type in [np.int, np.uint16, np.uint32, np.int16, np.int32]:
            fmt = 'i'
        else:
            fmt = 'f'
        nrows = myraster.nrows
        ncols = myraster.ncols
        nodatavalue = myraster.nodatavalue
        
        # Use them to initialise a InMemory raster
        result = imr.InMemoryRaster("C:\dummy_folder\dummyfile.nix", mydata, fmt)
        if not result.open('w', ncols, nrows, myraster.xll, myraster.yll, myraster.dx, nodatavalue):
            raise Exception("Unable to initialise InMemoryRaster.")
        
        # Now copy the data
        for i in range(myraster.nrows):
            line = myraster.next()
            line.shape = (ncols,)
            result.data[i,:] = line

    except Exception as e:
        raise Exception("Error in module copylib: %s" + str(e))
    finally:
        result.reset()
        myraster.reset()
        return result
    