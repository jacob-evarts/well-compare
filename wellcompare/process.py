#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 16:32:51 2019

Updated June 4, 2021

@author: jacob
"""

""" Program to automate the production of graphs, heatmaps, and significance
    tests (ttest) on growth curve data. Raw data should be named in the format
    protein_stressAndPlate_rawOD (pus6_31B_rawOD.xlsx) and put into a folder 
    called RawOD before being run through combineOD.py before being run
    through this program. 
        - direct well to well comparison between two plates
"""

import os
from sys import exit

# Helper files
import extract
from grph import graph
import plate

# Enter folder name hard coded here if running graph.py as main for testing
DATA_PATH_HC = "../Screens/Test/"  
              
def process(dp, hm_flag, log_flag):
    global DATA_PATH
    DATA_PATH = dp
    
    # Extracts the data from the format output by the Epoch2 plate reader
    df_dict = extract.extr(DATA_PATH)
            
    print("Graphing...\n")
    
    # Create Directories
    make_dir(DATA_PATH + "Graphs")
    #make_dir(DATA_PATH + "Graphs/Replicates")
    #make_dir(DATA_PATH + "Summaries")
    # Heatmap functionality is being updated
    #make_dir(DATA_PATH + "Heatmaps")
    #make_dir(DATA_PATH + "Heatmaps/GR")
    #make_dir(DATA_PATH + "Heatmaps/Ymax")
    
    # Checks to see if plate mapping file exists is present
    map_file = ""
    try:
        for file in os.listdir(DATA_PATH):
            # if the element is an xlsx file then
            if file == "plate_mapping.txt" or file == "plate_mappings.txt":
                map_file = file 
    except FileNotFoundError:
        print("FileNotFoundError, try making a plate_mapping.txt file and trying again")
        exit(0)
        
    # Build data structures for comparisons
    plate_names = list(df_dict.keys())
    # Initialize plate objects for each plate
    plate_obj_list = {}
    for plate_name in plate_names:
        plate_obj_list[plate_name] = plate.Plate(plate_name, {}) 
        
    # List to hold all comparisons being made
    comparisons = []
    # Parse plaate_mapping.txt for instructions
    with open(DATA_PATH + map_file, "r") as map_f:
        for line in map_f:
            # Mapping of experimental replicates
            if "replicates" in line.lower():
                line = map_f.readline()
                while line != "\n" and line != "":
                    # Plate name
                    if line.strip(":\n") in plate_names:
                        # Create a plate object
                        plate_name = line.strip(":\n")                        
                        line = map_f.readline()
                        # Replicate mapping in plate
                        while line != "\n" and line != "" and line.replace(":\n", "") not in plate_names:
                            wells = []
                            tokens = line.split(":")
                            repl_name = tokens[0]
                            well_str = tokens[1]
                            indiv_wells = well_str.split(",")
                            for well in indiv_wells:
                                wells.append(well.strip(", \n"))
                            # Add replicate info to the corresponding plate object
                            plate_obj_list[plate_name].add_repl(repl_name, wells)
                            line = map_f.readline()
            
            elif "compare" in line.lower():
                line = map_f.readline()
                while line != "\n" and line != "":
                    comp = []
                    tokens = line.split(":")
                    for token in tokens:
                        comp.append(token.strip(" \n"))
                    comparisons.append(comp)
                    line = map_f.readline()
                               
                    
    for comparison in comparisons:
        # Comparing two strains
        if len(comparison) == 2:
            exp_repl = comparison[0]
            exp_data = {}
            con_repl = comparison[1]
            con_data = {}
            # Loop through plates pulling out groupings of replicates
            for plate_name in plate_obj_list.keys():
                plat = plate_obj_list[plate_name]
                
                if exp_repl in plat.get_repl_names():
                    exp_data[plate_name] = plat.get_wells(exp_repl)
                    
                elif con_repl in plat.get_repl_names():
                    con_data[plate_name] = plat.get_wells(con_repl)
                    
            # If log flag was chosen create extra directory
            if log_flag:
                make_dir(DATA_PATH + "Graphs/" + exp_repl + "/Log2_Graphs")
                
        # Comparing three strains comping in future update
        elif len(comparison) == 3:
            pass

        graph(df_dict, con_data, exp_data, con_repl, exp_repl, DATA_PATH, hm_flag, log_flag, avg=True)
        
    print("Finished.")
    
""" Auxillary Functions """
def make_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
       #print("Creation of the directory %s failed" % (dir_name))
       pass
       
if __name__ == "__main__":
    process(DATA_PATH_HC, hm_flag = False, log_flag = False)