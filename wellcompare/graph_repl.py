#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 09:31:00 2020

@author: jacob
"""
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optim
import numpy as np
from scipy import stats
import seaborn as sns

# Graph the average of all the wells in a given replicate
def graph_repls(df, repl_wells, repl_n, data_path, xscale):
    file_n = df.name
    # Parameter fits
    control_grs = []
    control_ymax = []
    exp_grs = []
    exp_ymax = []
    
    for well in repl_wells:
        # Get parameters from control well
        cwell = well + "_No_PO"
        gr1, ymax1, line1 = fit_model(df, cwell)
        # Remove erroneous values
        if gr1 < 1.5:
            control_grs.append(gr1)
        if ymax1 < 2:
            control_ymax.append(ymax1)
        # Get parameters from experimental well
        ewell = well + "_PO"
        gr2, ymax2, line2 = fit_model(df, ewell)
        if gr2 < 1.5:
            exp_grs.append(gr2)
        if ymax2 < 2:
            exp_ymax.append(ymax2)
        
    # Test the significance of the fitted parameters
    gr_stats = t_test(exp_grs, control_grs)
    ymax_stats = t_test(exp_ymax, control_ymax)
    # Get P-values from statistics
    gr_pval = gr_stats[1]
    ymax_pval = ymax_stats[1]
            
    # Calculate average of wells to graph
    exp_avg, exp_std, exp_ci95 = avg_well(df, repl_wells, control=False)
    control_avg, control_std, control_ci95 = avg_well(df, repl_wells, control=True)
    
    df["Exp_avg_" + str(repl_n)] = exp_avg
    df["Control_avg_" + str(repl_n)] = control_avg
    
    gr1, ymax1, line1 = fit_model(df, "Control_avg_" + str(repl_n))
    gr2, ymax2, line2 = fit_model(df, "Exp_avg_" + str(repl_n))
    
    # Convert the list of param values to dataframe for graphing
    gr_df = pd.DataFrame(control_grs, columns=["GR"])
    gr_df["Strain"] = "Control"
    gr_df_inter = pd.DataFrame(exp_grs, columns=["GR"])
    gr_df_inter["Strain"] = "Experimental"
    
    ymax_df = pd.DataFrame(control_ymax, columns=["Ymax"])
    ymax_df["Strain"] = "Control"
    ymax_df_inter = pd.DataFrame(exp_ymax, columns=["Ymax"])
    ymax_df_inter["Strain"] = "Experimental"
    
    gr_df = pd.concat([gr_df, gr_df_inter], ignore_index=True)
    ymax_df = pd.concat([ymax_df, ymax_df_inter], ignore_index=True)
    
    if ymax1 > 0.2 and ymax2 > 0.2:
        gr_ratio = (gr2 / gr1) 
        ymax_ratio = (ymax2 / ymax1)
    else:
        gr_ratio = 0
        ymax_ratio = 0
            
    # Includes significance in graph
    gr_sig = ""
    if gr_pval <= 0.001:
        gr_sig = " GR:*** "
    elif gr_pval <= 0.01:
        gr_sig = " GR:**  "
    elif gr_pval <= 0.05:
        gr_sig = " GR:*   "
    else:
        gr_sig = " GR: NS "
            
    ymax_sig = ""
    if ymax_pval <= 0.001:
        ymax_sig = " Ymax:*** "
    elif ymax_pval <= 0.01:
        ymax_sig = " Ymax:**  "
    elif ymax_pval <= 0.05:
        ymax_sig = " Ymax:*   "
    else:
        ymax_sig = " Ymax: NS "

    """ Plotting """
    control_color = '#2980b9'
    exp_color = '#e74c3c'
    
    # You typically want your plot to be ~1.33x wider than tall.
    fig = plt.figure(figsize=(8,8))
    fig.tight_layout(pad=4.0)
    ax = []
    # Image 1: Growth curves
    # Remove the plot frame lines. They are unnecessary
    ax0 = fig.add_subplot(211)
    ax.append(ax0)
    ax[0].spines["top"].set_visible(False)
    ax[0].spines["bottom"].set_visible(False)
    ax[0].spines["right"].set_visible(False)
    ax[0].spines["left"].set_visible(False)
    
    # Set background to white
    ax[0].set_facecolor('white')

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    ax[0].get_xaxis().tick_bottom()
    ax[0].get_yaxis().tick_left()

    # Limit the range of the plot to only where the data is.
    ax[0].set_ylim(0, 2)
    ax[0].set_xlim(0, xscale)

    # Make sure your axis ticks are large enough to be easily read.
    ax[0].set_yticks(np.arange(0, 1.7, 0.2))
    ax[0].set_yticklabels([str(round(x, 1)) for x in np.arange(0, 1.7, 0.2)], fontsize=14)
    ax[0].set_xticks(np.arange(0, xscale, 12))
    ax[0].set_xticklabels([str(round(x,1)) for x in np.arange(0, xscale, 12)], fontsize=12)
    
    # Provide tick lines across the plot to help your viewers trace along the axis ticks.
    for y in np.arange(0, 1.7, 0.2):
        ax[0].plot(range(0, xscale), [y] * len(range(0, xscale)), "--", lw=0.5, color="black")
    
    ax[0].set_xlabel("Time (h)", fontsize=12)
    ax[0].set_ylabel("OD 600", fontsize=14)
    
    # Graph Averags
    ax[0].plot(df["Time"], control_avg, color=control_color,  label=("Control"), linewidth=2.0)
    ax[0].plot(*line1, 'b', linestyle = "--", linewidth=1)
    ax[0].plot(df["Time"], exp_avg, color=exp_color, label=("Experimental"), linewidth=2.0)
    ax[0].plot(*line2, 'r', linestyle = "--", linewidth=1)
    
    # Calculate 95% confidence intervals
    ciA_hi =  control_avg + control_ci95
    ciA_low = control_avg - control_ci95
    ciB_hi = exp_avg + exp_ci95
    ciB_low = exp_avg - exp_ci95
    # Graph 95% confidence intervals
    ax[0].plot(df["Time"], ciA_hi, color=control_color, linestyle=":", linewidth=1)
    ax[0].plot(df["Time"], ciA_low, color=control_color, linestyle=":", linewidth=1)
    ax[0].plot(df["Time"], ciB_hi, color=exp_color, linestyle=":", linewidth=1)
    ax[0].plot(df["Time"], ciB_low, color=exp_color, linestyle=":", linewidth=1)   
    
    # Place a legend to the right
    lgd = ax[0].legend(
                    borderaxespad = 0., 
                    facecolor = 'white', 
                    fontsize = 16)
    
    # Include a title  
    titl = f"Replicate {str(repl_n)}: {gr_sig} GR_ratio: {round(gr_ratio, 3)} {ymax_sig} Ymax_ratio: {round(ymax_ratio, 3)}"
    ax[0].set_title(titl, fontsize=24)
    
    # Image 2: histogram of growth rates
    ax1 = fig.add_subplot(223)
    ax.append(ax1)
    ax[1].set_xlabel("Growth rate value bins", fontsize=14)
    ax[1].set_ylabel("Frequency", fontsize=14)    
    ax[1].set_facecolor('white')

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    ax[1].get_xaxis().tick_bottom()
    ax[1].get_yaxis().tick_left()
    
    # Add vertical mean line to histogram
    control_mean = mean(control_grs)
    exp_mean = mean(exp_grs)
    ax[1].axvline(control_mean, color=control_color)
    ax[1].axvline(exp_mean, color=exp_color)
    
    # Plot histogram and estimated PDF
    sns.histplot(data=gr_df, x="GR", hue="Strain", 
                 ax=ax[1], legend=False, color=control_color, 
                 bins = 15, kde=False, multiple="layer",
                 palette=['#3867d6', '#eb3b5a'])  
    
    # Image 3: historgram of ymaxs
    ax2 = fig.add_subplot(224, sharey=ax[1])
    ax.append(ax2)
    ax[2].set_xlabel("Ymax value bins", fontsize=14)
    ax[2].set_ylabel(" ")
    ax[2].set_facecolor('white')

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    ax[2].get_xaxis().tick_bottom()
    ax[2].get_yaxis().tick_left()
    
    # Add vertical mean line to histogram
    control_mean = mean(control_ymax)
    exp_mean = mean(exp_ymax)
    ax[2].axvline(control_mean, color=control_color)
    ax[2].axvline(exp_mean, color=exp_color)
    
    # Plot histogram and estimated PDF
    sns.histplot(data=ymax_df, x = "Ymax", 
                 hue="Strain", ax=ax[2], legend=False,
                 color=control_color, bins = 15, 
                 kde=False, multiple = "layer",
                 palette=['#3867d6', '#eb3b5a'])  
    
    # Save the images  
    path = data_path + "Graphs/Replicates/" + file_n + "/avg_repl_" + str(repl_n)
    plt.savefig(path, bbox_extra_artists=(lgd,),bbox_inches='tight')
    plt.close()
    
""" Auxillary Functions """       
# P-test on individual wells
def t_test(data1, data2) -> int:
    ind_ttest = stats.ttest_ind(data1, data2)
    return ind_ttest

def mean(lst):
    return round((sum(lst) / len(lst)), 3)
    
def avg_well(df, col_list, control=False): 
    col_lst = []
    post = ""
    # Control wells
    if control:
        post = "_No_PO"
    # Exp wells
    else:
        post = "_PO"
        
    for well in col_list:
        col_lst.append(well + post)
        
    col = df.loc[:, col_lst]
    mean = col.mean(axis=1)
    std = col.std(axis=1)
    n = len(col_lst)
    std_err = col.sem(axis=1)
    ci95 = std_err * stats.t.ppf((1 + 0.95) / 2, n - 1)
    return mean, std, ci95

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