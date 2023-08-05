# Copyright (c) 2004-2020 WUR, Wageningen
import numpy as np
import lmgeo.toolbox.cliplib as cp
import lmgeo.formats.gridenvelope2d as ge
from pyproj import Proj, transform

__author__ = "Steven B. Hoek"

# Constants
eps = 0.00000001

# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. See http://www.ariel.com.au/a/python-point-int-poly.html
def point_inside_polygon(x,y,poly):
    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

def point_inside_tetragon(x,y,poly):
    # Initialise
    result = False
    
    # Determine twice two lines and check that the point lies in between them
    # TODO: the tetragon could be self-intersecting - check for this
    for cornerpairs in [[(0,1), (2,3)], [(1,2), (3,0)]]:
        params = []
        for (i, j) in cornerpairs:
            params.append(get_linear_coeffs(poly[i], poly[j]))
        result = point_between_lines(x, y, params[0], params[1])
        if not result: break
    return result      

def point_between_lines(x, y, params1, params2):
    if params1[1] == float("inf") or params2[1] == float("inf"):
        params1 = swap_axes(params1)
        params2 = swap_axes(params2)
        x, y = y, x
    y1 = params1[0] + params1[1] * x 
    y2 = params2[0] + params2[1] * x
    result = ((y1 <= y) and (y2 >= y)) or ((y1 >= y) and (y2 <= y)) 
    return result

def swap_axes(params):
    if params[1] == float("inf"): params[1] = 0.0
    else: 
        if abs(params[1]) > eps: params[1] = 1 / float(params[1])
        else: params[1] = 1 / eps
        params[0] = -1 * params[0] * params[1]
    return params
    
def get_linear_coeffs(pt1, pt2):
    dx = float(pt2[0] - pt1[0])
    if abs(dx) > eps: 
        rc = (pt2[1] - pt1[1]) / dx 
        ic = pt2[1] - rc * pt2[0]
    else: 
        rc = float("inf")
        ic = pt2[0]
    return [ic, rc] 

def snap_feature_bounds(bbox, rastergrid):
    # Initialise
    result = 4 * [0.0]

    # Now calculate the offsets - bbox has to be in the same coordinate system!
    factor = divmod(bbox[0] - rastergrid.xll, rastergrid.dx)[0]
    result[0] = rastergrid.xll + factor * rastergrid.dx
    factor = divmod(bbox[1] - rastergrid.yll, rastergrid.dy)[0]
    result[1] = rastergrid.yll + factor * rastergrid.dy
    factor = 1.0 + divmod(bbox[2] - rastergrid.xll, rastergrid.dx)[0]
    result[2] = rastergrid.xll + factor * rastergrid.dx
    factor = 1.0 + divmod(bbox[3] - rastergrid.yll, rastergrid.dy)[0]
    result[3] = rastergrid.yll + factor * rastergrid.dy
    return result

"""Avoid calling the following method for too large boundary boxes, to avoid slow performance"""
def get_mask(snapped_bbox, points, cellsize, inproj4='', outproj4=''):
    # Assume that the cellsize can be derived from the rastergrid
    xll, yll = snapped_bbox[0], snapped_bbox[1]
    dx, dy = 2 * [cellsize]
    
    # Initialise further
    ncols = int((snapped_bbox[2] - xll) / dx)
    nrows = int((snapped_bbox[3] - yll) / dy)
    result = np.zeros((nrows, ncols), dtype=np.int)
    
    try:      
        # Determine the nature of the polygon
        tetragon = False
        if len(points) == 4:
            tetragon = True
        elif len(points) == 5:
            pt1, ptn = points[0], points[-1]
            if (abs(pt1[0] - ptn[0]) < eps) and (abs(pt1[1] - ptn[1]) < eps):
                tetragon = True            
        
        # Now pass over the grid within the boundary box - punch where centroids are located
        for i in range(nrows):
            for k in range(ncols):
                centroid = (xll + (k+0.5)*dx, yll + (nrows-i-0.5)*dy)
                if tetragon:
                    result[i, k] = int(not point_inside_tetragon(centroid[0], centroid[1], points))
                else:
                    result[i, k] = int(not point_inside_polygon(centroid[0], centroid[1], points))
    except Exception as e:    
        print(e)        
    finally:
        return result

"""This is to find the index of a field in the fields of a shapefile or similar structure"""
def get_field_index(fields, srchfld):
    # Check whether the searched field is in the fields
    k = 0
    for field in fields:
        if field[0] == srchfld:
            found = True
            break
        k += 1
    if not found:
        raise ValueError("Indicated field %s is not part of the shapefile" % srchfld)
    k = k - 1 # DeletionFlag is always the first field, but is not represented in the records
    return k

def get_transformed_boundary_box(bbox, inproj4='', outproj4='', rotate=True):
    # Initialise
    result = []
    
    # Check input
    if (inproj4 == '') or (outproj4 == ''):
        raise Exception("Proj.4 string cannot be empty!")
    
    try:
        inProj = Proj(inproj4)
        outProj = Proj(outproj4)
        pt1 = (bbox[0], bbox[1]) # LL
        pt2 = (bbox[0], bbox[3]) # UL
        pt3 = (bbox[2], bbox[1]) # LR
        pt4 = (bbox[2], bbox[3]) # UR
        minx, miny = transform(inProj, outProj, pt1[0], pt1[1])
        maxx, maxy = minx, miny
        if not rotate: result.append((minx,miny))
        for pt in [pt2, pt3, pt4]:
            x, y = transform(inProj, outProj, pt[0], pt[1])
            if rotate:
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y) 
            else:
                result.append((x,y))
        if rotate:         
            result = [minx, miny, maxx, maxy] 
                
    except Exception as e:
        print("Error in method get_transformed_boundary_box of module punchlib: " + str(e))
    finally:
        return result

