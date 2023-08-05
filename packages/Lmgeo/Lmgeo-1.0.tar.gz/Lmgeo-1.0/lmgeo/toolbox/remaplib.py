# -*- coding: latin-1 -*-
# Copyright (c) 2004-2020 WUR, Wageningen
"""RemapLib - a Python library for remapping raster data"""
from pyproj import Proj, transform
from shapely.geometry import Polygon
from lmgeo.formats.gridenvelope2d import GridEnvelope2D
from lmgeo.formats import netcdf4raster
from lmgeo.formats.raster import Raster
from lmgeo.formats import const
from calendar import monthrange
from shutil import copyfile
from collections import OrderedDict
import csv
import logging
import os.path
import time
try:
    import numpy as np
    import pandas as pd
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

__author__ = "Steven B. Hoek"
    
# With remapping we mean converting raster data with a particular projection
# to raster data with a different projection. Cell size of the target grid
# should be approximately the same as the one of the source grid.

# Column headers for outputfile
const = const.Const()
const.srcid = 'source_id'
const.tgtid = 'target_id'
const.area  = 'area'
const.wt    ='weight'

class Pixel:
    xll = 0.0
    yll = 0.0
    dx = 1.0
    dy = 1.0
    
    def __init__(self, grid, colidx, rowidx):
        self.dx = grid.dx
        self.dy = grid.dy
        self.xll = grid.xll + colidx * self.dx
        self.yll = grid.yll + (grid.nrows - 1 - rowidx) * self.dy
        
    def get_points(self):
        points = []
        points.append((self.xll, self.yll))
        points.append((self.xll, self.yll+self.dy))
        points.append((self.xll+self.dx, self.yll+self.dy))
        points.append((self.xll+self.dx, self.yll))
        points.append(points[0])
        return points
        
    def get_polygon(self):
        # Get a shapely Polygon that represents the pixel
        points = self.get_points()
        return Polygon(points)

def calc_weights(srcgrid, srcproj, tgtgrid, tgtproj, outfn):
    # Input
    # srcgrid: the source raster, already open - with unique identifiers for each pixel
    # srcproj: projection string applicable to the source raster
    # tgtgrid: the target raster, already open - with unique identifiers for each pixel
    # tgtproj: projection string applicable to the target raster
    # outfn  : filename for the output file - should be a CSV-file
    
    # Check input
    if not isinstance(srcgrid, Raster):
        raise Exception("First argument is not a Raster!")
    if not isinstance(tgtgrid, Raster):
        raise Exception("Third argument is not a Raster!") 
    if not os.path.exists(os.path.dirname(outfn)):
        raise Exception("Fifth argument refers to non-existing path!")
        
    # Check that the pixel sizes are approximately the same for the 2 grids
    if srcproj == 'epsg:4326':
        cellsize_in_meters = srcgrid.cellsize * 20000000 / 180
    else:
        cellsize_in_meters = srcgrid.cellsize
    A = (cellsize_in_meters < 0.75 * tgtgrid.cellsize)
    B = (cellsize_in_meters > 1.25 * tgtgrid.cellsize)
    if A or B:
        msg = "Cell sizes of source and target grid differ much."
        msg += "This script may miss certain intersections!"
        raise Warning(msg)
        
    # Initialise
    outfile = None
    
    try:
        outfile = open(outfn, 'w', newline='')
        ordered_fieldnames = OrderedDict([(const.srcid,None),(const.tgtid,None),(const.area,None),(const.wt,None)])
        dw = csv.DictWriter(outfile, delimiter=',', fieldnames=ordered_fieldnames)
        dw.writeheader()
        
        # Loop over the pixels of the target grid
        for i in range(tgtgrid.nrows):
            line = tgtgrid.next()
            for k in range(tgtgrid.ncols):
                # Determine the grid code as well as the position of the centroid
                tgtid = int(line[k])
                x1, y1 = (k+0.5)*tgtgrid.dx, (tgtgrid.nrows - i - 0.5)*tgtgrid.dy
                px = Pixel(tgtgrid, k, i)
                tgtplg = px.get_polygon()
                
                # Convert the coordinates
                x2, y2 = transform(tgtproj, srcproj, x1, y1)
                
                # Now get some information about the source pixels in the neighbourhood
                srcpxlist = []
                c, r = srcgrid.getColAndRowIndex(x2, y2)
                indices = [(r-1, c-1), (r-1, c), (r-1, c+1)]
                indices.extend([(r, c-1), (r, c), (r, c+1)])
                indices.extend([(r+1, c-1), (r+1, c), (r+1, c+1)])
                
                # Loop over the pixels indicated in the list "indices"
                for idx in indices:
                    srcid = srcgrid.get_value(idx[0], idx[1])
                    px = Pixel(srcgrid, idx[1], idx[0])
                    trfpx = []
                    points = px.get_points()
                    for pt in points:
                        # Projection in opposite direction
                        x3, y3 = transform(srcproj, tgtproj, pt[0], pt[1])
                        trfpx.append((x3, y3))
                    srcplg = Polygon(trfpx)
                    
                    # Check if this source pixel intersects with the target pixel
                    if tgtplg.intersects(srcplg):
                        # If so get the overlapping area
                        area = tgtplg.intersection(srcplg).area
                        srcpxlist.append({'source_id':srcid, 'target_id':tgtid, 'area':round(area)})
                        
                # Check that the total area sums up to area of target pixel, 
                totalarea = sum(item['area'] for item in srcpxlist)
                if abs((totalarea - tgtgrid.dx * tgtgrid.dy) / (tgtgrid.dx * tgtgrid.dy)) > 1.0:
                    Warning("Sum of overlapping areas differs more than 1% from total area")
                
                # Calculate the weights and write output
                for pxdict in srcpxlist:
                    pxdict['weight'] = pxdict['area'] / totalarea
                    dw.writerow(pxdict)
                outfile.flush()
                
    finally:
        if not outfile is None: outfile.close()

