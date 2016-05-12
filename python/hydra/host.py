import subprocess

def getNumactlHardware():
    #return subprocess.check_output(["numactl", "--hardware"])
    f = open("numactl_hardware.txt", "r")

    return f.read();
    
def getDplaceQQQ():
    #return subprocess.check_output(["dplace", "-qqq"])
    f = open("place_qqq.txt", "r")

    return f.read();
    
def getDlookByName(name):
    # out = subprocess.check_output(["dlook", name])
  
    f = open("dlook.txt", "r")
    out = f.read();
    
    if not out.startswith("Peek:"):
        print("dlook failed. '" + out + "'")
        return ""
        
    return out