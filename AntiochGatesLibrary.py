from AntiochComponent import *

class NOT_Gate(Component):
    """ Creates a canvas object with the shape of a standard NOT Gate 
    
    Constructor: NotGate(Canvas, complex, string, [int], [int])
    """
    
    #dimension keyword exists for compatability. Antioch originally used
    #"dimension" to specify the size of the NOT Gate however, Logisim uses 
    #"size"
    def __init__(self, canvas, location, dimension = None,
                 direction = E, width = 1, size = 1):
        
        NARROW = (WIDTH - 10,HEIGHT - 10)
        WIDE = (WIDTH,HEIGHT - 10)
        
        if dimension == "narrow" or size == 20:
            Component.__init__(self, canvas, location, NARROW[0], 
                               NARROW[1], direction, width)
        elif dimension == "wide" or size == 30:
            Component.__init__(self, canvas, location, WIDE[0], 
                               WIDE[1], direction, width)
        else:
            raise Exception('spam', 'eggs')

        self.canvas = canvas
        
        
        self.canvas.addtag_withtag("{'lib':'1', 'name':'NOT Gate'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'width': width, \
                                        'size': size}), self._bb)
        
        self.inputPin()
        self.triangle()
        self.bubble()
        self.outputPin()
    
    def inputPin(self):
        start = self._yCenter
        end = self._yCenter + complex(self._widthx/8.0, 0)
        self._input = InputPin(self._canvas, start, end, self._width)
                                              
    def outputPin(self):
        start = self._yCenter + complex(self._widthx*7/8.0, 0)
        end = self._yCenter + complex(self._widthx)
        self._output = OutputPin(self._canvas, start, end, self._width)
    
    def border(self):
        NW = self._location
        NE = self._location + complex(self._widthx, 0)
        SE = self._location + complex(self._widthx, self._height)
        SW = self._location + complex(0, self._height)
        
        xy = [(NW.real, NW.imag),(NE.real, NE.imag), 
              (SE.real, SE.imag),(SW.real, SW.imag)]
        
        self._canvas.create_polygon(xy, outline = "black", fill="")
        
    def triangle(self):
        NW = self._location + complex(self._widthx/8.0, 0)
        E = self._center + complex(self._widthx*2/8.0,0)
        SW = self._location + complex(self._widthx/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (E.real, E.imag), (SW.real, SW.imag)]
        self._canvas.create_polygon(xy, outline = "black", fill="")
        
    def bubble(self):
        #should always stay a circle centered with respect to height
        NW = self._yCenter + complex(self._widthx * 6/8.0, 
                                     -self._widthx * 1/16.0)
        SE = self._yCenter + complex(self._widthx* 7/8.0, self._widthx* 1/16.0)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        self._canvas.create_oval(xy)
        
class Buffer(Component):
    """ Creates a canvas object with the shape of a standard Buffer Gate 
    
    Constructor: NotGate(canvas, complex, [int], [int])
    """
    
    def __init__(self, canvas, location, direction = E, width = 1):
        Component.__init__(self, canvas, location, WIDTH - 10, HEIGHT - 10, 
                           direction, width)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'1', 'name':'Buffer'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'width': width}), self._bb)
    
        self.inputPin()
        self.outputPin()
        self.triangle()
        
    def inputPin(self):
        start = self._yCenter
        end = self._yCenter + complex(self._widthx/8, 0)
        self._input = InputPin(self._canvas, start, end, self._width)
                                              
    def outputPin(self):
        start = self._yCenter + complex(self._widthx*7/8.0, 0)
        end = self._yCenter + complex(self._widthx)
        self._output = OutputPin(self._canvas, start, end, self._width)
                                                
    def triangle(self):
        NW = self._location + complex(self._widthx/8, 0)
        E = self._yCenter + complex(self._widthx* 7/8.0,0)
        SW = self._location + complex(self._widthx/8, self._height)
        
        xy = [(NW.real, NW.imag), (E.real, E.imag), (SW.real, SW.imag)]
        self._canvas.create_polygon(xy, outline = "black", fill="")
       
