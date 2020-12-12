#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 16:32:51 2019

@author: jacob
"""

""" Program to automate the production of graphs, heatmaps, and significance
    tests (ttest) on growth curve data. Raw data should be named in the format
    protein_stressAndPlate_rawOD (pus6_31B_rawOD.xlsx) and put into a folder 
    called RawOD before being run through combineOD.py before being run
    through this program. 
        - direct well to well comparison between two plates
"""

import pandas as pd
import os
from sys import exit

# Helper files
import extract
import combine
from grph import graph

# For graphing different datasets
# Options: "Screen1/"         *ORIGINAL SCREEN*
#          "Screen2/"         *FOLLOW UP*
#          "Screen3/"         *CHECKING SOME OTHER STRAINS*
#          "Full_Drop1/"      *TESTING FULL DROUPOUT MEDIA*
#          "Full_Drop2/"
# or create your own directory inside Screens folder

# Enter folder name hard coded here if running graph.py as main
DATA_PATH_HC = "../Screens/Screen2/"  
              
def process(dp, hm_flag, log_flag):
    global DATA_PATH
    DATA_PATH = dp
    
    inp=""
    print("\nDoes data need to be extracted and cleaned? (y/n)")
    while inp != "y" and inp != "n":
        inp = input("- ")
        if inp == "y":
            # Extracts the data from the format output by the Epoch2 plate reader
            extract.extr(DATA_PATH)
            # Combines two raw files and does some light cleaning
            combine.comb(DATA_PATH)
    
    # Create Directories
    make_dir(DATA_PATH + "Graphs")
    make_dir(DATA_PATH + "Graphs/Replicates")
    make_dir(DATA_PATH + "Summaries")
    make_dir(DATA_PATH + "Heatmaps")
    make_dir(DATA_PATH + "Heatmaps/GR")
    make_dir(DATA_PATH + "Heatmaps/Ymax")            
    # Reads in input files
    inp = ""
    file_names = []
    print("\nEnter list of proteins and conditions to GRAPH (Ex. Pus6_17), or type all; stop to end:")
    while inp != "stop" and inp != "all":
        inp = input("- ")
        if inp == "stop":
            continue
        elif inp == "all":
            try:
                for file in os.listdir(DATA_PATH + "Data/Model_OD"):
                    # if the element is an xlsx file then
                    if file[-5:] == ".xlsx":
                        file = file[0:-19]
                        if file not in file_names:
                            file_names.append(file)
            except FileNotFoundError:
                print("Could not find file or directory " + DATA_PATH + "Data/Raw_OD - Exiting...")
                exit(1)
        else:
            file_names.append(inp)
    print("\nStarting...\n")
    
    # Loops throught the input files to process
    for file_name in file_names:
        # Try to read the excel sheet
        try:
            df = pd.read_excel(DATA_PATH + "Data/Model_OD/" + file_name + "_well_combined.xlsx")
            df.name = file_name
        except FileNotFoundError:
            print("Could not find " + file_name)
            continue
        
        make_dir(DATA_PATH + "Graphs/" + file_name)
        make_dir(DATA_PATH + "Graphs/" + file_name + "/Raw_graphs")
        make_dir(DATA_PATH + "Graphs/Replicates/" + file_name)
        # If log flag was chosen create extra directory
        if log_flag:
            make_dir(DATA_PATH + "Graphs/" + file_name + "/Log2_Graphs")
            
        graph(df, DATA_PATH, hm_flag, log_flag)

""" Auxillary Functions """
def make_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
       print("Creation of the directory %s failed" % (dir_name))
       
if __name__ == "__main__":
    process(DATA_PATH_HC, hm_flag = False, log_flag = False)