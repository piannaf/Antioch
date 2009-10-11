#Create default Toolbars

from Tkinter import *
import AntiochMenus

class ToolBar(Frame):
    """Defines a toolbar widget"""
    def __init__(self, master):
        Frame.__init__(self, master, bd = 2, relief = GROOVE, width = 100)
        
        self._container = master

        # Each toolbar has a handle
        # They are all the same
        # They can be right clicked to modify the toolbar in various ways
        self._handle = Frame(self, bd = 2, relief = RAISED, cursor = 'plus',
                             bg = 'white', height = 30, width = 4)
        self._handle.grid(row = 0, column = 0)
        self._handle.bind('<Button-3>', self.do_popup)

        # Each toolbar has a label and buttons
        self._showLabel = True
        self._label = None
        self._buttons = []
        
    def _populate(self):
        """Private method to populate the toolbar with buttons"""

        #buttons always start at index 2
        i = 2
        for button in self._buttons:
            TBButton(self, text = button.get('text'),
                image = button.get('image')).grid(row = 0, column = i, padx = 1)
            i += 1

    def setLabel(self, label):
        self._label = Label(self, text = label)
        
    def getLabel(self):
        return self._label

    def toggleLabel(self):
        """Toggles whether the toolbar's label is shown"""
        if self._label:
            if self._showLabel:
                self._label.grid(row = 0, column = 1)
                self._showLabel = False
            else:
                self._label.grid_remove()
                self._showLabel = True
            
            if not self._checkSpace():
                self.toggleLabel()

    def setButtons(self, buttons):
        for button in buttons:
            self._buttons.append(button)
    
    def do_popup(self, event):
        """Modified from http://effbot.org/zone/tkinter-popup-menu.htm"""
        # create a menu
        popup = Menu(root, tearoff=0)
        popup.add_command(label="Toggle Label", command = self.toggleLabel)
        popup.add_separator()
        popup.add_command(label="Move Right", command = self._moveRight)
        popup.add_command(label="Move Left", command = self._moveLeft)
        popup.add_command(label="Tearoff", command = self._tearOff)
        popup.add_separator()
        popup.add_command(label="Remove", command = self._remove)
        
        # display the popup menu
        try:
            popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            popup.grab_release()
            
    def _moveRight(self):
        self._container.moveTB(self, 'right')
        self._container.render()
        
    def _moveLeft(self):
        self._container.moveTB(self, 'left')
        self._container.render()        
        
    def _tearOff(self):
        self._remove()
        top = Toplevel()
        top.title(self.getLabel()['text'])
        top.resizable(0,0)
        
        # duplicate the toolbar for the new master
        tb = ToolBar(top)
        tb._buttons = self._buttons
        tb._populate()
        tb.grid(row = 0, column = 0, padx = 1)
        # this is torn off, no need for a handle
        tb._handle.grid_remove()
        
    def _remove(self):
        self._container._popup.invoke(self._label['text'])
        
    def render(self, col = 0):
        """Render the toolbar"""
        if self._buttons:
            self._populate()
        self.grid(row = 0, column = col, padx = 1)
        if not self._checkSpace():
            self._remove()
        
    def _checkSpace(self):
        """ Returns true if there is space to draw the widget"""
        #strange behaviour: there's never enough space on init so if less than
        #two toolbars visible, always return true
        if len(self._container.getTBList()) > 1:
            lastWidget = self._container.getTBList()[-1][1]
        
            self.update_idletasks()
            if lastWidget.winfo_width() + lastWidget.winfo_x() > \
                self._container.winfo_width():
                    return False
        return True
        

class TBButton(Button):
    """Defines a toolbar button widget"""
    def __init__(self, master, **options):
        Button.__init__(self, master, **options)
        self.config(padx = 2, pady = 2)
        
