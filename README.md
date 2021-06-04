# [GarciaLab](https://www.garcialab.org)

## Info-
Code developed for research on modeling prion growth dynamics in budding yeast.
This package is used to compare 96 well plates that contain groupings of 
experimental and control replicates. This code generates graphs, heatmaps, 
and sumarries of your data, while also performing some basic statistics.

## Usage -
Make a directory every screen that you run (Ex. "Screen1"). Inside of your 
individual screen directory, create another folder called 'Data' and put the 
excel file producefrom the Epoch2 plate reader inside. Then, from outside that
directory, run the package ($ python -m wellcompare) on the terminal. 
The programwill create several directories for you. Some notable ones are 
'Graphs', which contains graphs and data summaries, and 'Heatmaps' 
(if -hm flag added) (temporarily disabled until further updates).

Example Directory Structure:

|- Outer_folder    <- run python -m wellcompare inside this outer directory   
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|- Screen1  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|- Data    
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|- screen1.xslx   
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|- Screen2   
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|- Data  
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|- screen2.xslx   


## Requirements -
Also outlined in requirements.txt:
1. Python3
2. Pip3
3. Pandas
4. Numpy
5. Maplotlib
6. Scipy
7. Seaborn
8. ArgParse
9. xlrd

## Setup & Installation (MacOS)-
Download Package (recommended):
- Type the following commands into terminal
1. $ pip install wellcombine
2. $ python -m wellcompare \[options\]

-- OR --

Clone Repo:
- Type the following commands into terminal
1. $ git clone https://github.com/jacobian0208/well_compare.git
2. $ pip install -r requirements.txt
3. $ python -m wellcompare \[options\]

## Files & Directories -
1. process.py : module that coordinates graphs and organizes experiment 
   analysis
2. graph.py : module to graph cleaned data
3. extract.py : module to extract and clean data from Epoch2 microplate reader 
   output
4. __main__.py : main file to run package as script
5. requirements.txt : a list of required packages to install to run this 
   program correctly
6. LICENSE : an MIT license to allow use of this program
