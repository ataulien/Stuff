import subprocess

if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

def getNumactlHardware():
    return subprocess.check_output(["numactl", "--hardware"])
    # f = open("numactl_hardware.txt", "r")

    # return f.read();
    
def getDplaceQQQ():
    return subprocess.check_output(["dplace", "-qqq"])
    # f = open("place_qqq.txt", "r")

    # return f.read();
    
def getDlookByName(name):
    out = subprocess.check_output(["dlook", name])
  
    # f = open("dlook.txt", "r")
    # out = f.read();
    
    # if not out.startswith("Peek:"):
    #     print("dlook failed. '" + out + "'")
    #     return ""
        
    # return out