import evaluate
import parse_numactl
import host
import argparse
import sys

print("Got output: " + host.getNumactlHardware())

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-closest', metavar='-c', type=int,
                   help='outputs a list of nodes, sorted by the distance to the specified node')
                   
parser.add_argument('-test', metavar='-t', type=int,
                   help='outputs a list of nodes, sorted by the distance to the specified node')                   


args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_usage();
    exit()

if not any(args.values()):
    parser.error('Use -h to display possible commandline-arguments.')
    
print(args.accumulate(args.integers))

