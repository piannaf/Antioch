#Create Sidebar

from Tkinter import *

class SideBar(Frame):
    """The sidebar contains the Library and Component Attribute frames."""
    def __init__(self, master):
        Frame.__init__(self, master)
        
        self._master = master
        
        #set default width
        self._width = 300
    
        # sidebar has a handle on the right which allows the user to resize it
        self._handle = Frame(self, bd = 2, relief = RAISED, 
                             cursor = 'sb_h_double_arrow', bg = 'white',
                             width = 4)
        self._handle.pack(side = RIGHT, anchor = E, fill = Y)
        self._handle.bind('<B1-Motion>', self._resize)
        
        self._libraryFrame = LibraryFrame(self, width = self._width, 
                          text = "Project Library")    
        self._compAttrFrame = CompAttrFrame(self, width = self._width, 
                          text = "foobar")

    def _resize(self, e):
        self._width = (e.x_root - self.winfo_rootx())
        self._libraryFrame.resize(self._width)
        self._compAttrFrame.resize(self._width)
        
class LibraryFrame(LabelFrame):
    def __init__(self, master, **options):
        LabelFrame.__init__(self, master, **options)
        self.pack(fill = Y, expand = 1)
        
        self._body = Canvas(self, bg = 'green', width = self['width'])
        self._body.pack()
        
    def resize(self, newWidth):
        self['width'] = newWidth
        self._body['width'] = newWidth
        
class CompAttrFrame(LabelFrame):
    def __init__(self, master, **options):
        LabelFrame.__init__(self, master, **options)
        self.pack(fill = Y, expand = 1)
        
        self._body = Canvas(self, bg = 'red', width = self['width'])
        self._body.pack()
        
    def resize(self, newWidth):
        self['width'] = newWidth
        self._body['width'] = newWidth

def test(master):
    master.minsize(700,480)
    master.geometry("800x600")
    SideBar(master).pack(side = LEFT, fill = Y)

if __name__ == '__main__':
    root = Tk()
    test(root)
    root.mainloop()
