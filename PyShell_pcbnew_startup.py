import pcbnew
import os
import json
import numpy as np
class pcbnew1(pcbnew.ActionPlugin):
    def board(self):
        board = pcbnew.GetBoard()
        return board
    def pin_set(self):
        """ Returns an array with all pins in the circuit.""" 
        
        board = self.board()
        modList = board.GetModules()
        modListVals =[]
        for x in modList:
            modListVals.append(str(x.GetReference()))
        return modListVals

    def net_list(self):
        """ Returns a 2d array with all netcodes and net names in the circuit."""
        
        nets =[]
        num =0
        board = self.board()
        netcodes = board.GetNetsByNetcode()
        for netcode, net in netcodes.items():
            nets.append([])
            nets[num].append(netcode)
            nets[num].append(str(net.GetNetname()))
            num = num+1
        return nets
        
    def pad_list(self):
        """ Returns a 2d array with pads in the circuit."""
        
        board = self.board()
        modListVals=self.pin_set()
        num = 0
        pads = []
        for z in modListVals: 
            pads.append([])
            mod = board.FindModuleByReference(z)
            for pad in mod.Pads():
                pads[num].append(str(mod.GetReference())+"_"+str(pad.GetPadName()))
            num=num+1
        return pads
        
    def position(self):
        """ Returns a 2d array with coordinates of pins."""
        
        board = self.board()
        modListVals=self.pin_set()
        positions = []
        temp =0
        for z in modListVals: 
            positions.append([])
            mod = board.FindModuleByReference(z)
            pos = mod.GetFootprintRect()
            posCenter= pos.Centre()
            positions[temp].append(posCenter.x/1000)
            positions[temp].append(posCenter.y/1000)
            temp = temp +1
        return positions
        
    def dimensions(self):
        """ Returns a 2d array with dimensions of pins."""
        
        board = self.board()
        modListVals=self.pin_set()
        compDimensions = []
        temp=0
        for z in modListVals: 
            compDimensions.append([])
            mod = board.FindModuleByReference(z)
            pos = mod.GetFootprintRect()
            posHeight= pos.GetHeight()
            posWidth = pos.GetWidth()
            compDimensions[temp].append(posWidth/1000)
            compDimensions[temp].append(posHeight/1000)
            temp = temp+1
        return compDimensions
        
    def matrix_no_pads(self):
        """ Returns an adjacency matrix of components, not pads with names."""
        
        
        board = self.board()
        connections = []
        nums = 0
        temp =0
        modListVals=self.pin_set()
        for x in range (0, len(modListVals)+1):
            connections.append([])
            for y in range (0,len(modListVals)+1):
                connections[nums].append(0)
            nums = nums +1
        for x in range(1,len(modListVals)+1):
            connections[0][x]=modListVals[temp]
            connections[x][0]=modListVals[temp]
            temp = temp +1
        for x in range(1,len(modListVals)+1):
            mod = board.FindModuleByReference(connections[0][x])
            for pad in mod.Pads():
                netNum = pad.GetNetCode()
                for y in range (1,len(modListVals)+1):
                    mod1 = board.FindModuleByReference(connections[0][y])
                    for pad1 in mod1.Pads():
                        netNum1 = pad1.GetNetCode()
                        if netNum==netNum1 and not mod.GetReference() ==mod1.GetReference():
                            connections [x][y]=1
                            connections [y][x]=1
        return connections
            
    def matrix_pads(self): 
        """ Returns an adjacency matrix of pads."""
        
        board = self.board()
        connections = []
        connections1 =[]
        pads1 = []
        temp =0
        nums = 0
        modListVals=self.pin_set()
        num = 0
        pads = []
        for z in modListVals: 
            pads.append([])
            mod = board.FindModuleByReference(z)
            for pad in mod.Pads():
                pads[num].append(str(mod.GetReference())+" "+str(pad.GetPadName()))
            num=num+1
        for x in pads:
            for y in x:
                pads1.append(y)
        for x in range (0, len(pads1)+1):
            connections.append([])
            for y in range (0,len(pads1)+1):
                connections[nums].append(0)
            nums = nums+1    
        for x in range(1,len(pads1)+1):
            connections[0][x]=pads1[temp]
            connections[x][0]=pads1[temp]
            temp = temp +1
        padNetList = []
        temp = 0
        nums =0
        padNames = []
        for x in range(0,len(modListVals)):
            mod = board.FindModuleByReference(modListVals[x])
            for y in mod.Pads():
                padNetList.append(y.GetNetCode())
        for x in range (1,len(connections[0])):
            padNames.append(connections[0][x])
        temp = 0
        padNameNetList = []
        for x in range(0,len(padNames)):
            padNameNetList.append([])
            padNameNetList[temp].append(padNames[x])
            padNameNetList[temp].append(padNetList[x])
            temp = temp+1
        for x in range(0,len(padNameNetList)):
            for y in range(0,len(padNameNetList)):
                if padNameNetList[x][1]== padNameNetList[y][1] and not padNameNetList[x][0] ==padNameNetList[y][0]:
                    connections[x+1][y+1]=1
                    connections[y+1][x+1]=1
        temp = 0
        for x in range(1,len(connections)):
            connections1.append([])
            for y in range(1,len(connections[x])):
                connections1[temp].append(connections[x][y])
            temp = temp +1
        return connections1
     
    def net_matrix(self):
        """ Returns a matrix of pins connected by each net."""
        
        board = self.board()
        nets =[]
        connections = []
        netcodes = board.GetNetsByNetcode()
        for netcode, net in netcodes.items():
            nets.append(netcode)
        modListVals=self.pin_set()
        temp = 0
        for x in nets:
            connections.append([])
            for y in modListVals:
                connections[temp].append(0)
            temp = temp +1
        for x in range(0,len(modListVals)):
            mod = board.FindModuleByReference(modListVals[x])
            for y in mod.Pads():
                for z in range(0,len(nets)):
                    if y.GetNetCode() == z:
                        connections[z][x]=1
        connections=np.asarray(connections)
        return connections
        
        
    def writeToDoc(self):
        """Writes arrays to a python doc"""
    
        base_path = "C:\\Northeastern\\Semester 2\\Kicad project\\parsing"
        filename = "info.txt"
        path_to_file = os.path.join(base_path, filename)
        # with open(path_to_file, 'w+') as f:
            # print>> f,"pin_set=",(self.pin_set())
            # print>>f,"print(pin_set)"
            # print >>f,"net_matrix=", self.net_matrix()
            # print >>f, "print(net_matrix)"
            # print>>f,"adjacency_matrix=",self.matrix_pads()
            # print >>f, "print(adjacency_matrix)"
            # print>>f,"position_array=",self.position()
            # print >>f, "print(position_array)"
            # print>>f,"dimension_array=", self.dimensions()
            # print>>f,"print(dimension_array)"
        d={}
        d[0] = {'pin_set': self.pin_set()}
        d[1]={'net_matrix': self.net_matrix()}
        d[2]={'adjacency_matrix': self.matrix_pads()}
        d[3]={'position_array':self.position()}
        d[4]={'dimension_array':self.dimensions()}
        with open(path_to_file, 'w') as file:
            file.write(json.dumps(d))
               
        
def main():
        """Creates a new pcbnew1 object and calls writeToDoc"""
        a = pcbnew1()
        a.writeToDoc()
        
       
if __name__ == "__main__":
        main()