import numpy as np

# ==============================================================================
# Helper Functions


def get_pins_from_cell(cell):
    """ Return the list of pins for the cell """

    # TODO
    return ['empty']


def get_pins_from_cells(cells):

    return {get_pins_from_cell(c) for c in cells}


# ==============================================================================
# Costs functions

def calculate_net_pins_WA(net, pins_locations):
    """ Calculates the Weighted Average Wirelenght for the net and pins. """

    # TODO
    return float('inf')


def calculate_net_WA(net, cell_locations):
    """ 
    Calculates the Weighted Average Wirelenght for the net and pins of cells. 
    """

    return calculate_net_pins_WA(net, cell_locations)


def calculate_nets_WA(nets, cell_locations):
    """ 
    Calculates the Weighted Average Wirelenght for the net and pins of cells. 
    """

    return np.sum([calculate_net_WA(net, cell_locations) for net in nets])


def calculate_density_penalty(cell_locations):

    # TODO
    return float('inf')


def calculate_cost(nets, cell_locations):
    """
    Merge results of WA cost with density penalty for the full design
    """

    with cell_locations as cls, nets as ns:
        return calculate_nets_WA(ns, cls)+calculate_density_penalty(cls)

# ==============================================================================
# Optimization functions


def optimize_WA(nets, cell_locations):
    """ Update cell_locations (Global Placement) based on gradient descent """

    # TODO
    return None


def main():
    print("Hello")


if __name__ == "__main__":
    main()
