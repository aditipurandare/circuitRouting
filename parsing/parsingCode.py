import os
import numpy as np
from argparse import ArgumentParser


def print_matrix(mat1):
    for a in range(0, len(mat1)):
            print(mat1[a])


def get_adjacency_from_file(filename):
    """
    Expects the path to a dsn file.
    returns a list of lists containing the adjacency matrix
    """
    base_path = ""
    path_to_file = os.path.join(base_path, filename)
    fd = open(path_to_file, 'r')
    lines = []
    connections1 = []
    connections2 = []
    pins = []
    for line in fd:
        lines.append(line)
    for x in lines:
        if '(pins' in x:
            loc3 = x.find("(")+6
            x = x[loc3:]
            loc3 = x.find(")")
            x = x[:loc3]
            temp = x
            connections1 = []
            while True:
                loc = temp.find(" ")
                if(loc == -1):
                    pins.append(temp)
                    connections1.append(temp)
                    connections2.append(connections1)
                    break
                else:
                    pins.append(temp[:loc])
                    connections1.append(temp[:loc])
                    temp = (temp[(1+loc):])
    mat = [[]]
    mat[0] = [""]
    for x in pins:
        temp = [x]
        mat.append(temp)
        mat[0].append(x)
    size = len(pins)+1
    for a in range(1, size):
        for b in range(1, size):
            mat[a].append(0)
    for a in range(1, len(mat)):
        for b in range(0, len(connections2)):
            for c in range(0, len(connections2[b])):
                if mat[a][0] == connections2[b][c]:
                    for d in connections2[b]:
                        for e in range(1, len(mat[0])):
                            if d == mat[0][e]and not d == mat[a][0]:
                                mat[a][e] = 1
    return mat

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

def main():

    parser = ArgumentParser(description="Parses DSN files")
    parser.add_argument("-i", dest="filename", required=True,
                        help="input dsn file", metavar="FILE",
                        # type=lambda x: is_valid_file(parser, x)
                        )

    args = parser.parse_args()

    print (args.filename)
    mat = get_adjacency_from_file(args.filename)

    print_matrix(mat)

if __name__ == "__main__":
    main()
