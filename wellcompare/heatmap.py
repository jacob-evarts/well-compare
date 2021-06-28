#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:48:26 2020

@author: jacob
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
        
def hm(plat, data_path):
    plate_name = plat.get_plate_name()
    params = plat.get_all_params()
    
    # List for making heatmaps
    row_letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    cols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    w, h = 3, 96
    hm_data_gr = [[0 for x in range(w)] for y in range(h)]
    hm_data_ymax = [[0 for x in range(w)] for y in range(h)]
    
    index = 0
    for i in range(8):
        for j in range(12):
            no_growth_flag=False
            well = row_letters[i] + str(cols[j])
            hm_data_gr[index][0] = row_letters[i]
            hm_data_gr[index][1] = cols[j]
            
            hm_data_ymax[index][0] = row_letters[i]
            hm_data_ymax[index][1] = cols[j]
            
            try:
                hm_data_ymax[index][2] = params[well][1]
                if params[well][1] < 0.2:
                    no_growth_flag=True
            except KeyError:
                hm_data_ymax[index][2] = None
            
            if no_growth_flag:
                hm_data_gr[index][2] = 0
            else:
                try:
                    hm_data_gr[index][2] = params[well][0]
                except KeyError:
                    hm_data_gr[index][2] = None      
            index += 1
            
    # Tranposes data
    hm_df_gr = pd.DataFrame(hm_data_gr)
    hm_df_gr.columns = ["Rows", "Columns", "GR"]
    hm_df_gr = hm_df_gr.pivot(index="Rows", columns="Columns", values="GR")
    
    hm_df_ymax = pd.DataFrame(hm_data_ymax)
    hm_df_ymax.columns = ["Rows", "Columns", "Ymax"]
    hm_df_ymax = hm_df_ymax.pivot(index="Rows", columns="Columns", values="Ymax")

    # Formatting heatmap to align with 96 well plate
    sns.set(font_scale=3)
    f, ax = plt.subplots(figsize=(42,28))
    with sns.axes_style("white"):
        sns.heatmap(hm_df_gr, ax=ax, mask=hm_df_gr.isnull(), linewidth=0.5, cmap="magma", annot=True, vmin=0.05)
    ax.set_title(plate_name + ": Raw Growth Rate Values\n\n")
    plt.yticks(rotation=0)
    ax.xaxis.tick_top()  
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    plt.savefig(data_path + "Heatmaps/GR/" + plate_name) 
    plt.close()
    
     # Formatting heatmap to align with 96 well plate
    sns.set(font_scale=3)
    f, ax = plt.subplots(figsize=(42,28))
    with sns.axes_style("white"):
        sns.heatmap(hm_df_ymax, ax=ax, mask=hm_df_ymax.isnull(), linewidth=0.5, cmap="magma", annot=True, vmin=0.2)
    ax.set_title(plate_name + ": Raw Ymax Values\n\n")
    plt.yticks(rotation=0)
    ax.xaxis.tick_top()  
    ax.set_xlabel('')
    ax.set_ylabel('')

    plt.savefig(data_path + "Heatmaps/Ymax/" + plate_name)
    plt.close()
    