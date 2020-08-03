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
    through this program 
        - direct well to well comparison between two plates
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import scipy.optimize as optim
import seaborn as sns
import os

# Helper files
from wellcompare import extract
from wellcompare import combine

# How many hours are graphed (max for 4 day run: 97)
XSCALE = 73

# For graphing different datasets
# Options: "Screen1/"         *ORIGINAL SCREEN*
#          "Screen2/"         *FOLLOW UP*
#          "Screen3/"         *CHECKING SOME OTHER STRAINS*
#          "Full_Drop1/"       *TESTING FULL DROUPOUT MEDIA*
#          "Full_Drop2/"
# or create your own directory inside Screens folder

# Enter folder name here if running app.py as main
DATA_PATH_HC = "Test/"
DATA_PATH_HC = "../Screens/" + DATA_PATH_HC
    
        
row_letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
cols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
      
# List for making heatmaps
w, h = 3, 96
hm_data_gr = [[0 for x in range(w)] for y in range(h)]  
hm_data_ymax = [[0 for x in range(w)] for y in range(h)]  

index = 0
for i in range(8):
    for j in range(12):
        hm_data_gr[index][0] = row_letters[i]
        hm_data_gr[index][1] = cols[j]
        
        hm_data_ymax[index][0] = row_letters[i]
        hm_data_ymax[index][1] = cols[j]
        index += 1
        
def grph(dp, hm_flag):
    global DATA_PATH
    DATA_PATH = dp
    
    # Extracts the data from the format output by the Epoch2 plate reader
    extract.extr(DATA_PATH)
    # Combines two raw files and does some light cleaning
    combine.comb(DATA_PATH)
    
    # Create Directories
    try:
        os.mkdir(DATA_PATH + "Graphs")
    except OSError:
        print ("Creation of the directory %s failed" % (DATA_PATH + "Graphs"))
    try:
        os.mkdir(DATA_PATH + "Graphs/Summaries")
    except OSError:
        print ("Creation of the directory %s failed" % (DATA_PATH + "Graphs/WSummaries"))
    try:
        os.mkdir(DATA_PATH + "Heatmaps")
    except OSError:
        print ("Creation of the directory %s failed" % (DATA_PATH + "Heatmaps"))
    try:
        os.mkdir(DATA_PATH + "Heatmaps/GR")
    except OSError:
        print ("Creation of the directory %s failed" % (DATA_PATH + "Heatmaps/GR"))
    try:
        os.mkdir(DATA_PATH + "Heatmaps/Ymax")
    except OSError:
        print ("Creation of the directory %s failed" % (DATA_PATH + "Heatmaps/Ymax"))
            
    # Read in input strains
    inp = ""
    file_names = []
    print("\nEnter list of proteins and conditions to GRAPH (Ex. Pus6_17), or type all; stop to end:")
    while inp != "stop" and inp != "all":
        inp = input("- ")
        if inp == "stop":
            continue
        elif inp == "all":
            try:
                for file in os.listdir(DATA_PATH + "Model_OD/By_Well"):
                    # if the element is an xlsx file then
                    if file[-5:] == ".xlsx":
                        file = file[0:-19]
                        if file not in file_names:
                            file_names.append(file)
            except FileNotFoundError:
                print("Could not find file or directory " + DATA_PATH + "Raw_OD - Exiting...")
                exit(1)
        else:
            file_names.append(inp)
    print("\nStarting...")
    
    for file_name in file_names:
        # Create directories
        try:
            os.mkdir(DATA_PATH + "Graphs/" + file_name)
        except OSError:
            print ("Creation of the directory %s failed" % (DATA_PATH + "Graphs/" + file_name))
        try:
            os.mkdir(DATA_PATH + "Graphs/" + file_name + "/Raw_Graphs")
        except OSError:
            print ("Creation of the directory %s failed" % (DATA_PATH + "Graphs/" + file_name + "/Raw_Graphs"))
        try:
            os.mkdir(DATA_PATH + "Graphs/" + file_name + "/Log2_Graphs")
        except OSError:
            print ("Creation of the directory %s failed" % (DATA_PATH + "Graphs/" + file_name + "/Log2_Graphs"))
        
        df = pd.read_excel(DATA_PATH + "Model_OD/By_Well/" + file_name + "_well_combined.xlsx")
        
        # Dropping rows if run stopped early
        if DATA_PATH == "Screen3/":
            df.drop(df.index[[47, 48]], inplace=True)
        
        # Keeping track of significant wells
        global sig_wells 
        sig_wells = []
        
        # Keeping track of significance by replicate
        global sig_reps 
        sig_reps = {"R1":0, "R2":0, "R3":0, "R4":0}
        
        # Graph the growth curves of all wells and their logarithms
        for i in range(4):
            for j in range(8):
                for k in range(3):
                    col_name = str(row_letters[j]) + str((k+i*3) + 1)
                    w1 = col_name + "_No_PO"
                    w2 = col_name + "_PO"
                    col_n = (k+i*3 + 1)
                    row_n = j
                    graph_wells(df, w1, w2, col_n, row_n, file_name)
            
        if hm_flag:
            # Create heatmaps
            hm_df_gr = pd.DataFrame(hm_data_gr)
            hm_df_gr.columns = ["Rows", "Columns", "GR"]
        
            hm_df_ymax = pd.DataFrame(hm_data_ymax)
            hm_df_ymax.columns = ["Rows", "Columns", "Ymax"]
            # Create heatmap for growth rate ratios
            heatmap_gr(hm_df_gr, file_name)
            # Create heatmap for ymax ratios
            heatmap_ymax(hm_df_ymax, file_name)
        
        # Text file to summarize well data
        file_text = DATA_PATH + "Graphs/Summaries/" + file_name + ".txt"
        f = open(file_text, "w+")
        
        # Write summary of plate to txt file
        f.write("List of significant wells for " + file_name + ":\n")
        
        num_sig = len(sig_wells)
        if num_sig == 0:
            f.write("No significant wells\n")
        else:
            for i in sig_reps:
                f.write(i + "- " + str(sig_reps[i]))
                f.write("\t")
            f.write("Total- " + str(sum(sig_reps.values())))
            f.write("\n\nWells:\n")
            for i in range(len(sig_wells)):
                f.write(sig_wells[i])
                f.write("\n")
    
        f.close()
        
        print("Finished " + file_name + "\n")
        
