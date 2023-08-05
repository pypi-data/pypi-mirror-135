import os.path
import unittest
import numpy as np
import numpy.ma as ma
import stat
from array import array
from lmgeo.formats.csfraster import CsfRaster

__author__ = "Steven B. Hoek"

def get_dtype_from_fmtspec(fmt):
    # TODO: check this and work out further
    if fmt == 'c':
        result = np.ubyte
    elif fmt == 'h':
        result = np.int16
    elif fmt == 'H':
        result = np.uint16
    else:
        result = np.int32
    return result

class TestBaseRaster(unittest.TestCase):
    test_class = None
    int_extension = 'xxx'
    flt_extension = 'xxx'
    
    def test_int_grid(self):
        f = None
        br = None
        curdir = os.path.dirname(__file__)
        try:
            if self.test_class != None:
                # Print class name for debugging purposes
                print("Testing class " + self.test_class.__name__ + " with integers")
                
                # Test writing and reading of a grid with integer numbers; first the data
                fn = os.path.join(curdir, 'data', 'intasc.npy')
                data = np.load(fn)
                
                # Then the header
                hfn = os.path.join(curdir, 'data', 'intasc.hdr')
                f = open(hfn, 'r')
                hls = f.readlines()
                ncols = int(hls[0].replace('ncols', ''));
                nrows = int(hls[1].replace('nrows', ''));
                xll = float(hls[2].replace('xllcorner', ''));        
                yll = float(hls[3].replace('yllcorner', ''));        
                cellsize = float(hls[4].replace('cellsize', ''));        
                nodatavalue = int(hls[5].replace('NODATA_value', ''))
                
                # Get nodatavalue, minimum and maximum for the new raster
                cellrepr = None
                if (self.test_class.__name__ == 'CsfRaster'):
                    cellrepr = CsfRaster.dataformat2cellrepr('i')
                    _, _, specialnodatavalue = CsfRaster.get_min_max_nodata(None, cellrepr)
                elif (self.test_class.__name__ == 'BitmapRaster'):
                    # Assume that either minimum or maximum value has not been used yet
                    dtype = get_dtype_from_fmtspec(self.test_class.datatype)
                    if not np.iinfo(dtype).max in data: specialnodatavalue = np.iinfo(dtype).max
                    else: specialnodatavalue = np.iinfo(dtype).min
                    data[data == nodatavalue] = specialnodatavalue
                    nodatavalue = specialnodatavalue
                else: specialnodatavalue = nodatavalue
                
                # Get minimum and maximum
                mdata = ma.array(data, mask = (data == nodatavalue))
                minimum = np.min(mdata)
                maximum = np.max(mdata)
                
                # Write the file

                if (self.test_class.__name__ == 'CsfRaster'):
                    br = self.test_class(os.path.join(curdir, 'output', 'int.' + self.int_extension), 'i', minimum, maximum, cellrepr)
                    br.open('w', ncols=ncols, nrows=nrows, xll=xll, yll=yll, cellsize=cellsize, nodatavalue=specialnodatavalue, valueScale='VS_NOMINAL')
                else:    
                    br = self.test_class(os.path.join(curdir, 'output', 'int.' + self.int_extension), 'i')
                    br.open('w', ncols=ncols, nrows=nrows, xll=xll, yll=yll, cellsize=cellsize, nodatavalue=nodatavalue)
                    
                # Now loop over the data
                for i in range(nrows):
                    line = data[i, :]
                    if (self.test_class.__name__ == 'CsfRaster'):
                        line[line == nodatavalue] = specialnodatavalue
                    br.writenext(line) 
                nodatavalue = specialnodatavalue
        except Exception as e:
            print(e)  
        finally:
            if f != None: f.close()
            if br != None: br.close()
            br = None
            
        try:
            if self.test_class != None:
                # Open file for reading again
                fname = os.path.join(curdir, 'output', 'int.' + self.int_extension)
                br = self.test_class(fname, 'i')  
                br.open('r')
                self.assertEqual(nrows, br.nrows)
                self.assertEqual(ncols, br.ncols)
                self.assertEqual(xll, br.xll)
                self.assertEqual(yll, br.yll)
                self.assertEqual(cellsize, br.cellsize)
                self.assertEqual(nodatavalue, br.nodatavalue)
                if (self.test_class.__name__ == 'CsfRaster'):
                    raster_header = br.get_raster_header()
                    item = list(filter(lambda v: v['name'] == 'minVal', raster_header))[0]
                    if isinstance(item['value'], array) or isinstance(item['value'], np.ndarray):
                        self.assertEqual(item['value'][0], minimum)
                    else:
                        self.assertEqual(item['value'], minimum)
                    item = list(filter(lambda v: v['name'] == 'maxVal', raster_header))[0] 
                    if isinstance(item['value'], array) or isinstance(item['value'], np.ndarray):   
                        self.assertEqual(item['value'][0], maximum)
                    else:
                        self.assertEqual(item['value'], maximum)
                
                # Also check the values     
                for i in range(nrows):
                    line = br.next()
                    for k in range(ncols):
                        self.assertEqual(data[i,k], line[k])
                br.close()
                    
                if (self.test_class.__name__ == 'CsfRaster'):                
                    fileinfo = os.stat(fname)
                    filesize = fileinfo[stat.ST_SIZE]
                    self.assertGreater(filesize, 256, "File is too small!")
        except Exception as e:
            print(e)    
        finally:
            if br != None: br.close()   
            
    def test_flt_grid(self):         
        f = None
        br = None
        curdir = os.path.dirname(__file__) 
        try:
            if self.test_class != None:
                print("Testing class " + self.test_class.__name__ + " with floats")
                
                # Test reading and writing of a grid with float numbers; first the data
                fn = os.path.join(curdir, 'data', 'fltasc.npy')
                data = np.load(fn)
            
                # Then the header
                hfn = os.path.join(curdir, 'data', 'fltasc.hdr')
                f = open(hfn, 'r')
                hls = f.readlines()
                ncols = int(hls[0].replace('ncols', ''));
                nrows = int(hls[1].replace('nrows', ''));
                xll = float(hls[2].replace('xllcorner', ''));        
                yll = float(hls[3].replace('yllcorner', ''));        
                cellsize = float(hls[4].replace('cellsize', ''));        
                nodatavalue = float(hls[5].replace('NODATA_value', ''));
                mdata = ma.array(data, mask = abs(data - nodatavalue) < 0.0000001)
                minimum = np.min(mdata)
                maximum = np.max(mdata)
    
                # Write the file
                br = self.test_class(os.path.join(curdir, 'output', 'flt.' + self.flt_extension), 'f', minimum, maximum)
                if (self.test_class.__name__ == 'CsfRaster'):
                    br.open('w', ncols=ncols, nrows=nrows, xll=xll, yll=yll, cellsize=cellsize, nodatavalue=nodatavalue, valueScale='VS_SCALAR')
                else:
                    br.open('w', ncols=ncols, nrows=nrows, xll=xll, yll=yll, cellsize=cellsize, nodatavalue=nodatavalue)
                    
                # Now loop over the data
                for i in range(nrows):
                    line = data[i, :]
                    br.writenext(line) 
        except Exception as e:
            print(e)    
        finally:
            if f != None: f.close()
            if br != None: br.close()

        try:
            if self.test_class != None:
                # Open file for reading again
                fname = os.path.join(curdir, 'output', 'flt.' + self.flt_extension)
                br = self.test_class(fname, 'f')  
                br.open('r')
                self.assertEqual(nrows, br.nrows)
                self.assertEqual(ncols, br.ncols)
                self.assertAlmostEqual(xll, br.xll, places=3)
                self.assertAlmostEqual(yll, br.yll, places=3)
                self.assertAlmostEqual(cellsize, br.cellsize, places=3)
                self.assertAlmostEqual(nodatavalue, br.nodatavalue, places=3)
                if (self.test_class.__name__ == 'CsfRaster'):
                    raster_header = br.get_raster_header()
                    item = list(filter(lambda v: v['name'] == 'minVal', raster_header))[0]
                    if isinstance(item['value'], array) or isinstance(item['value'], np.ndarray):
                        self.assertAlmostEqual(item['value'][0], minimum, places=3)
                    else:
                        self.assertAlmostEqual(float(item['value']), minimum, places=3) 
                    item = list(filter(lambda v: v['name'] == 'maxVal', raster_header))[0]  
                    if isinstance(item['value'], array) or isinstance(item['value'], np.ndarray):
                        self.assertAlmostEqual(item['value'][0], maximum, places=3)
                    else:
                        self.assertAlmostEqual(float(item['value']), maximum, places=3) 
                
                # Also check the values 
                for i in range(nrows):
                    line = br.next()
                    for k in range(ncols):
                        if not np.isnan(line[k]): self.assertAlmostEqual(data[i,k], line[k], places=3)
                br.close()
                
                if (self.test_class.__name__ == 'CsfRaster'):                
                    fileinfo = os.stat(fname)
                    filesize = fileinfo[stat.ST_SIZE]
                    self.assertGreater(filesize, 256, "File is too small!")
        except Exception as e:
            print(e)  
        finally:
            if br != None: br.close() 


            