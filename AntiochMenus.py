# create a menu

from Tkinter import *

class MenuBar:
    """The complete static menu for Antioch.
    Override methods for a dynamic, interactive menu.
    """
    def __init__(self, master):
        # Initialize a stack for menu parsing
        self._currentMenu = [Menu(master)]
        
        master.config(menu=self._currentMenu[-1])

        # code menu datastructure. Useful for using this data to create other
        # menus and toolbars

        self._menuItems = \
        (
            ('File',
                [
                    {'label': 'New Project', 'command': self.newProject},
                    {'label': 'Open...', 'command': self.openFile},
                    {'label': 'Close Project', 'command': self.closeProject},
                    {'label': 'Save Project', 'command': self.saveProject},
                    {'label': 'Export Project', 
                        'command': self.exportProject},
                    {'label': 'Print', 'command': self.printProject},
                    {'type': 'separator'},
                    {'label': 'Exit', 'command': self.quit},
                ]
            ),
            ('Edit',
                [
                    {'label': 'Undo', 'command': self.undo},
                    {'label': 'Redo', 'command': self.redo},
                    {'label': 'Cut', 'command': self.cut},
                    {'label': 'Copy', 'command': self.copy},
                    {'label': 'Paste', 'command': self.paste},
                    {'label': 'Delete', 'command': self.delete},
                    {'label': 'Duplicate', 'command': self.duplicate},
                    {'label': 'Select All', 'command': self.selectAll},
                    {'label': 'Deselect All', 'command': self.deslectAll},
                ]
            ),
            ('View',
                [
                    ('Toolbars',
                        [
                            {'type': 'checkbutton', 'variable': '1',
                                'label': 'Standard', 'command': self.showStdTB},
                            {'label': 'Menus', 'command': self.showMenuTB},
                            {'label': 'Component Libraries', 
                                'command': self.showLibTB}
                        ]
                    ),
                    {'label': 'Libraries Frame', 
                        'command': self.showLibFrame},
                    {'label': 'Menu', 'command': self.showMenu},
                    {'label': 'Component Attributes Frame', 
                        'command': self.showCAFrame},
                ]
            ),
            ('Project',
                [
                    {'label': 'Rename Project', 'command': self.renameProject},
                    {'label': 'New Circuit', 'command': self.newCircuit},
                    {'label': 'Rename Circuit', 'command': self.renameCircuit},
                    {'label': 'Save Circuit as Component', 
                        'command': self.saveComponent},
                    {'label': 'Load Library...', 'command': self.loadLibrary},
                    {'label': 'Unload Libraries...', 
                        'command': self.unloadLibraries},
                ]
            ),
            ('Simulate',
                [
                    {'label': 'Not Yet Implemented', 
                        'command': self.simulate, 'state': 'disabled'},
                ]
            ),
            ('Window',
                [
                    {'label': 'Tabify', 'command': self.tabbify},
                    {'label': 'Cascade', 'command': self.cascade},
                    {'label': 'Tile Horizontally', 'command': self.tileH},
                    {'label': 'Tile Vertically', 
                        'command': self.tileV},
                    {'label': 'Minimize all', 'command': self.minimizeAll},
                ]
            ),
            ('Help',
                [
                    {'label': 'Antioch Help', 'command': self.help},
                    {'label': 'Release Notes', 'command': self.notes},
                    {'label': 'About Antioch', 'command': self.about},
                ]
            ),
        )
        
        self._parse(self._menuItems)
    # general Menu methods
    def _parse(self, menuItems):
        """ A private method for parsing the menu datastructure into a Tkinter
        menu widget.
        
        Precondition: menuItems is a tuple consisting of tuples of length two
        and dictionaries. A tuple of length two describes a cascading menu item.
        A dictionary describes other types of menu items defined by Tkinter.
        
        _parse((string, (dict,tuple))) -> None
        """
        for item in menuItems:
            if len(item) == 2 and isinstance(item, tuple):
                self._currentMenu.append(Menu(self._currentMenu[-1], tearoff=0))
                self._currentMenu[-2].add_cascade(label = item[0], menu = 
                    self._currentMenu[-1])
                self._parse(item[1])
            elif isinstance(item, dict):
                itemType = item.pop('type', None)
                if itemType:
                    self._currentMenu[-1].add(itemType, item)
                else:
                    self._currentMenu[-1].add_command(item)
            else:
                print "poorly formed menu"
        self._currentMenu.pop(-1)
        
    def _getIndex(self, menuLabel):
        """ A private method for retrieving the index of a cascading menu with 
        the given label.
        """
        
    def add(self, item, root):
        """ A method for adding a single sub-item to a given menu.
        
        Precondition: The object to be passed in as 'item' must be a dictionary
        which conforms to parameters taken by the Tkinter.Menu.add() method or,
        if not specifying an 'itemType', by the Tkinter.Menu.add_command()
        method.
        
        add(dict, string) -> None
        """
        pass
        
    def remove(self, itemLabel, root):
        """A method for removing a single sub-item from a given menu.
        
        remove(string, string) -> None
        """
        pass
        
    # methods for File Menu
    def newProject(self):
        pass
    def openFile(self):
        pass
    def closeProject(self):
        pass
    def saveProject(self):
        pass
    def exportProject(self):
        pass
    def printProject(self):
        pass
    def quit(self):
        root.destroy()

    # methods for Edit Menu
    def undo(self):
        pass
    def redo(self):
        pass
    def cut(self):
        pass
    def copy(self):
        pass
    def paste(self):
        pass
    def delete(self):
        pass
    def duplicate(self):
        pass
    def selectAll(self):
        pass
    def deslectAll(self):
        pass

    # methods for View Menu
    def showStdTB(self):
        pass
    def showMenuTB(self):
        pass
    def showLibTB(self):
        pass
    def showLibFrame(self):
        pass
    def showMenu(self):
        pass
    def showCAFrame(self):
        pass
        
    # methods for Project Menu
    def renameProject(self):
        pass
    def newCircuit(self):
        pass
    def renameCircuit(self):
        pass
    def saveComponent(self):
        pass
    def loadLibrary(self):
        pass
    def unloadLibraries(self):
        pass
    
    # methods for Simulate Menu',
    def simulate(self):
        pass
    
    # methods for Window Menu
    def tabbify(self):
        pass
    def cascade(self):
        pass
    def tileH(self):
        pass
    def tileV(self):
        pass
    def minimizeAll(self):
        pass
    
    # methods for Help Menu
    def help(self):
        pass
    def notes(self):
        pass
    def about(self):
        pass
        
def test(master):
    MenuBar(master)

if __name__ == '__main__':
    root = Tk()
    test(root)
    root.mainloop()
