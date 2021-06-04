#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 13:10:02 2020

Updated on June 2, 2021

@author: jacob
"""

""" Extracts and cleans the relevant data from the standard output of the Epoch2
    Biotek machine in the 30C room of Striesinger
    Hall, University of Oregon """

import pandas as pd
import numpy as np
import os
from sys import exit


def extr(DATA_PATH):
    print("Extracting and cleaning...\n")

    data_file = ""
    # Data files from the experiment
    try:
        n_files = 0
        for file in os.listdir(DATA_PATH + "/Data"):
            # if the element is an xlsx file then
            if file[-5:] == ".xlsx":
                data_file = file
                n_files += 1
                if n_files > 1:
                    print("Too many data files, combine into one excel file. Exiting...")
                    exit(1)
    except FileNotFoundError:
        print("Could not find file or directory " + DATA_PATH + "/Data - exiting...")
        exit(0)
        
    # Create directory for parsed data
    try:
        os.mkdir(DATA_PATH + "Data/Raw_OD")
    except OSError:
        pass
       
    # Checks to see if experimental info exists is present
    info_file = ""
    try:
        for file in os.listdir(DATA_PATH):
            # if the element is an xlsx file then
            if file == "experiment_info.txt" or file == "experimental_info.txt":
                info_file = file 
    except FileNotFoundError:
        print("FileNotFoundError, try making an experiment_info.txt file and trying again")
        exit(0)
      
    # Experimental info
    ignore_plates = []
    plate_names = []
    num_measurements = ""
    water_plate_pres = False
    
    # Full spreadsheet
    xls = pd.ExcelFile(DATA_PATH + "Data/" + data_file)
    # List of all sheets in spreadsheet
    df_dict = pd.read_excel(xls, None)
        
    # Pulling info from experimental_info.txt
    print("Using information from experiment_info.txt\n")
    
    water_plates = ["top water", "bottom water", "water"]
    with open(DATA_PATH + info_file, "r") as info_f:
        for line in info_f:
            # Read in plate names
            if "plate names" in line.lower():
                line = info_f.readline()
                while line != "\n" and line != "":
                    # Checks if water plate
                    if line.lower().replace("\n", "") not in water_plates:
                        plate_names.append(line.replace("\n", ""))
                    else:
                        water_plate_pres = True
                    line = info_f.readline()
                    
            # Read in plates to ignore
            elif "plates to ignore" in line.lower():
                line = info_f.readline()
                while line != "\n" and line != "":
                    if line.lower().replace("\n", "") != "none":
                        ignore_plates.append(line.strip("\n "))
                    line = info_f.readline()
                
            # Read in the number of measurements
            elif "number of measurements" in  line.lower():
                line = info_f.readline()
                while line != "\n" and line != "":
                    try:
                        num_measurements = int(line.strip("\n "))
                    except ValueError:
                        print("Number of measurements should be an integer. Exiting...")
                        exit(0)
                    line = info_f.readline()
    plate_names = plate_names[::-1] 
                    
    # Experimental information has been loaded, now processing file 
    offset = 0
    df_dict = {}
    if water_plate_pres:
        offset = 1

    stop = len(plate_names)
    for i in range(0, stop):
        plate_name = plate_names[i]
        if plate_name in ignore_plates:
            continue
        else:
            sheet_name = "Plate " + str(i + 1 + offset) + " - Sheet1"
            # Format the dataframe to save correctly to an excel file
            df = pd.read_excel(xls, sheet_name)
            column_names = df.iloc[[25], 1:99].values
            column_names = column_names[0]
            df_new = pd.DataFrame(df.iloc[25:(25 + num_measurements + 1), 1:99])
            df_new.reset_index(drop=True, inplace=True)
            df_new.columns = column_names
            
            # Drop the temperature and time columns
            df_new.drop(columns=["T° 600", "Time"], inplace=True)
            
            # Create a times column with integer approximations of time since start
            times = ["Time"]
            for x in range((df_new.shape[0] - 1)):
                times.append(x*2)
            times_array = np.array(times)
            df_new["Time"] = times_array
            
            df_new.drop(df.index[0], inplace=True) 
            # Rearrange the columns to "Time" is at the front
            cols = df_new.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            df_new = df_new[cols]

            # Store dataframes in a dictionary
            df_new.name = plate_name
            df_dict[plate_name] = df_new
            
            # Write dataframes to excel
            file_path = DATA_PATH + "Data/Raw_OD/" + plate_name + "_OD600.xlsx"
            df_new.to_excel(file_path, index=False)
            
    return df_dict
                
        
if __name__ == "__main__":
    print("Enter name of screen directory (Ex. 'Screen1')")
    inp = input("- ")
    extr("../Screens/" + inp + "/")