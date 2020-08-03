#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 13:10:02 2020

@author: jacob
"""

""" Extracts the useful data from the standard output of the Epoch2
    Biotek machine in the 30C room of Striesinger
    Hall, University of Oregon """

import pandas as pd
import os


def extr(DATA_PATH):
    # Create Directory
    try:
        os.mkdir(DATA_PATH + "Raw_OD")
    except OSError:
        print ("Creation of the directory %s failed" % (DATA_PATH + "Raw_OD"))
        
    file_names = []
    for file in os.listdir(DATA_PATH + "Data"):
        # if the element is an xlsx file then
        if file[-5:] == ".xlsx":
            if file not in file_names:
                file_names.append(file)
            
    for file_name in file_names:
        # Full spreadsheet
        xls = pd.ExcelFile(DATA_PATH + "Data/" + file_name)
        df_dict = pd.read_excel(xls, None)
        
        num_sheets = len(df_dict) + 1
        
        # Checks for if the first and last plate are water plates
        ig_plates =[]
        inp = ""
        print("\nAre the first and last plates of " + file_name + " water plates? (y/n)")
        while (inp != "yes" and inp!= "y") and (inp != "no" and inp != "n"):
            inp = input("- ")
            if inp == "yes" or inp == "y":
                ig_plates.append(1)
                ig_plates.append(num_sheets - 1)
                continue
            elif inp == "no" or inp == "n":
                continue
        
        # Checks if any plates can be ignored
        print("\nAre there any sheets/plates that can be ignored? (y/n) Out of " + \
              str(num_sheets) + " sheets.")
        inp = input("- ")
        if inp == "y" or inp == "yes":
            print("Please enter plate numbers that can be ignored one at a time (Ex. 3); stop to end.")
            while inp != "stop":
                inp = input("- ")
                if inp == "stop":
                    continue
                else:
                    try:
                        inp = int(inp)
                        if(inp > 0):
                            ig_plates.append(inp)
                        else:
                            print("Please enter a valid integer; 'stop' to end")
                    except:
                        print("Please enter a valid integer; 'stop' to end")
                        continue
           
        # Dealing with each worksheet
        print("\nEnter the protein, condition, and letter of each plate " + \
              " Note: Plate 1 is at the bottom" + \
              " of the stack and might have been removed if water plate.")
        for i in range(1, num_sheets):
            if i in ig_plates:
                continue
            else:
                print("\nEnter the protein, condition, and letter of plate " +\
                str(i) + " (Ex. Abd1_15A).")
                inp = input("- ")
                plate_name = "Plate " + str(i) + " - Sheet1"
                # Format the dataframe to save correctly to an excel file
                df = pd.read_excel(xls, plate_name)
                df = df.iloc[25:75, 1:99]
                
                file_path = DATA_PATH + "Raw_OD/" + inp + "_rawOD.xlsx"
                df.to_excel(file_path, header=False, index=False)
            
        print("\nExtracting...\n")