Low-Memory GEOgraphic information system library - lmgeo

Lmgeo is a Python raster GIS library with low memory requirements. Aim is to provide software building blocks with a low-memory footprint that can be used to automate specific tasks without necessarily requiring common GIS software like ArcGIS or QGIS. 

These building blocks can be used in the following ways:
- as basis for easy-to-use GIS applications with an interface designed according to the so-called LIME approach (less is more). Non-expert users can be taught how to use such applications for recurring tasks which would otherwise require the intervention of expert users.
- as part of integrated software that deals with more than only the domain of GIS
- to automate tasks which would cause ArcGIS / QGIS to reserve a lot of memory and would slow down the execution 
- to automate tasks that are error-prone in ArcGIS - e.g. certain raster GIS operations.

The folllowing principles were used in the implementation of lmgeo:
- should work on any platform (Windows, Linux or Mac)
- the library was implemented as much as possible in pure python with as few dependencies as possible
- modular design, allowing easy replacement of components 
- a common interface for all classes dedicated to image formats
- reading, processing and writing of image data as much as possible line by line, to limit memory usage.

Supported image formats:
- ASCII grid (*.asc)
- Floating point rasters (*.flt)
- Band interleaved by line (*.bil)
- Band sequential (*.bsq)
- GeoTiff (*.tif)
- PCRaster (*.map)
- HDF5 (*.hdf5)
- NetCDF4 (*.nc4).

Dependencies:
- numpy
- pylibtiff
- PyTables
- netCDF4
- pyproj
- cython.

More documentation is in preparation. Feel free to ask if you need assistance.
