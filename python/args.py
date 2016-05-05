import argparse

parser = argparse.ArgumentParser(description='Process some stuff.')
parser.add_argument('stuff', metavar='N', nargs=5)
parser.add_argument('-f', action='store_true')

args = parser.parse_args()
print(args.f)
