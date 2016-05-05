import subprocess

def getNumactlHardware():
    return subprocess.check_output(["numactl", "--hardware"])