from Tkinter import *
from AntiochCanvas import *
from AntiochToolbars import *
from AntiochSidebar import *

class Antioch:
    """The main application class.
    All elements needed for running Antioch are instantiated by this class.
    """
    def __init__(self, master):
        #init master window
        master.minsize(700,480)
        master.geometry("800x600")
        self._master = master
        
        #init menu and toolbars
        self._menu = AntiochMenus.MenuBar(self._master)
        self._toolbar = TBContainer(self._master, self._menu)
        self._toolbar.pack(side = TOP, fill = X)
        
        #container for sidebar and workspace
        self._lowerHalf = Frame(self._master)
        self._lowerHalf.pack(side = TOP, fill = BOTH, expand = 1)
        
        #init sidebar
        self._sidebar = SideBar(self._lowerHalf).pack(side = LEFT, fill = Y)
        
        #init workspace
        self._circuit = Circuit()
        self._workspace = WorkSpace(self._lowerHalf, self._circuit)
        self._workspace.pack(side = RIGHT, fill = BOTH, expand = 1)
        
        
def main():
    root = Tk()
    app = Antioch(root)
    root.mainloop()

if  __name__ == '__main__':
    main()