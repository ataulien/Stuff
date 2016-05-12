import StringIO   
import math
from parse import *

class DistanceMatrix:
    nodes = []
    def __init__(self, lines): 
        # Input are lines like this:
        # node   0   1   2   ...
        #   0:  10  50  65  ... 
        #   1:  50  10  65  ... 

        # Catch an empty input-list
        if not lines:
            return

        # Check for the right input-terms
        assert lines[0].startswith("node"), "Unexpected input"
        
        # Strip the table-column-descriptor
        lines = lines[1:]
        
        # Create an empty nxn-matrix
        self.nodes =  [[0 for i in xrange(len(lines))] for i in xrange(len(lines))] 
        
        i=0
        for l in lines:
            assert ":" in l, "Expected format '##: ...', got: '" + l + "'"
            
            # Strip the node-number and : from the begining
            l = l[l.index(":")+1:]
            
            # Remove multiple spaces
            l = ' '.join(l.split())
            
            # Get all numbers as list, thus creating an array of distances from 
            # this node to the one at the specific array index
            d = [int(n) for n in l.split(' ')]
            
            # Fill each nodes distance to each other
            for j in xrange(0, len(d)):
                self.nodes[i][j] = d[j]
            
            i+=1
            
        #self.normalize()
        return
        
        
    def distance(self, n1, n2):
        """ Returns the distance between the nodes n1 and n2 """
        return self.nodes[n1][n2]

    def normalize(self):
        """ Forces all distance-values to between 0 and 1 """
        m = 0
        
        # Calculate max distance
        for i in xrange(0, len(self.nodes)):
                m = max(m, max(self.nodes[i]))
                
        # Normalize all data entries
        for i in xrange(0, len(self.nodes)):
            for j in xrange(0, len(self.nodes)):
                self.nodes[i][j] = self.nodes[i][j] / float(m)
                        
        return    



class HardwareInfo:
    # Total number of nodes available
    nodesAvailable = 0
        
    # dict of nodes and a list of their associated CPU indices
    nodeCPUs = []
    nodeMemSize = []
    nodeMemFree = []
    totalNumCPUs = 0
    firstHyperThreadingCPU = 0
    distanceMatrix = DistanceMatrix([])
    
    # Map of CPU indices and nodes 
    nodesByCPUIdx = []
    
    def __init__(self, in_str, noHT=False):
        """ Parses the output of numactl --hardware and returns a HardwareInfo-Object """
        
        buf = StringIO.StringIO(in_str)
        lines = buf.readlines()
        lines = [l.rstrip() for l in lines] # Remove newlines, as we already linefied this
        
        i = 0
        for l in lines:
            # Parse all possible line-types
            rvalue = parse("{name}:{body}", l)
            rsection = parse("{name}:", l) 
            rcpu = parse("node {node:d} cpus: {nlist}", l)
            rmemsize = parse("node {node:d} size: {size:d} MB", l)
            rmemfree = parse("node {node:d} free: {free:d} MB", l)
            
            if rvalue != None:
                if rvalue["name"] == "available":
                    # Parse number and range of available nodes
                    rn = parse("{n:d} nodes ({nodes})", rvalue["body"])
                                       
                    self.nodesAvailable = int(rn["n"])
                    
                    # Initialize info-lists
                    self.nodeCPUs = [0] * self.nodesAvailable
                    self.nodeMemFree = [0] * self.nodesAvailable
                    self.nodeMemSize = [0] * self.nodesAvailable
                                                
            if rsection != None:
                if rsection["name"] == "node distances":
                    # Parse the Node-Distance matrix
                    self.distanceMatrix = DistanceMatrix(lines[(i+1):])
            
            if rcpu != None:
                # Add the list of all CPUs of this node
                self.nodeCPUs[rcpu["node"]] = [int(n) for n in rcpu["nlist"].split(' ')]
                self.totalNumCPUs = max(self.totalNumCPUs, max(self.nodeCPUs[rcpu["node"]]) + 1)
            
            if rmemsize != None:
                self.nodeMemSize[rmemsize["node"]] = rmemsize["size"];
                
            if rmemfree != None:
                self.nodeMemFree[rmemfree["node"]] = rmemfree["free"];
                    
            i += 1
            
        # FIXME: This is pretty much bruteforce, O(n^2),
        #        but I don't wrap my head around calculating these now
        self.nodesByCPUIdx = [0] * self.totalNumCPUs
        for i in xrange(0, self.totalNumCPUs):
            self.nodesByCPUIdx[i] = self.__getNodeByCPU(i)
            
        # Get the first HT-CPU
        self.firstHyperThreadingCPU = self.__getFirstHTCpu()
            
        # Remove all hyperthreading cores, if wanted
        if noHT:
            for cl in self.nodeCPUs:
                rem = []
                for c in cl:
                    if c >= self.firstHyperThreadingCPU:
                        rem.append(c)
                for r in rem:
                    cl.remove(r)
            
        return        
        
    def __getFirstHTCpu(self):
        """ Returns the first Hyperthreading-CPU by index """
        return int(math.floor(self.totalNumCPUs / 2.0) + 1)
        
    def getNodeByCPU(self, cpu_idx):
        """ Returns the node-index of the node the given CPU is on """
        print(cpu_idx)
        return self.nodesByCPUIdx[cpu_idx]
        
    def __getNodeByCPU(self, cpu_idx):
        """ Returns the node-index of the node the given CPU is on """
        
        # Guess first
        
        # Couldn't find it there, search everywhere
        # TODO: This is pretty slow. Improve!
        i = 0
        for cl in self.nodeCPUs:
            
            if cpu_idx in cl:
                return i
            i += 1
            
        print("Failed to find CPU with index: " + str(cpu_idx))
        print(self.nodeCPUs)
        return -1
                
    def invertCPUSet(self, cpu_list, allowHT=True):
        """ 'Inverts' the given list of CPU-Ids, meaning that it will return a list 
            containing all available CPUs, except those which where in the input list
            @param cpu_list List of CPUs to exclude from the output-list
            @param allowHT Whether to allow Hyperthreading CPUs to appear in the output-list """
        
        r = []    
        for cl in self.nodeCPUs:
            for c in cl:
                if not c in cpu_list:
                    r.append(c)
        
        return r
        
    def invertNodeSet(self, node_list):
        """ 'Inverts' the given list of nodes. The output list will contain 
            all nodes not given in the input list. """
        
        r = range(0, self.nodesAvailable)
        r = [x for x in r if not x in node_list]
        return r
        
    def stripCPUSet(self, cpu_list):
        """ Leaves only those CPUs in the output list which appear with every other CPU on their corresponding node.
            CPUs which share the node with CPUs not given in the list, will be removed. """
        
        # Only allow cpus of which their nodes cpus are a subset of the input-list
        return [x for x in cpu_list if set(self.nodeCPUs[self.getNodeByCPU[n]]) < set(cpu_list)]
                            
    
            
   