import numpy as np
import os
def readFromDoc():
    """Reads values from info and converts them into numpys"""
    base_path = [insert path]
    filename = "info.txt"
    path_to_file = os.path.join(base_path, filename)
    w = eval(open(path_to_file, 'r').read())
    #w[0]:list of pins
    #w[1]:matrix of nets showing connected components
    #w[2]:pad connection matrix
    #w[3]:coordinates of component position
    #w[4]:dimensions of components
    for x in w:
        w[x] = np.asarray(w[x])
        
def main():
        """"""
        readFromDoc()
if __name__ == "__main__":
        main()