# Graphs wells with estimated growth rates and logs results
def graph_wells(df, well1, well2, col, row, file_n):
    # Calculate exponential portion of data for line fit
    exp1 = exponential_section(df, well1)
    exp2 = exponential_section(df, well2)

    # Fitting lines to exponential portions to graph
    slope1 = 0
    slope2 = 0
    if not exp1.empty:
        slope1, line1 = fit_line(exp1, well1)
    else:
        line1 = [(0,0), (0,0)]

    if not exp2.empty:
        slope2, line2 = fit_line(exp2, well2)
    else:
        line2 = [(0,0), (0,0)]

    # Fit a logistical model to calculate growth rate
    p0 = np.random.exponential(size=3) # Initialize random values
    bounds = (0, [10000000., 100., 10000000.]) #Set bounds
   
    # Prepare model 1
    xt1 = np.array(df["Time"])
    yt1 = np.array(df[well1])
    # Prepare model 2
    xt2 = np.array(df["Time"])
    yt2 = np.array(df[well2])
    
    # If no logistic curve can be fit, default to less sophisticated method of fitting line to exponentional section of the graph
    try:
        # Fit model 1
        (a1, gr1, cc1), cov1 = optim.curve_fit(logistic, xt1, yt1, bounds=bounds, p0=p0)
        # Fit model 2
        (a2, gr2, cc2), cov2 = optim.curve_fit(logistic, xt2, yt2, bounds=bounds, p0=p0)
    except RuntimeError:
        gr1 = slope1
        gr2 = slope2
        cc1 = df[well1].max()
        cc2 = df[well2].max()
    
    # Previous O/E over no previous O/E 
    # Cutoff for virtually no growth
    ymax1 = max(df[well1])
    ymax2 = max(df[well2])
    if ymax1 > 0.2 and ymax2 > 0.2:
        gr_ratio = (gr2 / gr1)
        ymax_ratio = (cc2 / cc1)
    else:
        gr_ratio = 0
        ymax_ratio = 0
        
    # Gets well address
    well = ""
    if col < 10:
        well = well1[0:2]
    else:
        well = well1[0:3]
    
    # Format data for heatmaps
    hm_data_gr[(col + row * 12) - 1][2] = gr_ratio
    hm_data_ymax[(col + row * 12) - 1][2] = ymax_ratio
    
    # Calculates what replicate the well belongs to
    replicate = 0
    if col <= 3:
        replicate = "R1"
    elif col <= 6:
        replicate = "R2"
    elif col <= 9:
        replicate = "R3"
    else:
        replicate = "R4"
    
    # Includes significance in graph
    pval = sig_test(df, well1, well2)
    sig = ""
    if pval:
        sig = "    Significant Dif."
        # Significantly better growth relating to 'live fast die young'
        if gr_ratio > 1 or (gr_ratio > 0.9 and ymax_ratio > 1):
            sig_wells.append(well2)
            sig_reps[replicate] += 1
    else:
        sig = "    Not significant"
        
    """ Plotting """
    # You typically want your plot to be ~1.33x wider than tall.
    # Common sizes: (10, 7.5) and (12, 9)
    plt.figure(figsize=(8, 6))

    # Remove the plot frame lines. They are unnecessary
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    
    # Set background to white
    ax.set_facecolor('white')

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # Limit the range of the plot to only where the data is.
    plt.ylim(0, 2)
    plt.xlim(0, XSCALE)

    # Make sure your axis ticks are large enough to be easily read.
    plt.yticks(np.arange(0, 1.7, 0.2), [str(round(x, 1)) for x in np.arange(0, 1.7, 0.2)], fontsize=14)
    plt.xticks(np.arange(0, XSCALE, 24), [str(round(x,1)) for x in np.arange(0, XSCALE, 24)], fontsize=14)

    # Provide tick lines across the plot to help your viewers trace along the axis ticks.
    for y in np.arange(0, 1.7, 0.2):
        plt.plot(range(0, XSCALE), [y] * len(range(0, XSCALE)), "--", lw=0.5, color="black", alpha=0.3)
        
    plt.plot(df["Time"], df[well1], label="No PO/E", linewidth=1.0)
    plt.plot(df["Time"], df[well2], label="PO/E", linewidth=1.0)
    plt.plot(*line1, 'b', linestyle = "--", linewidth=0.5)
    plt.plot(*line2, 'r', linestyle = "--", linewidth=0.5)
    
    # Place a legend to the right
    lgd = ax.legend(bbox_to_anchor = (1.35, 0.9), 
                    loc = 'upper right', 
                    borderaxespad = 0., 
                    facecolor = 'white', 
                    fontsize = 20
                    )
        
    plt.title("Well- " + well + "    " + replicate + "    GR_ratio: %.3f" % (gr_ratio) + sig, fontsize=24)
    path = DATA_PATH + "Graphs/" + file_n + "/Raw_Graphs/" + well + "_" + replicate
    plt.savefig(path, bbox_extra_artists=(lgd,),bbox_inches='tight')
    plt.close()
    