class AND_Gate(MultiInSingleOut):
    """ Creates a canvas object with the shape of a standard AND Gate
    
    Constructor: AndGate(canvas, complex, keywords)
        Valid keywords: direction, width, inputs
    """
    def __init__(self, canvas, location, direction = E, width = 1,
                 inputs = 2, size = None):
        MultiInSingleOut.__init__(self, canvas, location, 
            direction, width, inputs)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'1', 'name':'AND Gate'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'width': width, \
                                        'size': size, 'inputs': inputs}), self._bb)

        self.inputPins()
        self.outputPin()
        self.body()
    
    def body(self):
        # left side is an open box
        NE = self._xCenter
        NW = self._location + complex(self._widthx/8.0,0)
        SW = NW + complex(0, self._height)
        SE = NE + complex(0, self._height)
        
        xy = [(NE.real, NE.imag),(NW.real, NW.imag), 
              (SW.real, SW.imag),(SE.real, SE.imag)]
        
        self._canvas.create_line(xy)
        
        # right side is an arc
        SE = SW + complex(self._widthx*6/8.0, 0)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=270, extent=180, style=ARC)
       
class OR_Gate(MultiInSingleOut):
    """ Creates a canvas object with the shape of a standard OR Gate
    
    Constructor: OrGate(canvas, complex, keywords)
        Valid keywords: direction, width, inputs
    """
    def __init__(self, canvas, location, direction = E, width = 1,
                 inputs = 2, size = None):
        MultiInSingleOut.__init__(self, canvas, location, 
            direction, width, inputs)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'1', 'name':'OR Gate'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'width': width, \
                                        'size': size, 'inputs': inputs}), self._bb)
            
        self._inputList = []
        self.inputPins()
        self.outputPin()
        self.body()
    
    def body(self):
        # left side is a narrow arc
        NW = self._location - complex(self._widthx/8.0,0)
        SE = self._location + complex(self._widthx/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=270, extent=180, style=ARC)
        
        # right side is half an oval
        NW = self._location - complex(self._widthx, 0)
        SE = self._location + complex(self._widthx*7/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=275, extent=170, style=ARC)
       
class NAND_Gate(MultiInSingleOutNot):
    """ Creates a canvas object with the shape of a standard NAND Gate
    
    Constructor: NandGate(canvas, complex, keywords)
        Valid keywords: direction, width, inputs
    """
    def __init__(self, canvas, location, direction = E, width = 1,
                 inputs = 2, size = None):
        MultiInSingleOut.__init__(self, canvas, location, 
            direction, width, inputs)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'1', 'name':'NAND Gate'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'width': width, \
                                        'size': size, 'inputs': inputs}), self._bb)

        self.inputPins()
        self.outputPin()
        self.body()
        self.bubble()
    
    def body(self):
        # left side is an open box
        NE = self._xCenter - complex(self._widthx/8.0,0)
        NW = self._location + complex(self._widthx/8.0,0)
        SW = NW + complex(0, self._height)
        SE = NE + complex(0, self._height)
        
        xy = [(NE.real, NE.imag),(NW.real, NW.imag), 
              (SW.real, SW.imag),(SE.real, SE.imag)]
        
        self._canvas.create_line(xy)
        
        # right side is an arc
        NW = NW - complex(self._widthx/8.0, 0)
        SE = SW + complex(self._widthx*5/8.0, 0)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=270, extent=180, style=ARC)
       
class NOR_Gate(MultiInSingleOutNot):
    """ Creates a canvas object with the shape of a standard NOR Gate
    
    Constructor: NorGate(canvas, complex, keywords)
        Valid keywords: direction, width, inputs
    """
    def __init__(self, canvas, location, direction = E, width = 1,
                 inputs = 2, size = None):
        MultiInSingleOut.__init__(self, canvas, location, 
            direction, width, inputs)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'1', 'name':'NOR Gate'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'width': width, \
                                        'size': size, 'inputs': inputs}), self._bb)
            
        self._inputList = []
        self.inputPins()
        self.outputPin()
        self.body()
        self.bubble()
    
    def body(self):
        # left side is a narrow arc
        NW = self._location - complex(self._widthx/8.0,0)
        SE = self._location + complex(self._widthx/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=270, extent=180, style=ARC)
        
        # right side is half an oval
        NW = self._location - complex(self._widthx, 0)
        SE = self._location + complex(self._widthx*6/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=280, extent=160, style=ARC)
       
