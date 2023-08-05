# -*- coding: latin-1 -*-
# Copyright (c) 2004-2020 WUR, Wageningen
"""TileLib - a Python library for tiling raster data"""
from ..formats.gridenvelope2d import GridEnvelope2D
from ..formats.raster import Raster
from ..formats.inmemoryraster import InMemoryRaster
from ..toolbox.striplib import StripManager
from math import ceil
import numpy as np
import os.path

__author__ = "Steven B. Hoek"
    
class Tile(InMemoryRaster):
    rowidx = 0
    colidx = 0
    
    def __init__(self, filepath, data=None, *datatype):
        # Initialise
        InMemoryRaster.__init__(self, filepath, data, datatype)
        
'''
Below you can find the code for 2 classes: TileManager and TileStitcher, with the former capable
of creating tiles with overlapping edges and the latter capable of reconstructing an overall 
image from such tiles. To arrive again at a correctly reconstructed image, the TileStitcher 
instance needs to be invoked with the same parameters as the TileManager instance was invoked 
beforehand. For the last parameters, use the following table to get the corresponding options:

            \ bottomright_edges | topleft_edges
-------------------------------------------
no-edges     | False            | False
bottomright  | True             | False
topleft      | False            | True
allsides     | True             | True
average      | not implemented  | not implemented
'''
    
