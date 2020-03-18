import random
import string
import itertools

import numpy as np


def generate_random_name():
    """Generte a random string with three letters and two numbers"""

    output = ''.join([random.choice(string.ascii_letters).upper()
                      for n in range(3)])
    output = output+"_" + \
        "".join([random.choice(string.digits) for n in range(2)])
    return output


def generate_random_position(grid_dim=(200, 200), mode='uniform', sigma=None):
    """Generate a (x,y) tuple within the specified gridsize"""
    if (mode == 'gaussian'):
        x = grid_dim[0]/2
        y = grid_dim[1]/2
        if (sigma == None):
            sigma = x/10
        x = np.floor(random.gauss(mu=x, sigma=sigma))
        y = np.floor(random.gauss(mu=x, sigma=sigma))
    else:
        x = np.floor(random.random()*grid_dim[0])
        y = np.floor(random.random()*grid_dim[1])
    return x, y


def generate_random_sizes(size_l_lim=1, size_u_lim=10, mode='uniform'):
    """Generate a random (w,h) tuple withing the specified limits"""
    w = size_l_lim
    h = size_l_lim

    size_range = size_u_lim-size_l_lim

    if (mode == 'triangular'):
        #params=(size_l_lim, size_l_lim+size_range*.1, size_u_lim, 1)
        w = np.floor(random.triangular(
            size_l_lim, size_l_lim+size_range*.3, size_u_lim))
        h = np.floor(random.triangular(
            size_l_lim, size_l_lim+size_range*.3, size_u_lim))
    else:
        w = np.floor(random.random()*size_range+size_l_lim)
        h = np.floor(random.random()*size_range+size_l_lim)

    return w, h
