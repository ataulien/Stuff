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
        lastJob = None
        for l in lines:
            # Parse all possible line-types
            rjob = parse("0x{key} {nTasks:d} {owner} {pid:d} {cpu:d} {name}", l)
            rfork = parse("{pid} {cpu:d} {name}", l)
            
            if rjob != None:
                # Init with an empty list, if this is the first entry
                if not rjob["name"] in self.processes:
                   self.processes[rjob["name"]] = [] 
                   
                self.processes[rjob["name"]].append({"nTasks":rjob["nTasks"], 
                                                "owner":rjob["owner"], 
                                                "pid":rjob["pid"], 
                                                "cpu":rjob["cpu"],   
                                                "name":rjob["name"]})
                lastJob = rjob
            elif rfork != None and lastJob != None:
                # Forked process use an other format, but are listed below the parent
                self.processes[lastJob["name"]].append({"nTasks":lastJob["nTasks"], 
                                                "owner":lastJob["owner"], 
                                                "pid":rfork["pid"], 
                                                "cpu":rfork["cpu"],   
                                                "name":rfork["name"]})
                                                               
            

    def getUsedCPUSet(self):
        """ Returns a list of all currently used CPUs """
        r = []
        
        for n in self.processes:
            for p in self.processes[n]:
                r.append(p["cpu"])
        
        r = sorted(r)
        
        return r
        
    def getCPUsByJobname(self, job):
        """ Returns a list of all currently used CPUs of the given job """
        
        if not job in self.processes:
            return []
        
        ls = []
        for p in self.processes[job]:
            ls.append(p["cpu"]) 
       
        ls = list(set(sorted(ls)))
       
        return ls
        
    def getProcessesByJobname(self, job):
        """ Returns the list of processes for the given jobname """
        
        if not job in self.processes:
            return []
            
        return self.processes[job] 
        
