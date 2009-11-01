from AntiochComponent import *

class Adder(MultiInSingleOut):
    """ Creates a canvas object with the shape of a standard Full Adder
    
    Constructor: Adder(canvas, complex, keywords)
        Valid keywords: direction, width, inputs
    """
    def __init__(self, canvas, location, direction = E, width = 1):
        MultiInSingleOut.__init__(self, canvas, location, 
            direction, width, 2)

        self.canvas = canvas
    
        #high level attribute tags
        self.canvas.addtag_withtag("{'lib':'3', 'name':'Adder'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'width': width}), self._bb)
        

        self._inputList = []
        self.inputPins()
        self.outputPin()
        self.body()
        self.carryIn()
        self.carryOut()    
        
    def initDimensions(self, inputs):
        """override the parent's method so that we can have a nice square"""
        widthx = (inputs)*WIDTH - 10
        height = (inputs)*HEIGHT
        return (widthx, height)
    
    def body(self):
        # just a rectangle
        NW = self._location + complex(self._widthx/8.0, self._height/8.0)
        SE = self._location + complex(self._widthx*7/8.0, self._height*7/8.0)
        
        xy = [(NW.real, NW.imag), (SE.real, SE.imag)]
        
        self._canvas.create_rectangle(xy, outline = "black", fill="")
        
        # c in label
        xy = (self._center.real, self._center.imag - self._height/4.0)
        
        self._canvas.create_text(xy, text = 'c in')
        
        # c out label
        xy = (self._center.real, self._center.imag + self._height/6.0)
        
        self._canvas.create_text(xy, text = 'c out')
        
        # A input label
        xy = (self._yCenter.real + self._widthx/16.0,
              self._location.imag + self._height/3.0 - 8)
        
        self._canvas.create_text(xy, text = 'A')
        
        # B input label
        xy = (self._yCenter.real + self._widthx/16.0,
              self._location.imag + self._height*2/3.0 - 8)
        
        self._canvas.create_text(xy, text = 'B')
        
        # sum output label
        xy = (self._center.real + self._widthx/4.0, self._center.imag - 1)
        
        self._canvas.create_text(xy, text = '+', font = ("Times", 20, "bold"))
    
    def carryIn(self):
        start = self._xCenter
        end = start + complex(0, self._height/8.0)
        self._carryIn = InputPin(self._canvas, start, end, 1)
    
    def carryOut(self):
        start = self._xCenter + complex(0, self._height)
        end = start - complex(0, self._height/8.0)
        self._carryIn = InputPin(self._canvas, start, end, 1)