'''        
# Constants and functions applicable for the methods remap and remapycon;
# adapt acc. to your needs - i.e. realise your own configuration
# and then add 'const' etc. as argument to the function calls
const.IN_FN_PREFIX = "ERA5_"
const.ID_GRID      = 'target_id'    # ID label used for the target grid
const.ID_MET_GRID  = 'source_id'    # ID label used for the source grid - e.g. for meteo data
const.VAR_NAME     = 'RR'           # Label used to indicate the meteo variable of interest
const.VAR_DESC     = "Total precipitation (06-06LT)"
const.VAR_UNITS    = "mm d-1"
const.X_RANGE      = 'x'
const.Y_RANGE      = 'y'
const.ID_OFFSET    = 2000000        # Constant used when converting ID's
const.NUM_ROWS     = 121            # Wrt. target grid
const.NUM_COLS     = 249  
const.OUT_FN_PREFIX= "ERA5_"        # String used as beginning when coining the name of the output file
const.OUT_FN_SUFFIX= "_ruk"         # String used as end when coining the name of the output file
const.DATA_DIR     = os.path.join("..", "data")
const.OUTPUT_DIR   = os.path.join("..", "temp") 
const.DEBUG        = True

def parse_id(code):
    if not isinstance(code, int): 
        raise Exception("Received identifier not an integer as expected ...")
    try:
        code = code - const.ID_OFFSET
        rowidx = (code // 1000)
        colidx = code - (rowidx*1000)
        rowidx = const.NUM_ROWS - 1 - rowidx # in case of descending ids 
        return rowidx, colidx
    except Exception as e:
        print(e)
        
# Define the function to be applied to the result of a group by 'target_id'
weighted_mean_function = lambda g: (g.RR*g.weight).sum()
'''
            
