import evaluate
import parse_numactl
import host
import argparse
import sys
import actions

# Global numactl --hardware information
numaHardware = parse_numactl.HardwareInfo(host.getNumactlHardware());


# Fill the arguments into the parser
parser = argparse.ArgumentParser(description='Hydra program startup script. <TODO: MORE DESC>')
parser.add_argument('-cdf', "--closest", metavar='N', type=int,
                   help='outputs a list of nodes, sorted by the distance to the specified node.')
                   
parser.add_argument('-m', "--nodeMemorySuggestion", metavar='N', type=str, nargs=3,
                   help='Displays what nodes to to use to allocate ... TODO! (nodeIdx, maxMB, nodeMinMB)')
                                 
# Parse commandline
args = parser.parse_args()

# Print usage message, if no commands where specified
if len(sys.argv) <= 1:
    parser.print_usage();
    exit()

if args.closest != None:
    actions.printClosestTo(args.closest, numaHardware)
elif args.nodeMemorySuggestion != None:
    actions.printNodeMemSuggestion(args.nodeMemorySuggestion[0], 
                                    args.nodeMemorySuggestion[1], 
                                    numaHardware, args.nodeMemorySuggestion[2])
else:
    print("Nope");

