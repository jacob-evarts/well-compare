#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:46:52 2020

@author: jacob
"""
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optim
import numpy as np
from scipy import stats

from heatmap import heatmap_gr, heatmap_ymax
from graph_repl import graph_repls

# How many hours are graphed
XSCALE = 97

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
                
def graph(df, data_path, hm_flag, log_flag):
    # Keeping track of significant better wells
    global sig_wells 
    sig_wells = []
        
    # Keeping track of total number of significant wells
    global total_sig
    total_sig = 0
    
    # Keeping track of the number of wells that grew in BOTH plates
    global num_viable
    num_viable = 0
        
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
                graph_wells(df, w1, w2, col_n, row_n, data_path, log_flag)
                
    # Calculates all the wells in each replicates
    for i in range(4):
        repl = [x + str(y+1) for x in row_letters for y in range((i*3), (i+1) * 3)]
        graph_repls(df, repl, (i+1), data_path, XSCALE)
        
    file_n = df.name
    # If user indicates they want heatmaps (hm_flag = True)
    if hm_flag:
        # Create heatmaps
        hm_df_gr = pd.DataFrame(hm_data_gr)
        hm_df_gr.columns = ["Rows", "Columns", "GR"]
    
        hm_df_ymax = pd.DataFrame(hm_data_ymax)
        hm_df_ymax.columns = ["Rows", "Columns", "Ymax"]
        # Create heatmap for growth rate ratios
        heatmap_gr(hm_df_gr, file_n, data_path)
        # Create heatmap for ymax ratios
        heatmap_ymax(hm_df_ymax, file_n, data_path)
        
    # Text file to summarize well data
    file_text = data_path + "Summaries/" + file_n + ".txt"
    f = open(file_text, "w+")
    
    # Write summary of plate to txt file
    f.write("List of significant better wells per replicate for " + file_n + ":\n")
    num_sig = len(sig_wells)
    if total_sig == 0:
        f.write("No significant wells\n")
    else:
        for i in sig_reps:
            f.write(i + "- " + str(sig_reps[i]))
            f.write("\t")
        f.write("\nNumber of significantly better wells- " + str(num_sig) + 
                " out of  " + str(num_viable) + " wells that grew\n")
        f.write("Total number of significant wells- " + str(total_sig))
        f.write("\n\nWells:\n")
        for i in range(num_sig):
            f.write(sig_wells[i])
            f.write("\n")
    f.close()
        
    print("Finished " + file_n + "\n")

# Graphs wells with estimated growth rates and logs results
def graph_wells(df, well1, well2, col, row, data_path, log=False):  
    file_n = df.name
    global num_viable
    global sig_wells
    global total_sig
    global sig_reps 
    
    gr1, ymax1, line1 = fit_model(df, well1)
    gr2, ymax2, line2 = fit_model(df, well2)
    
    # Previous O/E over no previous O/E 
    # Cutoff for virtually no growth
    if ymax1 > 0.2 and ymax2 > 0.2:
        gr_ratio = (gr2 / gr1)
        ymax_ratio = (ymax2 / ymax1)
        num_viable += 1
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
    
    # Test the significance of the fitted parameters
    gr_stats = t_test(df[well1], df[well2])
    #ymax_stats = t_test(exp_ymax, control_ymax)
        
    gr_pval = gr_stats[1]
    #ymax_pval = ymax_stats[1]
        
    # Includes significance in graph
    gr_sig = ""
    if gr_pval > 0.05:
        gr_sig = " GR: NS "
    else:
        if gr_pval <= 0.001:
            gr_sig = " GR:*** "
        elif gr_pval <= 0.01:
            gr_sig = " GR:**  "
        else:
            gr_sig = " GR:*   "
        # If growth is significantly better
        if gr_ratio > 1 or ymax_ratio > 1:
            sig_wells.append(well2)
            sig_reps[replicate] += 1
        # If growth is significant
        if gr_ratio > 0:
            total_sig += 1
        
    """ Plotting """
    control_color = '#3867d6'
    exp_color = '#eb3b5a'
    
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
        
    plt.plot(df["Time"], df[well1], color=control_color, label="No PO/E", linewidth=1.0)
    plt.plot(df["Time"], df[well2], color=exp_color, label="PO/E", linewidth=1.0)
    plt.plot(*line1, 'b', linestyle = "--", linewidth=0.5)
    plt.plot(*line2, 'r', linestyle = "--", linewidth=0.5)
    
    # Place a legend to the right
    lgd = ax.legend(bbox_to_anchor = (1.35, 0.9), 
                    loc = 'upper right', 
                    borderaxespad = 0., 
                    facecolor = 'white', 
                    fontsize = 20
                    )
        
    plt.title("Well- " + well + "    " + replicate + "    GR_ratio: %.3f" % (gr_ratio) + gr_sig, fontsize=24)
    path = data_path + "Graphs/" + file_n + "/Raw_Graphs/" + well + "_" + replicate
    plt.savefig(path, bbox_extra_artists=(lgd,),bbox_inches='tight')
    plt.close()
    
""" Auxillary Functions """       
# P-test on individual wells
def t_test(data1, data2) -> int:
    ind_ttest = stats.ttest_ind(data1, data2)
    return ind_ttest

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

def fit_model(df, well):
    # Calculate exponential portion of data for line fit
        exp = exponential_section(df, well)
        # Fitting lines to exponential portions to graph
        slope = 0
        if not exp.empty:
            slope, line = fit_line(exp, well)
        else:
            line = [(0,0), (0,0)]
                
        # Fit a logistical model to calculate growth rate
        p0 = np.random.exponential(size=3) # Initialize random values
        bounds = (0, [10000000., 100., 10000000.]) #Set bounds
        # Prepare model 1
        xt = np.array(df["Time"])
        yt = np.array(df[well])
            
        # If no logistic curve can be fit, default to less sophisticated method of fitting line to exponentional section of the graph
        try:
            # Fit model 1
            (a, gr, ymax), cov = optim.curve_fit(logistic, xt, yt, bounds=bounds, p0=p0)
        except (RuntimeError, ValueError):
            gr = slope 
            ymax = max(df[well])
        return gr, ymax, line

# Logistical funtion used to model growth rate
def logistic(t, a, b, c):
    return c / (1 + a * np.exp(-b*t))