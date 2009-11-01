from AntiochComponent import *
        
class Multiplexer(MultiInSingleOut):
    """ Creates a canvas object with the shape of a standard Multiplexer
    
    Constructor: Mux(canvas, complex, keywords)
        Valid keywords: direction, width, select
    """
    def __init__(self, canvas, location, direction = E, width = 1,
                 select = 1):
        self._numSelects = select
        inputs = 2**self._numSelects
        
        MultiInSingleOut.__init__(self, canvas, location, 
            direction, width, inputs)

        self.canvas = canvas
    
        self.canvas.addtag_withtag("{'lib':'2', 'name':'Multiplexer'}", self._bb)
        #low level attribute tags
        #TODO make it so these don't have to be so hardcoded
        self.canvas.addtag_withtag(str({'facing': 'east', 'select': select,
                                        'width': width}), self._bb)
            
        self._inputList = []
        self.inputPins()
        self.outputPin()
        self.body()
        self._selects = []
        self.selectPins()
        
    def initDimensions(self, inputs):
        """override the parent's method so that widthx will grow slower"""
        widthx = (inputs/sqrt(inputs**1.5))*(WIDTH - 10)
        height = (inputs/sqrt(inputs*2.0))*HEIGHT
        return (widthx, height)
    
    def body(self):
        # trapazoid with base on left
        NW = self._location + complex(self._widthx/8.0,0)
        SW = NW + complex(0, self._height)
        NE = self._location + complex(self._widthx*7/8.0, self._height/3.0)
        SE = NE + complex(0, self._height/3.0)
        
        xy = [(NW.real, NW.imag),(NE.real, NE.imag), 
              (SE.real, SE.imag),(SW.real, SW.imag)]
        
        self._canvas.create_polygon(xy, outline = "black", fill="")
        
        # MUX label
        xy = (self._center.real, self._center.imag)
        
        self._canvas.create_text(xy, text = 'MUX')
        
        # D0 label
        NW = self._location + complex(0, self._height/(self._inputs + 1)/2.0)
        xy = (NW.real + self._widthx/32.0, NW.imag - 2)
        self._canvas.create_text(xy, text = '0')
        
    def selectPins(self):
        dx = float(self._widthx)/(self._numSelects + 1)
        for n in range(1,self._numSelects + 1):
            start = self._location + complex(n*dx,self._height)
            end = start - complex(0, 
                ((self._height/3.0)/(self._widthx))* \
                (n*self._widthx/self._numSelects) - \
                self._height/32.0)
            self._inputList.append(InputPin(self._canvas, start, end, self._width))