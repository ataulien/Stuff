import StringIO
from parse import *

class SingleProcessInfo:
    totalMemoryUsed = 0
    nodesAllocatedOn = [] # Pair of (nodeIdx, bytes)
        
    def __init__(self, in_str=""): 
        """ Parses the output of dlook <PID> """
        
        if in_str == "":
            return
        
        buf = StringIO.StringIO(in_str)
        lines = buf.readlines()
        lines = [l.rstrip() for l in lines] # Remove newlines, as we already linefied this
        lines = [' '.join(l.split()) for l in lines] # Remove whitespace
        
        nodeSet = {}
        
        i = 0
        for l in lines:
            # Parse all possible line-types
            rpages = parse("[{memStart}-{memEnd}] {pages:d} {huge}pages on node {node:d} {flags}", l)
            
            if rpages != None:
                # Read memory range as Base-16
                memStart = int(rpages["memStart"], 16)
                memEnd = int(rpages["memEnd"], 16)
                memPages = memEnd - memStart
                
                if not rpages["node"] in nodeSet:
                    nodeSet[rpages["node"]] = 0
                
                # Accumulate
                self.totalMemoryUsed += memPages
                nodeSet[rpages["node"]] += memPages
                           
        self.nodesAllocatedOn = nodeSet.items()
        
    def aggregate(self, spList): 
        # Generate dict again
        nodeSet = dict((key, value) for (key, value) in self.nodesAllocatedOn)
    
        for p in spList:
            self.totalMemoryUsed += p.totalMemoryUsed
            
            if not p[0] in nodeSet:
                    nodeSet[p[0]] = 0
                    
            nodeSet[p[0]] += p[1]
            
        self.nodesAllocatedOn += nodeSet.items()   