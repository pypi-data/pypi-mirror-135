from xml.dom import minidom
import os.path
from math import floor
import traceback
 
__author__ = "Steven B. Hoek" 

class AuxiliaryFile(object):
    """A helper class that can handle the common *.aux.xml files used by ArcGIS and GDAL"""
    datafile = None
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        try:
            if exc_type is not None:
                traceback.print_exception(exc_type, exc_value, tb)
                return False
            else:
                return True
        finally:
            if self.datafile is not None: self.datafile.close()            
        
    def __getpath(self, aRaster):
        result = os.path.join(aRaster.folder, aRaster.name) + ".aux.xml"
        return result
    
    def read(self, aRaster):
        result = -9999
        pathtoxml = self.__getpath(aRaster)
        if os.path.exists(pathtoxml):
            # Assume there is only a single band
            doc = minidom.parse(pathtoxml)
            nodatatag = doc.getElementsByTagName("NoDataValue")
            tmpstr = nodatatag[0].firstChild.nodeValue
            if tmpstr.find('.') != -1: result = floor(float(tmpstr))
            else: result = int(tmpstr)
        return result
    
    def write(self, aRaster):
        pathtoxml = self.__getpath(aRaster)        
        if not os.path.exists(pathtoxml):
            xmldoc = minidom.Document()               
            root = xmldoc.createElement('PAMDataset')  
            xmldoc.appendChild(root)               
            bandChild = xmldoc.createElement('PAMRasterBand') 
            bandChild.setAttribute('band', '1')               
            root.appendChild(bandChild)     
            nodataChild = xmldoc.createElement('NoDataValue') 
            bandChild.appendChild(nodataChild)
            textnode = xmldoc.createTextNode(str(aRaster.nodatavalue))
            nodataChild.appendChild(textnode) 
            xmltext = xmldoc.toprettyxml(indent ="  ")
            with open(pathtoxml, 'w') as outfile:
                outfile.write(xmltext)
        else:
            # Check if such a file already contains a NoDataValue node
            dirty = False
            with open(pathtoxml, 'r') as infile:
                xmltext = "".join(infile.readlines())
                xmltext = xmltext.replace("\n", "")
            xmldoc = minidom.parseString(xmltext)
            
            nodatatags = xmldoc.getElementsByTagName("NoDataValue")
            if len(nodatatags) != 0:
                nodatatags[0].firstChild.nodeValue = aRaster.nodatavalue
                dirty = True
            else:
                bandChildren = xmldoc.getElementsByTagName("PAMRasterBand")
                if len(bandChildren) != 0:
                    nodataChild = xmldoc.createElement('NoDataValue')             
                    bandChildren[0].appendChild(nodataChild)
                    textnode = xmldoc.createTextNode(str(aRaster.nodatavalue))
                    nodataChild.appendChild(textnode) 
                    dirty = True
            if dirty: 
                # Ensure pretty looking XML: no lines with only whitespace!
                xmltext = xmldoc.toprettyxml(indent = "  ")
                xmllist = [line for line in xmltext.splitlines() if line.strip() != ""]
                xmltext = "\n".join(xmllist)
                with open(pathtoxml, 'w') as outfile:
                    outfile.writelines(xmltext)
