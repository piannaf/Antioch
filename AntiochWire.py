from Tkinter import *

class Wire:
    """ Defines a wire object
    
    The arguments start and end are complex numbers, width is an integer, color
    is a tkinter defined colour or valid hex string
    """
    def __init__(self, canvas, start, end, width = 1, color = "black"):
        self._canvas = canvas
        self._start = start
        self._end = end
        self._width = width
        self._color = color
        
        self._index = self._canvas.create_line(start.real, start.imag,
                                               end.real, end.imag, tags = "wire")
        
        
        if self._width > 4:
            wireWidth = 4
        else:
            wireWidth = self._width
        self._canvas.itemconfig(self._index, tags="wire", fill=color,
                                width=wireWidth)
                                
        # Set invisible bounding box
        xy = [(self._start.real - (wireWidth + 1),
               self._start.imag - (wireWidth + 1)),
              (self._end.real + (wireWidth + 1), 
               self._end.imag + (wireWidth + 1))]
               
        self._bb = self._canvas.create_rectangle(xy, outline = '',
                                                 fill = '', tags = "compBBox")
        self._canvas.addtag_withtag("Wire", self._bb)
                                               
    def start(self, start = None):
        """ A getter and setter for the starting point of a wire object
        If a start value is provided as an argument, the wire's starting point
        is set to the new value and the new value is returned. Otherwise, the 
        current value will be returned.
        
        start([complex]) -> complex
        """
        if start:
            self._start = start
        return self._start
        
    def end(self, end = None):
        """ A getter and setter for the ending point of a wire object
        If an end value is provided as an argument, the wire's ending point
        is set to the new value and the new value is returned. Otherwise, the 
        current value will be returned.
        
        end([complex]) -> complex
        """
        if end:
            self._end = end
        return self._end
        
    def width(self, width = None):
        """ A getter and setter for the width of a wire object
        If a width value is provided as an argument, the wire's width
        is set to the new value and the new value is returned. Otherwise, the 
        current value will be returned.
        
        end([int]) -> int
        """
        if width:
            self._width = width
        return self._width
        
    def color(self, color = None):
        """ A getter and setter for the color of a wire object
        If a color value is provided as an argument, the wire's color
        is set to the new value and the new value is returned. Otherwise, the 
        current value will be returned.
        
        color([string]) -> string
        """
        if color:
            self._end = end
        return self._end