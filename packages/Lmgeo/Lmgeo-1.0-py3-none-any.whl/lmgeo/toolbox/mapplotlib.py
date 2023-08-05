# Copyright (c) 2004-2021 WUR, Wageningen
"""MapPlotLib - a Python library with tools that help to plot maps"""
import re
# TODO: replace the following with a pure python equivalent!
# E.g. with this: https://github.com/karimbahgat/Shapy
from shapely.geometry import Polygon 
from descartes import PolygonPatch
from matplotlib.colors import LinearSegmentedColormap
import colorsys
import numpy as np

class IntervalLegend():
    intervals = []
    colors = []
    minval = 0.0 # default
    maxval = 1.0 # default
    
    def __get_min_value(self):
        result = min([cls[0] for cls in self.intervals])
        return result
        
    def __get_max_value(self):
        result = max([cls[1] for cls in self.intervals])
        return result
    
    def __init__(self, intervals, colors):
        # Process input
        self.intervals = intervals
        self.colors = colors
        
        # Check that intervals and colors match somehow
        if len(intervals) != len(colors):
            raise ValueError("Number of intervals and number of colors not the same!")
        
        # Check given intervals
        for interval in self.intervals:
            if interval[0] > interval[1]:
                raise ValueError("Invalid interval: " + str(interval))
        eps = 0.0000000001
        for i in range(len(self.intervals) - 1):
            curcls = self.intervals[i]
            nextcls = self.intervals[i+1]
            if abs(curcls[1] - nextcls[0]) > eps:
                raise ValueError("At least one gap found in given intervals!")
        
        # Check given colors
        expr = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
        for color in colors:
            if not re.search(expr, color): 
                raise ValueError("Invalid color code: " + color)

        # Finally calculate minimum and maximum values
        self.minval = self.__get_min_value()
        self.maxval = self.__get_max_value()


    def get_color(self, value):
        # Check input
        if self.minval > value or value > self.maxval: 
            raise ValueError("Index not in range [%s:%s] as expected!" % (self.minval, self.maxval)) 
            
        # Assign an appropriate color
        result = self.colors[-1]
        for cls, color in zip(self.intervals, self.colors):
            if cls[0] <= value and value < cls[1]:
                result = color
                break
        return result
    
    def get_html(self, fmt, title=""):
        result = ''
        if fmt == 'table':
            # Assume a horizontal table is required
            result += '<table cellpadding="5" border="0">\n'
            result + '<tr>\n'
            if title != '': result += '<td><strong>' + title + '</strong>&nbsp;</td>\n'
            for cls, color in zip(self.intervals, self.colors):
                result += '<td style="background:%s">%s - %s</td>\n' % (color, cls[0], cls[1])
            result += '</tr>\n'
            result += '</table>\n'
        else: raise ValueError("Format %s not implemented" % fmt)
        return result

def get_colored_patch(listwithcoords, fillcolor, edgecolor):
    # The result can be added to the current axes of a matplotlib figure by means of the method add_patch
    polygon = Polygon(np.array(listwithcoords))
    result = PolygonPatch(polygon, fc=fillcolor, ec=edgecolor, alpha=1.0)
    return result

def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    if type not in ('bright', 'soft'):
        print ('Please choose "bright" or "soft" for type')
        return
    if verbose:
        print('Number of labels: ' + str(nlabels))
    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in range(nlabels)]
        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))
        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]
        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)
    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]
        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]
        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)
    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))
        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)
        cb = colorbar.ColorbarBase(ax, cmap=random_colormap, norm=norm, spacing='proportional', ticks=None,
                                   boundaries=bounds, format='%1i', orientation=u'horizontal')
    return random_colormap