def remap(wtdf, metdf, logger, weighted_mean_function, const):
    # Initialise
    result = None
    
    try:
        # Check input
        if not isinstance(wtdf, pd.DataFrame): 
            raise Exception("First argument of method remap is not a dataframe!")
        if not isinstance(metdf, pd.DataFrame): 
            raise Exception("Second argument of method remap is not a dataframe!")
        if not callable(weighted_mean_function):
            raise Exception("Third argument should refer to a function!")
        if const is None:
            raise Exception("Last argument should not be equal to None!")

        # Realise a join
        mydf = metdf.join(wtdf, on=const.ID_MET_GRID, how='inner')
        mydf.dropna(subset=[const.ID_GRID], inplace=True)
        if const.DEBUG: 
            logger.log(logging.INFO, "Join between the 2 datasets established with success!")
    
        # Group by the target_id's and get the weighted means
        grp = mydf.groupby(const.ID_GRID)
        result = pd.DataFrame(grp.apply(weighted_mean_function), columns=[const.VAR_NAME])
        # TODO Build in a check that the weights sum up to 1.0 approximately
        
        # The weighted means are indexed by the target_id's - make sure it's a column too
        result[const.ID_GRID] = result.index
    except Exception as e:
        logger.log(logging.ERROR, e)        
    finally:
        return result

def get_date_str(year, month, day):
    return str(year) + str(month).zfill(2) + str(day).zfill(2)

