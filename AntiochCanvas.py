#Create Canvas

from AntiochGatesLibrary import *
from AntiochPlexerLibrary import *
from AntiochArithmeticLibrary import *
from AntiochMemoryLibrary import *
from AntiochIOLibrary import *
from AntiochCircuits import *
import tkFileDialog

DEBUG = False

class WorkSpace(Canvas):
    """Defines the WorkSpace widget
    One should pass in a circuit instance so that they can be loaded or saved
    from the right click menu
    """
    def __init__(self, master, circuit = None):
        Canvas.__init__(self, master, bg = 'yellow')
        
        self._master = master
        self._circuit = circuit
        
        #grid
        self.renderGrid(20)
        
        #bindings
        self.bind("<Button-1>", self.pressButton1)
        self.bind("<B1-Motion>", self.b1Motion)        
        self.bind("<ButtonRelease-1>", self.releaseButton1)
        self.bind('<Button-3>', self.do_popup)
        self.bind("<Configure>", self.resize)
        
        #useful for finding objects to select/move
        self._saveCoords = []
        
    def pressButton1(self, e):
        """Event handler for <Button-1>
        Allow for selection of a component. This works with releaseButton1 to
        determine whether an object should be deselected or selected.
        """
        self.startx = e.x
        self.starty = e.y

        selection = self.clickedComponent(self.startx, self.starty)
        if selection: # we want to select something
            # visualize the selection
            self.itemconfigure(selection, outline = "pink", width = 2)
            # find all objects within the selection area
            for obj in self.find_overlapping(*self.bbox(selection)):
                objtags = self.gettags(obj)
                # we don't want to select grid objects
                if "grid" not in objtags:
                    #first time click, no click status tags
                    if "selected" not in objtags and "released" not in objtags:
                        #add tag to indicate we've made a selection
                        self.addtag_withtag("selected", obj)
                        #save the selection coordinates
                        self._saveCoords.append((obj, self.coords(obj)))
                        if DEBUG:
                            try:
                                self.itemconfigure(obj, outline = "green", )
                            except TclError:
                                self.itemconfigure(obj, fill = "green", )
                    # this is the second time we've clicked it
                    else:
                        #so what?
                        pass                   
                        
    def clickedComponent(self, x, y):
        """ Searches for the object which the cursor is inside.
        It will send out tracers starting at (x,y) to find the object.
        If more than one tracers finds the object then the cursor is inside its
        bounding box.
        """
        selection = []
        selection.append(self.search(x,y, complex(0,1)))
        selection.append(self.search(x,y, complex(1,0)))
        
        if selection[0] == selection[1]:
            return selection[0]
        return None
            
    def search(self, x, y, direction):
        """ Sends out soldiers to search for components and return the first one 
        they find
        """
        cangle = direction
        cangle = cangle / abs(cangle)
    
        search = True
        startx, starty = x, y
        while search:
            xy = [x-2,y-2,x+2,y+2]
            foundObjs = self.find_overlapping(*xy)
            if DEBUG:
                #make search box visible
                self.create_rectangle(xy, outline = "blue", fill = '')
            # check if we hit the border of a component
            for obj in foundObjs:
                objTags = self.gettags(obj)
                if ("compBBox" in objTags) and ("selected" not in objTags):
                    search = False
                    return obj
            # still searching?
            if x < self._widthx and y < self._height and search:
                x += 4 * direction.real * cangle.real
                y += 4 * direction.imag * cangle.imag
            else:
                search = False
        return None
        
    def b1Motion(self, e):
        """Event handler for <B1-Motion>.
        If an object is selected, it will be dragged.
        """
        dx = e.x - self.startx
        dy = e.y - self.starty
        self.startx = e.x
        self.starty = e.y
        selected = self.find_withtag("selected")
        for obj in selected:
            self.move(obj, dx, dy)
            self.addtag_withtag("dragged", obj)
    
    def releaseButton1(self, e):
        """Event handler for <ButtonRelease-1>. 
        This works with pressButton1 to determine whether an object should be 
        deselected or selected.
        """
        toRemove = []   #elements to remove in the end
        toChange = []   #elements to change in the end
        changeTo = []   #element values in the end
        
        selection = self.clickedComponent(e.x, e.y)
        # Trying to place on another component
        if selection:
            # move it back where it came from
            for obj in self._saveCoords:
                self.coords(obj[0], *obj[1])
        # Trying to place in a good spot
        else:
            # Remove the old coords and save the new ones
            for obj in self._saveCoords:
                toChange.append(obj)
                changeTo.append((obj[0], self.coords(obj[0])))
                
            for obj in toChange:
                self._saveCoords.remove(obj)
            for coord in changeTo:
                self._saveCoords.append(coord)
        
        #find all objects we've selected
        for obj in self._saveCoords:
            objtags = self.gettags(obj[0])
            # first time released, has tag selected but not released
            if "released" not in objtags and "selected" in objtags:
                # add tag to indicate we've released it once
                self.addtag_withtag("released", obj[0])
            # this is the second time we've released
            else:
                # we were dragging before release
                if "dragged" in objtags:
                    # indicate we're no longer dragging
                    self.dtag(obj[0], "dragged")
                # we're just full clicking a second time
                else:
                    toRemove.append(obj)
                    #remove visualization of selection
                    if "compBBox" in objtags:
                        self.itemconfigure(obj[0], outline = '')
                    #remove all click status
                    self.dtag(obj[0], "released")
                    self.dtag(obj[0], "selected")
        #remove from saved coordinate list
        for obj in toRemove:
            self._saveCoords.remove(obj)
        if DEBUG:
            print "\nSaved: " + str(self._saveCoords)
    
    def save_new_coords(self, obj):
        """ Saves new coordinates if the component has been moved """
        self._saveCoords.remove(obj)
        self._saveCoords.append((obj[0], self.coords(obj[0])))
                
    def do_popup(self, event):
        """Event handler for <Button-3>.
        Constructs and displays a popup menu.
        Modified from http://effbot.org/zone/tkinter-popup-menu.htm
        """
        # create a menu
        popup = Menu(self, tearoff=0)
        popup.add_command(label="Save Circuit", command = self.saveCircuit)
        popup.add_command(label="Load Circuit", command = self.loadCircuit)
        popup.add_separator()
        popup.add_command(label="Close Circuit", command = self.closeCircuit)
        
        # display the popup menu
        try:
            popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            popup.grab_release()
            
    def saveCircuit(self):
        """Saves the currently displayed circuit.
        modified from http://tkinter.unpythonic.net/wiki/tkFileDialog
        """
        file_opt = options = {}
        options['defaultextension'] = '.circ'
        options['filetypes'] = [('Logisim Circuit File', '.circ'), ('all files', '.*') ]
        options['title'] = 'Save your circuit'
        
        filename = tkFileDialog.asksaveasfilename(**file_opt)
        if filename:
            self._circuit.save(self, filename)
            
    def loadCircuit(self):
        """This will load a new circuit file but first close the current circuit
        
        modified from http://tkinter.unpythonic.net/wiki/tkFileDialog
        """
        file_opt = options = {}
        options['defaultextension'] = '.circ'
        options['filetypes'] = [('Logisim Circuit File', '.circ'), ('all files', '.*') ]
        options['title'] = 'Load a circuit'
        
        filename = tkFileDialog.askopenfilename(**file_opt)
        if filename:
            self.closeCircuit()
            self._circuit = Circuit()
            self._circuit.load(filename)
            self._circuit.render(self)
            
    def closeCircuit(self):
        """Should clear the workspace and update the sidebar.
        Right now, just clear the workspace
        """
        allObjs = self.find_all()
        for obj in allObjs:
            if "grid" not in self.gettags(obj):
                self.delete(obj)
                
        
    def resize(self, e):
        #remove grid
        grid_lines = self.find_withtag("grid")
        for line in grid_lines:
            self.delete(line)
        #re-add grid with current spacing intact then send to back
        self.renderGrid(self._gridSpacing)
        self.tag_lower("grid")
        
        
    def renderGrid(self, spacing):
        """Renders the grid to the workspace with a given spacing"""
        self._gridSpacing = spacing
        self.currentDimensions()
        for y in range(0,self._height,self._gridSpacing):
            self.create_line((0,y),(self._widthx,y), fill = "gray",
                             tags = "grid", state = DISABLED)
        for x in range(0,self._widthx,self._gridSpacing):
            self.create_line((x,0),(x,self._height), fill = "gray", 
                             tags = "grid", state = DISABLED)
                             
    def currentDimensions(self):
        self._master.update_idletasks()
        self._widthx = self._master.winfo_width()
        self._height = self._master.winfo_height()
        
