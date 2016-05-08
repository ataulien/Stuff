import evaluate

def memStringToMByte(memstr):
    """ Checks whether the unit was added to the given memory-size value and converts it to megabytes.
        For example: 1GB -> 1024- """
        
    if memstr.find("GB") != -1:
        return int(memstr[0:memstr.find("GB")]) * 1024
    else:
        return int(memstr)

def printNodeMemSuggestion(nodeIdx, maxMB, hardwareInfo, minNodeFreeMB=0):
    """ Prints what nodes to use to the maxMB MByte of RAM from the given source-node """
    r = evaluate.nodesForMemory(int(nodeIdx), memStringToMByte(maxMB), hardwareInfo, memStringToMByte(minNodeFreeMB))
    
    if r == None:
        print("Could not find nodes matching the given criteria.")
        return
    
    print("Need " + str(len(r["list"])) + " nodes: " + str(r["list"])[1:-1])
    print("Max distance: " + str(r["maxDist"]))
    
    if r["memLeft"] != 0:
        print("WARNING: " + str(r["memLeft"] )) + "MB leftover!"

def printClosestTo(nodeIdx, hardwareInfo):
    """ Prints a list if nodes with the shortest distance to the given input node """
    # Get list of nodes sorted by distance
    dl = evaluate.shortestDistanceFrom(nodeIdx, hardwareInfo)
    
    print("Nodes sorted by distance to Node #" + str(nodeIdx) + ":")
    print(str(dl)[1:-1])
    