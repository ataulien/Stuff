import StringIO
from parse import *

class ProcessInfo:
    processes = {} # Map of process-names and a list of their PIDs and CPUs
    def __init__(self, in_str): 
        """ Parses the output of dplace -qqq """
        
        buf = StringIO.StringIO(in_str)
        lines = buf.readlines()
        lines = [l.rstrip() for l in lines] # Remove newlines, as we already linefied this
        lines = [' '.join(l.split()) for l in lines] # Remove whitespace
        
        i = 0
        for l in lines:
            # Parse all possible line-types
            rjob = parse("0x{key} {nTasks:d} {owner} {pid:d} {cpu:d} {name}", l)
            
            if rjob != None:
                # Init with an empty list, if this is the first entry
                if not rjob["name"] in self.processes:
                   self.processes[rjob["name"]] = [] 
                   
                self.processes[rjob["name"]].append({"nTasks":rjob["nTasks"], 
                                                "owner":rjob["owner"], 
                                                "pid":rjob["pid"], 
                                                "cpu":rjob["cpu"],   
                                                "name":rjob["name"]})

    def getUsedCPUSet(self):
        """ Returns a list of all currently used CPUs """
        r = []
        
        for n in self.processes:
            for p in self.processes[n]:
                r.append(p["cpu"])
        
        return r
       
            
        
