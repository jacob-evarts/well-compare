#!/usr/bin/python

import argparse
from wellcompare.graph import grph

parser = argparse.ArgumentParser(description='Graphing options.',
                                 usage='%(prog) -m [-hm] [--version]')
# Adds a flag for heatmap generation
parser.add_argument('-hm', 
                    action='store_true',
                    help='Creates heatmaps of plate growth (default=False)')
args = parser.parse_args()

if __name__ == "__main__":
    print("Enter name of screen directory (Ex. 'Screen1')")
    inp = input("- ")
    grph("Screens/" + inp + "/", args.hm)
    
