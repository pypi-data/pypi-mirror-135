# Raster based on lossless webp image
# https://en.wikipedia.org/wiki/WebP
# https://developers.google.com/speed/webp/docs/webp_lossless_bitstream_specification
# https://gdal.org/drivers/raster/webp.html
from .const import Const, constants as const
from .raster import Raster
from .gridenvelope2d import GridEnvelope2D

import os.path

class WebpRaster(Raster, GridEnvelope2D):

    def __init__(self, filepath='', *args):
        pass
        
    def open(self, mode, ncols=1, nrows=1, xll=0.0, yll=0.0, cellsize=100.0, nodatavalue=-9999):
        pass
        
    def next(self, parseLine=True):
        pass
        
    def writenext(self, sequence_with_data):
        pass