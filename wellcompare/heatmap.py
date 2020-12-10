#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:48:26 2020

@author: jacob
"""
import seaborn as sns
import matplotlib.pyplot as plt

def heatmap_gr(heatmap_df, file_n, data_path, log=False):
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
        plt.savefig(data_path + "Heatmaps/GR/" + file_n + "_Log")
    else:
        plt.savefig(data_path + "Heatmaps/GR/" + file_n) 
    plt.close()
    
def heatmap_ymax(heatmap_df, file_n, data_path, log=False):
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
        plt.savefig(data_path + "Heatmaps/Ymax/" + file_n + "_Log")
    else:
        plt.savefig(data_path + "Heatmaps/Ymax/" + file_n) 
    plt.close()