"""VclipLib - a Python library for clipping from vector based spatial data"""
from array import array
from enum import Enum
from .vectorlib import ShapeRecords, SimpleShape

class HLocation(Enum):
    HBETWEEN = 1
    LEFT = 2
    RIGHT = 3
    
class VLocation(Enum):
    VBETWEEN = -1
    BELOW = -2
    ABOVE = -3
    
def Locate(x, y, bbox):
    result = [HLocation.HBETWEEN, VLocation.VBETWEEN]
    if len(bbox) != 4: raise Exception('Invalid boundary box found!')
    if (x<=bbox[0]): result[0] = HLocation.LEFT
    elif (x>=bbox[2]): result[0] = HLocation.RIGHT
    if (y<=bbox[1]): result[1] = VLocation.BELOW
    elif (y>=bbox[3]): result[1] = VLocation.ABOVE
    return result

def get_clip_result(shpRecs, bbox):
    # Get a simplified copy of each record, with its shape and the parts and points thereof
    # TODO make it possible to omit bbox
    simpleRecords = ShapeRecords()
    for record in shpRecs:
        k = 0
        simpleShape = SimpleShape()
        for i in range(len(record.shape.parts)):
            i_start = record.shape.parts[i]
            if i==len(record.shape.parts)-1:
                i_end = len(record.shape.points)
            else:
                i_end = record.shape.parts[i+1]
                
            # Loop over the points now in this part
            if len(simpleShape.shape.parts) == 0: simpleShape.shape.parts.append(int(0))
            xp, yp = 0.0, 0.0
            for pt in record.shape.points[i_start:i_end]:
                # Point is located within bbox
                loc = Locate(pt[0], pt[1], bbox)
                if (loc[0] == HLocation.HBETWEEN) and (loc[1] == VLocation.VBETWEEN):
                    newpt = array('f', [float(pt[0]), float(pt[1])])
                    simpleShape.shape.points.append(newpt)
                    xp = pt[0]
                    yp = pt[1]
                    k += 1
                else:
                    # Check whether the current part has already been copied partially
                    if (xp == 0.0) and (yp == 0.0): continue
                    
                    # Add a point on the edge and break out of this loop
                    newpt = None
                    if (loc[0] == HLocation.HBETWEEN) or (loc[1] == VLocation.VBETWEEN):
                        # Point is located beyond only one edge
                        if loc[0] == HLocation.LEFT:
                            y = yp + ((pt[1] - yp) * (bbox[0] - xp) / (pt[0] - xp))
                            newpt = array('f', [float(bbox[0]), float(y)])
                        elif loc[0] == HLocation.RIGHT:
                            y = yp + ((pt[1] - yp) * (bbox[2] - xp) / (pt[0] - xp))
                            newpt = array('f', [float(bbox[2]), float(y)])
                        elif loc[1] == VLocation.ABOVE:
                            x = xp + ((pt[0] - xp) * (bbox[3] - yp) / (pt[1] - yp))
                            newpt = array('f', [float(x), float(bbox[3])])
                        elif loc[1] == VLocation.BELOW:
                            x = xp + ((pt[0] - xp) * (bbox[1] - yp) / (pt[1] - yp))
                            newpt = array('f', [float(x), float(bbox[1])]) 
                    else:
                        # Point is located in quadrant beyond 1 of the corners of the bbox
                        if (loc[0] == HLocation.LEFT) and (loc[1] == VLocation.ABOVE):
                            newpt = array('f', [float(bbox[0]), float(bbox[3])])
                        elif (loc[0] == HLocation.RIGHT) and (loc[1] == VLocation.ABOVE):
                            newpt = array('f', [float(bbox[2]), float(bbox[3])])
                        elif (loc[0] == HLocation.LEFT) and (loc[1] == VLocation.BELOW):
                            newpt = array('f', [float(bbox[0]), float(bbox[1])])
                        elif (loc[0] == HLocation.RIGHT) and (loc[1] == VLocation.BELOW):
                            newpt = array('f', [float(xp), float(bbox[3])]) 
                    if newpt != None: 
                        simpleShape.shape.points.append(newpt)
                        k += 1   
                        
                    # Assume that the rest of this part does not coincide with bbox
                    break
            
            # After looping through the points of this part, check whether it should be added
            if (k>0) and (k not in simpleShape.shape.parts): 
                simpleShape.shape.parts.append(int(k))
        
        # Add simpleShape to result if relevant
        if len(simpleShape.shape.parts) > 1: simpleRecords.append(simpleShape)
        simpleShape = None
        
    return simpleRecords

def get_simple_copy(shpRecs):
    # Only copy the _Shape part from the shpRecs 
    # So forget about the info originating from the dbf!
    simpleRecords = ShapeRecords()
    for record in shpRecs:
        simpleShape = SimpleShape()
        for part in record.shape.parts:
            simpleShape.shape.parts.append(int(part))
        for pt in record.shape.points:
            newpt = array('f', [float(pt[0]), float(pt[1])])
            simpleShape.shape.points.append(newpt)
        simpleRecords.append(simpleShape)
        simpleShape = None
    return simpleRecords

def idealise(shpRec):
    # For every part in the _Shape part of shpRec create a simpleShape
    # with simplified geographical features
    simpleShape = SimpleShape()
    for part in shpRec.shape.parts: 
        # Why not use Ramon-Douglas--Peucker algorithm implemented in package rdp???
        
        # Create an in memory raster that covers this part
        
        # First get a boundary box
        
        # For every centre point of the raster check whether it's inside the polygon
        
        # If so, mark the raster as selected in a 2D boolean array
        
        # Draw a new polygon, from one corner of the raster to the next 
        
        # Add to the simple shape
        pass
    
    # Return the result as a simple shape
    return simpleShape