def test(master):
    master.minsize(700,480)
    master.geometry("800x600")
    
    circuit = Circuit()
    workspace = WorkSpace(master, circuit)
    workspace.pack(fill = BOTH, expand = 1)
    
    wire1 = Wire(workspace,complex(50,20),complex(200,20))
    
    notgate = NOT_Gate(workspace, complex(50,50), "narrow")
    notgate = NOT_Gate(workspace, complex(150,50), "wide")

    buffer = Buffer(workspace, complex(50,100), width = 4)

    andgate1 = AND_Gate(workspace, complex(50,150))
    andgate2 = AND_Gate(workspace, complex(150,150), inputs = 3)
    andgate3 = AND_Gate(workspace, complex(250,150), inputs = 4)

    orgate1 = OR_Gate(workspace, complex(50,200))
    orgate2 = OR_Gate(workspace, complex(150,200), inputs = 3)
    orgate3 = OR_Gate(workspace, complex(250,200), inputs = 4)

    nandgate1 = NAND_Gate(workspace, complex(50,250))
    nandgate2 = NAND_Gate(workspace, complex(150,250), inputs = 3)
    nandgate3 = NAND_Gate(workspace, complex(250,250), inputs = 4)

    norgate1 = NOR_Gate(workspace, complex(50,300))
    norgate2 = NOR_Gate(workspace, complex(150,300), inputs = 3)
    norgate3 = NOR_Gate(workspace, complex(250,300), inputs = 4)

    xorgate1 = XOR_Gate(workspace, complex(50,350), size = 50)
    xorgate2 = XOR_Gate(workspace, complex(150,350), inputs = 3, width = 2, size = 50)
    xorgate3 = XOR_Gate(workspace, complex(250,350), inputs = 4, size = 50)

    xnorgate1 = eval("XNOR_Gate(workspace, complex(50,400),size = 50)")
    xnorgate2 = XNOR_Gate(workspace, complex(150,400), inputs = 3, size = 50)
    xnorgate3 = XNOR_Gate(workspace, complex(250,400), inputs = 4)

    constant1 = Constant(workspace, complex(150,100))
    constant2 = Constant(workspace, complex(250,100), value = 12)
    constant3 = Constant(workspace, complex(350,100), value = 0x04d2)
    constant4 = Constant(workspace, complex(450,100), value = 12345)
    constant5 = Constant(workspace, complex(550,100), value = 0xAAAAAAAA)
    
    mux1 = Multiplexer(workspace, complex(350, 150))
    mux2 = Multiplexer(workspace, complex(350, 210), select = 2)
    mux3 = Multiplexer(workspace, complex(350, 270), select = 3)
    mux3 = Multiplexer(workspace, complex(350, 350), select = 4)

    adder1 = Adder(workspace, complex(450,150))
    adder2 = Adder(workspace, complex(450,225), width = 4)
    adder3 = Adder(workspace, complex(450,300), width = 8)
    
    dflipflop = D_Flip_Flop(workspace, complex(450, 375))
    
    pin = Pin(workspace, complex(550, 150))
    
    pb = Button(workspace, complex(550, 200))
    
    hex = Hex_Digit_Display(workspace, complex(550, 250))
    
    led = LED(workspace, complex(550, 350))
    
if __name__ == '__main__':
    root = Tk()
    test(root)
    root.mainloop()
    
