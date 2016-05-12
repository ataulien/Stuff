import evaluate
import host
import argparse
import sys
import actions
import util

# Fill the arguments into the parser
parser = argparse.ArgumentParser(description='Hydra program startup script. <TODO: MORE DESC>', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', "--info", metavar='[closest|used|free|proc]', choices=['closest', 'used', 'free', 'proc'],
                   help='Prints information about the given choice:\n' + 
                        ' - closest: With the "-n N" argument passed, this will print all nodes ordered by the distance to node N.\n' +
                        ' - used:    Displays used nodes (By processes only) and used CPUs, as well as what process is using which CPUs.\n' +
                        ' - free:    Displays free nodes (By processes only) and free CPUs.\n' +
                        ' - proc:    Displays information about the process given with the "-p"-flag.\n ')
  
parser.add_argument('-n', "--node", metavar='N', type=int,
                   help='Sets the source node for operations needing a single input-node.\n ')

parser.add_argument('-p', "--proc", metavar='P',
                   help='Sets the name of the process to operate on.\n ')              
          
parser.add_argument('--noHT', action='store_true',
                   help='Ignores all Hyperthreading-Cores while parsing.\n ')

#parser.add_argument('-m', "--nodeMemorySuggestion", metavar='N', type=str, nargs=3,
#                   help='Displays what nodes to to use to allocate ... TODO! (nodeIdx, maxMB, nodeMinMB)')

#parser.add_argument('-s', "--stripcpus", action='store_true',
#                   help='''If a cpu list is given as output by any of the other flags, this will ensure, that the list only contains
#                         CPUs of which all the other CPUs on the same node appear in the output list. ''')

#parser.add_argument("--makecmd", action='store_true',
#                   help='''Output a sample command using the specified options of the other arguments''')                         

# Parse commandline
args = parser.parse_args()

# Print usage message, if no commands where specified
if len(sys.argv) <= 1:
    parser.print_usage();
    exit()

if args.info != None:
    actions.printInfo(args)


