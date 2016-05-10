import subprocess

def getNumactlHardware():
    #return subprocess.check_output(["numactl", "--hardware"])
    f = open("numactl_hardware.txt", "r")

    return f.read();
    
def getDplaceQQQ():
    #return subprocess.check_output(["dplacec", "-qqq"])
    f = open("place_qqq.txt", "r")

    return f.read();