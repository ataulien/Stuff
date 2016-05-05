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
        return nodes[n1][n2]

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
    
    def __init__(self, in_str):
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
                    rn = parse("{n:d} nodes ({s:d}-{e:d})", rvalue["body"])
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
                self.totalNumCPUs = max(self.totalNumCPUs, max(self.nodeCPUs[rcpu["node"]]))
            
            if rmemsize != None:
                self.nodeMemSize[rmemsize["node"]] = rmemsize["size"];
                
            if rmemfree != None:
                self.nodeMemFree[rmemfree["node"]] = rmemfree["free"];
                    
            i += 1
            
        # Get the first HT-CPU
        self.firstHyperThreadingCPU = self.__getFirstHTCpu()
            
        return        
        
    def __getFirstHTCpu(self):
        """ Returns the first Hyperthreading-CPU by index """
        return int(math.floor(self.totalNumCPUs / 2.0) + 1)
        
   