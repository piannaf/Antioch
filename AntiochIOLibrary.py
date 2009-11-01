from AntiochComponent import *

class Pin(Component):
    """ Creates a canvas object for a toggle switch 
    
    Constructor: Switch(canvas, complex, [int])
    """
    
    def __init__(self, canvas, location, direction = E, width = None):
        Component.__init__(self, canvas, location, WIDTH - 20, WIDTH - 20, 
                           direction, width = 1)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'0', 'name':'Pin'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'output':'false',
                                        'width':'1', 'tristate':'false',
                                        'pull': 'none', 'label': '', 
                                        'labelloc':'center',
                                        'labelfont':"SansSerif plain 12"}), self._bb)

        self.outputPin()
        self.body()
                                              
    def outputPin(self):
        start = self._yCenter + complex(self._widthx*7/8.0, 0)
        end = self._yCenter + complex(self._widthx)
        self._output = OutputPin(self._canvas, start, end, self._width)
                                                
    def body(self):
        # Circle
        NW = self._location + complex(self._widthx/8.0, self._height/8.0)
        SE = self._location + complex(self._widthx*7/8.0, self._height*7/8.0)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        self._canvas.create_oval(xy, outline = "black", fill="")

class Button(Component):
    """ Creates a canvas object for a push button
    
    Constructor: PushButton(canvas, complex, [int])
    """
    
    def __init__(self, canvas, location, direction = E):
        Component.__init__(self, canvas, location, WIDTH - 20, WIDTH - 20, 
                           direction, width = 1)

        self.canvas = canvas
        
        #set tag to correspond with Logisim .circ format
        self.canvas.addtag_withtag("{'lib':'5', 'name':'Button'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'east', 'color': '#ffffff',
                                        'label': '', 'labelloc':'center',
                                        'labelfont':"SansSerif plain 12",
                                        'labelcolor': '#000000'}), self._bb)
                                        
        self.inputPin()
        self.body()
                                              
    def inputPin(self):
        start = self._yCenter
        end = self._yCenter + complex(self._widthx/8.0, 0)
        self._input = InputPin(self._canvas, start, end, self._width)
                                                
    def body(self):
        # Circle
        NW = self._location + complex(self._widthx/8.0, self._height/8.0)
        SE = self._location + complex(self._widthx*7/8.0, self._height*7/8.0)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        self._canvas.create_rectangle(xy, outline = "black", fill="")
        
class Hex_Digit_Display(Component):
    """ Creates a canvas object with the shape of a standard Hex Display 
    
    Constructor: HexDisplay(canvas, complex, [int])
    """
    
    def __init__(self, canvas, location, direction = E):
        Component.__init__(self, canvas, location, WIDTH, HEIGHT + 40, 
                           direction, 4)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'5', 'name':'Hex Digit Display'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'color':'#f00000'}), self._bb)
    
        self.numIn()
        self.pointIn()
        self.body()
        self.interior()
        
    def numIn(self):
        start = self._location + complex(self._widthx/3.0, self._height)
        end = start - complex(0, self._height/8.0)
        self._numIn = InputPin(self._canvas, start, end, 4)
                                              
    def pointIn(self):
        start = self._location + complex(self._widthx*2/3.0, self._height)
        end = start - complex(0, self._height/8.0)
        self._pointIn = InputPin(self._canvas, start, end, 1)
                                                
    def body(self):
        NW = self._location
        SW = self._location + complex(self._widthx, self._height*7/8.0)
        
        xy = [(NW.real, NW.imag), (SW.real, SW.imag)]
        self._canvas.create_rectangle(xy, outline = "black", fill="")
    def interior(self):
        self._N = self._hRect(self._location + complex(self._widthx*2/8.0, self._height/8.0))
        self._NW = self._vRect(self._location + complex(self._widthx*3/32.0, self._height*3/16.0))
        self._SW = self._vRect(self._location + complex(self._widthx*3/32.0, self._height*7/16.0))
        self._S = self._hRect(self._location + complex(self._widthx*2/8.0, self._height*11/16.0))
        self._NW = self._vRect(self._location + complex(self._widthx*11/16.0, self._height*3/16.0))
        self._SW = self._vRect(self._location + complex(self._widthx*11/16.0, self._height*7/16.0))
        self._MID = self._hRect(self._location + complex(self._widthx*2/8.0, self._height*13/32.0))
        self._DECP = self._decPoint(self._location + complex(self._widthx*13/16.0, self._height*11/16))
    def _vRect(self, nw):
        """ Private method for drawing a verticle rectangle """
        NW = nw
        SE = NW + complex(self._height/16.0, self._widthx/2.5)
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        self._canvas.create_rectangle(xy, outline = "black", fill="")
        
    def _hRect(self, nw):
        """ Private method for drawing a horizontal rectangle """
        NW = nw
        SE = NW + complex(self._widthx/2.5, self._height/16.0)
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        return self._canvas.create_rectangle(xy, outline = "black", fill="")
        
    def _decPoint(self, nw):
        """ Private method for drawing a decimal point """
        NW = nw
        SE = NW + complex(self._widthx/8.0, self._widthx/8.0)
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        return self._canvas.create_oval(xy, outline = "black", fill="")
   
class LED(Component):
    """ Creates a canvas object for an LED
    
    Constructor: LED(canvas, complex, [int])
    """
    
    def __init__(self, canvas, location, direction = E):
        Component.__init__(self, canvas, location, WIDTH - 20, WIDTH - 20, 
                           direction, width = 1)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'5', 'name':'LED'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing':'west', 'color': "#f00000", \
                                        'label': "", 'labelloc': "center", \
                                        'labelfont': "SansSerif plain 12", \
                                        'labelcolor': "#000000"}), self._bb)

        self.inputPin()
        self.body()
                                              
    def inputPin(self):
        start = self._yCenter
        end = self._yCenter + complex(self._widthx*1/8.0, 0)
        self._input = OutputPin(self._canvas, start, end, self._width)
                                                
    def body(self):
        # Circle
        NW = self._location + complex(self._widthx/8.0, self._height/8.0)
        SE = self._location + complex(self._widthx*7/8.0, self._height*7/8.0)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        self._canvas.create_oval(xy, outline = "black", fill="")