class TileManager():
    '''
    Class that retrieves enough rows of data from a given raster grid to obtain a strip
    with a given number of rows; then from that strip it produces tiles - also as a raster grid.
    Tiles are returned in the following order: from left to right and from top to bottom. 
    '''
    # Default settings
    __depth = 1
    __width = 1
    __curcol = 0
    __rowidx = -1 # actually strip index
    __colidx = -1
    __curstrip = None
    __stripmanager = None
    __rowoffset = 0 # row offset
    __coloffset = 0 # column offset
    __rowoverlap = 0
    __coloverlap = 0
    __rowbuf = None
    __colbuf = None
    __BRedges = True
    __TLedges = False
    
    def __init__(self, rg, tilewidth, tileheight, coloverlap=0, rowoverlap=0, bottomright_edges=False, topleft_edges=False):
        '''
        Initialisation of the tile manager with tile width and tile height. In addition, it can be
        indicated whether there should be column and row overlap and if so how many pixels. It can be 
        indicated whether edges should be added to the tiles: so-called bottomright on the right side 
        and at the bottom. Aim might be to make sures all delivered tiles are of the same width and 
        height. So-called topleft edges can be added also: at the top and to the left. Aim might be
        to analyse the tiles whilst avoiding "edge effects".
        
        Input variables:
        rg - raster grid which serves as the source
        tilewidth - width of the tiles to be produced
        tileheight - height of the tiles to be produced
        coloverlap - number of columns that should overlap per edge
        rowoverlap - number of lines that should overlap per edge
        bottomright_edges - edges should be added at the bottom and to the right of the tile (T/F)
        topleft_edges - edges should be added to the top and to the left of the tile (T/F)       
        '''
        # Check the inputs
        if not isinstance(rg, Raster):
            raise TypeError("Input is not a raster!")
        if not isinstance(rg, GridEnvelope2D):
            raise TypeError("Input is not a grid envelope!")
        
        # Assume: rg is a raster grid with an open file at position 0
        self.__rg = rg
        self.__xll = rg.xll
        self.__yll = rg.yll
        self.__ncols = rg.ncols
        self.__nrows = rg.nrows
        if hasattr(rg, "nbands"):
            self.__nbands = rg.nbands
        else:
            self.__nbands = 1
        self.__datatype = rg.datatype
        self.__stripmanager = StripManager(rg, tileheight)
        self.__stripmanager.stripheight = tileheight
        self.__depth = tileheight
        self.__width = tilewidth
        
        # Deal with input concerning edges and overlap
        self.__BRedges = bottomright_edges        
        self.__TLedges = topleft_edges
        if (rowoverlap < 0) or (coloverlap < 0):
            ValueError("Overlap cannot be negative!")
        if (self.__BRedges ^ self.__TLedges) and (rowoverlap > tileheight):
            raise ValueError("Overlap cannot be greater than the tile height!")
        if (self.__BRedges and self.__TLedges) and (2 * rowoverlap > tileheight):
            raise ValueError("Top and bottom edges together cannot be greater than the tile height!")
        if (self.__BRedges ^ self.__TLedges) and (coloverlap > tilewidth):
            raise ValueError("Overlap cannot be greater than the tile width!")
        if (self.__BRedges and self.__TLedges) and (2 * coloverlap > tilewidth):
            raise ValueError("Left and right edges together cannot be greater than the tile width!")
        if self.__BRedges or self.__TLedges:
            if (rowoverlap == 0) and (coloverlap == 0):
                raise Warning("Overlap indicated as zero: no edges will be added!")
                self.__BRedges = False
                self.__TLedges = False
            self.__rowoverlap = rowoverlap
            self.__coloverlap = coloverlap
        else:
            if (rowoverlap > 0) or (coloverlap > 0):
                raise Warning("No edges selected: indicated overlap will be ignored!")
            
        # Get the first strip ready
        self.nextstrip()

    def __iter__(self):
        return TileIterator(self)

    def next(self):
        '''Returns a tile with number of rows and columns'''
        # TODO: implement the option to have row and column offsets
        result = None
        maxrowno = (self.__nrows - 1)// self.__depth # no. of strips needed, zero-based
        colsleft = self.__ncols - self.__curcol
        if colsleft > self.__width:
            # Still more tiles to be written
            width = self.__width
        else:
            # Last tile of this strip 
            width = colsleft 
            
        # Local variables
        colovlp   = self.__coloverlap
        rowovlp   = self.__rowoverlap
        nodataval = self.__rg.nodatavalue
        nbands    = self.__nbands

        if (colsleft > 0) and (not self.__curstrip is None):
            # In case buffer contains rows, prepare to add them at the beginning of the output raster
            if self.__BRedges and (self.__curcol + width + colovlp <= self.__ncols):
                width += colovlp
                
            # Whatever is the case, get the data from the current strip now
            if self.__nbands == 1:
                data = self.__curstrip.data[:, self.__curcol:self.__curcol + width]
            else:
                data = self.__curstrip.data[:, :, self.__curcol:self.__curcol + width]
            
            # Check whether extra columns have to be added on the right to ensure the indicated tile width
            if self.__nbands == 1:
                width = data.shape[1]
            else:
                width = data.shape[2]
            if (width < self.__width + colovlp) and self.__BRedges:
                if self.__nbands == 1:
                    extradata = np.full((data.shape[0], self.__width + colovlp - data.shape[1]), nodataval)
                    data = np.append(data, extradata, 1)
                else:
                    extradata = np.full((nbands, data.shape[1], self.__width + colovlp - data.shape[2]), nodataval)
                    data = np.append(data, extradata, 2)
                    
            # Check whether extra columns have to be added to the left 
            if self.__TLedges:
                if self.__nbands == 1:
                    if not self.__colbuf is None:
                        extradata = self.__colbuf
                    else:
                        extradata = np.full((data.shape[0], colovlp), nodataval)
                    data = np.append(extradata, data, 1)
                else:
                    if not self.__colbuf is None:
                        extradata = self.__colbuf
                    else:
                        extradata = np.full((nbands, data.shape[1], colovlp), nodataval)
                    data = np.append(extradata, data, 2)
                    
            # Adjust the variables width and height
            if self.__nbands == 1:
                width = data.shape[1]
            else:
                width = data.shape[2]
            height = self.__curstrip.nrows
                
            # Also the coordinates of the lower left point
            if not self.__TLedges:
                xll = self.__xll + (self.__curcol * self.__rg.dx)
            else:
                xll = self.__xll + (self.__curcol - colovlp) * self.__rg.dx
            yll = self.__curstrip.yll
            
            # Check whether extra rows have to be added at the bottom
            if (self.__rowidx == maxrowno) and (height < self.__depth + self.__rowoverlap) and self.__BRedges:
                if self.__nbands == 1:
                    extradata = np.full((self.__depth - height + rowovlp, width), nodataval)
                    data = np.append(data, extradata, 0)
                else:
                    extradata = np.full((nbands, self.__depth - height + rowovlp, width), nodataval)
                    data = np.append(data, extradata, 1)
                    
                # Adjust y-coordinate and then also height of the lower left point
                yll = yll - (self.__depth - height + rowovlp) * self.__rg.dy
                height = self.__depth + rowovlp
                
            # Check whether extra rows need to be added at the top
            if self.__TLedges:
                if self.__nbands == 1:
                    if not self.__rowbuf is None:
                        if self.__curcol - colovlp < 0: 
                            # Extra columns were added on the left to the curstrip data, but not yet to the buffer
                            extradata = self.__rowbuf[:, 0:self.__curcol - colovlp + width]
                            extradata = np.append(np.full((rowovlp, colovlp), nodataval), extradata, 1)
                        else:
                            # Get the rows from the row buffer; check whether they are long enough
                            extradata = self.__rowbuf[:, self.__curcol - colovlp:self.__curcol - colovlp + width]
                            if extradata.shape[1] < width: 
                                extradata = np.append(extradata, np.full((rowovlp, width - extradata.shape[1]), nodataval), 1)
                    else:
                        extradata = np.full((rowovlp, width), nodataval)
                    data = np.append(extradata, data, 0)
                else:
                    if not self.__rowbuf is None:
                        if self.__curcol - colovlp < 0:
                            # Extra columns were added on the left to the curstrip data, but not yet to the buffer
                            extradata = self.__rowbuf[:, :, 0:self.__curcol - colovlp + width]
                            extradata = np.append(np.full((nbands, rowovlp, colovlp), nodataval), extradata, 2)
                        else:
                            # Get the rows from the row buffer; check whether they are long enough
                            extradata = self.__rowbuf[:, :, self.__curcol - colovlp:self.__curcol - colovlp + width]
                            if extradata.shape[2] < width: 
                                extradata = np.append(extradata, np.full((nbands, rowovlp, width - extradata.shape[2]), nodataval), 2)
                    else:
                        extradata = np.full((nbands, rowovlp, width), nodataval)
                    data = np.append(extradata, data, 1)
                height += rowovlp
            
            # In view of the next tile, copy some columns into the column buffer
            maxcolidx = self.__ncols // self.tilewidth
            if (self.__colidx < maxcolidx - 1) and self.__TLedges:
                tilelastcol = self.__curcol + self.__width
                if self.__nbands == 1:
                    self.__colbuf = self.__curstrip.data[:, tilelastcol - colovlp:tilelastcol]
                else:
                    self.__colbuf = self.__curstrip.data[:, :, tilelastcol - colovlp:tilelastcol]
            else:
                self.__colbuf = None
            
            # Now that we have retrieved enough particulars, prepare the result
            imr = Tile("dummy_file.ext", data, self.__datatype)
            imr.open('w', width, height, nbands, xll, yll, self.__rg.dy, nodataval)
            self.__curcol += self.__width
            self.__colidx += 1
            imr.rowidx = self.__rowidx
            imr.colidx = self.__colidx
            result = imr
        return result
    
    def nextstrip(self):
        # Initialise
        result = False
        rowbuf = None
        try:
            # If there's row overlap, keep the last few lines of the strip in 1 or 2 buffers
            rowovlp = self.__rowoverlap
            if self.__TLedges and (not self.__curstrip is None):
                # We're going to fill a buffer for use in other methods of this class 
                if self.__BRedges:
                    if self.__nbands == 1:
                        self.__rowbuf = self.__curstrip.data[-2 * rowovlp:-1 * rowovlp, :]
                    else:
                        self.__rowbuf = self.__curstrip.data[:, -2 * rowovlp:-1 * rowovlp, :]
                else:
                    if self.__nbands == 1:
                        self.__rowbuf = self.__curstrip.data[-1 * rowovlp:, :]
                    else:
                        self.__rowbuf = self.__curstrip.data[:, -1 * rowovlp:, :]
            
            if self.__BRedges and (not self.__curstrip is None):
                # We are going to fill a buffer for local use
                if self.__nbands == 1:
                    rowbuf = self.__curstrip.data[-1 * rowovlp:, :]
                else:
                    rowbuf = self.__curstrip.data[:, -1 * rowovlp:, :]
                    
            # Overlap is only counted in case of edges at the bottom and to the right
            if self.__BRedges:
                self.__curstrip = self.__stripmanager.next(rowbuf, self.__rowoverlap)
            else:
                self.__curstrip = self.__stripmanager.next(rowbuf)
            self.__curcol = 0
            self.__colidx = -1
            self.__rowidx += 1
            result = True
        except Exception as e:
            print(e)
            raise StopIteration
        finally:    
            return result

    def close(self):
        self.__rg = None
        self.__initialised = False

    @property
    def tileheight(self):
        return self.__depth

    @tileheight.setter
    def tileheight(self, tileheight):
        self.__depth = tileheight
        self.__stripmanager.stripheight = tileheight
        
    @property
    def tilewidth(self):
        return self.__width

    @tilewidth.setter
    def tilewidth(self, tilewidth):
        self.__width = tilewidth
    
    @property
    def rowoffset(self):
        return self.__rowoffset
        
    @rowoffset.setter
    def rowoffset(self, rowoffset):
        self.__rowoffset = rowoffset
        
    @property
    def coloffset(self):
        return self.__coloffset
        
    @coloffset.setter
    def coloffset(self, coloffset):
        self.__coloffset = coloffset

    @property
    def curcol(self):
        return self.__curcol
    
    @property
    def ncols(self):
        return self.__ncols

    @property
    def rowoverlap(self):
        return self.__rowoverlap
    
    @property
    def coloverlap(self):
        return self.__coloverlap
    

