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
        
        # Checks for if the first and last plate are water plates
        inp = ""
        wplate = False
        print("\nAre the first and last plates of " + file_name + " water plates? (y/n)")
        while (inp != "yes" and inp!= "y") and (inp != "no" and inp != "n"):
            inp = input("- ")
            if inp == "yes" or inp == "y":
                wplate = True
                continue
            elif inp == "no" or inp == "n":
                continue
           
        # Dealing with each worksheet
        print("\nEnter the protein, condition, and letter of each plate " + \
              " Note: Plate 1 is at the bottom" + \
              " of the stack and might have been removed if water plate.")
        num_sheets = len(df_dict) + 1
        for i in range(1, num_sheets):
            if wplate and (i == 1 or i == (num_sheets - 1)):
                continue
            else:
                print("\nEnter the protein, condition, and letter of plate " +\
                str(i) + " (Ex. Abd1_15A).")
                inp = input("- ")
                plate_name = "Plate " + str(i) + " - Sheet1"
                df = pd.read_excel(xls, plate_name)
                df = df.iloc[25:75, 1:99]
                
                file_path = DATA_PATH + "Raw_OD/" + inp + "_rawOD.xlsx"
                df.to_excel(file_path)
            
        print("\nExtracting...\n")
            
            
                
            