class XOR_Gate(MultiInSingleOut):
    """ Creates a canvas object with the shape of a standard XOR Gate
    
    Constructor: XorGate(canvas, complex, keywords)
        Valid keywords: direction, width, inputs
    """
    def __init__(self, canvas, location, direction = E, width = 1,
                 inputs = 2, size = None):
        MultiInSingleOut.__init__(self, canvas, location, 
            direction, width, inputs)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'1', 'name':'XOR Gate'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'width': width, \
                                        'size': size, 'inputs': inputs, \
                                        'xor':1}), self._bb)
            
        self._inputList = []
        self.inputPins()
        self.outputPin()
        self.body()
    
    def body(self):
        # left side is a two narrow arcs
        NW = self._location - complex(self._widthx/8.0,0)
        SE = self._location + complex(self._widthx/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=270, extent=180, style=ARC)

        xy = [(NW.real + self._widthx/8.0, NW.imag),
              (SE.real + self._widthx/8.0, SE.imag)]
        
        self._canvas.create_arc(xy, start=270, extent=180, style=ARC)
        
        # right side is half an oval
        NW = self._location - complex(self._widthx*6/8.0, 0)
        SE = self._location + complex(self._widthx*7/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=275, extent=170, style=ARC)
       
class XNOR_Gate(MultiInSingleOutNot):
    """ Creates a canvas object with the shape of a standard XNOR Gate
    
    Constructor: XnorGate(canvas, complex, keywords)
        Valid keywords: direction, width, inputs
    """
    def __init__(self, canvas, location, direction = E, width = 1,
                 inputs = 2, size = 1):
        MultiInSingleOut.__init__(self, canvas, location, 
            direction, width, inputs)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'1', 'name':'XNOR Gate'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'width': width, \
                                        'size': size, 'inputs': inputs, 
                                        'xor':1}), self._bb)
            
        self._inputList = []
        self.inputPins()
        self.outputPin()
        self.body()
        self.bubble()
    
    def body(self):
        # left side is a two narrow arcs
        NW = self._location - complex(self._widthx/8.0,0)
        SE = self._location + complex(self._widthx/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=270, extent=180, style=ARC)

        xy = [(NW.real + self._widthx/8.0, NW.imag),
              (SE.real + self._widthx/8.0, SE.imag)]
        
        self._canvas.create_arc(xy, start=270, extent=180, style=ARC)
        
        # right side is half an oval
        NW = self._location - complex(self._widthx*6/8.0, 0)
        SE = self._location + complex(self._widthx*6/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_arc(xy, start=280, extent=160, style=ARC)
        
class Constant(Component):
    """ Creates a canvas object for a constant output. 
    
    Constructor: Constant(canvas, complex, [int], [int], [int])
    """
    
    def __init__(self, canvas, location, direction = E, width = 1, value = 1):
        self._value = value
        widthx = (WIDTH - 15)*sqrt(len("%x" % self._value))
    
        Component.__init__(self, canvas, location, widthx, HEIGHT - 10, 
                           direction, width)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'1', 'name':'Constant'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'width': width, \
                                        'value': self._value}), self._bb)

        self.outputPin()
        self.body()
                                              
    def outputPin(self):
        start = self._yCenter + complex(self._widthx*7/8.0, 0)
        end = self._yCenter + complex(self._widthx)
        self._output = OutputPin(self._canvas, start, end, self._width)
                                                
    def body(self):
        NW = self._location
        SE = self._location + complex(self._widthx*7/8.0, self._height)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        self._canvas.create_rectangle(xy, outline = "black", fill="")
      
        xy = (self._center.real - 2, self._center.imag)
        self._canvas.create_text(xy, text = ("%x" % self._value))