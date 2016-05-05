import StringIO # for readline
import parse_numactl
import evaluate

f = open("numactl_hardware.txt", "r")

txt = f.read();

inf = parse_numactl.HardwareInfo(txt)
print(inf.nodesAvailable)

evaluate.shortestDistanceFrom(3, inf)