def heatmap_gr(heatmap_df, file_n, log=False):
    # Tranposes data
    heatmap_df = heatmap_df.pivot(index="Rows", columns="Columns", values="GR")
    
    # Formatting heatmap to align with 96 well plate
    sns.set(font_scale=3)
    f, ax = plt.subplots(figsize=(42,28))
    sns.heatmap(heatmap_df, ax=ax, linewidth=0.5, cmap="magma", annot=True, vmin=0.5, vmax=1.5)
    ax.set_title(file_n + ": Growth Rate Stress Ratio\n\n")
    plt.yticks(rotation=0)
    ax.xaxis.tick_top()  
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    if log:
        plt.savefig(DATA_PATH + "Heatmaps/GR/" + file_n + "_Log")
    else:
        plt.savefig(DATA_PATH + "Heatmaps/GR/" + file_n) 
    plt.close()
    
def heatmap_ymax(heatmap_df, file_n, log=False):
    # Tranposes data
    heatmap_df = heatmap_df.pivot(index="Rows", columns="Columns", values="Ymax")
    
    # Formatting heatmap to align with 96 well plate
    sns.set(font_scale=3)
    f, ax = plt.subplots(figsize=(42,28))
    sns.heatmap(heatmap_df, ax=ax, linewidth=0.5, cmap="magma", annot=True, vmin=0.5, vmax=1.5)
    ax.set_title(file_n + ": Ymax Stress Ratio\n\n")
    plt.yticks(rotation=0)
    ax.xaxis.tick_top()  
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    if log:
        plt.savefig(DATA_PATH + "Heatmaps/Ymax/" + file_n + "_Log")
    else:
        plt.savefig(DATA_PATH + "Heatmaps/Ymax/" + file_n) 
    plt.close()

""" Auxillary Functions """
# P-test on individual wells
def sig_test(df, well1, well2) -> int:
    p_val = 0.05
    ind_ttest = stats.ttest_ind(df[well1], df[well2])
    if ind_ttest[1] <= p_val:
        return ind_ttest
    return 0

# Estimates expinential growth section of growth curve to compute growth rate
def exponential_section(df, well):
    ymax = max(df[well])
    ymin = min(df[well])
    ymid = (ymax + ymin) / 2.0
    span = ymax - ymin
    low = ymid - (span * 0.40)
    high = ymid + (span * 0.40)
    exp = df.loc[(df[well] >= low) & (df[well] <= high)]
    return exp[["Time", well]]

# Fits a line to a given section of a graph. Returns the slope and endpoints of the line
def fit_line(exp, well):
    slope, intercept, r_value, p_value, std_err = stats.linregress(exp["Time"], exp[well])
    x1 = int(exp.iloc[:1,:1].values)
    x2 = int(exp.iloc[-1:,:1].values)
    y1 = x1 * slope + intercept
    y2 = x2 * slope + intercept
    p1 = (x1, x2)
    p2 = (y1, y2)
    line = [p1, p2]
    return slope, line

# Logistical funtion used to model growth rate
def logistic(t, a, b, c):
    return c / (1 + a * np.exp(-b*t))

if __name__ == "__main__":
    grph(DATA_PATH_HC, True)