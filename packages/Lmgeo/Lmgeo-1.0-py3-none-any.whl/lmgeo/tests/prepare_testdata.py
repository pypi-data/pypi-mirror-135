import os.path
from lmgeo.formats.asciigrid import AsciiGrid
import numpy as np
from tifffile import imread, TiffFile

__author__ = "Steven B. Hoek"

# Aim is to produce 2 *.npy files with data saved in numpy format, for use in test units
def main():
    # First prepare files with integer data
    ag = None
    try:
        fn = os.path.join('..', '..', 'geodata', 'provinces.asc')
        ag = AsciiGrid(fn, 'i')
        ag.open('r')
        
        # The following will cause that the header is written to the given file
        tmp = AsciiGrid(os.path.join('data', 'intasc.hdr'), 'i')
        tmp.open('w', ag.ncols, ag.nrows, ag.xll, ag.yll, ag.cellsize, ag.nodatavalue)
        tmp.close()
        
        # We'll now write the data to a separate file
        data = np.zeros((ag.nrows, ag.ncols), dtype=np.int)
        for i in range(ag.nrows):
            line = ag.next()
            for k in range(ag.ncols):
                data[i,k] = line[k]
                
        # We'll leave numpy to do save the file; probably the pickle format will be used
        np.save(os.path.join('data', 'intasc.npy'), data) 
    finally:
        if ag != None: ag.close()

    # Now prepare a file with float data
    f = None
    try:
        # Derive the size from the TIFF file
        fn = os.path.join('..', '..', 'geodata', 'float.tif')
        with TiffFile(fn) as tif:
            page = tif.pages[0]
            nrows = page.tags['ImageLength'].value
            ncols = page.tags['ImageWidth'].value
            
        # Also derive the data from the TIFF file; divide by 10 to get some decimals!    
        # And add some extra noise to make sure not all numbers in a line are the same
        data = imread(fn) / 10 
        for i in range(nrows):
            for k in range(ncols):
                data[i,k] = data[i,k] + k*0.005

        # Derive the geographic origin and pixel size from the world file (manipulated)
        fn = os.path.join('..', '..', 'geodata', 'float.wld')
        f = open(fn, 'r')
        lines = f.readlines()
        dx = float(lines[0].strip())
        dy = float(lines[3].strip())
        xll = float(lines[4].strip()) - 0.5*dx
        yll = float(lines[5].strip()) - (nrows - 0.5) * abs(dy) 
        
        # The following will cause that the header is written to the given file
        tmp = AsciiGrid(os.path.join('data', 'fltasc.hdr'), 'f')
        tmp.open('w', ncols, nrows, xll, yll, dx, -1)
        tmp.close()
        
        # We'll leave numpy to do save the file; probably the pickle format will be used
        np.save(os.path.join('data', 'fltasc.npy'), data)
    finally:
        if f!= None: f.close()
        
if __name__ == "__main__":
    main()