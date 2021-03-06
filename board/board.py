# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

class Element:
    """Base class for all the Modules, Pins, Nets etc."""

    def __init__(self, name):
        self.name = name
        self.element_type = None

    def get_name(self):
        print(self.name)

    def get_type(self):
        print(self.element_type)


class Pin(Element):
    """Pin of a Module."""

    def __init__(self, name, x_offset=0, y_offset=0):
        Element.__init__(self, name)

        self.x_offset = x_offset
        self.y_offset = y_offset


class Module(Element):
    """Module is a component that contains pins under its surface."""

    def __init__(self, name, x_pos=0, y_pos=0, width=10, height=10):
        Element.__init__(self, name)
        Element.element_type = 'Module'

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

        # Every module has at least one pin
        self.pin_count = 0
        self.pins = []
        self.pins.append(Pin(self.name+"{:02d}".format(self.pin_count)))
        self.pin_count = 1


class Net(Element):
    """Net connects pins together."""

    def __init__(self, name):
        Element.__init__(self, name)


class Board(Element):
    """Board is the enviroment with Modules and Nets."""

    # List of nets
    # List of Modules

    def __init__(self, name, width=0, height=0):
        Element.__init__(self, name)
        
        self.width = width
        self.height = height

        self.modules = []
        self.nets = []
