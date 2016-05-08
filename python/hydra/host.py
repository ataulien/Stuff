import subprocess

def getNumactlHardware():
    #return subprocess.check_output(["numactl", "--hardware"])
    f = open("numactl_hardware.txt", "r")

    return f.read();