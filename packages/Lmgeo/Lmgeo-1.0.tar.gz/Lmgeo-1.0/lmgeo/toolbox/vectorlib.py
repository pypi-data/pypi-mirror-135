"""VectorLib - a Python library for representing and handling vector based spatial data"""
from math import sqrt, copysign
from delaunay_triangulation.triangulate import delaunay
from delaunay_triangulation import typing
import warnings

def distance(xy1, xy2):
    # Be prepared to handle sequenced coordinates as well as x & y attributes
    if hasattr(xy1, "__len__") and hasattr(xy2, "__len__"):
        xdist, ydist = xy1[0] - xy2[0], xy1[1] - xy2[1]
    elif hasattr(xy1, "x") and hasattr(xy1, "y") and hasattr(xy2, "x") and hasattr(xy2, "y"):
        xdist, ydist = xy1.x - xy2.x, xy1.y - xy2.y
    result = sqrt(xdist**2 + ydist**2)
    return result

class Triangle(object):
    __points = []
    
    def __init__(self, points):
        # Check input - be prepared to handle input in different forms
        if hasattr(points, "__len__"):
            if len(points) != 3: raise ValueError("Sequence of length 3 expected!")
        else:
            if not hasattr(points, "__getitem__"): ValueError("Indexed object expected!")
        try:
            for i in range(3):
                if (not hasattr(points[i], "x")) or (not hasattr(points[i], "y")): 
                    raise ValueError("Attributes x and y expected!")
        except Exception as e:
            print(e)
        finally:
            self.__points = points

    def area(self):
        # Calculate the length of the sides
        a = distance(self.__points[0], self.__points[1])
        b = distance(self.__points[1], self.__points[2])
        c = distance(self.__points[0], self.__points[2])
        
        # Now we'll use Heron's formula
        s = (a + b + c) / 2 # semi-perimeter
        result = sqrt(s * (s - a) * (s - b) * (s - c))
        return result
        
    def centroid(self):
        # Validate input
        if hasattr(self, "__len__"): 
            assert len(self.__points) == 3, "Triangle must have 3 corners!" 
        
        # Calculate the centroid by averaging the coordinates
        if hasattr(self.__points[0], "__len__"):
            xc = sum([pt[0] for pt in self.__points]) / 3
            yc = sum([pt[1] for pt in self.__points]) / 3
        elif hasattr(self.__points[0], "x") and hasattr(self.__points[0], "y"):
            xc = sum([pt.x for pt in self.__points]) / 3
            yc = sum([pt.y for pt in self.__points]) / 3
        return xc, yc

# TODO: develop this class 
class Polygon(object):
    __vertices = []
     
    def __init__(self, vertices):
        pass
         
    def area(self):
        pass
     
    def contains_point(self, point):
        # For the meantime, use method contains_points from class Path found in matplotlib.path
        pass
        
    def triangles(self):
        # Carry out a Delaunay triangulation to split up the polgon into triangles
        pass
        
    def centroid(self):
        pass
    
class ShapeRecords(list):
    def __init__(self):
        pass

class SimplePoint(object):
    x = None
    y = None
    
    def __init__(self, x, y):
        self.x = x
        self.y = y   
        
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __repr__(self):
        return self.__str__()