"""Extra functionality is that the shape and the raster can have different coordinate systems
   and the obtained values can be transformed using the supplied function f before analysis,
   i.e. in case a table is requested showing a frequency analysis. E.g. if the last digit of the 
   values are not interesting, then f could be: lambda x: divmod(x, 10)[0] """
def get_zonal_stats_record(myshape, rastergrid, stat_types, inproj4='', outproj4='', f=None, idname=''):
    # Initialise and check input
    if "TABLE" in stat_types:
        result = []
        if len(stat_types) > 1:
            msg = "A table of values and their counts cannot be generated together with other statistics."
            raise Warning(msg)
            stat_types = ["TABLE"]
    else:
        result = len(stat_types) * [0.0]  
    
    try:
        if (inproj4 != '') and (outproj4 != ''):
            # Apparently, the coordinate system is not the same for the raster and the shape
            # Convert all the points in order to be sure we get a proper boundary box and mask    
            bbox = get_transformed_boundary_box(myshape.bbox)
            points = []
            inProj = Proj(inproj4)
            outProj = Proj(outproj4)
            for pt in myshape.points:
                x, y = transform(inProj, outProj, pt[0], pt[1])
                points.append([x, y])        
        else:
            bbox = myshape.bbox
            points = myshape.points            
        
        # Now get an area of whole cells that completely cover this area
        snapped_bbox = snap_feature_bounds(bbox, rastergrid)
        
        # Mask the rastergrid
        mask = get_mask(snapped_bbox, points, rastergrid.cellsize, inproj4, outproj4)
        (nrows, ncols) = mask.shape
        (xll, yll) = snapped_bbox[0:2]
        nvlp = ge.GridEnvelope2D(ncols, nrows, xll, yll, rastergrid.cellsize, rastergrid.cellsize)  
        masked_data = cp.get_masked_clip_result(rastergrid, nvlp, mask)
        assert masked_data.size > 0, "Array with masked data has zero size!"
        
        # Now obtain the statistics
        stat = ""
        for stat in stat_types:
            value = 0.0
            if stat == "MEAN":
                value = np.mean(masked_data)
            elif stat == "MAX":
                value = np.max(masked_data)
            elif stat == "MIN":
                value = np.min(masked_data)
            elif stat == "MEDIAN":
                value = np.median(masked_data)
            elif stat == "SUM":
                value = np.sum(masked_data)
            elif stat == "STD":
                value = np.std(masked_data)
            elif stat == "TABLE":
                break
            else:
                raise ValueError("Indicated statistic not supported: " + stat)
            
        if stat != "TABLE":
            result.append(value)
        else:
            # Retrieve the values and tally them (Dutch: turven)
            # The array masked_data is a numpy masked array
            if idname == '': idname = "value"
            if f != None: masked_data = f(masked_data) 
            for i in range(nrows):
                for k in range(ncols):
                    if mask[i,k] == 1: continue
                    value = masked_data[i,k]
                    valdict = filter(lambda x: x[idname] == value, result)
                    if len(valdict) != 0: valdict[0]["count"] += 1
                    else: result.append({idname: value, "count":1}) 
            result = sorted(result, key=lambda k: k["count"]) 
            
    except Exception as e:
        print(e)
    finally:
        return result

"""For each shape we'll tally how many grid cells with values a, b etc. occur within its boundary box"""
def get_zonal_stats_as_table(shapeRecords, srchfld, rastergrid, stat_types):
    result = []
    rec = {srchfld:0}
    k = get_field_index(shapeRecords[0], srchfld)
                    
    for shpRec in shapeRecords:
        fldvalue = shpRec.record[k]
        statrec = get_zonal_stats_record(shpRec.shape, rastergrid, stat_types)
        rec[srchfld] = fldvalue
        for i in range(len(stat_types)):
            stat = stat_types[i]
            rec[stat] = statrec[i]
        result.append(rec)
    return result

def get_centroid(rastergrid, colidx, rowidx):
    result = [rastergrid.xll + (colidx+0.5)*rastergrid.dx]
    result.extend([rastergrid.yll + (rastergrid.nrows-rowidx-0.5)*rastergrid.dy])
    return result

def get_coords_from_id(rastergrid, id, startrow=0, endrow=-1):
    # Initialise
    result = None
    if endrow == -1: endrow = rastergrid.nrows - 1
    
    # The rastergrid is assumed to hold unique values
    for i in range(startrow): rastergrid.next(False)
    for i in range(startrow, endrow+1):
        line = rastergrid.next(True)
        for k in range(rastergrid.ncols):
            if line[k] == id:
                result = get_centroid(rastergrid, k, i)
                rastergrid.reset()
                return result
            else:

                if (i == endrow) and (k == rastergrid.ncols - 1):
                    if (startrow == 0):
                        # We searched everywhere but did not find
                        rastergrid.reset()
                        return result # None
                    else:
                        # We have reached the end of the file w/o success
                        rastergrid.reset()
                        result = get_coords_from_id(rastergrid, id, endrow=startrow-1)
                        return result
                        
    
    