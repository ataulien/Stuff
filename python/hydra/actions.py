import evaluate
import parse_dplace

def memStringToMByte(memstr):
    """ Checks whether the unit was added to the given memory-size value and converts it to megabytes.
        For example: 1GB -> 1024- """
        
    if memstr.find("GB") != -1:
        return int(memstr[0:memstr.find("GB")]) * 1024
    else:
        return int(memstr)

def printNodeMemSuggestion(args, hardwareInfo):
    """ Prints what nodes to use to the maxMB MByte of RAM from the given source-node """
    r = evaluate.nodesForMemory(int(args.nodeMemorySuggestion[0]), memStringToMByte(args.nodeMemorySuggestion[1]), hardwareInfo, memStringToMByte(args.nodeMemorySuggestion[2]))
    
    if r == None:
        print("Could not find nodes matching the given criteria.")
        return
    
    print("Need " + str(len(r["list"])) + " nodes: " + str(r["list"])[1:-1])
    print("Distance:")
    print(" - max: " + str(r["maxDist"]))
    print(" - average: " + str(int(round(r["avgDist"]))))
    
    if r["memLeft"] != 0:
        print("WARNING: " + str(r["memLeft"] )) + "MB leftover!"

def printClosestTo(args, hardwareInfo):
    """ Prints a list of nodes with the shortest distance to the given input node """
    # Get list of nodes sorted by distance
    dl = evaluate.shortestDistanceFrom(args.node, hardwareInfo)
    dist = [hardwareInfo.distanceMatrix.distance(args.node, x) for x in dl]
    
    print("Nodes sorted by distance to Node #" + str(args.node) + ":")
    print("Nodes: " + str(dl)[1:-1])
    print("Distances:")
    
    dmap = {}
    
    # Init list
    for d in dist:
        dmap[d] = []
        
    i = 0
    for d in dist:
        dmap[d].append(dl[i])
        i += 1
        
    # Print nodes by distance
    for d in sorted(dmap):
        print( " - " + str(d) + ": " + str(dmap[d])[1:-1])
    
def printInfo(args, hardwareInfo, processInfo):
    """ Prints all (un)used nodes and CPUs or distance-information about a given node """
    
    # Get list of used and unsused CPUs/Nodes
    # TODO: Use dlook to check whether a node is used by a process on a different node
    #       There are no access rights for querying another process yet, though!
    usedCPUs = processInfo.getUsedCPUSet()
    unusedCPUs = hardwareInfo.invertCPUSet(usedCPUs)
    
    usedNodes = list(set([hardwareInfo.getNodeByCPU(x) for x in usedCPUs]))
    unusedNodes = hardwareInfo.invertNodeSet(usedNodes)
    
    if args.info == "used":
        print(str(len(usedNodes)) + " used Nodes: " + hardwareInfo.stringifySequences(usedNodes))
        print(str(len(usedCPUs)) + " used CPUs: " + hardwareInfo.stringifySequences(usedCPUs))
        
    elif args.info == "free":
        print(str(len(unusedNodes)) + " unused Nodes: " + hardwareInfo.stringifySequences(unusedNodes))
        print(str(len(unusedCPUs)) + " unused CPUs: " + hardwareInfo.stringifySequences(unusedCPUs))
    
    elif args.info == "closest":
        if args.node == None:
            print(""" "closest"-operation needs source-node specified by -n """)
            exit()
        
        printClosestTo(args, hardwareInfo)
