import parse_numactl

def cmpNodes(x, y):
    # If distances are the same, compare the free memory
    if x[0] == y[0]: 
        if x[1] > y[1]:
           return -1
        return 0
                                        
    if x[0] < y[0]:
        return -1
    else:
        return 1

def shortestDistanceFrom(nodeIdx, hardwareInfo):
    """ Returns a list of nodes sorted by their distance to the given node
        Note: This list does contain the given node itself. 
              Nodes with the same distance are sorted by free memory.  
        @param nodeIdx [int] Index of the source-node
        @param hardwareInfo [parse_numactl.HardwareInfo] parsed info from numactl"""

    # Get the list of all nodes this node can reach
    nodesDist = hardwareInfo.distanceMatrix.nodes[nodeIdx]
    memFree = hardwareInfo.nodeMemFree;

    # Zip with their specific index, creating a list like this:
    # [(0, 123, 3), (1, 123, 4), ... (dist, free, idx)]
    zipped = zip(nodesDist, memFree, range(0, hardwareInfo.nodesAvailable))

    # Sort by distance-key
    # zipped = sorted(zipped, key=lambda x: x[0])
    zipped = sorted(zipped, cmp=cmpNodes)

    # Unzip that list again
    unzipped = zip(*zipped)

    # Third entry of the unzipped pair does now contain the sorted node-indices
    return unzipped[2]

def nodesForMemory(nodeIdx, maxMB, hardwareInfo, nodeMinMBFree=0):
    """ Returns a dict of nodes required to get 'memMB' MByte of RAM and the maximum distance to a node included in that list 
        @param nodeIdx Start node to search from 
        @param maxMB Maximum amount of memory to try to fit into the nodes RAM (In MByte) 
        @param hardwareInfo [parse_numactl.HardwareInfo] parsed info from numactl
        @param nodeMinMBFree Minimum amount if RAM which must be free on a node to qualify
        @return (resultList, max-Distance, memory leftover) """
    
    dl = shortestDistanceFrom(nodeIdx, hardwareInfo)
    
    r = [] # result list
    dr = [] # result node distance list
    
    memLeft = maxMB;
    for n in dl:
        if hardwareInfo.nodeMemFree[n] > nodeMinMBFree:
            # If this node has free memory, add it to the list
            r.append(n)
            memLeft = max(0, memLeft - hardwareInfo.nodeMemFree[n])
            
            # Also save the distance to this node to weight the results later
            dr.append(hardwareInfo.distanceMatrix.distance(nodeIdx, n))
            
            if memLeft == 0:
                break
                
    # Return result nodes and max distance                        
    if len(r) != 0:
        return {"list": r, 
            "maxDist": max(dr),
            "memLeft": memLeft}
    else:
        return None 
    