class SimpleShape(object):
    # TODO: things may not work in case of island polygons
    # Points either have x and y attributes or are sequences of length 2 
    shape = None
    def __init__(self):
        self.shape = InnerShape()
        
    def get_point_series(self):
        result = []
        for i in range(len(self.shape.parts)):
            points = []
            i_start = self.shape.parts[i]
            if i==len(self.shape.parts)-1:
                i_end = len(self.shape.points)
            else:
                i_end = self.shape.parts[i+1]
            for i in self.shape.points[i_start:i_end]:
                pt  = SimplePoint(i[0], i[1])
                points.append(pt)
            result.append(points)
        return result 
    
    def get_simplified_coords(self):
        # TODO: use Ramon-Douglas-Peucker algorithm to simplify the shape 
        # from rdp import rdp
        raise NotImplementedError("Not implemented yet!")
        return []
        
    # Simple method for estimating centroid    
    def get_dirty_centroid(self):
        points = sum(self.get_point_series(), [])
        x_coords = [p.x for p in points]
        y_coords = [p.y for p in points]
        _len = len(x_coords)
        return [sum(x_coords)/_len, sum(y_coords)/_len]
    
    def get_centroid(self)  -> typing.Vertex:
        result = (-1.0, -1.0)
        try:
            # Get all the points and then do the triangulation
            points = sum(self.get_point_series(), [])
            triangles = delaunay([typing.Vertex(p.x, p.y) for p in points])
    
            # Now loop over the triangles
            total_area = total_xweighted = total_yweighted = 0.0
            for tr in triangles:
                mytr = Triangle(tr)
                centroid = mytr.centroid()
                if self.contains_point(centroid):
                    area = mytr.area()
                    total_area += area
                    total_xweighted += centroid[0] * area 
                    total_yweighted += centroid[1] * area
            result = typing.Vertex(total_xweighted / total_area, total_yweighted / total_area)
            
        except Exception as e:
            print(e)
        finally:
            return result
        
    def get_nearest_point(self, otherpoint) -> typing.Vertex:
        # Validate input
        if hasattr(otherpoint, "__len__"): x0, y0 = otherpoint[0], otherpoint[1]
        elif hasattr(otherpoint, "x") and hasattr(otherpoint, "y"): x0, y0 = otherpoint.x, otherpoint.y
        
        # Get the 2 points that are nearest to the other point
        pt1, pt2 = self.get_nearest_edge_points(otherpoint)
        
        # Determine a line through the otherpoint perpendicular to the line through these points
        line1 = typing.get_standard_line(typing.Vertex(pt1[0], pt1[1]), typing.Vertex(pt2[0], pt2[1]))
        if line1.B == 0: result = typing.Vertex(pt1[0], y0) 
        elif line1.A == 0: result = typing.Vertex(x0, pt1[1])
        else: 
            line2 = self.get_plumb_line(line1, otherpoint)
            result = typing.get_line_intersection(line1, line2)
        
        # Check that the result lies on the edge of the polygon
        A = (min(pt1[0], pt2[0])) <= result.x and (max(pt1[0], pt2[0]) >= result.x)
        B = (min(pt1[1], pt2[1])) <= result.y and (max(pt1[1], pt2[1]) >= result.y)
        if (not A) and (not B):
            # The intersection point is on the line but outside the x- and y-range 
            result = typing.Vertex(pt1[0], pt1[1]) # Still nearest point
        return result 
    
    def get_nearest_edge_points(self, otherpoint) -> (typing.Vertex, typing.Vertex):
        # Process input
        if hasattr(otherpoint, "__len__"): x0, y0 = otherpoint[0], otherpoint[1]
        elif hasattr(otherpoint, "x") and hasattr(otherpoint, "y"): x0, y0 = otherpoint.x, otherpoint.y
        
        # Get 2 points of the polygon that are near to the given point, on both sides
        points = sum(self.get_point_series(), [])
        n = len(points)
        mydicts = [{"point":(p.x, p.y), "distance":distance((p.x,p.y), (x0,y0)), "index":i} for i, p in zip(range(n), points)]
        sorted_points = sorted(mydicts, key=lambda p: p['distance'])
        
        # We assume that this is the nearest point, but there may even be a line through points further away that runs closer by:
        spt1 = sorted_points[0] 
        pt1 = spt1["point"]
        
        # The 2 nearest points are not necessarily the right ones. Which line starting / ending in pt1 runs closest by?
        for j in [-1, 1]:
            spt2 = list(filter(lambda p: p["index"] == spt1["index"]+j, mydicts))[0]
            pt2 = spt2["point"]
            line = typing.get_standard_line(typing.Vertex(pt1[0], pt1[1]), typing.Vertex(pt2[0], pt2[1]))
            if line.A != 0:
                plumb_line = self.get_plumb_line(line, otherpoint)
                edgepoint = typing.get_line_intersection(line, plumb_line)
            else:
                edgepoint = typing.Vertex(x0, pt1[1])
            A = (min(pt1[0], pt2[0])) <= edgepoint.x and (max(pt1[0], pt2[0]) >= edgepoint.x)
            B = (min(pt1[1], pt2[1])) <= edgepoint.y and (max(pt1[1], pt2[1]) >= edgepoint.y)
            if A and B: break
        return typing.Vertex(pt1[0], pt1[1]), typing.Vertex(pt2[0], pt2[1])
    
    def get_plumb_line(self, line, point) -> typing.StandardLine:
        # Validate / process input
        if line.A == 0: raise ValueError("Line without slope not allowed as input!")
        if hasattr(point, "__len__"):
            x0, y0 = point[0], point[1]
        elif hasattr(point, "x") and hasattr(point, "y"):
            x0, y0 = point.x, point.y
        
        # Determine a line perpendicular to the given line which  passes through the given point
        intercept = y0 - (line.B / line.A) * x0 
        result = typing.StandardLine(-1 * line.B / line.A, 1.0, intercept)
        return result  
    
    def get_area(self):
        # Get all the points and then do the triangulation
        points = sum(self.get_point_series(), [])
        triangles = delaunay([typing.Vertex(p.x, p.y) for p in points])

        # Now loop over the triangles
        result = 0.0
        for tr in triangles:
            mytr = Triangle(tr)
            centroid = mytr.centroid()
            if self.contains_point(centroid):
                result += mytr.area()
        return result
    
    def contains_point(self, point):
        # Initialise
        if hasattr(point, "__len__"): x, y = point[0], point[1] 
        else: x, y = point.x, point.y
        poly = [(p.x, p.y) for p in sum(self.get_point_series(), [])]
        n = len(poly)
        result = False
    
        # Loop over the points
        p1x, p1y = poly[0]
        for i in range(n+1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / float((p2y - p1y)) + p1x
                        if p1x == p2x or x <= xinters:
                            result = not result
            p1x, p1y = p2x, p2y
        return result 
    
    def get_point_inside(self, edgepoint, distance) -> typing.Vertex:
        # Initialise
        result = None
        
        # Validate input
        try:
            if distance <= 0.0: raise ValueError("Invalid value for distance!")
            if hasattr(edgepoint, "__len__"): x, y = edgepoint[0], edgepoint[1] 
            else: x, y = edgepoint.x, edgepoint.y
            
            # Get the nearest 2 edge points of the polygon and check that the point lies on the edge of the polygon
            pt1, pt2 = self.get_nearest_edge_points(edgepoint)
            eps = 0.0000000001
            if abs(pt1.x - pt2.x) < eps and abs(pt1.y - pt2.y) < eps: # TODO: find a good way to handle this
                raise ValueError("Two consecutive points of the shape are located too close to each other!")
            A = (min(pt1[0], pt2[0]) <= x) and (max(pt1[0], pt2[0]) >= x)
            B = (min(pt1[1], pt2[1]) <= y) and (max(pt1[1], pt2[1]) >= y)
            if not (A and B): warnings.warn("It seems that the given point is not located on the nearest edge!")
            
            # Make sure a point inside the shape is found that is distance away from the edge
            line1 = typing.get_standard_line(typing.Vertex(pt1[0], pt1[1]), typing.Vertex(pt2[0], pt2[1]))
            if line1.A == 0:
                if self.contains_point((x, y + distance)): result = typing.Vertex(x, y + distance)
                else: result = typing.Vertex(x, y - distance)
            else:
                line2 = self.get_plumb_line(line1, edgepoint)
                slope = line2.A / line2.B
                dx = distance / sqrt(1 + slope**2)
                dy = slope * dx
                if self.contains_point((x + dx, y + dy)): result = typing.Vertex(x + dx, y + dy)
                else: result = typing.Vertex(x - dx, y - dy)
                    
        except Exception as e:
            print(e)
        finally:
            return result
        
class InnerShape(object):
    # A list called parts holds index which indicates the point of next part
    # A list called points holds list / array with only 2 places
    bbox = None
    parts = None
    points = None
    def __init__(self):
        self.bbox = 4*[0.0]
        self.parts = []
        self.points = []
        