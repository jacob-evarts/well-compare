#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:46:52 2020

Updated on June 3, 2021

@author: jacob
"""
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optim
import numpy as np
from scipy import stats

#from heatmap import heatmap_gr, heatmap_ymax
#from graph_repl import graph_repls

# How many time points are graphed
XSCALE = 97

def graph_avg(df_dict, con_data, exp_data, con_name, exp_name, data_path, plate_list, hm_flag=False, log_flag=False):
    """ Plot Formatting """
    # You typically want your plot to be ~1.33x wider than tall.
    # Common sizes: (10, 7.5) and (12, 9)
    plt.figure(figsize=(10, 7.5))
    
    con_color = "#0466c8"
    exp_color = "#d62828"

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
        
    """ Calculations """   
    # Parameter fits for individual control wells
    control_grs = []
    control_ymaxs = []
    # Storing wells to compute average of replicate
    control_wells = []
    con_avg = con_name + "_avg"
    
    # Lists of parameter values for the experimental replicate
    exp_grs = []
    exp_ymaxs = []
    # Storing wells to compute average of replicate
    exp_wells = []
    exp_avg = exp_name + "_avg"
    
    avg_df = pd.DataFrame()
    
    # Calculate parameter values for individual wells
    for plate_name in con_data.keys():
        # Plate
        df = df_dict[plate_name]
        plat = plate_list[plate_name]
        # Wells in that specific plate that belong to given control replicate
        wells = con_data[plate_name]
        for well in wells:
            if well == "":
                break
            control_wells.append(df[well])
            gr, ymax, line = fit_model(df, well)
            plat.add_params(gr, ymax, well)
            if gr < 2:
                control_grs.append(gr)
            if ymax < 2: 
                control_ymaxs.append(ymax)
                
    for plate_name in exp_data.keys():
        # Plate
        df = df_dict[plate_name]
        plat = plate_list[plate_name]
        # Wells in that specific plate that belong to given control replicate
        wells = exp_data[plate_name]
        for well in wells:
            if well == "":
                break
            exp_wells.append(df[well])
            gr, ymax, line = fit_model(df, well)
            plat.add_params(gr, ymax, well)
            if gr < 2:
                exp_grs.append(gr)
            if ymax < 2: 
                exp_ymaxs.append(ymax)
                
    avg_df["Time"] = df["Time"]
    # Calculate averages for replicates
    con_mean, con_std, con_ci = avg_well(control_wells)
    avg_df[con_avg] = con_mean
    avg_df[con_name + "_std"] = con_std
    avg_df[con_name + "_ci"] = con_ci
    
    exp_mean, exp_std, exp_ci = avg_well(exp_wells)
    avg_df[exp_avg] = exp_mean
    avg_df[exp_name + "_std"] = exp_std
    avg_df[exp_name + "_ci"] = exp_ci
    
    # Parameter fits for average control model
    con_gr, con_ymax, con_line = fit_model(avg_df, con_avg)
    # Parameter fits for average exp model
    exp_gr, exp_ymax, exp_line = fit_model(avg_df, exp_avg)
    
    # T-test for growth rate and ymax parameter values
    gr_stats = t_test(exp_grs, control_grs)
    ymax_stats = t_test(exp_ymaxs, control_ymaxs)
    # P-values
    gr_pval = gr_stats[1]
    ymax_pval = ymax_stats[1]
    
    if con_ymax > 0.01 and exp_ymax > 0.01:
        # Normalize experimental parameters with control parameters
        gr_ratio = (exp_gr / con_gr) 
        ymax_ratio = (exp_ymax / con_ymax)
    else:
        gr_ratio = 0
        ymax_ratio = 0
            
        # Symbols on graph to indicate better growth by experimental strain
    better_gr = ""
    if gr_ratio > 1:
        better_gr += "^ "
    better_ymax = ""
    if ymax_ratio > 1:
        better_ymax += "^ "
    
    """ Graphing """
    # Graph average experimental line
    plt.plot(avg_df["Time"], avg_df[exp_avg], color=exp_color, label=(exp_name), linewidth=3.0)
    # plt.plot(*exp_line, 'r', linestyle = "--", color=exp_color, linewidth=1)
    # Confidence intervals
    exp_ci_hi =  avg_df[exp_avg] + avg_df[exp_name + "_ci"]
    exp_ci_low = avg_df[exp_avg] - avg_df[exp_name + "_ci"]
    plt.plot(avg_df["Time"], exp_ci_hi, color=exp_color, linestyle=":", linewidth=1.5)
    plt.plot(avg_df["Time"], exp_ci_low, color=exp_color, linestyle=":", linewidth=1.5)
        
    # Graph average control line  
    plt.plot(avg_df["Time"], avg_df[con_avg], color=con_color, label=(con_name), linewidth=3.0)
    # plt.plot(*con_line, 'r', linestyle = "--", color=con_color, linewidth=1)
    # Confidence intervals
    con_ci_hi =  avg_df[con_avg] + avg_df[con_name + "_ci"]
    con_ci_low = avg_df[con_avg] - avg_df[con_name + "_ci"]
    plt.plot(avg_df["Time"], con_ci_hi, color=con_color, linestyle=":", linewidth=1.5)
    plt.plot(avg_df["Time"], con_ci_low, color=con_color, linestyle=":", linewidth=1.5)
    
    # Plot histograms
    # graph_repls(con_grs, con_ymaxs, exp_grs, exp_ymax,con_name, exp_name, data_path)
    
    # Place a legend to the right
    lgd = ax.legend(
                    loc = 'upper right', 
                    borderaxespad = 0., 
                    facecolor = 'white', 
                    fontsize = 16)
    
    # Format P-values
    if gr_pval < 0.001:
        gr_pval = "<0.001"
    else:
        gr_pval = round(gr_pval, 3)
    if ymax_pval < 0.001:
        ymax_pval = "<0.001"
    else:
        ymax_pval = round(ymax_pval, 3)
        
    plt.title(f"{exp_name} vs. {con_name}- GR ratio:{round(gr_ratio, 3)} ({gr_pval}) Ymax ratio: {round(ymax_ratio, 3)} ({ymax_pval})", fontsize=20)
    path =  data_path + "Graphs/Averages/" + exp_name + "_vs_" + con_name
    plt.savefig(path, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close()
    
# Graph each well of a replicate
def graph_indiv(df_dict, repl_data, repl_name, data_path, plate_list, log_flag=False):
    """ Graph Formatting """
    # You typically want your plot to be ~1.33x wider than tall.
    # Common sizes: (10, 7.5) and (12, 9)
    plt.figure(figsize=(10, 7.5))

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

    # Graph each replicate well
    n = 0
    for plate_name in repl_data.keys():
        # Plate
        df = df_dict[plate_name]
        plat = plate_list[plate_name]
        # Wells in that specific plate that belong to given control replicate
        wells = repl_data[plate_name]
        # Counter for number of viable wells
        n = 0
        
        for well in wells:
            if well == "":
                break
            try:
                gr, ymax = plat.get_params(well)
            except KeyError:
                gr, ymax, line = fit_model(df, well)
                plat.add_params(gr, ymax, well)
            
            if ymax > 0.2:
                n += 1
            plt.plot(df["Time"], df[well], label=well, linewidth=2.5)
                
    # Place a legend to the right
    lgd = ax.legend(
                    loc = 'upper right', 
                    borderaxespad = 0., 
                    facecolor = 'white', 
                    ncol = 2,
                    fontsize = 16)
        
    plt.title(f"{repl_name} Isolates: ({n} isolates with growth)", fontsize=24)
    path =  data_path + "Graphs/" + repl_name 
    plt.savefig(path, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close()
    
""" Auxillary Functions """
# P-test on individual wells
def t_test(data1, data2) -> int:
    ind_ttest = stats.ttest_ind(data1, data2)
    return ind_ttest

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
        bounds = (0, [10000000., 100., 10000000.]) # Set bounds
        # Prepare model 
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
    exp["Time"] = pd.to_numeric(exp["Time"])
    exp[well] = pd.to_numeric(exp[well])
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

# Returns several statistics for group of dataframe columns (mean, SD, 95% CI)
def avg_well(well_list):   
    col = pd.DataFrame()
    n = 0
    for i in range(len(well_list)):
        well = well_list[i]
        # Check if well was viable
        if max(well) > 0.2:
            col[str(i)] = well
            n += 1 
    mean = col.mean(axis=1).reset_index(drop=True)
    std = col.std(axis=1).reset_index(drop=True)
    std_err = col.sem(axis=1).reset_index(drop=True)
    ci95 = std_err * stats.t.ppf((1 + 0.95) / 2, n - 1)
    return mean, std, ci95  