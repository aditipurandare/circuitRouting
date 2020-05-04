import pcbnew
board = pcbnew.GetBoard()

#modules
modList = board.GetModules()
modListVals =[]
for x in modList:
	modListVals.append(str(x.GetReference()))
	
#networks
nets =[]
num =0
netcodes = board.GetNetsByNetcode()
for netcode, net in netcodes.items():
	nets.append([])
	nets[num].append(netcode)
	nets[num].append(str(net.GetNetname()))
	num = num+1
	
#pads
modList = board.GetModules()
modListVals =[]
for x in modList:
	modListVals.append(str(x.GetReference()))
num = 0
pads = []
for z in modListVals: 
    pads.append([])
    mod = board.FindModuleByReference(z)
    for pad in mod.Pads():
        pads[num].append(str(mod.GetReference())+" "+str(pad.GetPadName()))
    num=num+1
	
#position
xPos= []
yPos = []
for z in modListVals: 
    mod = board.FindModuleByReference(z)
    pos = mod.GetFootprintRect()
    posCenter= pos.Centre()
    xPos.append(posCenter.x/1000)
    yPos.append(posCenter.y/1000)
	
#heights+widths+area
compHeights = []
compWidths = []
compAreas = []
for z in modListVals: 
    mod = board.FindModuleByReference(z)
    pos = mod.GetFootprintRect()
    posHeight= pos.GetHeight()
    posWidth = pos.GetWidth()
    posArea = pos.GetArea()
    compHeights.append(posHeight/1000)
    compWidths.append(posWidth/1000)
    compAreas.append(posArea/1000000)
    
#matrix without pads
connections = []
nums = 0
temp =0
modList = board.GetModules()
modListVals =[]
for x in modList:
	modListVals.append(str(x.GetReference()))
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
                    
#pad matrix              
connections = []                 
pads1 = []
tempNums = []
temp =0
nums = 0
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