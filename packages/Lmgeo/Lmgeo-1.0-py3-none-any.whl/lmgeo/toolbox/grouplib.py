# Copyright (c) 2004-2020 WUR, Wageningen
import numpy as np
import lmgeo.formats.inmemoryraster as imr
from lmgeo.formats.raster import Raster
from lmgeo.formats.gridenvelope2d import GridEnvelope2D
from shapely import geometry

import shapely

__author__ = "Steven B. Hoek"

def get_ranges(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))

def get_slices(aRaster, aLineno, aRanges):
    result = []
    
    # Construct dictionaries, each having a list of row-column index pairs as well as a Shapely polygon
    for rng in aRanges:
        pixels = []
        for k in range(rng[0], rng[1]+1):
            pixels.append((aLineno, k))
        pg = create_polygon(aRaster.xll, aRaster.yll, aRaster.dx, aRaster.dy, aLineno, rng)
        myslice = {"pixels":pixels, "polygon":pg}
        result.append(myslice)   
    return result 

def create_polygon(xll, yll, dx, dy, rowidx, aRange):
    result = None
    try:
        p1 = geometry.Point(xll+aRange[0]*dx, yll+rowidx*dy)
        p2 = geometry.Point(xll+(aRange[1]+1)*dx, yll+rowidx*dy)
        p3 = geometry.Point(xll+(aRange[1]+1)*dx, yll+(rowidx+1)*dy)
        p4 = geometry.Point(xll+aRange[0]*dx, yll+(rowidx+1)*dy)
        pointList = [p1, p2, p3, p4, p1]
        result = geometry.Polygon([[p.x, p.y] for p in pointList])
    finally:
        return result
    
def clump(myraster, nodatavalue=-999):
    # Check input
    if not isinstance(myraster, Raster):
        raise Exception("Input is not a raster")
    if not isinstance(myraster, GridEnvelope2D):
        raise Exception("Input is not a grid envelope")
    
    result = None
    try:
        # Get particulars from the input 
        numpy_type = myraster.get_type()
        if numpy_type in [int, np.int, np.uint16, np.uint32, np.int16, np.int32]:
            fmt = 'i'
        else:
            raise Exception("no support for input rasters other than those with integers ")
        nrows = myraster.nrows
        ncols = myraster.ncols

        # Use them to initialise a InMemory raster
        result = imr.InMemoryRaster("C:\Temp\dummyfile.txt", None, fmt)
        if not result.open('w', ncols, nrows, myraster.xll, myraster.yll, myraster.dx, nodatavalue):
            raise Exception("Unable to initialise InMemoryRaster.")

        # Get unique values
        unique_values = []
        for i in range(myraster.nrows):
            line = myraster.next()
            for k in range(myraster.ncols):
                value = line[k]
                if not value in unique_values:
                    unique_values.append(value) 
        
        # Now start looking for the groups
        myraster.reset()
        rvpairs = []
        finished = False
        while not finished:
            for value in unique_values:
                for i in range(myraster.nrows):
                    line = myraster.next()
                    if not type(line) is np.ndarray:
                        line = np.array(line)
                        
                    # Scan the next line for occurrences
                    idx = np.where(line == value)[0]
                    if len(idx) > 0:
                        # Use the index to construct slices of consecutive pixels with this value and 
                        # vectorise these into tiny polygons
                        myranges = get_ranges(idx)
                        myslices = get_slices(myraster, i, myranges)
                        for tinypg in myslices: rvpairs.append(tinypg)
                    
                # Now merge the slices together which touch - into larger polygons. Use the functions 
                # touches and cascaded_union of Shapely. Keep an administration of the slices / pixels  
                # which belong to the polygons.
                pass
            
                # Mark those pixels in the result raster
                pass
            
            
            

            
    except Exception as e:
        errmsg = "Error in module grouplib: " + str(e)
        print(errmsg)
        raise Exception(errmsg)
    finally:
        if not result is None:
            result.reset()
        myraster.reset()
        return result
            
        