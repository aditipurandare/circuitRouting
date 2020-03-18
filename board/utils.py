import itertools
import numpy as np


def get_adjacency_matrix(net_matrix):
    """Returns adjacency matrix based on nets matrix"""
    N_NETS = net_matrix.shape[0]
    N_COMPONENTS = net_matrix.shape[1]

    adjacency_matrix = np.zeros(shape=(N_COMPONENTS, N_COMPONENTS))
    for net_idx in range(N_NETS):
        to_connect = []
        for pin_idx in range(N_COMPONENTS):
            if net_matrix[net_idx, pin_idx] == 1:
                to_connect.append(pin_idx)

        index_list = [index for index in itertools.product(
            to_connect, to_connect)]

        for index in index_list:
            adjacency_matrix[index] = 1

    # componets do not connect to themselves
    adjacency_matrix[np.identity(N_COMPONENTS, dtype=bool)] = 0
    return adjacency_matrix