class TileIterator:
    ''' Class that actally makes sure that the TileManager is iterable'''
    def __init__(self, tilemanager):
        self.__tilemanager = tilemanager
    
    def __next__(self):
        # Initialise
        result = None
        
        # Determine whether another tile can be obtained from the current strip       
        curcol = self.__tilemanager.curcol
        width = self.__tilemanager.tilewidth
        ncols = self.__tilemanager.ncols
        tilesleft = ceil((ncols - self.__tilemanager.coloverlap - curcol) / width)
        if tilesleft > 0:
            result = self.__tilemanager.next()
        else:
            # Try to see whether a new strip is available
            if self.__tilemanager.nextstrip():
                result = self.__tilemanager.next()
            else:    
                raise StopIteration
        return result
    
class TileStitcher():
    '''
    Class that can join tiles together again - even if they have overlap. Assumption is that the last part 
    of the file names - before the extension - contain row and column indices which are separated by under-
    scores or another separator. Assumption is that all tiles are of the same width and height and all have
    the same overlaps.
    '''
    __ncols = 1
    __nrows = 1
    __nbands = 1 # default
    __tilewidth = 1
    __tileheight = 1
    __coloverlap = 0
    __rowoverlap = 0
    __tilelist = []
    __option = "bottomright"
    
    def __init__(self, tilewidth, tileheight, coloverlap=0, rowoverlap=0, option="no-edges"):
        '''
        Option "no-edges" is the default. In the case of option "bottomright" it is assumed that the tiles 
        have been produced by the TileManager with so-called bottomright edges. In this case values from over-
        lapping edges coming from the left and from the top are basically ignored. In other words: for the out-
        put raster, values from the tiles located to the right and below are used. For option "topleft", values 
        from the overlapping edges belonging to tiles located to the left and above are rather used instead of 
        the values belonging to the tiles located to the right and below. In case of the option "no-edges", the 
        tiles are assumed to have no overlap and are stitched together without any problems. In case of option 
        "allsides", the tiles are assumed to have been produced with edges on all sides and values from all 
        overlapping edges are ignored. Option "average" is yet to be implemented fully. Idea is that the values
        in the output raster are obtained by taking the average of all the values contained in the overlapping 
        edges. For option "average" edges are assumed to exist on all sides.
        
        Input variables:
        tilewidth - width of the tiles to be processed, without column overlap
        tileheight - height of the tiles to be processed, without row overlap 
        coloverlap - number of columns that should overlap per edge
        rowoverlap - number of lines that should overlap per edge
        option - no-edges, bottomright, topleft, allsides or average: what kind of edges do the tiles have and how to process them.
        '''
        self.__tilewidth = tilewidth
        self.__tileheight = tileheight
        if not option in ['average', 'topleft', 'bottomright', "no-edges", "allsides"]:
            raise ValueError("Invalid option: %s!" % option)
        self.__option = option
        if (coloverlap < 0) or (rowoverlap < 0):
            raise ValueError("Overlap cannot be negative!")
        if (option in ['topleft', 'bottomright']) and (rowoverlap > tileheight):
            raise ValueError("Overlap cannot be greater than the tile height!")
        if (option in ['allsides', 'average']) and (2 * rowoverlap > tileheight):
            raise ValueError("Top and bottom edges together cannot be greater than the tile height!")
        if (option in ['topleft', 'bottomright']) and (coloverlap > tilewidth):
            raise ValueError("Overlap cannot be greater than the tile width!")
        if (option in ['allsides', 'average']) and (2 * coloverlap > tilewidth):
            raise ValueError("Left and right edges together cannot be greater than the tile width!")
        if option != "no-edges":
            if (rowoverlap == 0) and (coloverlap == 0):
                raise Warning("Overlap indicated as zero: no edges will be added!")
                option = "no-edges"
        self.__coloverlap = coloverlap
        self.__rowoverlap = rowoverlap
        self.__nbands = 1
    
    def add(self, filename, separator="_"):
        '''Method for adding to the TileStitcher a tile that should be used for the stitching. It is 
        assumed that the filename follows a pattern. Not considering the file extensions, the filenames are 
        expected to end with numbers indicating the place of the tile in the mesh, i.e. by means of the zero-
        based row  and the column numbers. These numbers are separated from each other and from the rest of 
        the filename by means of separators. The default separator is an underscore "_".
        
        Input variables:
        filename - name of the image file that is storing the tile
        separator - special token that is used to separate the figures 
        '''
        # Initialise
        if not os.path.exists(filename):
            raise ValueError("File %s does not exist!" % filename)
        
        # Assume that the last 2 underscores in the filename are to separate 2-digit row and column indices (zero-based)
        basename = os.path.splitext(os.path.basename(filename))[0]
        if basename.count(separator) < 2:
            raise ValueError("Filename %s does not contain enough separator characters!" % filename)
        parts = basename.split("_")
        rowidx = int(parts[-2])
        colidx = int(parts[-1])
        self.__tilelist.append({"rowidx": rowidx, "colidx":colidx, "filename":filename})
    
    def process(self, RasterClass, datatype, outputraster):
        '''
        After all the tiles have been added, this method can be invoked with an output raster
        which is still closed!
        
        Input variables:
        RasterClass - the class that should be used for the output raster, from lmgeo.formats
        datatype - e.g. integer or float, indicated as 'i' or 'f' repectively
        outputraster - actual instance of the RasterClass that serves as output raster.
        '''
        # Check whether output raster is already open
        if (outputraster.nrows != 1) and (outputraster.ncols != 1):
            raise Warning("Output raster seems to be open already!")
        
        # Determine minimum and maximum rowidx etc.
        tmplist = [t["rowidx"] for t in self.__tilelist]
        minrowidx, maxrowidx = min(tmplist), max(tmplist)
        self.__nrows = maxrowidx - minrowidx + 1

        # Check that the list of tiles is complete 
        for i in range(self.__nrows):
            tiles = list(filter(lambda t: t["rowidx"] == i, self.__tilelist))
            if len(tiles) < (maxrowidx - minrowidx + 1):
                raise ValueError("Row of tiles with index %s is not complete!" % i)

        # Determine minimum and maximum colidx etc.
        tmplist = [t["colidx"] for t in self.__tilelist]
        mincolidx, maxcolidx = min(tmplist), max(tmplist)
        self.__ncols = maxcolidx - mincolidx + 1

        # Now loop over the tiles; in principle i and k should be zero-based
        xul, yul = 0.0, 0.0
        data = None
        nodatavalue = -9999.0
        if self.__option == "average":
            # TODO: implement! We'll need to store some values temporarily
            colbuffer = np.empty((self.__tileheight, self.__coloverlap))
            rowbuffer = np.empty((self.__rowoverlap, self.__tilewidth * self.__nrows))
            
        # Now loop over the tiles. The output raster will be written strip by strip
        for i in range(minrowidx, maxrowidx + 1):
            for k in range(mincolidx, maxcolidx + 1):
                # Get hold of the right tile
                tile = list(filter(lambda t: t["rowidx"] == i and t["colidx"] == k, self.__tilelist))[0]
                fn = tile["filename"]
                if not os.path.exists(fn): raise ValueError("File %s does not exist" % fn)
                rg = RasterClass(fn, datatype)
                rg.open('r')
                
                # Check the number of bands
                if hasattr(rg, "nbands"): nbands = rg.nbands
                else: nbands = 1
                if i == minrowidx and k == mincolidx: 
                    self.__nbands = nbands
                    print("First tile detected. It has %s bands ..." % nbands)
                else:
                    if nbands != self.__nbands: 
                        errmsg = "Tile detected with %s bands, but %s expected!" 
                        raise Exception(errmsg % (nbands, self.__nbands))

                # Check the size of the opened raster
                if self.__option == "bottomright":
                    crit1 = (rg.ncols < self.__tilewidth + self.__coloverlap)
                    crit2 = (rg.nrows < self.__tileheight + self.__rowoverlap)
                elif self.__option in ["allsides", "average"]:
                    crit1 = (rg.ncols < self.__tilewidth + 2 * self.__coloverlap)
                    crit2 = (rg.nrows < self.__tileheight + 2 * self.__rowoverlap)
                elif self.__option == "topleft":
                    crit1 = (rg.ncols < self.__tilewidth + self.__coloverlap) and (k < maxcolidx)
                    crit2 = (rg.nrows < self.__tileheight + self.__rowoverlap) and (i < maxrowidx)
                elif self.__option == "no-edges":
                    crit1 = (rg.ncols < self.__tilewidth) and (k < maxcolidx)
                    crit2 = (rg.nrows < self.__tileheight) and (i < maxrowidx)
                else:
                    raise NotImplementedError("Option %s not yet implemented!" % self.__option)
                if crit1: raise Exception("Tile represented by file %s has unexpected width!" % fn)
                if crit2: raise Exception("Tile represented by file %s has unexpected height!" % fn)
                
                # If necessary, prepare an array for the data 
                if data is None:
                    # Determine dimension of the strip which we are going to fill
                    stripheight = self.__tileheight + self.__rowoverlap
                    stripwidth  = self.__ncols * self.__tilewidth + self.__coloverlap
                    
                    # Create array
                    if self.__nbands == 1:
                        data = np.empty((stripheight, stripwidth))
                    else:
                        data = np.empty((self.__nbands, stripheight, stripwidth))

                # Initialise the array data in view of the next steps
                if (i == minrowidx) and (k == mincolidx):
                    nodatavalue = rg.nodatavalue
                    data = data.astype(rg.datatype)
                    data.fill(nodatavalue)

                # Check that the tiles will indeed land at the right place in the tile grid
                if (i == minrowidx) and (k == mincolidx):
                    # For the first tile, we determine the coordinates of the upper left corner 
                    if self.__option in ["allsides", "average"]:
                        xul, yul = rg.xll, rg.yll + (self.__tileheight + 2 * self.__rowoverlap) * rg.dy 
                    elif self.__option in ["topleft", "bottomright"]:
                        # Get the coordinates of the upper left corner        
                        xul, yul = rg.xll, rg.yll + (self.__tileheight + self.__rowoverlap) * rg.dy
                    else:
                        xul, yul = rg.xll, rg.yll + self.__tileheight * rg.dy
                else:
                    # Check whether the coordinates of the current tile are correct relative to those of the first tile
                    eps = 0.00001
                    if self.__option in ["allsides", "average"]:
                        stripheight = self.__tileheight + 2 * self.__rowoverlap
                    elif self.__option in ["topleft", "bottomright"]:
                        stripheight = self.__tileheight + self.__rowoverlap
                    else:
                        stripheight = self.__tileheight
                        
                    # The variables xul and yul have been determined in the first loop
                    xdiff = rg.xll - (k-mincolidx)*self.__tilewidth*rg.dx - xul
                    if (self.__option in ["no-edges", "topleft"]) and (rg.nrows < stripheight):
                        ydiff = rg.yll + (i-minrowidx)*self.__tileheight*rg.dy + rg.nrows*rg.dy - yul
                    else:    
                        ydiff = rg.yll + (i-minrowidx)*self.__tileheight*rg.dy + stripheight*rg.dy - yul 
                    if (xdiff > eps) or (ydiff > eps): 
                        errmsg = "Tile with row index %s and column index %s is not georeferenced correctly!"
                        raise Exception(errmsg % (i, k))

                # Add the data from the tile at the correct location in the data array
                # When there are edges at the top, we will skip those lines  
                if (i < maxrowidx): numlines = self.__tileheight
                else: numlines = self.__tileheight + self.__rowoverlap
                
                # Skip first few lines if necessary
                if self.__option in ["allsides", "topleft", "average"]:
                    for j in range(self.__rowoverlap):
                        rg.next(False)
                
                # Now loop over the remaining lines
                for j in range(numlines):
                    # Get the next line
                    line = rg.next()
                    if line is None: break
                    
                    if (self.__option == "average") and (k > mincolidx):
                        # TODO: use the data from the column buffer to do the calculations
                        pass
                    elif self.__option in ["allsides", "average"]:
                        # Chop off the first part of the line if appropriate
                        if self.__nbands == 1:
                            line = line[self.__coloverlap:]
                        else:
                            line = line[:, self.__coloverlap:]
                    elif self.__option in ["no-edges", "topleft"]:
                        # The line may not be long enough
                        if self.__nbands == 1:
                            if len(line) < self.__tilewidth:
                                line = np.append(line, np.full((self.__tilewidth - len(line)), rg.nodatavalue), axis=0)
                        else:
                            if line.shape[1] < self.__tilewidth:
                                extrapos = self.__tilewidth - line.shape[1]
                                line = np.append(line, np.full((self.__nbands, extrapos), rg.nodatavalue), axis=1)
                    
                    # Add data from the line, but leave out the data from the overlap on the right 
                    if self.__nbands == 1:
                        data[j, k*self.__tilewidth:(k+1)*self.__tilewidth] = line[0:self.__tilewidth]
                    else:
                        data[:, j, k*self.__tilewidth:(k+1)*self.__tilewidth] = line[:, 0:self.__tilewidth]
                        
                    if self.__option == "average":
                        # TODO: implement! Fill the column buffer with new data
                        if self.__nbands == 1:
                            colbuffer[j, 0:self.__coloverlap] = line[self.__tilewidth:self.__tilewidth + self.__coloverlap]
                        else:
                            pass 
                        
                # If option average has been selected, keep the values from the overlapping edge in a buffer
                if self.__option == "average":
                    # TODO: implement!
                    rg.reset()
                    for j in range(self.__rowoverlap):
                        line = rg.next()
                        if self.__nbands == 1:
                            rowbuffer[j, k*self.__tilewidth:(k+1)*self.__tilewidth] = line[0:self.__tilewidth]
                        else:
                            rowbuffer[:, j, k*self.__tilewidth:(k+1)*self.__tilewidth] = line[:, 0:self.__tilewidth]

                # When the last column is filled, write the strip to disk
                if (k == maxcolidx):
                    # When dealing with the last tile of a strip, we may add the data from the overlapping columns if appropriate
                    rg.reset()
                    ovlpcol1 = (k+1) * self.__tilewidth # first column of overlap
                    if (i < maxrowidx): numlines = self.__tileheight
                    else: numlines = self.__tileheight + self.__rowoverlap
                    for j in range(numlines):
                        line = rg.next()
                        if line is None: break
                        
                        # Chop off the first part of the line if appropriate
                        if self.__option in ["allsides", "topleft", "average"]:
                            if self.__nbands == 1:
                                line = line[self.__coloverlap:]
                            else:
                                line = line[:, self.__coloverlap:]
                        
                        if self.__nbands == 1:
                            ovlpdata = line[self.__tilewidth:self.__tilewidth + self.__coloverlap]
                            if len(ovlpdata) == 0: break
                            data[j, ovlpcol1 : ovlpcol1 + self.__coloverlap] = ovlpdata
                        else:
                            ovlpdata = line[:, self.__tilewidth:self.__tilewidth + self.__coloverlap]
                            if ovlpdata.shape[1] == 0: break
                            data[:, j, ovlpcol1 : ovlpcol1 + self.__coloverlap] = ovlpdata
                    
                    # Take appropriate action when the last tile of the first strip has been processed
                    if (i == minrowidx):
                        # First row: open the file for writing!
                        ncols = self.__ncols * self.__tilewidth + self.__coloverlap  # Note: overlap is added!
                        nrows = self.__nrows * self.__tileheight + self.__rowoverlap # Idem
                        nbands = self.__nbands
                        
                        # Current image is the last tile of the first row
                        if self.__option == "allsides":
                            xll = rg.xll - (self.__ncols - 1) * self.__tilewidth * rg.dx + self.__coloverlap * rg.dx
                        else:
                            xll = rg.xll - (self.__ncols - 1) * self.__tilewidth * rg.dx
                        if self.__option == "topleft":
                            yll = rg.yll - (self.__nrows - 1) * self.__tileheight * rg.dy - self.__rowoverlap * rg.dy
                        else:
                            yll = rg.yll - (self.__nrows - 1) * self.__tileheight * rg.dy 

                        # Open the output file, write header info and prepare for writing of the lines
                        outputraster.open('w', ncols, nrows, nbands, xll, yll, rg.cellsize, rg.nodatavalue)
                    
                    if self.__option == "average":   
                        # TODO: if option average has been selected, use data in the row buffer to do the calculations
                        # TODO in case of last tile, tileheight and / or line length may have to be adjusted
                        pass
                    
                    # Now write the lines
                    if (i < maxrowidx): numlines = self.__tileheight
                    else: 
                        numlines = self.__tileheight + self.__rowoverlap
                    for j in range(numlines):
                        if self.__nbands == 1:
                            line = data[j, :]
                        else:
                            line = data[:, j, :]
                        outputraster.writenext(line)

                # Prepare to process the next tile
                rg.close()

            # Prepare to process the next strip 
            data.fill(nodatavalue)
 
        # Clean up
        print("Finished stitching the tiles together!")
        if not outputraster is None:
            outputraster.close()
