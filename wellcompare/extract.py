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
            if file[-5:] == ".xlsx" and file[0] != "~":
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
                # Pulling info from experimental_info.txt
                print("Using information from experiment_info.txt\n")
                break
    except FileNotFoundError:
        print("FileNotFoundError, try making an experiment_info.txt file and trying again")
        exit(0)
    if info_file == "":
        print("FileNotFoundError, try making an experiment_info.txt file and trying again")
        print("If this file already exists, try renaming it, deleting the last letter, then retyping the last letter")
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
    
    column_row = -1
    stop = len(plate_names)
    for i in range(0, stop):
        plate_name = plate_names[i]
        if plate_name in ignore_plates:
            continue
        else:
            sheet_name = "Plate " + str(i + 1 + offset) + " - Sheet1"
            # Format the dataframe to save correctly to an excel file
            df = pd.read_excel(xls, sheet_name)
            # Search through spreadsheet to find the start of the data
            if column_row < 0:
                for i in range(0, 40):
                    column_names = df.iloc[[i], 1:99].values[0]
                    #column_names = column_names[0]
                    if column_names[0] == "Time":
                        column_row = i
                        break
            # Didn't find data in the correct format
            if column_row < 0:
                print("Excel file is not in the correct format, see examples")
                exit(0)
                
            df_new = pd.DataFrame(df.iloc[column_row:(column_row + num_measurements + 1), 1:99])
            df_new.reset_index(drop=True, inplace=True)
            df_new.columns = column_names
            
            # Drop the temperature column
            df_new.drop(columns=["T° 600"], inplace=True)
            
            # Calculate the measurement times in minutes
            times = df_new.Time.values
            times_formatted = []
            minutes = 0
            for time in times:
                # Retrieve number days between first measurement and current
                try:
                    days = time.day
                except AttributeError:
                    days = 0
                # Retrieve hours
                try:
                    hours = time.hour
                except AttributeError:
                    hours = 0
                # Retrieve minutes
                try:
                    mins = time.minute
                except AttributeError:
                    mins = 0
                # Calculate minutes passed
                minutes = (days * 24 + hours) * 60 + mins
                total_hours = minutes / 60
                times_formatted.append(total_hours)
                
            # Assign newly formatted times to column
            df_new["Time"] = times_formatted
            df_new.drop(df.index[0], inplace=True)
            
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