import evaluate
import parse_dplace
import parse_dlook
import host
import util
import parse_numactl
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
    
def printProcInfo(args, hardwareInfo, processInfo):
    """ Prints information about the process given in args.proc """
    
    # Retrieve basic information about used CPUs and which nodes these CPUs are on
    cpus = processInfo.getCPUsByJobname(args.proc)
    nodes = set()
    for c in cpus:
        nodes.add(hardwareInfo.getNodeByCPU(c))
    
    # Query dlook for more information
    pinfo = parse_dlook.SingleProcessInfo(host.getDlookByName(args.proc))
    
    print("Process summary for '" + args.proc + "':")
    print(" - CPUs:")
    print("     Total: " + str(len(cpus)))
    
    if len(cpus) == 1:
        print("     Index: " + str(cpus[0]))
    else:
        print("     Indices: " + util.stringifySequences(cpus))
    
    print("     Nodes: " + util.stringifySequences(list(nodes)))
    print(" - Memory on: ")
    
    for n in pinfo.nodesAllocatedOn:
        print("     Node " + str(n[0]) + ": " + util.formatByteSize(n[1]))
        
    print(" - Total: " + util.formatByteSize(pinfo.totalMemoryUsed))
    
def printInfo(args):
    """ Prints all (un)used nodes and CPUs or distance-information about a given node """
    
    # numactl --hardware information
    
    hardwareInfo = parse_numactl.HardwareInfo("")
    try:
        hardwareInfo = parse_numactl.HardwareInfo(host.getNumactlHardware(), args.noHT)
    except Exception as e:
        print("Could not get hardware info. Exception:" + e.message)
    
    processInfo = parse_dplace.ProcessInfo("")
    try:
        processInfo = parse_dplace.ProcessInfo(host.getDplaceQQQ())
    except Exception as e:
        print("Could not get process info. Exception:" + e.message)
    
            
    
    # Get list of used and unsused CPUs/Nodes
    # TODO: Use dlook to check whether a node is used by a process on a different node
    #       There are no access rights for querying another process yet, though!
    usedCPUs = processInfo.getUsedCPUSet()
    unusedCPUs = hardwareInfo.invertCPUSet(usedCPUs)
    
    usedNodes = list(set([hardwareInfo.getNodeByCPU(x) for x in usedCPUs]))
    unusedNodes = hardwareInfo.invertNodeSet(usedNodes)
    
    if args.info == "used":
        print(str(len(usedNodes)) + " used Nodes: " + util.stringifySequences(usedNodes))
        print(str(len(usedCPUs)) + " used CPUs: " + util.stringifySequences(usedCPUs))
        print("")
        
        if len(processInfo.processes) > 0:          
            print("Process CPU summary:")
        
            # Print all CPUs used by the given process
            for j in processInfo.processes:
                print(" - " + j + ": " + util.stringifySequences(processInfo.getCPUsByJobname(j)))
        else:
            print("No processes running.")
        
    elif args.info == "free":
        print(str(len(unusedNodes)) + " unused Nodes: " + util.stringifySequences(unusedNodes))
        print(str(len(unusedCPUs)) + " unused CPUs: " + util.stringifySequences(unusedCPUs))
    
    elif args.info == "closest":
        if args.node == None:
            print(""" "closest"-operation needs source-node specified by -n """)
            exit()         
        
        printClosestTo(args, hardwareInfo)
    elif args.info == "proc":
        if args.proc == None:
            print(""" "proc"-operation needs process specified by -p """)
            exit()  
        
        printProcInfo(args, hardwareInfo, processInfo)
