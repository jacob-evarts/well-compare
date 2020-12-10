#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 11:25:05 2019

@author: jacob
"""

"""Minor cleaning and combining of two sets of data (Ex. No prior vs prior overexpression)
    for analysis. Creates document for replicate and document for well analysis"""
    
import pandas as pd
import os
from sys import exit

def comb(DATA_PATH):
    # Create Directories
    try:
        os.mkdir(DATA_PATH + "Data/Model_OD")
    except OSError:
        print ("Creation of the directory %s failed" % (DATA_PATH + "Data/Model_OD"))
        
    # Reads user input for plate names
    inp = ""
    file_names = []
    print("\nEnter list of proteins and conditions to COMBINE & CLEAN before graphing (Ex. Pus6_17), or type all; stop to end:")
    while inp != "stop" and inp != "all":
        inp = input("- ")
        if inp == "stop":
            continue
        elif inp == "all":
            try:
                for file in os.listdir(DATA_PATH + "Data/Raw_OD"):
                    # if the element is an xlsx file then
                    if file[-5:] == ".xlsx":
                        file = file[0:-12]
                        if file not in file_names:
                            file_names.append(file)
            except FileNotFoundError:
                print("Could not find file or directory " + DATA_PATH + "Data/Raw_OD - Exiting...")
                exit(1)
        else:
            file_names.append(inp)
    print("Starting...\n")
    
    # Loop through input strains data
    for file_name in file_names:
        try:
            # Growth with no prior overexpression
            df_A = pd.read_excel(DATA_PATH + "Data/Raw_OD/" + file_name + "A_rawOD.xlsx")
            # Growth with prior overexpression
            df_B = pd.read_excel(DATA_PATH + "Data/Raw_OD/" + file_name + "B_rawOD.xlsx")
        except FileNotFoundError:
            print("Could not find " + file_name)
            continue
        # Drop the temperature column
        df_A.drop(df_A.columns[1], axis=1, inplace=True)
        df_B.drop(df_B.columns[1], axis=1, inplace=True)
        
        #repl_combined_df = pd.DataFrame()
        well_combined_df = pd.DataFrame()
        
        # Well rows
        rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
        times = []
        
        for x in range(df_A.shape[0]):
            times.append(x*2)
            
        times_series = pd.Series(times)
        #repl_combined_df["Time"] = times_series
        well_combined_df["Time"] = times_series
        
        # Reordering of wells so that comperable wells are adjacent
        for i in range(12):
            for j in range(8):
                col_name = str(rows[j]) + str(i+1)
                well_combined_df[col_name + "_No_PO"] = df_A[col_name]
                well_combined_df[col_name + "_PO"] = df_B[col_name]
        
        path = DATA_PATH + "Data/Model_OD/"
        
        #repl_combined_df.to_excel(repl_path + file_name + "_repl_combined.xlsx")
        well_combined_df.to_excel(path + file_name + "_well_combined.xlsx")
        
if __name__ == "__main__":
    print("Enter name of screen directory (Ex. 'Screen1')")
    inp = input("- ")
    comb("../Screens/Data/" + inp + "/")
        