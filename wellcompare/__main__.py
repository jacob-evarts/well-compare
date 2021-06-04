#!/usr/bin/python
import argparse
if __package__ is None or __package__ == '':
    # uses current directory visibility
    from process import proces
else:
    # uses current package visibility
    from wellcompare.process import proces

parser = argparse.ArgumentParser(description='Graphing options.',
                                 usage='%(prog) -m [-hm] [-log] [--version]')
# Adds a flag for heatmap generation
parser.add_argument('-hm', 
                    action='store_true',
                    help='Creates heatmaps of plate growth (default=False)')

parser.add_argument('-log',
                    action='store_true',
                    help='Creates log growth curves (default=False)')

args = parser.parse_args()

if __name__ == "__main__":
    print("Enter name of screen directory (Ex. 'Screen1')")
    inp = input("- ")    
    proces(inp, args.hm, args.log)
    
