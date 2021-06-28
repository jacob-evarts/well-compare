#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:55:52 2021

@author: jacob
"""
"""
Object to hold data about each 96 well plate in an experiment,
including a mapping of where and how replicates are grouped """
class Plate(object):
    def __init__(self, name):
        self.name = name
        self.replicate_map = {}
        self.parameter_map = {}
        
    def __repl__(self):
        rep = f"{self.name}:\n"
        for repl_name in self.replicate_map.keys():
            rep += f"{repl_name}: {self.replicate_map[repl_name]}"
        return rep
        
    def __str__(self):
        rep = f"{self.name}:\n"
        for repl_name in self.replicate_map.keys():
            rep += f"{repl_name}: {self.replicate_map[repl_name]}\n"
        return rep
        
    def add_repl(self, repl_name, wells):
        self.replicate_map[repl_name] = wells
        
    # Keeps track of growth rates and ymaxs in each well of the plate
    # Note: not safe, wrap in try/catch statement (KeyError)
    def add_params(self, gr, ymax, well):
        self.parameter_map[well] = [gr, ymax]
     
    # Note: not safe, wrap in try/catch statement (KeyError)
    def get_params(self, well):
        return self.parameter_map[well][0], self.parameter_map[well][1]

    
    def get_all_params(self):
        return self.parameter_map
        
    def get_wells(self, repl_name):
        return self.replicate_map[repl_name]
    
    def get_repl_names(self):
        return list(self.replicate_map.keys())
    
    def get_plate_name(self):
        return self.name
    
    