def remapycon(srcgrid, wtfn, year, path_to_tpl_file, parse_id, weighted_mean_function, const):
    # Do conservative remapping of a meteorological variable for a whole year
    # Input of these meteorological data is assumed to be in NetCDF format
    # srcgrid:          the source raster, already open - with unique identifiers for each pixel
    # wtfn:             path to the file with the weights in CSV-format
    # path_to_tpl_file: NetCDF file with the right spatial extent and variable definition
    #                   already specified - i.e. a file that will be used as an output template
    # parse_id:         a Python function which translates one of the unique identifiers used
    #                   for the target grid to a row and column index 
        
    # Initialise
    wtdf = None
    metdf = None
    ncg = None
    
    # Check input
    if not isinstance(srcgrid, Raster):
        raise Exception("First argument is not a Raster!")
    if not os.path.exists(wtfn):
        raise Exception("Second argument refers to non-existing path!")
    if not os.path.exists(path_to_tpl_file):
        raise Exception("Fourth argument refers to non-existing file!")
    if not callable(parse_id):
        raise Exception("Fifth argument should refer to a function!")
    if not callable(weighted_mean_function):
        raise Exception("Sixth argument should refer to a function!")
    if const is None:
        raise Exception("Last argument should not be equal to None!")

    try:
        # Make a few constants know by a short name
        INFO = logging.INFO
        WARNING = logging.WARNING
        ERROR = logging.ERROR
        
        # Determine where the input file can be found and output should be written
        sourcedir = os.path.normpath(const.DATA_DIR)
        targetdir = os.path.normpath(const.OUTPUT_DIR)

        # Prepare for logging
        logfn =  os.path.join(targetdir, "remap_" + str(year) + ".log")
        logger = logging.getLogger(__name__)
        fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=INFO,filename=logfn,format=fmtstr)
    
        # Open the files with the weights etc.
        wtdf = pd.read_csv(wtfn)
        srcgrid.reset()
    
        # Loop over the days in this year
        for month in range(1,13):
            days = monthrange(year, month)
            for dayb0 in range(1, days[1]+1):
                t2 = time.time()
                metdf = None
                try:
                    # Open the file with meteo data for this day
                    metfn =  const.IN_FN_PREFIX + get_date_str(year, month, dayb0) + "_" + const.VAR_NAME.lower() + ".nc" 
                    metfn = os.path.join(targetdir, metfn)

                    # Prepare a structure to store results
                    mydata = np.zeros(shape=(const.NUM_ROWS, const.NUM_COLS), dtype=np.float64)
                    mydata.fill(np.nan) 
                        
                    # Now open the obtained NetCDF file
                    if not os.path.exists(metfn): logging.log(WARNING, "File %s does not exist!" % metfn)
                    else:
                        ncg = netcdf4raster.Netcdf4Raster(metfn)
                        ncg.open('r')
                        ncg._varname = const.VAR_NAME
                        
                        # Check that the 2 rasters coincide
                        if not ncg.hasSameExtent(srcgrid, 0.0007):
                            logger.log(WARNING, "The 2 rasters do not have exactly the same extent!")
                        
                        # Loop over the rows and columns
                        n = ncg.nrows * ncg.ncols
                        metdf = pd.DataFrame(index=range(n))
                        metdf[const.ID_MET_GRID] = n * [0]
                        metdf[const.VAR_NAME] = n * [0.0]
                        if const.DEBUG: 
                            logger.log(INFO, "Extra columns added with success!")
                        for i in range(ncg.nrows):
                            idline = srcgrid.next()
                            line = ncg.next()
                            idx0 = i * ncg.ncols
                            idxn = idx0 + ncg.ncols - 1
                            metdf.loc[idx0:idxn, (const.ID_MET_GRID)] = idline
                            metdf.loc[idx0:idxn, (const.VAR_NAME)] = line
                        if const.DEBUG: 
                            logger.log(INFO, "Extra columns filled with success!")
                finally:
                    if not ncg is None: ncg.close() 
                    ncg = None
                    
                try:
                    if not metdf is None:
                        # Set indices and remap!
                        metdf.set_index(const.ID_MET_GRID, inplace=True)
                        if (month == 1) and (dayb0 == 1): wtdf.set_index([const.ID_MET_GRID], inplace=True)
                        if const.DEBUG: 
                            logger.log(INFO, "Indices added with success!")
                        remapped = remap(wtdf, metdf, logger, weighted_mean_function, const)
                        if remapped is None: 
                            logger.log(ERROR, "Remapping failed for day %s/%s" % (str(dayb0), str(month)))
                        else:
                            # Add row and column indices and sort the data
                            rowidx = len(remapped)*[0]
                            colidx = len(remapped)*[0]
                            for i in range(len(remapped)):
                                rowidx[i], colidx[i] = parse_id(int(remapped[const.ID_GRID].iloc[i]))
                            remapped["ROW_INDEX"] = rowidx
                            remapped["COL_INDEX"] = colidx
                            remapped.sort_values(by=["ROW_INDEX", "COL_INDEX"], inplace=True)
                            
                            # Now assign the values to the output structure
                            for idx in range(len(remapped)):
                                j, k = remapped["ROW_INDEX"].iloc[idx], remapped["COL_INDEX"].iloc[idx]
                                mydata[j,k] = remapped[const.VAR_NAME].iloc[idx]
                            
                            # Prepare to write the output file (NetCDF)
                            fn = const.OUT_FN_PREFIX  + get_date_str(year, month, dayb0) 
                            fn = fn + const.OUT_FN_SUFFIX + ".nc" 
                            fp = os.path.join(targetdir, fn)
                            copyfile(path_to_tpl_file, fp)
                            ncg = netcdf4raster.Netcdf4Raster(fp)
                            ncg.set_xy_ranges(const.X_RANGE, const.Y_RANGE)
                            ncg.open('a', nodatavalue=-1) 
                            ncg.writeheader(const.VAR_NAME, const.VAR_DESC, const.VAR_UNITS)
                    
                            # Write the data - in reversed order: low row index -> high y
                            for j in range(const.NUM_ROWS-1, -1, -1):
                                line = mydata[j,:]
                                line.shape = (1,const.NUM_COLS)
                                ncg.writenext(line)
                        
                        # Report about the time taken
                        t3 = time.time()
                        datestr = str(dayb0) + "/" + str(month)
                        logger.log(INFO, "Total remapping for day %s took %s seconds" % (datestr, str(t3-t2)))
                        
                finally:
                    if not ncg is None: ncg.close()
                    if not srcgrid is None: srcgrid.reset()               

    except Exception as e:
        print(e)