class TBContainer(Frame):
    """Sets up a container for toolbar widgets"""
    def __init__(self, master, topMenu):
        Frame.__init__(self, master, bd = 2, relief = GROOVE, bg = 'green')
        self.pack(fill = BOTH, expand = 1)
        
        # a list of tuples consiting of the toolbar label and the toolbar object
        # self._tbList is a list of all currently rendered toolbars
        # self._tbMasterList is a list of all created toolbars
        self._tbList = []
        self._tbMasterList = []
        
        # pop up menu
        self._popup = Menu(root, tearoff=0)
        self.bind('<Button-3>', self.do_popup)
        self._topMenu = topMenu
        self._initPopup()
        
        # always initialize the standard toolbar
        tb3 = ToolBar(self)
        tb3.setButtons([{'text': "And"}, {'text': "then"}, {'text': "there"},
                    {'text': "were"}, {'text': "three"}])
        tb3.setLabel('Standard')
        tb3.toggleLabel()
        self.addTB(tb3)
        self._popup.invoke('Standard')
        
    def setTBList(self, tblist):
        """Clear the toolbar list and then populate it appropriately"""
        self._tbList = []
        for tb in tblist:
            self._tbList.append(tb.getLabel()['text'], tb)
        
    def removeTB(self, tb):        
        # the grid geometry manager needs to forget about this widget or else it
        # will put it back in whenever it can even if we never render it
        # explicitly. 
        tb.grid_forget()
        self._tbList.pop(self._tbList.index((tb.getLabel()['text'],tb)))
        self.render()
        
    def addTB(self, tb):
        tb_tuple = (tb.getLabel()['text'], tb)
        if tb_tuple not in self._tbMasterList:
            self._tbMasterList.append(tb_tuple)
        
    def moveTB(self, tb, direction):
        tb_tuple = (tb.getLabel()['text'], tb)
        i = self._tbList.index(tb_tuple)
        if direction == 'right':
            try:
                self._tbList[i] = self._tbList[i+1]
                self._tbList[i+1] = tb_tuple
            except IndexError:
                print "can't move right farther"
        elif direction == 'left':
            if i != 0:
                self._tbList[i] = self._tbList[i-1]
                self._tbList[i-1] = tb_tuple
            else:
                print "can't move left farther"
                
    def getTBList(self):
        return self._tbList
    
    def _initPopup(self):
        # add standard toolbar
        try:
            self._popup.index('Standard')
        except TclError:
            self._popup.add_checkbutton(label = 'Standard', 
                        command = lambda e = 'Standard': self._toggleTB(e))
            self._popup.add_separator()
        
        # create popup and toolbars from the top menu
        for item in self._topMenu.getList():
            try: #check if it's already been added
                self._popup.index(item[0])
            except TclError: #add the item and create the toolbar
                # Use lambda function to mimic an event binding
                self._popup.add_checkbutton(label = item[0], 
                        command = lambda e = item[0]: self._toggleTB(e))
                
                tb = ToolBar(self)
                tbButtons = []
                for button in item[1]:
                    if isinstance(button, dict) and button.get('label'):
                        tbButtons.append({'text': button.get('label'), 
                                          'icon': button.get('icon')})
                tb.setButtons(tbButtons)
                tb.setLabel(item[0])
                tb.toggleLabel()
                self.addTB(tb)
            
    
    def do_popup(self, event):
        """Modified from http://effbot.org/zone/tkinter-popup-menu.htm"""
        # display the popup menu
        try:
            self._popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self._popup.grab_release()
    
    def _toggleTB(self , e):
        found = False
        for tb in self._tbList:
            if e == tb[0]:
                # the toolbar is already showing so remove it
                found = True
                self.removeTB(tb[1])
        if not found:
            # the toolbar isn't showing so add it
            for tb in self._tbMasterList:
                if e == tb[0]:
                    self.addTB(tb[1])
                    self._tbList.append(tb)
    
        self.render()
    
    def render(self):
        i = 0
        for tb in self._tbList:
            tb[1].render(i)
            i += 1

def test(master):
    master.minsize(700,480)
    master.geometry("800x600")
    testMenu = AntiochMenus.MenuBar(master)
    tbContainer = TBContainer(master, testMenu)

    tb1 = ToolBar(tbContainer)
    tb2 = ToolBar(tbContainer)

    tb1.setButtons([{'text': "new"}, {'text': "edit"}])
    tb1.setLabel('test')
    tb1.toggleLabel()

    tb2.setButtons([{'text': "foo"}, {'text': "bar"}])
    tb2.setLabel('foobar')
    tb2.toggleLabel()
    
    for tb in [tb1,tb2]:
        tbContainer.addTB(tb)

if __name__ == '__main__':
    root = Tk()
    test(root)
    root.mainloop()
