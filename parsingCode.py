def out(mat1):
    for a in range(0,len(mat1)):
            print(mat1[a])
import os
import numpy as np
base_path = ""
filename = ""
path_to_file = os.path.join(base_path, filename)
fd = open(path_to_file , 'r')
lines =[]
connections1 = []
connections2 = []
pins = []
for line in fd:
    lines.append(line)
for x in lines:
    if '(pins' in x:
        loc3 = x.find("(")+6
        x = x[loc3:]
        loc3=x.find(")")
        x = x[:loc3]
        temp = x
        connections1 = []
        while True:
            loc = temp.find(" ")
            if(loc ==-1):
                pins.append(temp)
                connections1.append(temp)  
                connections2.append(connections1)
                break
            else:
                pins.append(temp[:loc])
                connections1.append(temp[:loc])
                temp = (temp[(1+loc):]) 
mat = [[]]
mat[0]=[""]
for x in pins:
    temp = [x]
    mat.append(temp)
    mat[0].append(x)
size = len(pins)+1
for a in range (1,size):
    for b in range(1,size):
        mat[a].append(0)
for a in range(1,len(mat)):
    for b in range(0,len(connections2)):
        for c in range(0,len(connections2[b])):
            if mat[a][0]==connections2[b][c]:
                for d in connections2[b]:
                    for e in range(1,len(mat[0])):
                        if d==mat[0][e]and not d==mat[a][0]:
                            mat[a][e]=1
out(mat)                           