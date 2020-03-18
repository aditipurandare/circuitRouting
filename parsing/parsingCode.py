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



def get_components_pos_from_file(filename):
    """
    Expects the path to a dsn file.
    returns a list of lists containing componets positions
    """
    base_path = ""
    path_to_file = os.path.join(base_path, filename)
    fd = open(path_to_file, 'r')

    lines = []
    l = [] 
    locations = [[]]

    for line in fd:
        lines.append(line)
    for x in lines:
        if '(place' in x:
            temp = x
            ne =0
            temp= temp[temp.find("place"):]
            temp= temp[temp.find(" "):]
            for _ in range(0,3):
                temp= temp[temp.find(" ")+1:]
                ne = temp.find(" ")+1
                l.append(temp[:ne])
    for _ in range(0,3):
        del l[0]
    for p in range(0,int(len(l)/3)-1):
            locations.append([])
    for p in range(0,int(len(l)/3)):
        for q in range(0,3):
            locations[p].append(l[q])
        for _ in range(0,3):
            del(l[0])
    return locations


def get_area(filename):
    lines =[]
    outlines = []
    xVals = []
    yVals = []
    base_path = ""
    path_to_file = os.path.join(base_path, filename)
    fd = open(path_to_file, 'r')
    for line in fd:
        lines.append(line)
    string =""
    n=0
    for line in fd:
        lines.append(line)
    outlines = []
    xVals = []
    yVals = []
    for x in range(0,len(lines)-1):
        if not "signal 50" in lines[x+1] and "signal 50" in lines[x]:
            outlines.append([])
            xVals.append([])
            yVals.append([])
    print(len(outlines))
    string =""
    n=0
    for x in range(0,len(lines)-1):
        if "outline" in lines[x]:
            lines[x]=lines[x][28:]
            if not "outline" in lines[x+1]:
                lines[x+1]=lines[x+1][28:]   
        if lines[x][0]=="5":
            lines[x]=lines[x][4:]
            l1 = lines[x].find(" ")
            xVals[n].append(lines[x][:l1])
            lines[x]=lines[x][l1+1:]
            l1 = lines[x].find(" ")
            yVals[n].append(lines[x][:l1])
            lines[x]=lines[x][l1+2:]
            l1 = lines[x].find(" ")
            xVals[n].append(lines[x][:l1])
            lines[x]=lines[x][l1+1:]
            l1 = lines[x].find(")")
            if lines[x].find(" ")>l1:
                yVals[n].append(lines[x][:lines[x].find(" ")])
            else:
                yVals[n].append(lines[x][:l1])
            string +=lines[x]
            if len(lines[x+1])<28 or not (lines[x+1][28:][0])=="5":
                string =""
                n+=1
    length = []
    width = []
    area = []
    lenNum = 0
    for p in range(0,len(yVals)):
        minValy = float(yVals[p][0])
        maxValy = float(yVals[p][0])
        for q in range(0,len(yVals[p])):
            if  (float(yVals[p][q]))<minValy:
                minValy = float(yVals[p][q])
            if (float(yVals[p][q]))>maxValy:
                maxValy = float(yVals[p][q])
    for p in range(0,len(yVals)):
        minValx = float(xVals[p][0])
        maxValx = float(xVals[p][0])   
        for q in range(0,len(yVals[p])):    
            if (float(xVals[p][q]))<minValx:
                minValx = float(xVals[p][q])
            if (float(xVals[p][q]))>maxValx:
                maxValx = float(xVals[p][q])
        length.append(maxValy-minValy)
        width.append(maxValx-minValx)
        area.append(length[lenNum]*width[lenNum])
        lenNum+=1
    return(area)
    
def main():

    # Parse arguments
    parser = ArgumentParser(description="Parses DSN files")
    parser.add_argument("-i", dest="filename", required=True,
                        help="input dsn file", metavar="FILE",
                        # type=lambda x: is_valid_file(parser, x)
                        )

    args = parser.parse_args()

    # Process matrices
    adj_mat = get_adjacency_from_file(args.filename)
    print_matrix(adj_mat)
    
    pos_mat = get_components_pos_from_file(args.filename)
    print(pos_mat)
    
    area=get_area(args.filename)
    print(area)

if __name__ == "__main__":
    main()
