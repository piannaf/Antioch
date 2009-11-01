import xml.parsers.expat
from AntiochCanvas import *

class Circuit:
    """Allows for loading and saving of circuit files in Logisim format """
    def __init__(self):

        self._parseIndex = 0
        self._wires = []
        self._components = []
        self._go = False
        self._loadedCircuit = ''

        #attributes which have been programmed so far
        self._attrList = ["inputs", "width", "value", "select", "size"]
        #components which have been programmed so far
        #TODO: Make this be generated when loading libraries so that they
        #can act as plugins
        self._compList = ["Wire", "NOT Gate", "Buffer", "AND Gate", "OR Gate",
                          "NAND Gate", "NOR Gate", "XOR Gate", "XNOR Gate",
                          "Constant", "Multiplexer", "Adder", "D Flip-Flop",
                          "Pin", "Button", "Hex Digit Display", "LED"]

    def start_element(self, name, attrs):
        """ Event handler on start of an XML element
        Uses expat parsing information to store data about wires, components
        and their attributes.
        """
        status = False

        if name == "circuit":
            self._go = True
        if self._go:
            
            if name == "wire":
                self._wires.append(attrs)
            if name == "comp":
                self._components.append([attrs, {}])
                self._parseIndex += 1
            if name == "a":
                self._components[self._parseIndex - 1][1][attrs['name']] \
                                                  = attrs['val']
    def load(self, file):
        """Loads a Logisim .circ file and parses it for circuit information
        It saves a list of every component which is compatible with Antioch
        into self._loadedCircuit
        
        load(self)-> None
        """
        self._circuitFile = open(file, 'U')
        
        self._parser = xml.parsers.expat.ParserCreate()
        self._parser.StartElementHandler = self.start_element

        self._parser.Parse(self._circuitFile.read())
        self._circuitFile.close()
        
        string = ''
        for wire in self._wires:
            string += "Wire(workspace,complex(*" + str(wire['from']) +\
                      "),complex(*" + str(wire['to']) + "))\n"
            
        for component in self._components:
            if component[0]['name'] in self._compList:
                string += component[0]['name'].replace(' ', '_').replace('-', '_') + \
                         "(workspace, complex(*" + component[0]['loc'] + ")"
                for key in component[1].keys():
                    #I've only implemented some parts
                    if key in self._attrList:
                      string += ',' + str(key) + " = " + str(component[1][key])
                string += ")\n"

        self._loadedCircuit = string.split('\n')
        
    def render(self, workspace):
        """Renders stored components onto workspace"""
        for component in self._loadedCircuit:
            #don't care about empty strings
            if component:
                #if there are any errors, print will show us where it happened
                #print component
                eval(component)
    
    def save(self, workspace, filename):
        """Saves the Antioch workspace to a Logisim .circ file as indicated by
        filename
        
        """
        
        string = self.preamble()
        for obj in workspace.find_all():
            objTags = workspace.gettags(obj)
            objCoords = workspace.coords(obj)
            if "compBBox" in objTags and "input" not in objTags and "output" not in objTags:
                if "Wire" in objTags:
                    string += "<wire from=\"(" + str(self.nearest10(objCoords[0])) + "," + \
                               str(self.nearest10(objCoords[1])) + ")\" to=\"(" + \
                               str(self.nearest10(objCoords[2])) + "," + \
                               str(self.nearest10(objCoords[3])) + ")\" />\n"
                else:
                    string += "<comp lib=\"" + eval(objTags[1])['lib'] + \
                              "\" name=\"" + eval(objTags[1])['name'] + \
                              "\" loc=\"(" + str(self.nearest10(objCoords[0])) + "," + \
                               str(self.nearest10(objCoords[1])) + ")\"/>\n"
                    attributes = eval(objTags[2])
                    for attr in attributes.keys():
                        string += "\t<a name=\"" + attr + "\" val=\"" +\
                                   str(attributes[attr]) + "\" />\n"
        
        string += "  </circuit>\n" + "</project>"
        
        savefile = open(filename, 'w')
        return savefile.write(string)
        
    def preamble(self):
        """A convenient place to write down the beginning of a .circ file
        This assumes only the default libraries will be used and that they will
        have the correct enumeration between different version of logisim.
        This has been tested with logisim version 2.3.0
        
        preamble(void)-> string
        """
        preamble = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" +\
                    "<project version=\"1.0\" source=\"2.3.0\">\n" +\
                    "  This file is intended to be loaded by Logisim (http://www.cburch.com/logisim/).\n" +\
                    "  <lib name=\"0\" desc=\"#Base\">\n" +\
                    "    <tool name=\"Edit Tool\" />\n" +\
                    "    <tool name=\"Select Tool\" />\n" +\
                    "    <tool name=\"Text Tool\">\n" +\
                    "      <a name=\"text\" val=\"\" />\n" +\
                    "      <a name=\"font\" val=\"SansSerif plain 12\" />\n" +\
                    "      <a name=\"halign\" val=\"center\" />\n" +\
                    "      <a name=\"valign\" val=\"base\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Splitter\">\n" +\
                    "      <a name=\"facing\" val=\"south\" />\n" +\
                    "      <a name=\"fanout\" val=\"2\" />\n" +\
                    "      <a name=\"incoming\" val=\"2\" />\n" +\
                    "      <a name=\"bit0\" val=\"0\" />\n" +\
                    "      <a name=\"bit1\" val=\"1\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Pin\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"output\" val=\"false\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"tristate\" val=\"true\" />\n" +\
                    "      <a name=\"pull\" val=\"none\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelloc\" val=\"west\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Probe\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"radix\" val=\"2\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelloc\" val=\"west\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Clock\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"highDuration\" val=\"1\" />\n" +\
                    "      <a name=\"lowDuration\" val=\"1\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelloc\" val=\"west\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Text\">\n" +\
                    "      <a name=\"text\" val=\"\" />\n" +\
                    "      <a name=\"font\" val=\"SansSerif plain 12\" />\n" +\
                    "      <a name=\"halign\" val=\"center\" />\n" +\
                    "      <a name=\"valign\" val=\"base\" />\n" +\
                    "    </tool>\n" +\
                    "  </lib>\n" +\
                    "  <lib name=\"1\" desc=\"#Gates\">\n" +\
                    "    <tool name=\"Constant\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"value\" val=\"0x1\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"NOT Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"30\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Buffer\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"AND Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"OR Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"NAND Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"NOR Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"XOR Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "      <a name=\"xor\" val=\"1\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"XNOR Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "      <a name=\"xor\" val=\"1\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Odd Parity\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Even Parity\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Controlled Buffer\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Controlled Inverter\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "    </tool>\n" +\
                    "  </lib>\n" +\
                    "  <lib name=\"2\" desc=\"#Plexers\">\n" +\
                    "    <tool name=\"Multiplexer\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"select\" val=\"1\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Demultiplexer\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"select\" val=\"1\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"tristate\" val=\"false\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Decoder\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"select\" val=\"1\" />\n" +\
                    "      <a name=\"tristate\" val=\"false\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Priority Encoder\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"select\" val=\"3\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"BitSelector\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "      <a name=\"group\" val=\"1\" />\n" +\
                    "    </tool>\n" +\
                    "  </lib>\n" +\
                    "  <lib name=\"3\" desc=\"#Arithmetic\">\n" +\
                    "    <tool name=\"Adder\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Subtractor\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Multiplier\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Divider\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Negator\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Comparator\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "      <a name=\"mode\" val=\"twosComplement\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Shifter\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "      <a name=\"shift\" val=\"ll\" />\n" +\
                    "    </tool>\n" +\
                    "  </lib>\n" +\
                    "  <lib name=\"4\" desc=\"#Memory\">\n" +\
                    "    <tool name=\"D Flip-Flop\">\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"T Flip-Flop\">\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"J-K Flip-Flop\">\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"S-R Flip-Flop\">\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Register\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Counter\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "      <a name=\"max\" val=\"255\" />\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Shift Register\">\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"length\" val=\"8\" />\n" +\
                    "      <a name=\"parallel\" val=\"true\" />\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Random\">\n" +\
                    "      <a name=\"width\" val=\"8\" />\n" +\
                    "      <a name=\"seed\" val=\"0\" />\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"RAM\">\n" +\
                    "      <a name=\"addrWidth\" val=\"8\" />\n" +\
                    "      <a name=\"dataWidth\" val=\"8\" />\n" +\
                    "      <a name=\"bus\" val=\"combined\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"ROM\">\n" +\
                    "      <a name=\"addrWidth\" val=\"8\" />\n" +\
                    "      <a name=\"dataWidth\" val=\"8\" />\n" +\
                    "      <a name=\"contents\">addr/data: 8 8 0</a>\n" +\
                    "    </tool>\n" +\
                    "  </lib>\n" +\
                    "  <lib name=\"5\" desc=\"#I/O\">\n" +\
                    "    <tool name=\"Button\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"color\" val=\"#ffffff\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelloc\" val=\"center\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "      <a name=\"labelcolor\" val=\"#000000\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Joystick\">\n" +\
                    "      <a name=\"bits\" val=\"4\" />\n" +\
                    "      <a name=\"color\" val=\"#ff0000\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Keyboard\">\n" +\
                    "      <a name=\"buflen\" val=\"32\" />\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"LED\">\n" +\
                    "      <a name=\"facing\" val=\"west\" />\n" +\
                    "      <a name=\"color\" val=\"#f00000\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelloc\" val=\"center\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "      <a name=\"labelcolor\" val=\"#000000\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"7-Segment Display\">\n" +\
                    "      <a name=\"color\" val=\"#f00000\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"Hex Digit Display\">\n" +\
                    "      <a name=\"color\" val=\"#f00000\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"DotMatrix\">\n" +\
                    "      <a name=\"inputtype\" val=\"column\" />\n" +\
                    "      <a name=\"matrixcols\" val=\"5\" />\n" +\
                    "      <a name=\"matrixrows\" val=\"7\" />\n" +\
                    "      <a name=\"color\" val=\"#00ff00\" />\n" +\
                    "      <a name=\"offcolor\" val=\"#404040\" />\n" +\
                    "      <a name=\"dotshape\" val=\"square\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool name=\"TTY\">\n" +\
                    "      <a name=\"rows\" val=\"8\" />\n" +\
                    "      <a name=\"cols\" val=\"32\" />\n" +\
                    "      <a name=\"trigger\" val=\"rising\" />\n" +\
                    "    </tool>\n" +\
                    "  </lib>\n" +\
                    "  <main name=\"main\" />\n" +\
                    "  <options>\n" +\
                    "    <a name=\"showgrid\" val=\"true\" />\n" +\
                    "    <a name=\"preview\" val=\"false\" />\n" +\
                    "    <a name=\"showhalo\" val=\"true\" />\n" +\
                    "    <a name=\"showhalo\" val=\"true\" />\n" +\
                    "    <a name=\"zoom\" val=\"1.0\" />\n" +\
                    "    <a name=\"gateUndefined\" val=\"ignore\" />\n" +\
                    "    <a name=\"simlimit\" val=\"1000\" />\n" +\
                    "    <a name=\"simrand\" val=\"0\" />\n" +\
                    "    <a name=\"radix\" val=\"2\" />\n" +\
                    "    <a name=\"radix2\" val=\"10signed\" />\n" +\
                    "    <a name=\"toolbarloc\" val=\"north\" />\n" +\
                    "  </options>\n" +\
                    "  <mappings>\n" +\
                    "    <tool lib=\"0\" name=\"Menu Tool\" map=\"Button2\" />\n" +\
                    "    <tool lib=\"0\" name=\"Menu Tool\" map=\"Button3\" />\n" +\
                    "    <tool lib=\"0\" name=\"Menu Tool\" map=\"Ctrl Button1\" />\n" +\
                    "  </mappings>\n" +\
                    "  <toolbar>\n" +\
                    "    <tool lib=\"0\" name=\"Poke Tool\" />\n" +\
                    "    <tool lib=\"0\" name=\"Edit Tool\" />\n" +\
                    "    <tool lib=\"0\" name=\"Text Tool\">\n" +\
                    "      <a name=\"text\" val=\"\" />\n" +\
                    "      <a name=\"font\" val=\"SansSerif plain 12\" />\n" +\
                    "      <a name=\"halign\" val=\"center\" />\n" +\
                    "      <a name=\"valign\" val=\"base\" />\n" +\
                    "    </tool>\n" +\
                    "    <sep />\n" +\
                    "    <tool lib=\"0\" name=\"Pin\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"output\" val=\"false\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"tristate\" val=\"false\" />\n" +\
                    "      <a name=\"pull\" val=\"none\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelloc\" val=\"west\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool lib=\"0\" name=\"Pin\">\n" +\
                    "      <a name=\"facing\" val=\"west\" />\n" +\
                    "      <a name=\"output\" val=\"true\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"tristate\" val=\"true\" />\n" +\
                    "      <a name=\"pull\" val=\"none\" />\n" +\
                    "      <a name=\"label\" val=\"\" />\n" +\
                    "      <a name=\"labelloc\" val=\"east\" />\n" +\
                    "      <a name=\"labelfont\" val=\"SansSerif plain 12\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool lib=\"1\" name=\"NOT Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"30\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool lib=\"1\" name=\"AND Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "    </tool>\n" +\
                    "    <tool lib=\"1\" name=\"OR Gate\">\n" +\
                    "      <a name=\"facing\" val=\"east\" />\n" +\
                    "      <a name=\"width\" val=\"1\" />\n" +\
                    "      <a name=\"size\" val=\"50\" />\n" +\
                    "      <a name=\"inputs\" val=\"5\" />\n" +\
                    "    </tool>\n" +\
                    "  </toolbar>\n" +\
                    "  <circuit name=\"main\">\n"
  
        return preamble
        
    def nearest10(self, n):
        """Round number to nearest 10
        
        nearest10(float)-> int
        """
        return int(divmod(n + 5, 10)[0]*10)
def test(master):
    master.minsize(700,480)
    master.geometry("800x600")
    
    #create and instance of a circuit before loading the workspace
    circuit = Circuit()
    workspace = WorkSpace(master, circuit)
    
    #test loading a Logism File
    circuit.load("./tests/Design.circ")
    circuit.render(workspace)
    
    #test saving to a Logism File
    circuit.save(workspace, "test.circ")
        
if __name__ == '__main__':
    root = Tk()
    test(root)
    root.mainloop()
