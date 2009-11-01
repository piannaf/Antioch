from AntiochComponent import *

class D_Flip_Flop(Component):
    """ Creates a canvas object with the shape of a standard D Flip-Flop 
    
    Constructor: NotGate(canvas, complex, [int])
    """
    
    def __init__(self, canvas, location, direction = E):
        Component.__init__(self, canvas, location, 2*WIDTH - 10, 2*HEIGHT + 10, 
                           direction, 1)

        self.canvas = canvas
                           
        self.canvas.addtag_withtag("{'lib':'4', 'name':'D Flip-Flop'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'trigger': 'rising', 'label':'',
                                        'labelfont':"SansSerif plain 12"}), self._bb)
    
        self.clockIn()
        self.dataIn()
        self.set()
        self.reset()
        self.enable()
        self.Q()
        self.notQ()
        self.body()
        
    def clockIn(self):
        start = self._location + complex(0, self._height*2/3)
        end = start + complex(self._widthx/8.0, 0)
        self._clockIn = InputPin(self._canvas, start, end, 1)
                                              
    def dataIn(self):
        start = self._location + complex(0, self._height*1/3)
        end = start + complex(self._widthx/8.0, 0)
        self._dataIn = InputPin(self._canvas, start, end, 1)
        
    def Q(self):
        start = self._location + complex(self._widthx, self._height*1/3.0)
        end = start - complex(self._widthx/8.0, 0)
        self._Q = InputPin(self._canvas, start, end, 1)
                                              
    def notQ(self):
        start = self._location + complex(self._widthx, self._height*2/3.0)
        end = start - complex(self._widthx/8.0, 0)
        self._notQ = InputPin(self._canvas, start, end, 1)
        
    def set(self):
        start = self._location + complex(self._widthx/4.0, self._height)
        end = start - complex(0, self._height/8.0)
        self._set = InputPin(self._canvas, start, end, 1)
        
    def enable(self):
        start = self._location + complex(self._widthx*2/4.0, self._height)
        end = start - complex(0, self._height/8.0)
        self._enable = InputPin(self._canvas, start, end, 1)
        
    def reset(self):
        start = self._location + complex(self._widthx*3/4.0, self._height)
        end = start - complex(0, self._height/8.0)
        self._reset = InputPin(self._canvas, start, end, 1)
    
    def body(self):
        # just a rectangle
        NW = self._location + complex(self._widthx/8.0, self._height/8.0)
        SE = self._location + complex(self._widthx*7/8.0, self._height*7/8.0)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_rectangle(xy, outline = "black", fill="")
        
        # Data input label
        xy = (self._yCenter.real + self._widthx/16.0,
              self._location.imag + self._height/3.0 - 8)
        
        self._canvas.create_text(xy, text = 'D')
        
        # Clock input label
        xy = (self._yCenter.real + self._widthx/16.0,
              self._location.imag + self._height*2/3.0 - 8)
        
        self._canvas.create_text(xy, text = 'C')
        
        # Clock input triangle
        NW = self._yCenter + complex(self._widthx/8.0, -self._height*5/18.0)
        E = NW + complex(self._widthx*1/8.0, self._height/9.0)
        SW = NW + complex(0, self._height*2/9.0)
        
        xy = [(NW.real,NW.imag),(E.real, E.imag), (SW.real, SW.imag)]
        
        self._canvas.create_line(xy)
        
        # Set label
        xy = (self._location.real + self._widthx/4.0, 
              self._location.imag + self._height*6/8.0)
        
        self._canvas.create_text(xy, text = '1')
        
        # Enable label
        xy = (self._location.real + self._widthx*2/4.0, 
              self._location.imag + self._height*6/8.0)
        
        self._canvas.create_text(xy, text = 'en')
        
        # Reset label
        xy = (self._location.real + self._widthx*3/4.0, 
              self._location.imag + self._height*6/8.0)
        
        self._canvas.create_text(xy, text = '0')
        
        # Q output label
        xy = (self._yCenter.real + self._widthx*15/16.0,
              self._location.imag + self._height/3.0 - 8)
        
        self._canvas.create_text(xy, text = 'Q')
        
        # ~Q label
        xy = (self._yCenter.real + self._widthx*15/16.0,
              self._location.imag + self._height*2/3.0 - 8)
        
        self._canvas.create_text(xy, text = '~Q')
        