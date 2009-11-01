from AntiochWire import *
from math import *

#global default dimensions
WIDTH = 40
HEIGHT = 30

class InputPin(Wire):
    """Defines a pin for a component which only allows input """
    def __init__(self, canvas, start, end, width = 1, color = "black"):
        Wire.__init__(self, canvas, start, end, width, color)
        self._canvas.addtag_withtag("input", self._index)
        self._canvas.addtag_withtag("input", self._bb)

class OutputPin(Wire):
    """Defines a pin for a component which only allows output """
    def __init__(self, canvas, start, end, width = 1, color = "black"):
        Wire.__init__(self, canvas, start, end, width, color)
        self._canvas.addtag_withtag("output", self._index)
        self._canvas.addtag_withtag("output", self._bb)
        
class Component:
    """General class for components
    
    Constructor: Component(canvas, location, widthx, height, direction, width)
        canvas specifies where to draw the component
        location places the upper-left corner of the bounding box on the canvas
        widthx and height define the dimensions of the bounding box
        direction is used in a child class for orientation of internal objects
        width specifies how many bits can pass through on input or output
            (of course one can do math on this for various purposes)
    """
    #Direction constants
    #TODO allow components to rotate in 90 degree increments
    E = 0
    S = 90
    W = 180
    N = -90

    def __init__(self, canvas, location, widthx, height, direction, width, size = None):
        
        self._canvas = canvas
        self._location = location
        self._widthx = widthx
        self._height = height
        self._direction = direction
        self._width = width
        
        #At this point, only for Logisim purposes
        self._size = size
        
        # Some useful variables
        self._xCenter = self._location + complex(self._widthx/2, 0)
        self._yCenter = self._location + complex(0, self._height/2)
        self._center = complex(self._xCenter.real, self._yCenter.imag)
        self._SEcorner = self._location + complex(self._widthx, self._height)
        
        # every part of the component gets added to the parts list
        self._parts = []
        
        # Set invisible bounding box
        xy = [(self._location.real - 2, self._location.imag - 2),
              (self._SEcorner.real + 2, self._SEcorner.imag + 2)]
        self._bb = self._canvas.create_rectangle(xy, outline = '',
                                                 fill = '', tags = "compBBox")
        self._parts.append(self._bb)
        
    def location(self, location = None):
        """A getter and setter for the location of a component.
        If the location value is provided as an argument, the component's 
        location is set to the new value and the value is returned. Otherwise, 
        the current value will be returned.
        
        location([complex]) -> complex
        """
        if location:
            self._location = location
        return self._location     
        
    def widthx(self, widthx = None):
        """A getter and setter for the widthx of a component.
        If the widthx value is provided as an argument, the component's widthx is
        set to the new value and the value is returned. Otherwise, the current
        value will be returned.
        
        widthx([int]) -> int
        """
        if widthx:
            self._widthx = widthx
        return self._widthx     
        
    def height(self, height = None):
        """A getter and setter for the height of a component.
        If the height value is provided as an argument, the component's height
        is set to the new value and the value is returned. Otherwise, the 
        current value will be returned.
        
        height([int]) -> int
        """
        if height:
            self._height = height
        return self._height
        
    def direction(self, direction = None):
        """A getter and setter for the direction of a component.
        If a valid direction value is provided as an argument, the component's 
        direction is set to the new value and the value is returned. Otherwise,
        the current value will be returned.
        
        Precondition: direction can be set to either N, S, E, or W
        
        direction([int]) -> int
        """
        if direction in [N, S, E, W]:
            self._direction = direction
        return self._direction    
        
    def width(self, width = None):
        """ A getter and setter for the width of a component
        If a width value is provided as an argument, the component's width
        is set to the new value and the new value is returned. Otherwise, the 
        current value will be returned.
        
        end([int]) -> int
        """
        if width:
            self._width = width
        return self._width
        
class MultiInSingleOut(Component):
    """ A standard class for components with multiple inputs on one side and
    a single output on the other.
    It is assumed that any such object will have at least 2 inputs and has
    initial dimensions based on the number of inputs.
    """
    def __init__(self, canvas, location, direction = E, width = 1,
                 inputs = 2, size = 1):
        """Initializes a Component instance with a certain number of inputs and 
        dimensions which are dependent on the number of inputs.
        """
        self._inputs = inputs

        if self._inputs < 2:
            raise Exception(('spam', 'eggs'))
        
        self._dimensions = self.initDimensions(inputs)
        Component.__init__(self, canvas, location, 
            self._dimensions[0], self._dimensions[1], direction, width)
            
        #Keep a record of all created inputs
        self._inputList = []
    
    def initDimensions(self, inputs):
        """ Initialize the dimensions of the component based on the number of
        inputs.
        """
        widthx = (inputs/sqrt(inputs*2))*WIDTH
        height = (inputs/sqrt(inputs*2))*HEIGHT
        return (widthx, height)
        
    def inputPins(self):
        """ Creates input pins which are placed equidistant from each other and
        centered on the component edge.
        They are then saved to private lists to be worked with in a simulation
        environment.
        """
        dy = float(self._height)/(self._inputs + 1)
        for n in range(1,self._inputs + 1):
            start = self._location + complex(0,n*dy)
            end = start + complex(self._widthx/8.0, 0)
            inputID = InputPin(self._canvas, start, end, self._width)
            self._inputList.append(inputID)
            self._parts.append(inputID)
            
    def outputPin(self):
        """Creates an output pin which is centered on the component edge.
        It is then saved into a private variable for use in a simulation
        environment.
        """
        start = self._yCenter + complex(self._widthx*7/8.0, 0)
        end = self._yCenter + complex(self._widthx)
        self._output = OutputPin(self._canvas, start, end, self._width)
        self._parts.append(self._output)
        
class MultiInSingleOutNot(MultiInSingleOut):
    """ Extends the parent class to add a bubble at the output """
    
    def bubble(self):
        """ Draws a bubble before the output pin """
        #should always stay a circle centered with respect to height
        NW = self._yCenter + complex(self._widthx * 6/8.0, 
                                     -self._widthx * 1/16.0)
        SE = self._yCenter + complex(self._widthx* 7/8.0, self._widthx* 1/16.0)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        bubbleID = self._canvas.create_oval(xy)
        self._parts.append(self._output)